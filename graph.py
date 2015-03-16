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
        self.data5 = []
        self.data6 = []

    # Add new values to graphs
    def update_lists( self, a,b,c,d,e,f,g,h,i,j,k,l ):
        self.data1.append( (a,g) )
        self.data2.append( (b,h) )
        self.data3.append( (c,i) )
        self.data4.append( (d,j) )
        self.data5.append( (e,k) )
        self.data6.append( (f,l) )

        if ( len(self.data1) > 780 ):
            del self.data1[0]
            del self.data2[0]
            del self.data3[0]
            del self.data4[0]
            del self.data5[0]
            del self.data6[0]

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

    def draw_data(self,ctx ):
        ctx.translate( 10, 50 )
        self.draw_tuple( ctx, self.data1, 0.25 )

        ctx.translate( 0, 120 )
        self.draw_tuple( ctx, self.data2, 50.0/6.28 )

        ctx.translate( 0, 120 )
        self.draw_tuple( ctx, self.data3, 1.0 )

        ctx.translate( 0, 120 )
        self.draw_tuple( ctx, self.data4, 2.0 )

        ctx.translate( 0, 120 )
        self.draw_tuple( ctx, self.data5, 4.0 )

        ctx.translate( 0, 120 )
        self.draw_tuple( ctx, self.data6, 50.0 )

    def draw(self, da, ctx):
        ctx.scale( 1.0, 1.0 )
        ctx.set_line_width(1)
        self.draw_data( ctx )


