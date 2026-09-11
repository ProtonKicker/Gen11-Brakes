#!/usr/bin/env python3
"""
Analyze downhill cases from an InfluxDB telemetry backup.

The tool accepts a telemetry folder like:
  telem/
    20260729T143336Z.manifest
    20260729T143336Z.30.tar.gz
    20260729T143336Z.34.tar.gz
    ...

It will:
1. Read the Influx backup manifest.
2. Stage the shard files into an engine layout that `influxd inspect export-lp`
   understands.
3. Export route-related measurements to Influx line protocol.
4. Aggregate to 1-second samples.
5. Detect plausible downhill segments.
6. Write CSV/JSON summaries including mean, median, typical, and worst cases.

Requirements:
- Python 3.10+
- pandas
- numpy
- InfluxDB OSS 2.x `influxd` available on PATH
"""

from __future__ import annotations

import argparse
import json
import math
import shutil
import subprocess
import tarfile
from collections.abc import Iterable
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


ROUTE_MEASUREMENTS = [
    "sensors.gps_position_deg",
    "sensors.gps_altitude_status_mm",
    "calculated_values.left_speed_mph",
    "calculated_values.right_speed_mph",
    "petals.can_pedal_pos",
]


def find_manifest(telem_dir: Path) -> Path:
    manifests = sorted(
        p
        for p in telem_dir.glob("*.manifest")
        if " (" not in p.name
    )
    if not manifests:
        raise FileNotFoundError(f"No manifest found in {telem_dir}")
    return manifests[0]


def load_manifest(manifest_path: Path) -> dict[str, Any]:
    return json.loads(manifest_path.read_text(encoding="utf-8"))


