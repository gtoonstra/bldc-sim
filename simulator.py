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

        self.va = 0.0
        self.vb = 0.0
        self.vc = 0.0
    
        self.Pelec = 0.0
        self.Te = 0.0
        self.Tl = 0.0

        self.Ta = 0.0
        self.Tb = 0.0
        self.Tc = 0.0

    # The simulator 
    def step_sim( self, dt, elapsed, epoch, load, va, vb, vc ):
        # Set the load
        sign = math.copysign( 1, self.omega )
        self.Tl = sign * load
        self.va = va
        self.vb = vb
        self.vc = vc

        # Calculate bemf 
        self.bemfa = simconstants.BEMF_CONSTANT * self.omega * math.sin( self.theta )
        self.bemfb = simconstants.BEMF_CONSTANT * self.omega * math.sin( self.theta - simconstants.DEG_120_RAD )
        self.bemfc = simconstants.BEMF_CONSTANT * self.omega * math.sin( self.theta - simconstants.DEG_240_RAD )

        # Calculate change in current per di/dt
        dot_ia = (1.0 / simconstants.La) * ( self.va - (simconstants.Ra * self.ia) - self.bemfa )
        dot_ib = (1.0 / simconstants.Lb) * ( self.vb - (simconstants.Rb * self.ib) - self.bemfb )
        dot_ic = (1.0 / simconstants.Lc) * ( self.vc - (simconstants.Rc * self.ic) - self.bemfc )

        # Apply changes to current in phases
        self.ia = self.ia + dot_ia * dt
        self.ib = self.ib + dot_ib * dt
        self.ic = self.ic + dot_ic * dt

        # Torque per phase. Since omega can be null, cannot derive from P/w
        self.Ta = simconstants.BEMF_CONSTANT * math.sin( self.theta ) * self.ia
        self.Tb = simconstants.BEMF_CONSTANT * math.sin( self.theta - simconstants.DEG_120_RAD ) * self.ib
        self.Tc = simconstants.BEMF_CONSTANT * math.sin( self.theta - simconstants.DEG_240_RAD ) * self.ic

        # Electrical power
        self.Pelec = self.bemfa * self.ia + self.bemfa * self.ib + self.bemfc * self.ic

        # Electrical torque
        # Add torque of all phases
        self.Te = self.Ta + self.Tb + self.Tc

        # Mechanical torque.
        # mtorque = ((etorque * (p->m->NbPoles / 2)) - (p->m->damping * sv->omega) - p->pv->torque);
        self.Tm = ((self.Te * (simconstants.NUM_POLES / 2)) - (sign * simconstants.Bdamping * abs(self.omega)) - self.Tl)

        # Friction calculations
        if abs(self.omega) < 1.0:
            if abs(self.Te) < simconstants.STATIC_FRICTION:
                self.Tm = 0.0
            else:
                self.Tm = self.Tm - simconstants.STATIC_FRICTION
        else:
           self.Tm = self.Tm - sign * ( simconstants.STATIC_FRICTION * math.exp( -5 * abs( self.omega )) + simconstants.FRICTION_S )

        # J is the moment of inertia
        dotOmega = (self.Tm / simconstants.J)
        self.omega = self.omega + dotOmega * dt

        self.I = 0.0
        if self.ia > 0.0:
            self.I = self.I + self.ia
        if self.ib > 0.0:
            self.I = self.I + self.ib
        if self.ic > 0.0:
            self.I = self.I + self.ic

        self.theta += self.omega * dt
        self.theta = self.theta % ( 2.0 * math.pi )

        return [self.omega, self.theta, self.va, self.ia, self.bemfa, self.Te]

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
        return ret

