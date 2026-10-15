# Thermal Simulation Results (SolidWorks)

This folder is reserved for exported/curated sim outputs (screenshots, plots, summary tables). Raw SolidWorks study artifacts live elsewhere in the repo.

## Naming Convention (exports)

Exports are stored under:

`solidworks_front_rotors_gen_xi_v2_spring_2026/<sim_id>_<study_name>/`

File naming:

- `temp_contour_t<time>s_step<step>_k.png`
- `temp_vs_time_node<node>_k.png`

## Sim Summary

| Sim ID | Study name (SolidWorks) | What | Key snapshot(s) | Notes |
|---:|---|---|---|---|
| 01 | `1G Braking(-Default-)` | Transient thermal | `t=3.05 s (step 61)` | Screenshot shows node `4126` at ~max temp |
| 02 | `Downhill(-Default-)` | Transient thermal | `t=0.4 s (step 4)` | Contour screenshot is early-time; graph runs to ~`123.6 s` |
| 03 | (pending) | (pending) | (pending) | Waiting on images |

## Sim 01 — 1G Braking(-Default-)

**Exports (expected paths)**

- Contour: `solidworks_front_rotors_gen_xi_v2_spring_2026/01_1g_braking_default/temp_contour_t3.05s_step61_k.png`
- Response graph: `solidworks_front_rotors_gen_xi_v2_spring_2026/01_1g_braking_default/temp_vs_time_node4126_k.png`

**From screenshot**

- Model: `Front Rotors Gen Xi - version 2 spring 2026`
- Plot type: `Thermal Thermal1`
- Time: `3.05 s` (time step `61`)
- Node: `4126`
- Max temp (plot annotation): `5.603e+02 K` (~`560.3 K`)
- Min temp (plot annotation): `3.109e+02 K` (~`310.9 K`)

**Raw study artifacts (repo reference)**

- `CAD/Front Rotors Gen Xi - version 2 spring 2026-1G Braking.*`

## Sim 02 — Downhill(-Default-)

**Exports (expected paths)**

- Contour: `solidworks_front_rotors_gen_xi_v2_spring_2026/02_downhill_default/temp_contour_t0.40s_step4_k.png`
- Response graph: `solidworks_front_rotors_gen_xi_v2_spring_2026/02_downhill_default/temp_vs_time_node9745_k.png`

**From screenshot**

- Model: `Front Rotors Gen Xi - version 2 spring 2026`
- Plot type: `Thermal Thermal1`
- Time: `0.4 s` (time step `4`)
- Node: `9745`
- Max temp (plot annotation): `3.127e+02 K` (~`312.7 K`)
- Min temp (plot annotation): `3.109e+02 K` (~`310.9 K`)
- Response graph time range: `0.10 s → 123.60 s` (exact end temperature not readable from screenshot)

**Raw study artifacts (repo reference)**

- `CAD/Front Rotors Gen Xi - version 2 spring 2026-Downhill.*`

## Sim 03 — Pending

Drop the remaining screenshots into:

`solidworks_front_rotors_gen_xi_v2_spring_2026/03_<name_here>/`

