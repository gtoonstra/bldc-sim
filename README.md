# bldc-sim

A simulator written in python with some basic diagramming functions, intended
to be used for BLDC motor control analysis, using a PWM signal to control either
torque or speed (your controller decides that). 

The simulator internally updates a **simulator model**, which has hidden 
(not directly observable) parameters and variables. The most important of those are
passed to the control algorithm, where you can decide which ones to use for motor control.

You plug in a **controller implementation**, which uses some of the observables as input. 
Of course, whether you can actually use them depends on your hardware implementation.

Some algorithms use so-called "observers", which tend to converge to the actual values
over time. So the simulator allows you to *cheat* and use some of the internal variables
you cannot directly observe until you have your implementation for those observers
figured out.

The default included controller is a very simple cheating feed-forward controller, which 
simply outputs a voltage proportional to the incoming PWM signal on the basis of current angle.

There are four diagrams that provide feedback on what the motor is actually doing:
- Omega (electrical rpm) in rad/s
- Angle (the actual motor position converted to degrees)
- Current (at the bus, so from/to the battery)
- Total torque

## Parts of a controller implementation

BLDC control now has a number of different implementations. The most basic of these implementations use:
- An algorithm to determine the current *electrical* angle of the rotor or bell.
- A module that acts on the incoming PWM signal, which determines how long to open the (high) mosfet.

These then have the following consequences:

* If the high mosfet is opened for longer, more current flows, so more torque is generated, so the motor runs faster.
* If the algorithm knows the electrical angle, it can decide which mosfets to switch and it can determine when
  to change between switching mosfets.

You can find the existing controllers in the *controllers* directory. 

The controller receives a set of variables in a python dictionary (all floats), from which you must determine
which observables you can really use given your hardware. 

## Simulator details

### Frequencies

The simulator is a non-realtime discrete event simulator. This means that the time in which you see things happen
onscreen has no relationship with actual time. This makes it possible to run the simulator on any hardware and
it guarantees that the results of the simulator will be equal on any hardware and there's very little impact of
the actual scheduling behavior of the host computer.

The main simulator loop uses a 64kHz sampling rate/frequency. The reason for that is that most BLDC controller
won't have sampling or control loops higher than 32kHz and a simulation should typically run at a rate of at least
2x higher than the maximum sampling rate for the controller.

The **controller implementation** should use a different frequency to run on as a divisor (or multiplier) of at least 2.
The actual number depends on the capabilities of your hardware and for motor control, probably ranges between 8kHz to 32kHz.

One of the simulation constants is the speed of readout of throttle inputs. This is basically the slider at the bottom
of the screen. If it appears somewhat "sluggish", that's not a bug in the program but a feature. Since the simulation doesn't run
in realtime, you're seeing the update being applied at the correct point in time given the frequency of the simulation
versus the frequency of input updates.

The only thing your controller needs to return are three values: **which voltage to apply to windings A,B,C**

So you'd typically see some code like this `return va, vb, vc` at the end of the control algorithm.

In a real hardware implementation you'd then apply those variables in the PWM module. An actual implementation must then
also consider using scaling and fixed float implementations to make it more efficient. 

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

The change in mechanical RPM is effected through a friction model. It uses static friction with the motor in standstill,
then being replaced by a model using dynamic friction mostly influenced by a friction coefficient (dynamic) times
the rpm. 




