# Gen11 Brakes

Working on the front brake rotor (CAD + thermal simulations).

## CAD

- Final CAD + simulation bundle (zipped): https://berkeley.box.com/s/p0zxtfpvc8ze6lw5cjav0ohw9hbjgl5t
- SolidWorks part (repo): https://github.com/ProtonKicker/Gen11-Brakes/blob/main/CAD/Front%20Rotors%20Gen%20Xi%20-%20version%202%20spring%202026.SLDPRT

## Simulation Results

- Summary / index: [Sim Results/README.md](file:///c:/Users/tdxt/OneDrive/Documents/GitHub/Gen11%20Brakes/Sim%20Results/README.md)

**Sim 01 — 1G Braking(-Default-)**

- Contour: [temp_contour_t3.05s_step61_k.png](file:///c:/Users/tdxt/OneDrive/Documents/GitHub/Gen11%20Brakes/Sim%20Results/solidworks_front_rotors_gen_xi_v2_spring_2026/01_1g_braking_default/temp_contour_t3.05s_step61_k.png)
- Response graph: [temp_vs_time_node4126_k.png](file:///c:/Users/tdxt/OneDrive/Documents/GitHub/Gen11%20Brakes/Sim%20Results/solidworks_front_rotors_gen_xi_v2_spring_2026/01_1g_braking_default/temp_vs_time_node4126_k.png)

**Sim 02 — Downhill(-Default-)**

- Contour: [temp_contour_t0.40s_step4_k.png](file:///c:/Users/tdxt/OneDrive/Documents/GitHub/Gen11%20Brakes/Sim%20Results/solidworks_front_rotors_gen_xi_v2_spring_2026/02_downhill_default/temp_contour_t0.40s_step4_k.png)
- Response graph: [temp_vs_time_node9745_k.png](file:///c:/Users/tdxt/OneDrive/Documents/GitHub/Gen11%20Brakes/Sim%20Results/solidworks_front_rotors_gen_xi_v2_spring_2026/02_downhill_default/temp_vs_time_node9745_k.png)

**Sim 03 — Cycle(-Default-)**

- Contour: [temp_contour_t55.1s_step551_k.png](file:///c:/Users/tdxt/OneDrive/Documents/GitHub/Gen11%20Brakes/Sim%20Results/solidworks_front_rotors_gen_xi_v2_spring_2026/03_cycle_default/temp_contour_t55.1s_step551_k.png)
- Response graph: [temp_vs_time_node9783_k.png](file:///c:/Users/tdxt/OneDrive/Documents/GitHub/Gen11%20Brakes/Sim%20Results/solidworks_front_rotors_gen_xi_v2_spring_2026/03_cycle_default/temp_vs_time_node9783_k.png)

## Slides / References

- Tachyon: https://docs.google.com/presentation/d/1pMEzpO6QZPY_rlKppHlrBsez1nrBPlveM59D0CdWgEI/edit?slide=id.p#slide=id.p
- Earlier Gen11 slides: https://docs.google.com/presentation/d/19nD-BmJuWEJKvXIxPnPb9kR-InqOBad3D03fBtdmWO4/edit?slide=id.g3cfb6c56c96_0_30#slide=id.g3cfb6c56c96_0_30

## Calculations / Inputs

- Heat transfer coefficient (avg h) reference doc: https://www.amazon.com/dp/B074ZHZZ5D?lv=shuf&channelId=500&plpRedirect=mhFallback&th=1
- Braking power + weight distribution sheet: https://docs.google.com/spreadsheets/d/1q0VddAqIyhRePzD90C7rjIV9bsIdHMh2iyM1maYyNhg/edit?gid=0#gid=0
- Brakes Calcs notebook (heat, brake force, brake power, and SolidWorks thermal inputs): https://github.com/ProtonKicker/Gen11-Brakes/blob/main/Brakes%20Calcs.ipynb
