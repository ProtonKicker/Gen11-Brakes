# Downhill Case Summary

This document summarizes the telemetry-derived downhill cases from the current `telem` backup and the brake-model outputs derived from them.

## Typical Case

- Segment type: `typical brake-relevant` observed downhill
- Distance: `470 m`
- Elevation drop: `13.95 m`
- Average grade: `2.97%` downhill
- Downhill angle: `1.70 deg`
- Average speed: `22.56 mph` (`10.09 m/s`)
- Max speed: `26.55 mph`
- Descent time: `46.6 s`

- Total braking force: `81.8 N`
- Front braking force: `53.8 N`
- Rear braking force: `28.0 N`
- Front/rear split: `65.7% / 34.3%`

- Total braking power: `0.825 kW`
- Front braking power: `0.542 kW`
- Rear braking power: `0.283 kW`

- Total descent energy: `38.45 kJ`
- Front energy: `25.27 kJ`
- Rear energy: `13.17 kJ`

## Worst Case

- Segment type: `worst brake-relevant by power`
- Distance: `1830 m`
- Elevation drop: `96.94 m`
- Average grade: `5.30%` downhill
- Downhill angle: `3.03 deg`
- Average speed: `47.94 mph` (`21.43 m/s`)
- Max speed: `58.01 mph`
- Descent time: `85.4 s`

- Total braking force: `145.8 N`
- Front braking force: `96.5 N`
- Rear braking force: `49.3 N`
- Front/rear split: `66.2% / 33.8%`

- Total braking power: `3.13 kW`
- Front braking power: `2.07 kW`
- Rear braking power: `1.06 kW`

- Total descent energy: `266.84 kJ`
- Front energy: `176.68 kJ`
- Rear energy: `90.15 kJ`

## Worst Energy Case

- Segment type: `worst brake-relevant by drop`
- Distance: `2650 m`
- Elevation drop: `105.85 m`
- Average grade: `3.99%` downhill
- Average speed: `47.95 mph`
- Descent time: `123.6 s`

- Total braking power: `2.36 kW`
- Total descent energy: `291.54 kJ`
- Front energy: `192.26 kJ`
- Rear energy: `99.28 kJ`

## Short Takeaway

- Typical case: about `3%` grade, `470 m`, `23 mph`, `0.83 kW`, `38 kJ`
- Worst thermal case: about `5.3%` grade, `1.83 km`, `48 mph`, `3.13 kW`, `267 kJ`
- Worst total-energy case: about `4.0%` grade, `2.65 km`, `48 mph`, `292 kJ`

## Notes

- These numbers come from the telemetry-derived downhill detector and the steady-speed downhill brake model.
- They are still road-load brake-demand estimates and do not yet subtract regenerative braking.
