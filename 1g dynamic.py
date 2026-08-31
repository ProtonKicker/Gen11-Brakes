# Goal: Find [braking force distribution] and [braking power distribution]

# note that all calculations refer to front total + rear total



# constants

g = 9.81

initial_speed = 30   # m/s
final_speed = 0   # m/s
decel = 9.81   # deceleration, m/s^2

total_mass = None
static_mass_front = None
static_mass_rear = None

axle_distance = None
cog_height = None



# secondary variables for calculations

## weight stuff

total_weight = total_mass * g   # G = mg
static_weight_front = static_mass_front * g
static_weight_rear = static_mass_rear * g

front_to_cog = axle_distance * static_mass_front / total_mass
rear_to_cog = axle_distance - front_to_cog

## energy stuff

    #speed_change = initial_speed - final_speed
energy_change = 0.5 * total_mass * ( initial_speed ** 2 - final_speed ** 2 )   # 0.5*mv^2 - 0.5*mv^2

braking_force_total = total_mass * decel   # F = ma



# dynamic weight tranfer (net torque = 0)

""" derivation

define F1 F2 as dynamic weight on axles front and rear. F3 is on cog_height

F1 F2 upwards, F3 in the driving direction

F1 * axle_distance = total_weight * rear_to_cog + total_mass * decel * cog_height
    note that moment equilibrium is about the rear axle

yet since the car cant just be heavier than itself, so it is also true that

F1 + F2 = total_weight

thus

F1 = (total_weight * rear_to_cog + total_mass * decel * cog_height) / axle_distance
F2 = total_weight - F1

"""

dynamic_weight_front = (total_weight * rear_to_cog + total_mass * decel * cog_height) / axle_distance
dynamic_weight_rear = total_weight - dynamic_weight_front

dynamic_braking_force_front = braking_force_total * dynamic_weight_front / total_weight
dynamic_braking_force_rear = braking_force_total - dynamic_braking_force_front

heat_front = energy_change * dynamic_weight_front / total_weight
heat_rear = energy_change - heat_front
