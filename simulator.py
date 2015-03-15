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
        self.Tl = load
        self.va = va
        self.vb = vb
        self.vc = vc

        # Calculate bemf
        self.bemfa = simconstants.BEMF_CONSTANT * self.omega * math.sin( self.theta )
        self.bemfb = simconstants.BEMF_CONSTANT * self.omega * math.sin( self.theta - simconstants.DEG_120_RAD )
        self.bemfc = simconstants.BEMF_CONSTANT * self.omega * math.sin( self.theta - simconstants.DEG_240_RAD )

        # Calculate change in current per di/dt
        self.didta = (1.0 / simconstants.La) * ( self.va - (simconstants.Ra * self.ia) - self.bemfa )
        self.didtb = (1.0 / simconstants.Lb) * ( self.vb - (simconstants.Rb * self.ib) - self.bemfb )
        self.didtc = (1.0 / simconstants.Lc) * ( self.vc - (simconstants.Rc * self.ic) - self.bemfc )

        # Apply changes to current in phases
        self.ia = self.ia + self.didta
        self.ib = self.ib + self.didtb
        self.ic = self.ic + self.didtc

        # Torque per phase. Since omega can be null, cannot derive from P/w
        self.Ta = simconstants.BEMF_CONSTANT * math.sin( self.theta )
        self.Tb = simconstants.BEMF_CONSTANT * math.sin( self.theta - simconstants.DEG_120_RAD )
        self.Tc = simconstants.BEMF_CONSTANT * math.sin( self.theta - simconstants.DEG_240_RAD )

        # Electrical power
        self.Pelec = self.bemfa * self.ia + self.bemfa * self.ib + self.bemfc * self.ic

        # Electrical torque
        # Add torque of all phases
        self.Te = self.Ta + self.Tb + self.Tc

        # Friction calculations
        if self.omega < 0.001:
            # At standstill. We have static friction to conquer.
            # If torque larger than torque required to counter static torque
            if abs(self.Te) > simconstants.STATIC_FRICTION:
                self.Tf = math.sign( self.Te ) * simconstants.STATIC_FRICTION
            else:
                self.Tf = self.Te
        else:
           self.Tf = math.sign( self.Te ) * ( simconstants.STATIC_FRICTION * math.exp( -50 * math.abs( self.omega )) + simconstants.FRICTION_S + simconstants.Bfriction * self.omega )

        # Calculate change in mechanical rpm
        dOmega = (1.0 / simconstants.J) * ( self.Te - self.Tl - self.Tf )
        self.omega = self.omega + dOmega

        return self.ia, self.va, 0,0,0,0,0,0

    def get_observables( self ):
        ret = {}
        ret[ "va" ] = self.va
        ret[ "vb" ] = self.va
        ret[ "vc" ] = self.va
        ret[ "ia" ] = self.ia
        ret[ "ib" ] = self.ib
        ret[ "ic" ] = self.ic
        return ret

    def get_nonobservables( self ):
        ret = {}
        ret[ "omega" ] = self.omega
        ret[ "theta" ] = self.theta
        ret[ "bemfa" ] = self.bemfa
        ret[ "bemfb" ] = self.bemfb
        ret[ "bemfc" ] = self.bemfc
        ret[ "torque" ] = self.Te
        ret[ "loadtorque" ] = self.Tl
        ret[ "frictiontorque" ] = self.Tf
        return ret

