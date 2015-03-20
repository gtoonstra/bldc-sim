import math

SIMFREQ = 64000
MIN_PWM = 1000
MAX_PWM = 2000
# 128 corresponds to ~ 500Hz, which is what many ESC's use nowadays.
THROTTLE_INTERVAL = 128
# 4 corresponds to 64/4 = 16kHz
CONTROLLER_INTERVAL = 4
# slow loop interval for PID updates, 64kHz / 64 = 1kHz
SLOW_INTERVAL = 64

BEMF_CONSTANT = 0.0137
DEG_120_RAD = 2.0 * math.pi / 3
DEG_240_RAD = 4.0 * math.pi / 3

# Motor specifics
# L here is L subtracted by mutual inductance M.
La = 0.000036
Lb = 0.000036
Lc = 0.000036

Ra = 0.52
Rb = 0.52
Rc = 0.52

Bdamping = 0.00001
J = 0.000012

STATIC_FRICTION = 0.01
FRICTION_S = 0.01
RPM_MAX = 900.0
RPM_MIN = 0.0

BUSVOLTAGE = 15.0
NUM_POLES = 2

