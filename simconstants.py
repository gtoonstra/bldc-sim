import math

SIMFREQ = 64000
MIN_PWM = 1000
MAX_PWM = 2000
# 128 corresponds to ~ 500Hz, which is what many ESC's use nowadays.
THROTTLE_INTERVAL = 128
CONTROLLER_INTERVAL = 4

BEMF_CONSTANT = 0.0537
DEG_120_RAD = 2.0 * math.pi / 3
DEG_240_RAD = 4.0 * math.pi / 3

# Motor specifics
# L here is L subtracted by mutual inductance M.
La = 0.00036
Lb = 0.00036
Lc = 0.00036

Ra = 1.05
Rb = 1.05
Rc = 1.05

Bfriction = 0.001
J = 0.0001

STATIC_FRICTION = 0.1
FRICTION_S=0.1

BUSVOLTAGE = 15.0

