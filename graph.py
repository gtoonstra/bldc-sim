import cairo
from gi.repository import Gdk, Gtk

SIZE = 30

class Graph(Gtk.DrawingArea):

    def __init__ (self):
        Gtk.DrawingArea.__init__(self)
        self.connect('draw', self.draw)

        # Data elements are 2-tuples of desired and actual
        self.data1 = []
        self.data2 = []
        self.data3 = []
        self.data4 = []

    # Add new values to graphs
    def update_lists( self, a,b,c,d,e,f,g,h ):
        self.data1.append( (a,b) )
        self.data2.append( (c,d) )
        self.data3.append( (e,f) )
        self.data4.append( (g,h) )

        if ( len(self.data1) > 780 ):
            del self.data1[0]
            del self.data2[0]
            del self.data3[0]
            del self.data4[0]

    def draw_line( self, ctx, data, idx ):
        for i in xrange(len( data )):
            ctx.line_to( i, data[i][idx] )

    def draw_tuple( self, ctx, data ):
        ctx.set_source_rgb(0, 0, 0)
        self.draw_line( ctx, data, 0 )
        ctx.stroke()
        ctx.set_source_rgb(0, 0, 1)
        self.draw_line( ctx, data, 1 )
        ctx.stroke()

    def draw_data(self,ctx ):
        ctx.translate( 10, 50 )
        self.draw_tuple( ctx, self.data1 )

        ctx.translate( 0, 150 )
        self.draw_tuple( ctx, self.data1 )

        ctx.translate( 0, 150 )
        self.draw_tuple( ctx, self.data1 )

        ctx.translate( 0, 150 )
        self.draw_tuple( ctx, self.data1 )

    def draw(self, da, ctx):
        ctx.scale( 1.0, 1.0 )
        ctx.set_line_width(1)
        self.draw_data( ctx )


