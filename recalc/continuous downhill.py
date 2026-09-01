# Goal: Find [braking force distribution] and [braking power distribution]
# for CONSTANT SPEED downhill (steady-state, a = 0)

# note that all calculations refer to front total + rear total
# downhill_angle is the slope angle from horizontal (positive downhill)
# counterintuitive vs 1g dynamic.py: braking must balance gravity component, not inertia


import math

# constants

g = 9.81

constant_speed = None   # m/s, steady downhill speed (constant)
downhill_angle = None   # degrees, slope angle from horizontal (e.g. 5 deg)
# if you prefer radians, set downhill_angle_rad directly and replace math.radians() calls
downhill_distance = None   # m along slope, e.g. 8000 for 8km

total_mass = None
static_mass_front = None
static_mass_rear = None

axle_distance = None   # wheelbase, m
cog_height = None      # height of CoG above ground (normal to ground), m



# secondary variables for calculations

## weight stuff

total_weight = total_mass * g   # G = mg
static_weight_front = static_mass_front * g
static_weight_rear = static_mass_rear * g

# CoG position along wheelbase (measured along slope, same as horizontal wheelbase for small angles)
# original 1g file had these swapped (front_to_cog actually was distance to rear).
# corrected here for clarity:
front_to_cog = axle_distance * static_mass_rear / total_mass   # distance from FRONT axle to CoG
rear_to_cog = axle_distance - front_to_cog                     # distance from REAR axle to CoG
# which is also = axle_distance * static_mass_front / total_mass
# for backwards compatibility with 1g file, rear_to_cog is the lever arm that loads the front

# for compatibility check:
# rear_to_cog_alt = axle_distance * static_mass_front / total_mass  # should equal rear_to_cog above

## slope stuff

downhill_angle_rad = math.radians(downhill_angle)   # convert deg -> rad

weight_normal_total = total_weight * math.cos(downhill_angle_rad)   # normal to slope
weight_parallel_total = total_weight * math.sin(downhill_angle_rad) # parallel to slope, downhill

## braking force / power (steady state: a = 0, braking balances gravity)

braking_force_total = weight_parallel_total   # F = m*g*sin(theta), constant speed

braking_power_total = braking_force_total * constant_speed   # P = F * v, Watts
# if constant_speed is None, this will error until filled - same as 1g file behaviour


# dynamic weight transfer on grade (moment equilibrium about rear contact patch)

""" derivation (steady downhill, constant speed, a=0)

define N1 N2 as dynamic normal loads on front/rear. CoG height = h normal to slope.
L = axle_distance, b = rear_to_cog (distance CoG to rear, downhill), c = front_to_cog

Coordinates: x downhill along slope, z normal outward from slope.
Origin at rear contact patch.

Forces at CoG:
  Fz = -total_weight * cos(theta)  (into slope)
  Fx = +total_weight * sin(theta)  (downhill)

Moment about rear:
  N1 * L + (b*(-W*cos) - h*(W*sin)) = 0
  => N1 * L = W*cos * b + W*sin * h

hence
  N1 = (W*cos * b + W*sin * h) / L
  N2 = W*cos - N1 = W*cos * c / L - W*sin * h / L

On horizontal theta=0 this reduces to N1 = W*b/L (static).

Braking distribution for ideal (no lockup) is proportional to normal loads:
  B1 = B_total * N1 / (W*cos)
  B2 = B_total - B1

Power distribution same ratio (P = B * v):
  P1 = P_total * N1 / (W*cos)
  P2 = P_total - P1

Energy per distance = B* distance, energy per time = power.
"""

dynamic_weight_front = (total_weight * math.cos(downhill_angle_rad) * rear_to_cog + total_weight * math.sin(downhill_angle_rad) * cog_height) / axle_distance
dynamic_weight_rear = weight_normal_total - dynamic_weight_front

dynamic_braking_force_front = braking_force_total * dynamic_weight_front / weight_normal_total
dynamic_braking_force_rear = braking_force_total - dynamic_braking_force_front

power_front = braking_power_total * dynamic_weight_front / weight_normal_total
power_rear = braking_power_total - power_front

# alternative: heat per second = power, heat per meter = braking_force
heat_rate_front = power_front        # Watts to front brakes
heat_rate_rear = power_rear          # Watts to rear brakes

# total energy / heat over the full descent
# energy = force * distance, also = power * time

descent_time = downhill_distance / constant_speed   # s, time to complete descent

energy_total = braking_force_total * downhill_distance   # J, also = braking_power_total * descent_time
energy_front = energy_total * dynamic_weight_front / weight_normal_total
energy_rear = energy_total - energy_front

# for compatibility with 1g dynamic.py naming:
heat_front = energy_front
heat_rear = energy_rear
heat_total = energy_total
