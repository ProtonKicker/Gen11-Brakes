# =============================================================================
# Gen11 Brakes — Continuous Downhill Braking Analysis
# Goal: Calculate braking force distribution and braking power distribution
#       for steady-speed downhill (constant velocity, a = 0)
# Vehicle: 2 wheels front, 1 wheel rear (three-wheeler from VDR)
# Note: All calculations refer to front total + rear total
#       Braking must balance gravity component, not inertia
# =============================================================================

import math

# ############################################################################
# USER INPUTS — Edit these values for your vehicle and scenario
# ############################################################################

# --- Physics ---
g = 9.81  # m/s^2, gravitational acceleration

# --- Vehicle Parameters (from Gen 11 Mechanical VDR, 2025-26.docx) ---
total_mass = 281.0          # kg, total vehicle mass
static_mass_front = 183.0   # kg, static mass on front axle
static_mass_rear = 98.0     # kg, static mass on rear axle

axle_distance = 2.30       # m, wheelbase (distance between axles)
cog_height = 0.473        # m, height of CoG above ground (47.30 cm)

# --- Downhill Scenario ---
constant_speed = None    # m/s, steady downhill speed (constant)
downhill_angle = None   # degrees, slope angle from horizontal (e.g. 5 deg)
downhill_distance = None # m, distance along slope (e.g. 8000 for 8km)


# ############################################################################
# CALCULATIONS — Derived from inputs above
# ############################################################################

# Weight calculations
total_weight = total_mass * g
static_weight_front = static_mass_front * g
static_weight_rear = static_mass_rear * g

# CoG position (distance from axles)
front_to_cog = axle_distance * static_mass_rear / total_mass
rear_to_cog = axle_distance - front_to_cog

# Slope components
downhill_angle_rad = math.radians(downhill_angle)
weight_normal_total = total_weight * math.cos(downhill_angle_rad)
weight_parallel_total = total_weight * math.sin(downhill_angle_rad)

# Braking force and power (steady state: a = 0, braking balances gravity)
braking_force_total = weight_parallel_total
braking_power_total = braking_force_total * constant_speed

# Dynamic weight transfer on grade
dynamic_weight_front = (total_weight * math.cos(downhill_angle_rad) * rear_to_cog + total_weight * math.sin(downhill_angle_rad) * cog_height) / axle_distance
dynamic_weight_rear = weight_normal_total - dynamic_weight_front

# Braking force distribution (proportional to dynamic normal loads)
dynamic_braking_force_front = braking_force_total * dynamic_weight_front / weight_normal_total
dynamic_braking_force_rear = braking_force_total - dynamic_braking_force_front

# Power distribution (proportional to dynamic normal loads)
power_front = braking_power_total * dynamic_weight_front / weight_normal_total
power_rear = braking_power_total - power_front

# Heat rates (Watts = Joules/second)
heat_rate_front = power_front
heat_rate_rear = power_rear

# Total energy over the full descent
descent_time = downhill_distance / constant_speed
energy_total = braking_force_total * downhill_distance
energy_front = energy_total * dynamic_weight_front / weight_normal_total
energy_rear = energy_total - energy_front

# Compatibility naming with 1g dynamic.py
heat_front = energy_front
heat_rear = energy_rear
heat_total = energy_total


# ############################################################################
# RESULTS SUMMARY
# ############################################################################

print("\n" + "="*70)
print("CONTINUOUS DOWNHILL BRAKING RESULTS")
print("="*70)
print(f"\nVehicle: mass={total_mass}kg, wheelbase={axle_distance}m, CoG={cog_height}m")
print(f"Downhill: {downhill_angle}° slope, {constant_speed}m/s for {downhill_distance}m")
print(f"Descent time: {descent_time/60:.1f} min")
print(f"\n--- Braking Force Distribution ---")
print(f"Front: {dynamic_braking_force_front:,.0f}N ({dynamic_braking_force_front/braking_force_total*100:.1f}%)")
print(f"Rear:  {dynamic_braking_force_rear:,.0f}N ({dynamic_braking_force_rear/braking_force_total*100:.1f}%)")
print(f"Total: {braking_force_total:,.0f}N")
print(f"\n--- Power (Heating) ---")
print(f"Front: {power_front/1000:.2f}kW ({power_front/braking_power_total*100:.1f}%)")
print(f"Rear:  {power_rear/1000:.2f}kW ({power_rear/braking_power_total*100:.1f}%)")
print(f"Total: {braking_power_total/1000:.2f}kW")
print("="*70 + "\n")


# =============================================================================
# DERIVATION NOTES — For reference, not required for operation
# =============================================================================

"""
Moment equilibrium about rear axle on a slope (steady-state, a=0):

Define:
  N1, N2 = dynamic normal loads on front/rear axles
  L = axle_distance
  b = rear_to_cog (distance from CoG to rear axle, downhill)
  c = front_to_cog (distance from CoG to front axle, downhill)
  h = cog_height (normal to slope)
  theta = downhill_angle

Coordinates: x downhill along slope, z normal outward from slope.
Origin at rear contact patch.

Forces at CoG:
  Fz = -total_weight * cos(theta)  (into slope)
  Fx = +total_weight * sin(theta)  (downhill)

Moment about rear:
  N1 * L + (b*(-W*cos) - h*(W*sin)) = 0
  => N1 * L = W*cos * b + W*sin * h

Hence:
  N1 = (W*cos * b + W*sin * h) / L
  N2 = W*cos - N1

At theta=0 (horizontal), this reduces to N1 = W*b/L (static).

Braking distribution for ideal (no lockup) is proportional to normal loads:
  B1 = B_total * N1 / (W*cos)
  B2 = B_total - B1

Power distribution same ratio (P = B * v):
  P1 = P_total * N1 / (W*cos)
  P2 = P_total - P1

Energy per distance = B * distance
Energy per time = power * time
"""
