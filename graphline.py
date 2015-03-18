from gi.repository import Gdk, Gtk
from graph import Graph

class GraphTable(Gtk.Table):

    def __init__ (self):
        Gtk.Table.__init__(self)
        self.resize( 6, 3 )
        self.graphs = []
        self.values = []

    def add_row( self, name, scale ):
        ln = Gtk.Label( name )
        vlabel = Gtk.Label( "0.00 / 0.00" )
        graph = Graph( scale )
    
        self.graphs.append( graph )
        self.values.append( vlabel )

        numrows = len(self.graphs)
        self.attach( ln, 0, 1, numrows, numrows+1, Gtk.AttachOptions.FILL, Gtk.AttachOptions.FILL )
        self.attach( graph, 1, 2, numrows, numrows+1 )
        self.attach( vlabel, 2, 3, numrows, numrows+1, Gtk.AttachOptions.FILL, Gtk.AttachOptions.FILL )

    def update_data( self, l1, l2 ):
        for i in xrange(0,len(l1)):
            self.graphs[i].update_graph( l1[i],l2[i] )
            self.values[i].set_text( "%3.2f / %3.2f"%( l1[i], l2[i] )) 

