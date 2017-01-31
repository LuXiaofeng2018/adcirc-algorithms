import sys
import random
from validate import validate14

class Fort14:

    def __init__( self, f14 ):

        self.node_shuffle = False
        self.element_shuffle = False
        self.node_offsets = []
        self.element_offsets = []
        self.elevation_boundaries = []
        self.flow_boundaries = []
        self.f14 = f14

        with open( f14, 'r' ) as f:

            self.nodes = dict()
            self.elements = dict()
            self.h1 = f.readline().strip()
            self.h2 = f.readline().strip()

            dat_line = self.h2.split()
            self.num_nodes = int( dat_line[1] )
            self.num_elements = int( dat_line[0] )

            for l in range( self.num_nodes ):

                line = f.next().split()
                n = int( line[0] )
                self.nodes[ n ] = line[1], line[2], line[3]

            for l in range( self.num_elements ):

                line = f.next().split()
                e = int( line[0] )
                n1 = int( line[2] )
                n2 = int( line[3] )
                n3 = int( line[4] )
                self.elements[ e ] = n1, n2, n3

            self.nope = int( f.next().split()[0] )
            self.neta = int( f.next().split()[0] )

            for segment in range( self.nope ):

                segnodes = int( f.next().split()[0] )
                segment = []

                for segnode in range( segnodes ):
                    segment.append( int( f.next().split()[0] ) )

                self.elevation_boundaries.append( segment )

            self.nbou = int( f.next().split()[0] )
            self.nvel = int( f.next().split()[0] )

            for segment in range( self.nbou ):

                segnodes = int( f.next().split()[0] )
                segment = []

                for segnode in range( segnodes ):
                    segment.append( int( f.next().split()[0] ) )

                self.flow_boundaries.append( segment )


    def info( self ):

        print self.f14
        print 'Nodes:', self.num_nodes
        print 'Elements:', self.num_elements

    def shuffle_nodes( self ):

        self.node_shuffle = True

    def shuffle_elements( self ):

        self.element_shuffle = True

    def offset_nodes( self, n, start=0, end=0 ):

        if end == 0:
            end = self.num_nodes

        self.node_offsets.append((start, end, n))

    def offset_elements( self, n, start=0, end=0 ):

        if end == 0:
            end = self.num_elements

        self.element_offsets.append((start, end, n))

    def write( self, o14 ):

        old_to_new_nodes = dict()
        old_to_new_elements = dict()
        nodes = [ i+1 for i in range( self.num_nodes ) ]
        elements = [ e+1 for e in range( self.num_elements ) ]

        # Apply shuffling

        if self.node_shuffle:
            random.shuffle( nodes )

        if self.element_shuffle:
            random.shuffle( elements )

        for i in range( self.num_nodes ):

            old_to_new_nodes[ i+1 ] = nodes[ i ]

        for i in range( self.num_elements ):

            old_to_new_elements[ i+1 ] = elements[ i ]

        # Apply offsets

        for start, end, n in self.node_offsets:

            for i in range( start, end ):

                old_to_new_nodes[ i+1 ] += n

        for start, end, n in self.element_offsets:

            for i in range( start, end ):

                old_to_new_elements[ i+1 ] += n

        # Check for valid node numbers
        check = dict()
        for old, new in old_to_new_nodes.iteritems():
            if new in check:
                print 'ERROR - Duplicate node number:', new
                return
            check[ new ] = old

        check.clear()
        for old, new in old_to_new_elements.iteritems():
            if new in check:
                print 'ERROR - Duplicate element number:', new
                return
            check[ new ] = old

        with open( o14, 'w' ) as f:

            f.write( self.h1 + '\n' )
            f.write( self.h2 + '\n' )

            node_nums = [ i+1 for i in range( self.num_nodes ) ]
            element_nums = [ i+1 for i in range( self.num_elements ) ]
            if self.node_shuffle:
                random.shuffle( node_nums )
            if self.element_shuffle:
                random.shuffle( element_nums )

            for i in node_nums:

                old_node = i
                new_node = old_to_new_nodes[ old_node ]
                x, y, z = self.nodes[ old_node ]
                f.write('{}\t{}\t{}\t{}\n'.format( new_node, x, y, z ) )

            for i in element_nums:

                old_element = i
                new_element = old_to_new_elements[ old_element ]
                n1, n2, n3 = self.elements[ old_element ]
                n1 = old_to_new_nodes[ n1 ]
                n2 = old_to_new_nodes[ n2 ]
                n3 = old_to_new_nodes[ n3 ]
                f.write('{}\t3\t{}\t{}\t{}\n'.format( new_element, n1, n2, n3 ) )

            f.write( '{}\n'.format( self.nope ) )
            f.write( '{}\n'.format( self.neta ) )

            for segment in self.elevation_boundaries:

                f.write( '{}\n'.format( len( segment ) ) )

                for n in segment:

                    f.write( '{}\n'.format( old_to_new_nodes[n] ) )

            f.write( '{}\n'.format( self.nbou ) )
            f.write( '{}\n'.format( self.nvel ) )

            for segment in self.flow_boundaries:

                f.write( '{}\n'.format( len( segment ) ) )

                for n in segment:

                    f.write( '{}\n'.format( old_to_new_nodes[n] ) )

def parse_input( options ):

    infile = options[0]
    outfile = options[1]
    validate = False

    i = 2

    f14 = Fort14( infile )
    f14.info()

    while i < len( options ):

        if options[i] == '-v':
            validate = True
            i += 1
            continue

        if options[i] == '-sn':
            print 'Shuffling nodes'
            f14.shuffle_nodes()
            i += 1
            continue

        if options[i] == '-se':
            print 'Shuffling elements'
            f14.shuffle_elements()
            i += 1
            continue

        if options[i] == '-on':
            i += 1
            n = int( options[i] )
            i += 1
            if i >= len( options ) or options[i][0] == '-':
                print 'Offsetting all nodes by', n
                f14.offset_nodes( n )
            else:
                start = int( options[i] )
                i += 1
                if i >= len( options ) or options[i][0] == '-':
                    print 'Offsetting nodes', start, 'through NP by', n
                    f14.offset_nodes( n, start-1 )
                else:
                    end = int( options[i] )
                    i += 1
                    print 'Offsetting nodes', start, 'through', end, 'by', n
                    f14.offset_nodes( n, start-1, end-1 )
            continue

        if options[i] == '-oe':
            i += 1
            n = int( options[i] )
            i += 1
            if i >= len( options ) or options[i][0] == '-':
                print 'Offsetting all elements by', n
                f14.offset_elements( n )
            else:
                start = int( options[i] )
                i += 1
                if i >= len( options ) or options[i][0] == '-':
                    print 'Offsetting elements', start, 'through NE by', n
                    f14.offset_elements( n, start-1 )
                else:
                    end = int( options[i] )
                    i += 1
                    print 'Offsetting elements', start, 'through', end, 'by', n
                    f14.offset_elements( n, start-1, end-1 )
            continue

        print 'Argument not recognized:', options[i]
        i += 1

    f14.write( outfile )

    if validate:
        validate14( infile, outfile )

def test( infile, outfile ):

    f14 = Fort14( infile )
    f14.info()
    f14.offset_nodes( 100 )
    f14.offset_elements( 100 )
    f14.shuffle_nodes()
    f14.shuffle_elements()
    f14.write( outfile )

if __name__ == '__main__':

    parse_input( sys.argv[1:] )