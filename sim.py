#!/usr/bin/env python
"""
Based on cairo-demo/X11/cairo-demo.c
"""
from gi.repository import Gdk, Gtk, GObject
from graph import Graph
import simconstants
from simulator import Simulator
import sys
import argparse

class SimulatorWindow(Gtk.Window):
    def __init__(self, controller):
        super( SimulatorWindow, self ).__init__()
        self.controller = controller
        self.elapsed = 0.0
        self.epoch = 0
        self.throttleval = 0.0
        self.loadval = 0.0
        self.committedThrottleVal = 0.0
        self.dt = 1.0 / simconstants.SIMFREQ
        self.va = 0.0
        self.vb = 0.0
        self.vc = 0.0

        self.connect('destroy', lambda w: Gtk.main_quit())
        self.set_default_size(800, 650)

        vbox = Gtk.VBox()
        self.add(vbox)

        self.graph = Graph()
        vbox.pack_start(self.graph, True, True, 0)

        hbox = Gtk.HBox()
        self.pwm = self.add_label( "throttle (%): ", hbox )
        adj1 = Gtk.Adjustment(0.0, 0.0, 101.0, 0.1, 1.0, 1.0)
        self.throttlescale = Gtk.HScale()
        self.throttlescale.set_adjustment( adj1 )
        self.throttlescale.set_digits(1)
        self.throttlescale.set_draw_value(True)
        hbox.pack_start( self.throttlescale, True, True, 0 )
        self.throttlescale.connect( "change-value", self.change_throttle )

        self.load = self.add_label( "load (Nm): ", hbox )
        adj2 = Gtk.Adjustment(0.0, 0.0, 5.0, 0.01, 1.0, 1.0)
        self.loadscale = Gtk.HScale()
        self.loadscale.set_adjustment( adj2 )
        self.loadscale.set_digits(2)
        self.loadscale.set_draw_value(True)
        hbox.pack_start( self.loadscale, True, True, 0 )
        self.loadscale.connect( "change-value", self.change_load )

        vbox.pack_start(hbox, False, False, 0)
        self.sim = Simulator()

        GObject.timeout_add( 5, self.callback )

        self.show_all()

    def run( self ):
        Gtk.main()

    def add_label( self, labelname, hbox ):
        ln = Gtk.Label( labelname )
        vlabel = Gtk.Label( "0.00" )
        hbox.pack_start( ln, True, True, 0 )
        hbox.pack_start( vlabel, True, True, 0 )
        return vlabel

    def change_throttle( self, scale, scroll, value ):
        if value > 100.0:
            value = 100.0
        if value < 0.0:
            value = 0.0
        self.throttleval = value
        return

    def change_load( self, scale, scroll, value ):
        if value > 5.0:
            value = 5.0
        if value < 0.0:
            value = 0.0
        self.loadval = value
        self.load.set_text( "%3.2f"%( self.loadval )) 
        return

    def callback( self ):
        self.elapsed = self.elapsed + (1.0 / self.dt)
        self.epoch = self.epoch + 1

        if self.epoch % simconstants.THROTTLE_INTERVAL == 0:
            self.committedThrottleVal = self.throttleval
            self.pwm.set_text( "%3.2f"%( self.committedThrottleVal )) 

        process_variables = self.sim.get_variables()

        if self.epoch % simconstants.CONTROLLER_INTERVAL == 0:
            self.va, self.vb, self.vc = self.controller.step_sim( self.dt, self.elapsed, self.epoch, self.committedThrottleVal, process_variables )

        # t = t in s after last step
        a,b,c,d = self.sim.step_sim( self.dt, self.elapsed, self.epoch, self.loadval, self.va, self.vb, self.vc )
        e,f,g,h = self.controller.get_variables()

        self.graph.update_lists( a,b,c,d,e,f,g,h )
        self.graph.queue_draw()

        return True

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("controller", help="Specify name of controller module (.py file minus directory)")
    args = parser.parse_args()

    mod = get_module( args.controller )
    controller = mod.make_controller()

    win = SimulatorWindow( controller )
    win.run()

def get_module(name):
    name = "controllers." + name
    mod = __import__(name, fromlist=[''])
    return mod

if __name__ == '__main__':
    main()

