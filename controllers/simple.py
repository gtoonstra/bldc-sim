import math

class SimpleController(object):
    def __init__( self ):
        self.omega = 0.0
        self.theta = 0.0
        self.I = 0.0
        self.bemf = 0.0
        self.DEG60 = math.pi / 3
        self.DEG120 = 2.0 * self.DEG60
        self.DEG180 = 3.0 * self.DEG60
        self.DEG240 = 4.0 * self.DEG60
        self.DEG300 = 5.0 * self.DEG60
        self.DEG360 = 6.0 * self.DEG60

    def step_sim( self, dt, elapsed, epoch, throttle, variables ):
        self.omega = variables["omega"]
        self.theta = variables["theta"]
        self.I = variables["I"]
        self.V = variables["V"]
        self.bemf = variables["bemfa"]

        va = 0.0
        vb = 0.0
        vc = 0.0

        if self.theta < self.DEG60:
            # first segment
            va = self.V * throttle / 100.0
            vb = -self.V * throttle / 100.0
            vc = 0.0
        elif self.theta < self.DEG120:
            # second segment
            va = self.V * throttle / 100.0
            vb = 0.0
            vc = -self.V * throttle / 100.0
        elif self.theta < self.DEG180:
            # second segment
            va = 0.0
            vb = self.V * throttle / 100.0
            vc = -self.V * throttle / 100.0
        elif self.theta < self.DEG240:
            # second segment
            va = -self.V * throttle / 100.0
            vb = self.V * throttle / 100.0
            vc = 0.0
        elif self.theta < self.DEG300:
            # second segment
            va = -self.V * throttle / 100.0
            vb = 0.0
            vc = self.V * throttle / 100.0
        elif self.theta < self.DEG360:
            # second segment
            va = 0.0
            vb = -self.V * throttle / 100.0
            vc = self.V * throttle / 100.0
        
        return va, vb, vc

    def get_variables( self ):
        return [ self.omega, self.theta, self.I, 0.0, self.bemf, 0.0 ]
        # return 0,0,0,0

    def get_errors( self ):
        return [ self.omega - self.omega, ( self.theta - self.theta ) * 180.0 / math.pi ]

def make_controller():
    return SimpleController()

