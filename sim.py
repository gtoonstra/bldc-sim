#!/usr/bin/env python
"""
Based on cairo-demo/X11/cairo-demo.c
"""
from gi.repository import Gdk, Gtk, GObject
from graph import Graph

class SimulatorWindow(Gtk.Window):
    def __init__(self):
        super( SimulatorWindow, self ).__init__()
        self.t = 0.0
        self.n = 0
    
        self.connect('destroy', lambda w: Gtk.main_quit())
        self.set_default_size(800, 650)

        vbox = Gtk.VBox()
        self.add(vbox)

        self.graph = Graph()
        vbox.pack_start(self.graph, True, True, 0)

        hbox = Gtk.HBox()
        plusbtn = Gtk.Button( "+" )
        plusbtn.connect( "clicked" , self.addpwm )
        hbox.pack_start( plusbtn, True, True, 0 )
        minbtn = Gtk.Button( "-" )
        minbtn.connect( "clicked" , self.subtractpwm )
        hbox.pack_start( minbtn, True, True, 0 )
        self.pwm = self.add_label( "pwm: ", hbox )

        vbox.pack_start(hbox, False, False, 0)
        # self.sim = Simulator()

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

    def addpwm( self, btn ):
        sim.movepwm(1)

    def subtractpwm( self, btn ):
        sim.movepwm(-1)

    def callback( self ):
        t = t + 1.0 / constants.FREQ
        n = n + 1

        pwm.set_text( "%d"%(sim.getPwm()) )

        # t = t in s after last step
        a,b,c,d,e,f,g,h = sim.step_sim( t, n )
        self.graph.update_lists( a,b,c,d,e,f,g,h )
        self.graph.queue_draw()

        return True

def main():
    win = SimulatorWindow()
    win.run()


if __name__ == '__main__':
    main()