def find_influxd() -> str:
    candidates = [
        shutil.which("influxd"),
        str(
            Path.home()
            / "AppData"
            / "Local"
            / "Microsoft"
            / "WinGet"
            / "Packages"
            / "InfluxData.InfluxDB.OSS_Microsoft.Winget.Source_8wekyb3d8bbwe"
            / "influxd.exe"
        ),
        str(
            Path.home()
            / "AppData"
            / "Local"
            / "Microsoft"
            / "WinGet"
            / "Links"
            / "influxd.exe"
        ),
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return candidate
    raise FileNotFoundError(
        "Could not find `influxd`. Install InfluxDB OSS 2.x or add influxd to PATH."
    )


def stage_engine_layout(telem_dir: Path, manifest: dict[str, Any], engine_root: Path) -> tuple[str, Path]:
    bucket = manifest["buckets"][0]
    bucket_id = bucket["bucketID"]
    bucket_engine_dir = engine_root / "data" / bucket_id
    if any(bucket_engine_dir.rglob("*.tsm")):
        return bucket_id, engine_root

    bucket_engine_dir.mkdir(parents=True, exist_ok=True)
    inspect_dir = telem_dir / "_inspect"

    for rp in bucket["retentionPolicies"]:
        rp_name = rp["name"]
        for shard_group in rp["shardGroups"]:
            for shard in shard_group["shards"]:
                shard_id = str(shard["id"])
                target_dir = bucket_engine_dir / rp_name / shard_id
                target_dir.mkdir(parents=True, exist_ok=True)

                inspect_shard_dir = inspect_dir / f"shard{shard_id}" / bucket_id / rp_name / shard_id
                if inspect_shard_dir.exists():
                    for tsm in inspect_shard_dir.glob("*.tsm"):
                        shutil.copy2(tsm, target_dir / tsm.name)
                    continue

                archive_path = telem_dir / shard["fileName"]
                if not archive_path.exists():
                    raise FileNotFoundError(
                        f"Missing shard archive {archive_path} and no unpacked shard in {inspect_shard_dir}"
                    )
                with tarfile.open(archive_path, "r:gz") as tar:
                    members = [m for m in tar.getmembers() if m.name.endswith(".tsm")]
                    if not members:
                        raise RuntimeError(f"No .tsm files found in {archive_path}")
                    tar.extractall(path=engine_root / "data", members=members)

    if not any(bucket_engine_dir.rglob("*.tsm")):
        raise RuntimeError(f"Failed to stage engine layout under {bucket_engine_dir}")

    return bucket_id, engine_root


def export_line_protocol(
    telem_dir: Path,
    engine_root: Path,
    bucket_id: str,
    export_path: Path,
    force: bool,
) -> Path:
    if export_path.exists() and export_path.stat().st_size > 0 and not force:
        return export_path

    export_path.parent.mkdir(parents=True, exist_ok=True)
    influxd = find_influxd()
    cmd = [
        influxd,
        "inspect",
        "export-lp",
        "--bucket-id",
        bucket_id,
        "--engine-path",
        str(engine_root),
        "--measurement",
        ",".join(ROUTE_MEASUREMENTS),
        "--output-path",
        str(export_path),
    ]
    subprocess.run(cmd, cwd=telem_dir, check=True)
    if not export_path.exists() or export_path.stat().st_size == 0:
        raise RuntimeError(f"Line protocol export was empty: {export_path}")
    return export_path


def parse_line_protocol_to_seconds(lp_path: Path) -> pd.DataFrame:
    bins: dict[int, dict[str, float]] = {}

    def get_bin(sec: int) -> dict[str, float]:
        row = bins.get(sec)
        if row is None:
            row = {
                "lat_sum": 0.0,
                "lat_n": 0.0,
                "lon_sum": 0.0,
                "lon_n": 0.0,
                "alt_sum": 0.0,
                "alt_n": 0.0,
                "fix_sum": 0.0,
                "fix_n": 0.0,
                "siv_sum": 0.0,
                "siv_n": 0.0,
                "left_sum": 0.0,
                "left_n": 0.0,
                "right_sum": 0.0,
                "right_n": 0.0,
                "brake_sum": 0.0,
                "brake_n": 0.0,
                "mech_max": 0.0,
            }
            bins[sec] = row
        return row

    with lp_path.open("r", encoding="utf-8", errors="ignore") as handle:
        for line in handle:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            try:
                measurement, fields, ts = line.split(" ")
            except ValueError:
                continue

            sec = int(ts) // 1_000_000_000
            row = get_bin(sec)

            for item in fields.split(","):
                if "=" not in item:
                    continue
                key, raw_value = item.split("=", 1)
                if raw_value.endswith("i"):
                    try:
                        value = int(raw_value[:-1])
                    except ValueError:
                        continue
                else:
                    try:
                        value = float(raw_value)
                    except ValueError:
                        continue

                if measurement == "sensors.gps_position_deg":
                    if key == "lat":
                        row["lat_sum"] += value
                        row["lat_n"] += 1
                    elif key == "lon":
                        row["lon_sum"] += value
                        row["lon_n"] += 1
                elif measurement == "sensors.gps_altitude_status_mm":
                    if key == "altitude":
                        row["alt_sum"] += value / 1000.0
                        row["alt_n"] += 1
                    elif key == "fixType":
                        row["fix_sum"] += value
                        row["fix_n"] += 1
                    elif key == "siv":
                        row["siv_sum"] += value
                        row["siv_n"] += 1
                elif measurement == "calculated_values.left_speed_mph" and key == "value":
                    row["left_sum"] += value
                    row["left_n"] += 1
                elif measurement == "calculated_values.right_speed_mph" and key == "value":
                    row["right_sum"] += value
                    row["right_n"] += 1
                elif measurement == "petals.can_pedal_pos":
                    if key == "brakePos":
                        row["brake_sum"] += value
                        row["brake_n"] += 1
                    elif key == "mechBrake":
                        row["mech_max"] = max(row["mech_max"], float(value))

    rows = []
    for sec, row in bins.items():
        speed_candidates = []
        if row["left_n"]:
            speed_candidates.append(row["left_sum"] / row["left_n"])
        if row["right_n"]:
            speed_candidates.append(row["right_sum"] / row["right_n"])
        speed_mph = float(np.mean(speed_candidates)) if speed_candidates else np.nan
        rows.append(
            {
                "sec": sec,
                "time": pd.to_datetime(sec, unit="s", utc=True),
                "lat": row["lat_sum"] / row["lat_n"] if row["lat_n"] else np.nan,
                "lon": row["lon_sum"] / row["lon_n"] if row["lon_n"] else np.nan,
                "alt_m": row["alt_sum"] / row["alt_n"] if row["alt_n"] else np.nan,
                "fixType": row["fix_sum"] / row["fix_n"] if row["fix_n"] else np.nan,
                "siv": row["siv_sum"] / row["siv_n"] if row["siv_n"] else np.nan,
                "speed_mph": speed_mph,
                "speed_mps": speed_mph * 0.44704 if not np.isnan(speed_mph) else np.nan,
                "brakePos": row["brake_sum"] / row["brake_n"] if row["brake_n"] else np.nan,
                "mechBrake": row["mech_max"],
            }
        )

    if not rows:
        raise RuntimeError(f"No route rows parsed from {lp_path}")

    return pd.DataFrame(rows).sort_values("sec").reset_index(drop=True)


def haversine_step_m(lat1: pd.Series, lon1: pd.Series, lat2: pd.Series, lon2: pd.Series) -> pd.Series:
    radius_m = 6_371_000.0
    lat1r = np.radians(lat1)
    lon1r = np.radians(lon1)
    lat2r = np.radians(lat2)
    lon2r = np.radians(lon2)
    dlat = lat2r - lat1r
    dlon = lon2r - lon1r
    a = np.sin(dlat / 2.0) ** 2 + np.cos(lat1r) * np.cos(lat2r) * np.sin(dlon / 2.0) ** 2
    return 2 * radius_m * np.arcsin(np.sqrt(a))


def summarize_numeric(df: pd.DataFrame, cols: Iterable[str]) -> dict[str, dict[str, float]]:
    if df.empty:
        return {}
    return {
        "mean": {col: float(df[col].mean()) for col in cols},
        "median": {col: float(df[col].median()) for col in cols},
    }


def nearest_to_median(df: pd.DataFrame, cols: list[str]) -> dict[str, Any] | None:
    if df.empty:
        return None
    med = df[cols].median(numeric_only=True)
    score = pd.Series(0.0, index=df.index)
    for col in cols:
        denom = max(abs(float(med[col])), 1.0)
        score += (df[col] - med[col]).abs() / denom
    return df.assign(_median_score=score).sort_values("_median_score").iloc[0].drop("_median_score").to_dict()


def detect_downhill_segments(
    route_df: pd.DataFrame,
    mass_kg: float,
    session_gap_s: float,
    grid_m: float,
    min_segment_distance_m: float,
    min_segment_drop_m: float,
    min_speed_mps: float,
    downhill_threshold_pct: float,
    plausible_avg_grade_min_pct: float,
    plausible_avg_grade_max_pct: float,
    plausible_steepest_min_pct: float,
    plausible_max_speed_mph: float,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    gravity = 9.81

    route = route_df[
        route_df["lat"].notna() & route_df["lon"].notna() & route_df["alt_m"].notna()
    ].copy()
    route["speed_mps"] = route["speed_mps"].interpolate(limit_direction="both", limit=5)
    route["brakePos"] = route["brakePos"].fillna(0)
    route["mechBrake"] = route["mechBrake"].fillna(0)
    route["dt_s"] = route["sec"].diff().fillna(0)

    route["raw_dist_m"] = haversine_step_m(
        route["lat"].shift(),
        route["lon"].shift(),
        route["lat"],
        route["lon"],
    ).fillna(0)

    speed_allow = route["speed_mps"].fillna(0).clip(lower=0)
    max_step = (speed_allow * route["dt_s"].clip(lower=0)) * 3 + 50
    route["dist_m"] = np.where(
        (route["dt_s"] <= session_gap_s)
        & (route["raw_dist_m"] <= max_step.clip(lower=80, upper=500)),
        route["raw_dist_m"],
        0.0,
    )
    route["session_break"] = (route["dt_s"] > session_gap_s) | (
        (route["dist_m"] == 0) & (route["raw_dist_m"] > 500)
    )
    route["session_id"] = route["session_break"].cumsum()

    segments: list[dict[str, Any]] = []
    for session_id, group in route.groupby("session_id"):
        group = group.copy().reset_index(drop=True)
        if len(group) < 20:
            continue

        group["cumdist_m"] = group["dist_m"].cumsum()
        if float(group["cumdist_m"].iloc[-1]) < 300:
            continue

        use = (
            group[["cumdist_m", "alt_m", "speed_mps", "brakePos", "mechBrake", "time"]]
            .groupby("cumdist_m", as_index=False)
            .agg(
                {
                    "alt_m": "mean",
                    "speed_mps": "mean",
                    "brakePos": "mean",
                    "mechBrake": "max",
                    "time": "first",
                }
            )
        )
        if len(use) < 20 or float(use["cumdist_m"].iloc[-1]) < 300:
            continue

        grid = np.arange(0.0, float(use["cumdist_m"].iloc[-1]) + grid_m, grid_m)
        alt = np.interp(grid, use["cumdist_m"], use["alt_m"])
        speed = np.interp(
            grid,
            use["cumdist_m"],
            use["speed_mps"].interpolate(limit_direction="both").fillna(0),
        )
        brake = np.interp(grid, use["cumdist_m"], use["brakePos"].fillna(0))
        mech = np.interp(grid, use["cumdist_m"], use["mechBrake"].fillna(0))

        alt_smoothed = pd.Series(alt).rolling(11, center=True, min_periods=1).mean().to_numpy()
        if len(grid) < 21:
            continue

        window = 5
        grade100 = np.full_like(grid, np.nan, dtype=float)
        grade100[window:-window] = (
            100.0
            * (alt_smoothed[window * 2 :] - alt_smoothed[: -window * 2])
            / (grid[window * 2 :] - grid[: -window * 2])
        )
        power_proxy = mass_kg * gravity * np.maximum(0.0, -grade100 / 100.0) * np.maximum(speed, 0.0)

        downhill = (grade100 <= downhill_threshold_pct) & (speed >= min_speed_mps)
        idx = np.where(downhill)[0]
        if len(idx) == 0:
            continue

        filled = downhill.copy()
        prev = idx[0]
        for cur in idx[1:]:
            if (cur - prev - 1) <= 3:
                filled[prev : cur + 1] = True
            prev = cur

        in_seg = False
        start = 0
        for i, flag in enumerate(filled):
            if flag and not in_seg:
                in_seg = True
                start = i
            elif not flag and in_seg:
                end = i - 1
                in_seg = False
                seg_dist = float(grid[end] - grid[start])
                seg_drop = float(alt_smoothed[start] - alt_smoothed[end])
                if seg_dist >= min_segment_distance_m and seg_drop >= min_segment_drop_m:
                    local_grade = grade100[start : end + 1]
                    local_power = power_proxy[start : end + 1]
                    local_speed = speed[start : end + 1]
                    local_brake = brake[start : end + 1]
                    local_mech = mech[start : end + 1]
                    segments.append(
                        {
                            "session_id": int(session_id),
                            "start_time": str(group["time"].iloc[0]),
                            "end_time": str(group["time"].iloc[-1]),
                            "segment_start_m": float(grid[start]),
                            "segment_end_m": float(grid[end]),
                            "distance_m": seg_dist,
                            "drop_m": seg_drop,
                            "avg_grade_pct": float(-seg_drop / seg_dist * 100.0),
                            "steepest_100m_grade_pct": float(np.nanmin(local_grade)),
                            "avg_speed_mps": float(np.nanmean(local_speed)),
                            "max_speed_mps": float(np.nanmax(local_speed)),
                            "avg_speed_mph": float(np.nanmean(local_speed) / 0.44704),
                            "max_speed_mph": float(np.nanmax(local_speed) / 0.44704),
                            "brake_fraction": float(np.mean((local_brake > 0) | (local_mech > 0))),
                            "avg_brake_signal": float(np.nanmean(local_brake)),
                            "avg_power_proxy_W": float(np.nanmean(local_power)),
                            "max_power_proxy_W": float(np.nanmax(local_power)),
                            "energy_proxy_kJ": float(mass_kg * gravity * seg_drop / 1000.0),
                        }
                    )

    segments_df = pd.DataFrame(segments)
    if segments_df.empty:
        raise RuntimeError("No downhill segments found in the exported route data.")

    plausible_df = segments_df[
        (segments_df["avg_grade_pct"] >= plausible_avg_grade_min_pct)
        & (segments_df["avg_grade_pct"] <= plausible_avg_grade_max_pct)
        & (segments_df["steepest_100m_grade_pct"] >= plausible_steepest_min_pct)
        & (segments_df["avg_speed_mph"] >= 0)
        & (segments_df["avg_speed_mph"] <= plausible_max_speed_mph)
        & (segments_df["max_speed_mph"] <= plausible_max_speed_mph)
    ].copy()

    brake_df = plausible_df[plausible_df["brake_fraction"] >= 0.1].copy()
    return segments_df, plausible_df, brake_df


def build_summary(
    route_df: pd.DataFrame,
    all_segments: pd.DataFrame,
    plausible_segments: pd.DataFrame,
    brake_segments: pd.DataFrame,
) -> dict[str, Any]:
    metrics = [
        "distance_m",
        "drop_m",
        "avg_grade_pct",
        "steepest_100m_grade_pct",
        "avg_speed_mph",
        "max_speed_mph",
        "avg_power_proxy_W",
        "max_power_proxy_W",
        "energy_proxy_kJ",
    ]

    all_clean = all_segments[
        (all_segments["avg_speed_mph"] >= 0)
        & (all_segments["avg_speed_mph"] <= 120)
        & (all_segments["max_speed_mph"] >= 0)
        & (all_segments["max_speed_mph"] <= 120)
    ].copy()

    summary: dict[str, Any] = {
        "rows_per_second": int(len(route_df)),
        "gps_rows": int(route_df["lat"].notna().sum()),
        "time_start": str(route_df["time"].min()),
        "time_end": str(route_df["time"].max()),
        "segment_count_all": int(len(all_segments)),
        "segment_count_plausible": int(len(plausible_segments)),
        "segment_count_brake_relevant": int(len(brake_segments)),
        "all_segments_stats": summarize_numeric(all_clean, metrics),
        "plausible_segments_stats": summarize_numeric(plausible_segments, metrics),
        "brake_relevant_stats": summarize_numeric(brake_segments, metrics),
    }

    if not plausible_segments.empty:
        summary["longest_plausible"] = plausible_segments.sort_values(
            ["distance_m", "drop_m"], ascending=[False, False]
        ).iloc[0].to_dict()
        summary["worst_plausible_by_drop"] = plausible_segments.sort_values(
            ["drop_m", "distance_m"], ascending=[False, False]
        ).iloc[0].to_dict()
        summary["worst_plausible_by_power"] = plausible_segments.sort_values(
            ["avg_power_proxy_W", "drop_m"], ascending=[False, False]
        ).iloc[0].to_dict()

    if not brake_segments.empty:
        summary["typical_brake_relevant"] = nearest_to_median(
            brake_segments,
            ["distance_m", "drop_m", "avg_grade_pct", "avg_speed_mph", "avg_power_proxy_W"],
        )
        summary["worst_brake_relevant_by_drop"] = brake_segments.sort_values(
            ["drop_m", "distance_m"], ascending=[False, False]
        ).iloc[0].to_dict()
        summary["worst_brake_relevant_by_power"] = brake_segments.sort_values(
            ["avg_power_proxy_W", "drop_m"], ascending=[False, False]
        ).iloc[0].to_dict()

    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze downhill cases from a telemetry backup.")
    parser.add_argument("telem_dir", type=Path, help="Path to the telemetry backup folder")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Directory for outputs. Defaults to <telem_dir>/_analysis",
    )
    parser.add_argument(
        "--engine-root",
        type=Path,
        default=None,
        help="Engine staging directory. Defaults to <telem_dir>/_engine",
    )
    parser.add_argument(
        "--force-export",
        action="store_true",
        help="Re-export line protocol even if a previous export exists",
    )
    parser.add_argument("--mass-kg", type=float, default=281.0, help="Vehicle mass for gravity power proxy")
    parser.add_argument("--session-gap-s", type=float, default=20.0, help="Gap that starts a new drive session")
    parser.add_argument("--grid-m", type=float, default=10.0, help="Distance grid for smoothing and grade analysis")
    parser.add_argument("--min-segment-distance-m", type=float, default=200.0)
    parser.add_argument("--min-segment-drop-m", type=float, default=5.0)
    parser.add_argument("--min-speed-mps", type=float, default=2.0)
    parser.add_argument("--downhill-threshold-pct", type=float, default=-0.5)
    parser.add_argument("--plausible-avg-grade-min-pct", type=float, default=-12.0)
    parser.add_argument("--plausible-avg-grade-max-pct", type=float, default=-0.5)
    parser.add_argument("--plausible-steepest-min-pct", type=float, default=-20.0)
    parser.add_argument("--plausible-max-speed-mph", type=float, default=80.0)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    telem_dir = args.telem_dir.resolve()
    output_dir = (args.output_dir or (telem_dir / "_analysis")).resolve()
    engine_root = (args.engine_root or (telem_dir / "_engine")).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    engine_root.mkdir(parents=True, exist_ok=True)

    manifest_path = find_manifest(telem_dir)
    manifest = load_manifest(manifest_path)
    bucket_id, engine_root = stage_engine_layout(telem_dir, manifest, engine_root)

    export_path = output_dir / "route_export.lp"
    export_line_protocol(
        telem_dir=telem_dir,
        engine_root=engine_root,
        bucket_id=bucket_id,
        export_path=export_path,
        force=args.force_export,
    )

    route_df = parse_line_protocol_to_seconds(export_path)
    all_segments, plausible_segments, brake_segments = detect_downhill_segments(
        route_df=route_df,
        mass_kg=args.mass_kg,
        session_gap_s=args.session_gap_s,
        grid_m=args.grid_m,
        min_segment_distance_m=args.min_segment_distance_m,
        min_segment_drop_m=args.min_segment_drop_m,
        min_speed_mps=args.min_speed_mps,
        downhill_threshold_pct=args.downhill_threshold_pct,
        plausible_avg_grade_min_pct=args.plausible_avg_grade_min_pct,
        plausible_avg_grade_max_pct=args.plausible_avg_grade_max_pct,
        plausible_steepest_min_pct=args.plausible_steepest_min_pct,
        plausible_max_speed_mph=args.plausible_max_speed_mph,
    )

    all_segments.to_csv(output_dir / "downhill_segments_all.csv", index=False)
    plausible_segments.to_csv(output_dir / "downhill_segments_plausible.csv", index=False)
    brake_segments.to_csv(output_dir / "downhill_segments_brake_relevant.csv", index=False)

    summary = build_summary(route_df, all_segments, plausible_segments, brake_segments)
    (output_dir / "downhill_summary.json").write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8",
    )

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
