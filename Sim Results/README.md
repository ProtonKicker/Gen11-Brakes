# Thermal Simulation Results (SolidWorks)

This folder is reserved for exported/curated sim outputs (screenshots, plots, summary tables). Raw SolidWorks study artifacts live elsewhere in the repo.

## Naming Convention (exports)

Exports are stored under:

`solidworks_front_rotors_gen_xi_v2_spring_2026/<sim_id>_<study_name>/`

File naming:

- `temp_contour_t<time>s_step<step>_k.png`
- `temp_vs_time_node<node>_k.png`
- `fos_factor_of_safety_min<min>.png`

## Sim Summary

| Sim ID | Study name (SolidWorks) | What | Key snapshot(s) | Notes |
|---:|---|---|---|---|
| 01 | `1G Braking(-Default-)` | Transient thermal | `t=3.05 s (step 61)` | Screenshot shows node `4126` at ~max temp |
| 02 | `Downhill(-Default-)` | Transient thermal | `t=0.4 s (step 4)` | Contour screenshot is early-time; graph runs to ~`123.6 s` |
| 03 | `Cycle(-Default-)` | Transient thermal | `t=55.1 s (step 551)` | Multi-event cycle; node `9783` peaks at ~`613.7 K` |
| 04 | `Position 1(-Default-)` | Static structural (FOS) | `Min FOS ≈ 2.057` | Torque load shown as `-329 N*m` |
| 05 | `Position 2(-Default-)` | Static structural (FOS) | `Min FOS ≈ 1.040` | Torque load shown as `-329 N*m` |
| 06 | `Position 3(-Default-)` | Static structural (FOS) | `Min FOS ≈ 1.021` | Torque load shown as `-329 N*m` |
| 07 | `Position 4(-Default-)` | Static structural (FOS) | `Min FOS ≈ 1.010` | Torque load shown as `-329 N*m` |
| 08 | `Position 5(-Default-)` | Static structural (FOS) | `Min FOS ≈ 1.094` | Torque load shown as `-329 N*m` |
| 09 | `Rev Position 1(-Default-)` | Static structural (FOS) | `Min FOS ≈ 2.057` | Torque load shown as `-329 N*m` |
| 10 | `Rev Position 2(-Default-)` | Static structural (FOS) | `Min FOS ≈ 1.040` | Torque load shown as `-329 N*m` |
| 11 | `Rev Position 3(-Default-)` | Static structural (FOS) | `Min FOS ≈ 1.021` | Torque load shown as `-329 N*m` |
| 12 | `Rev Position 4(-Default-)` | Static structural (FOS) | `Min FOS ≈ 1.010` | Torque load shown as `-329 N*m` |
| 13 | `Rev Position 5(-Default-)` | Static structural (FOS) | `Min FOS ≈ 1.094` | Torque load shown as `-329 N*m` |

## Sim 01 — 1G Braking(-Default-)

**Exports**

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

**Exports**

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

## Sim 03 — Cycle(-Default-)

**Exports**

- Contour: `solidworks_front_rotors_gen_xi_v2_spring_2026/03_cycle_default/temp_contour_t55.1s_step551_k.png`
- Response graph: `solidworks_front_rotors_gen_xi_v2_spring_2026/03_cycle_default/temp_vs_time_node9783_k.png`

**From screenshot**

- Model: `Front Rotors Gen Xi - version 2 spring 2026`
- Plot type: `Thermal Thermal1`
- Time: `55.1 s` (time step `551`)
- Node: `9783`
- Max temp (plot annotation): `6.137e+02 K` (~`613.7 K`)
- Min temp (plot annotation): `3.222e+02 K` (~`322.2 K`)

## Static Sims — Position 1–5 (Factor of Safety)

All five screenshots are from the same model and use the `Factor of Safety1` plot type with the displayed minimum FOS.

**Sim 04 — Position 1(-Default-)**

- Export: `solidworks_front_rotors_gen_xi_v2_spring_2026/04_position_01_default/fos_factor_of_safety_min2.057.png`
- From screenshot: `Min FOS ≈ 2.057`, torque load shown as `-329 N*m`

**Sim 05 — Position 2(-Default-)**

- Export: `solidworks_front_rotors_gen_xi_v2_spring_2026/05_position_02_default/fos_factor_of_safety_min1.040.png`
- From screenshot: `Min FOS ≈ 1.040`, torque load shown as `-329 N*m`

**Sim 06 — Position 3(-Default-)**

- Export: `solidworks_front_rotors_gen_xi_v2_spring_2026/06_position_03_default/fos_factor_of_safety_min1.021.png`
- From screenshot: `Min FOS ≈ 1.021`, torque load shown as `-329 N*m`

**Sim 07 — Position 4(-Default-)**

- Export: `solidworks_front_rotors_gen_xi_v2_spring_2026/07_position_04_default/fos_factor_of_safety_min1.010.png`
- From screenshot: `Min FOS ≈ 1.010`, torque load shown as `-329 N*m`

**Sim 08 — Position 5(-Default-)**

- Export: `solidworks_front_rotors_gen_xi_v2_spring_2026/08_position_05_default/fos_factor_of_safety_min1.094.png`
- From screenshot: `Min FOS ≈ 1.094`, torque load shown as `-329 N*m`

## Static Sims — Rev Position 1–5 (Factor of Safety)

**Sim 09 — Rev Position 1(-Default-)**

- Export: `solidworks_front_rotors_gen_xi_v2_spring_2026/09_rev_position_01_default/fos_factor_of_safety_min2.057.png`
- From screenshot: `Min FOS ≈ 2.057`, torque load shown as `-329 N*m`

**Sim 10 — Rev Position 2(-Default-)**

- Export: `solidworks_front_rotors_gen_xi_v2_spring_2026/10_rev_position_02_default/fos_factor_of_safety_min1.040.png`
- From screenshot: `Min FOS ≈ 1.040`, torque load shown as `-329 N*m`

**Sim 11 — Rev Position 3(-Default-)**

- Export: `solidworks_front_rotors_gen_xi_v2_spring_2026/11_rev_position_03_default/fos_factor_of_safety_min1.021.png`
- From screenshot: `Min FOS ≈ 1.021`, torque load shown as `-329 N*m`

**Sim 12 — Rev Position 4(-Default-)**

- Export: `solidworks_front_rotors_gen_xi_v2_spring_2026/12_rev_position_04_default/fos_factor_of_safety_min1.010.png`
- From screenshot: `Min FOS ≈ 1.010`, torque load shown as `-329 N*m`

**Sim 13 — Rev Position 5(-Default-)**

- Export: `solidworks_front_rotors_gen_xi_v2_spring_2026/13_rev_position_05_default/fos_factor_of_safety_min1.094.png`
- From screenshot: `Min FOS ≈ 1.094`, torque load shown as `-329 N*m`

