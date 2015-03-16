import math
import simconstants

class Simulator(object):

    def __init__ (self):
        self.bemfa = 0.0
        self.bemfb = 0.0
        self.bemfc = 0.0
        # omega = rpm ( w )
        self.omega = 0.0

        # theta = electrical angle normalized to 2*pi
        self.theta = 0.0

        # mTheta = mechanical angle normalized to 2*pi
        self.mTheta = 0.0

        self.ia = 0.0
        self.ib = 0.0
        self.ic = 0.0
        self.I = 0.0
        self.didta = 0.0
        self.didtb = 0.0
        self.didtc = 0.0

        self.va = 0.0
        self.vb = 0.0
        self.vc = 0.0
    
        self.Pelec = 0.0
        self.Te = 0.0
        self.Tl = 0.0
        self.Tf = 0.0

        self.Ta = 0.0
        self.Tb = 0.0
        self.Tc = 0.0

    # The simulator 
    def step_sim( self, dt, elapsed, epoch, load, va, vb, vc ):
        # Set the load
        self.Tl = math.copysign( 1, self.omega ) * load
        self.va = va
        self.vb = vb
        self.vc = vc

        # Calculate bemf 
        self.bemfa = simconstants.BEMF_CONSTANT * self.omega * math.sin( self.theta )
        self.bemfb = simconstants.BEMF_CONSTANT * self.omega * math.sin( self.theta - simconstants.DEG_120_RAD )
        self.bemfc = simconstants.BEMF_CONSTANT * self.omega * math.sin( self.theta - simconstants.DEG_240_RAD )

        # Calculate change in current per di/dt
        self.didta = (1.0 / simconstants.La) * ( self.va - (simconstants.Ra * self.ia) - self.bemfa ) * dt
        self.didtb = (1.0 / simconstants.Lb) * ( self.vb - (simconstants.Rb * self.ib) - self.bemfb ) * dt
        self.didtc = (1.0 / simconstants.Lc) * ( self.vc - (simconstants.Rc * self.ic) - self.bemfc ) * dt

        # Apply changes to current in phases
        self.ia = self.ia + self.didta
        self.ib = self.ib + self.didtb
        self.ic = self.ic + self.didtc

        # Torque per phase. Since omega can be null, cannot derive from P/w
        self.Ta = simconstants.BEMF_CONSTANT * math.sin( self.theta ) * self.ia
        self.Tb = simconstants.BEMF_CONSTANT * math.sin( self.theta - simconstants.DEG_120_RAD ) * self.ib
        self.Tc = simconstants.BEMF_CONSTANT * math.sin( self.theta - simconstants.DEG_240_RAD ) * self.ic

        # Electrical power
        self.Pelec = self.bemfa * self.ia + self.bemfa * self.ib + self.bemfc * self.ic

        # Electrical torque
        # Add torque of all phases
        self.Te = self.Ta + self.Tb + self.Tc

        # Friction calculations
        if abs(self.omega) < 1.0:
            # At standstill. We have static friction to conquer.
            # If torque larger than torque required to counter static torque
            if abs(self.Te) > simconstants.STATIC_FRICTION:
                self.Tf = math.copysign( 1, self.Te ) * simconstants.STATIC_FRICTION
            else:
                self.Tf = 0.0
        else:
           # self.Tf = math.copysign( 1, self.Te ) * ( simconstants.STATIC_FRICTION * math.exp( -50 * abs( self.omega )) + simconstants.FRICTION_S + simconstants.Bfriction * self.omega )
           self.Tf = math.copysign( 1, self.omega ) * ( simconstants.STATIC_FRICTION * math.exp( -50 * abs( self.omega )) + simconstants.FRICTION_S + simconstants.Bfriction * abs(self.omega) )

        # Calculate change in mechanical rpm
        torque = ( self.Te - self.Tl - self.Tf )

        # J is the moment of inertia
        dOmega = (1.0 / simconstants.J) * torque * dt
        self.omega = self.omega + dOmega

        self.I = 0.0
        if self.ia > 0.0:
            self.I = self.I + self.ia
        if self.ib > 0.0:
            self.I = self.I + self.ib
        if self.ic > 0.0:
            self.I = self.I + self.ic

        self.theta += dt * self.omega
        self.theta = self.theta % ( 2.0 * math.pi )

        return self.omega, self.theta, self.I, self.Te

    def get_variables( self ):
        ret = {}
        ret[ "va" ] = self.va
        ret[ "vb" ] = self.vb
        ret[ "vc" ] = self.vc
        ret[ "ia" ] = self.ia
        ret[ "ib" ] = self.ib
        ret[ "ic" ] = self.ic
        ret[ "I" ] = self.I
        ret[ "V" ] = simconstants.BUSVOLTAGE
        ret[ "omega" ] = self.omega
        ret[ "theta" ] = self.theta
        ret[ "bemfa" ] = self.bemfa
        ret[ "bemfb" ] = self.bemfb
        ret[ "bemfc" ] = self.bemfc
        ret[ "torque" ] = self.Te
        ret[ "loadtorque" ] = self.Tl
        ret[ "frictiontorque" ] = self.Tf
        return ret

