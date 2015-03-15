# bldc-sim
A simulator written in python with some basic diagramming functions, intended
to be used for BLDC motor control analysis, using a PWM signal to control either
torque or speed (your controller decides that). 

The simulator internally updates a **simulator model**, which has hidden 
(not directly observable) parameters. The output of that model has two
different channels: 
- Observables, which are things that you *can* observe directly, like voltage and current
- Internal simulator values, which are used for graphical display only, but should not be used
  directly by a controller, because they cannot be directly measured in reality.

You plug in a **controller implementation**, which uses the observables as input. Of course,
whether this makes sense depends on your hardware realization. As this simulator is
developed to allow people to develop their own BLDC controller software, the simulator
allows you to *cheat* and use one of the internal simulator values as a temporary replacement,
until you have written your own bits for that specific part of the code.

The default included controller is a very simple cheating feed-forward controller, which 
simply outputs a voltage proportional to the incoming PWM signal on the basis of current angle.

There are four diagrams that provide feedback on what the motor is actually doing:
- Omega (electrical rpm) in rad/s
- Angle (the actual motor position converted to degrees)
- Current (at the bus, so from/to the battery)
- 

## Parts of a controller implementation

BLDC control now has a number of different implementations. The most basic of these implementations use:
- An algorithm to determine the current *electrical* angle of the rotor or bell.
- A module that acts on the incoming PWM signal, which determines how long to open the (high) mosfet.

These then have the following consequences:

* If the high mosfet is opened for longer, more current flows, so more torque is generated, so the motor runs faster.
* If the algorithm knows the electrical angle, it can decide which mosfets to switch and it can determine when
  to change between switching mosfets.

## Simulator details

### Frequencies

The simulator is a non-realtime discrete event simulator. This means that the time in which you see things happen
onscreen has no relationship with actual time. This makes it possible to run the simulator on any hardware and
it guarantees that the results of the simulator will be equal on any hardware.

The main simulator loop uses a 64kHz sampling rate/frequency. The reason for that is that most BLDC controller
won't have sampling or control loops higher than 32kHz and a simulation should typically run at a rate of at least
2x higher than the maximum sampling rate for the controller.

The **controller implementation** should use a different frequency to run on as a divisor (or multiplier) of at least 2.
The actual number depends on the capabilities of your hardware and for motor control, probably ranges between 8kHz to 32kHz.

### Simulator model

The simulator assumes:
- a star-wound motor
- sinusoidal back emf (many BLDC's use trapezoidal)
- a 2-pole motor, so electrical rpm == mechanical rpm

It uses the following state-space model:

```
[ Ua ]   [ Ra 0  0  ][ Ia ]    [Laa Lab Lac][ Ia ]   [ Ea ]
[ Ub ] = [ 0  Rb 0  ][ Ib ] + p[Lba Lbb Lbc][ Ib ] + [ Eb ]
[ Uc ]   [ 0  0  Rc ][ Ic ]    [Lca Lcb Lcc][ Ic ]   [ Ec ]
```

- U.. = Voltage applied over the windings
- Rx = Stator resistance per phase
- Ix = Stator phase currents
- p = time derivative operator (d/dt)
- Lxx = Inductance over each phase pair
- Ex = back emf in each phase


