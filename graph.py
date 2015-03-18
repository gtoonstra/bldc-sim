import cairo
from gi.repository import Gdk, Gtk

SIZE = 30

class Graph(Gtk.DrawingArea):

    def __init__ (self, scale):
        Gtk.DrawingArea.__init__(self)
        self.connect('draw', self.draw)

        self.scale = scale
        # Data elements are 2-tuples of desired and actual

        self.data = []

    # Add new values to graphs
    def update_graph( self, a,b ):
        self.data.append( (-a,-b) )

        if ( len(self.data) > 780 ):
            del self.data[0]
        self.queue_draw()

    def draw_line( self, ctx, data, idx, factor ):
        for i in xrange(len( data )):
            ctx.line_to( i, data[i][idx] * factor )

    def draw_tuple( self, ctx, data, factor ):
        ctx.set_source_rgb(0, 0, 1)
        self.draw_line( ctx, data, 0, factor )
        ctx.stroke()
        ctx.set_source_rgb(1, 0, 0)
        self.draw_line( ctx, data, 1, factor )
        ctx.stroke()
        ctx.set_source_rgb(0, 0, 0)
        ctx.move_to( 780, -50 )
        ctx.line_to( 780, 50 )
        ctx.stroke()
        ctx.move_to( 0, 0 )
        ctx.line_to( 780, 0 )
        ctx.stroke()

    def draw_data(self,ctx, scale ):
        ctx.translate( 10, 50 )
        self.draw_tuple( ctx, self.data, scale )

    def draw(self, da, ctx):
        ctx.scale( 1.0, 1.0 )
        ctx.set_line_width(1)
        self.draw_data( ctx, self.scale )

