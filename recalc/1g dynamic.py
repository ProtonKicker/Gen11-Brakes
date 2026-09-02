# =============================================================================
# Gen11 Brakes — 1g Dynamic Braking Analysis
# Goal: Calculate braking force distribution and braking power distribution
#       for a transient stop (v0 -> 0) under 1g deceleration
# All calculations refer to front total + rear total
# =============================================================================

import math

# ############################################################################
# USER INPUTS — Edit these values for your vehicle
# ############################################################################

# --- Physics ---
g = 9.81  # m/s^2, gravitational acceleration

# --- Vehicle Parameters (from Gen 11 Mechanical VDR, 2025-26.docx) ---
total_mass = 281.0          # kg, total vehicle mass
static_mass_front = 183.0   # kg, static mass on front axle
static_mass_rear = 98.0     # kg, static mass on rear axle

axle_distance = 2.30       # m, wheelbase (distance between axles)
cog_height = 0.473        # m, height of center of gravity above ground (47.30 cm)

# --- Braking Scenario ---
initial_speed = 30.0  # m/s, starting speed
decel = 9.81         # m/s^2, deceleration (1g = 9.81)
final_speed = 0.0    # m/s, ending speed (0 for full stop)


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

# Energy and force
energy_change = 0.5 * total_mass * (initial_speed**2 - final_speed**2)
braking_force_total = total_mass * decel

# Dynamic weight transfer (during braking)
dynamic_weight_front = (total_weight * rear_to_cog + total_mass * decel * cog_height) / axle_distance
dynamic_weight_rear = total_weight - dynamic_weight_front

# Braking force distribution (proportional to dynamic normal loads)
dynamic_braking_force_front = braking_force_total * dynamic_weight_front / total_weight
dynamic_braking_force_rear = braking_force_total - dynamic_braking_force_front

# Energy distribution (proportional to dynamic normal loads)
heat_front = energy_change * dynamic_weight_front / total_weight
heat_rear = energy_change - heat_front

# Stopping metrics
stopping_time = (initial_speed - final_speed) / decel
stopping_distance = (initial_speed**2 - final_speed**2) / (2 * decel)
avg_power = energy_change / stopping_time


# ############################################################################
# RESULTS SUMMARY
# ############################################################################

print("\n" + "="*70)
print("1g DYNAMIC BRAKING RESULTS")
print("="*70)
print(f"\nVehicle: mass={total_mass}kg, wheelbase={axle_distance}m, CoG height={cog_height}m")
print(f"CoG position: {front_to_cog:.3f}m from front, {rear_to_cog:.3f}m from rear")
print(f"\nBraking: {initial_speed}m/s -> {final_speed}m/s @ {decel/g:.2f}g")
print(f"Stopping: {stopping_time:.2f}s, {stopping_distance:.1f}m")
print(f"\n--- Dynamic Normal Loads ---")
print(f"Front: {dynamic_weight_front:,.0f}N ({dynamic_weight_front/total_weight*100:.1f}%)")
print(f"Rear:  {dynamic_weight_rear:,.0f}N ({dynamic_weight_rear/total_weight*100:.1f}%)")
print(f"\n--- Braking Forces ---")
print(f"Front: {dynamic_braking_force_front:,.0f}N ({dynamic_braking_force_front/braking_force_total*100:.1f}%)")
print(f"Rear:  {dynamic_braking_force_rear:,.0f}N ({dynamic_braking_force_rear/braking_force_total*100:.1f}%)")
print(f"Total: {braking_force_total:,.0f}N")
print(f"\n--- Energy ---")
print(f"Front: {heat_front/1000:.1f}kJ per stop")
print(f"Rear:  {heat_rear/1000:.1f}kJ per stop")
print(f"Total: {energy_change/1000:.1f}kJ")
print(f"\n--- Power ---")
print(f"Average: {avg_power/1000:.1f}kW")
print("="*70 + "\n")


# =============================================================================
# DERIVATION NOTES — For reference, not required for operation
# =============================================================================

"""
Moment equilibrium about rear axle during deceleration:

Forces:
  F1 = dynamic normal load on front axle (upward)
  F2 = dynamic normal load on rear axle (upward)
  F3 = inertial force at CoG = m*decel (forward, opposite to decel direction)

Taking moments about the rear axle:
  F1 * axle_distance = total_weight * rear_to_cog + total_mass * decel * cog_height

Since F1 + F2 = total_weight (vertical equilibrium):
  F1 = (total_weight * rear_to_cog + total_mass * decel * cog_height) / axle_distance
  F2 = total_weight - F1

Braking force distribution assumes ideal proportional braking:
  B1/B2 = F1/F2
  => B1 = B_total * F1 / total_weight
  => B2 = B_total - B1

Energy distribution follows the same ratio as braking forces.
"""
