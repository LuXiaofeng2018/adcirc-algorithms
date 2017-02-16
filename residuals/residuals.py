import sys
import math
import matplotlib.pyplot as plt

class Fort14:

    def __init__( self, f14 ):

        self.elevation_boundaries = []
        self.flow_boundaries = []
        self.f14 = f14

        with open( f14, 'r' ) as f:

            self.nodes = dict()
            self.elements = dict()
            self.element_keys = []
            self.h1 = f.readline().strip()
            self.h2 = f.readline().strip()

            dat_line = self.h2.split()
            self.num_nodes = int( dat_line[1] )
            self.num_elements = int( dat_line[0] )

            for l in range( self.num_nodes ):

                line = f.next().split()
                n = int( line[0] )
                self.nodes[ n ] = float( line[1] ), float( line[2] ), float( line[3] )

            for l in range( self.num_elements ):

                line = f.next().split()
                e = int( line[0] )
                n1 = int( line[2] )
                n2 = int( line[3] )
                n3 = int( line[4] )
                self.element_keys.append( e )
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

def calculate_residuals ( f14, residuals_file, output_file ):

    fort14 = Fort14( f14 )

    with open( residuals_file, 'r' ) as r, open( output_file, 'w' ) as w:

        dt = float( r.readline().split()[0] )

        current = 0
        data = dict()

        for line in r:

            if current == 0:

                ts = line.split()[1]
                current += 1

            elif current <= fort14.num_nodes:

                dat = line.split()

                data[ int( dat[0] ) ] = map( lambda x: float(x), dat[1:len(dat)] )

                current += 1

                if current > fort14.num_nodes:

                    w.write('Timestep {}\n'.format(ts))

                    for element in fort14.element_keys:

                        n1, n2, n3 = fort14.elements[ element ]

                        node1 = dict()
                        node2 = dict()
                        node3 = dict()

                        node1['x'], node1['y'], node1['z'] = fort14.nodes[ n1 ]
                        node2['x'], node2['y'], node2['z'] = fort14.nodes[ n2 ]
                        node3['x'], node3['y'], node3['z'] = fort14.nodes[ n3 ]

                        node1['e0'], node1['u0'], node1['v0'], node1['e1'], node1['u1'], node1['v1'] = data[ n1 ]
                        node2['e0'], node2['u0'], node2['v0'], node2['e1'], node2['u1'], node2['v1'] = data[ n2 ]
                        node3['e0'], node3['u0'], node3['v0'], node3['e1'], node3['u1'], node3['v1'] = data[ n3 ]

                        e1 = [ node1, node2 ]
                        e2 = [ node2, node3 ]
                        e3 = [ node3, node1 ]


                        # Calculate average elevation for each timestep
                        xi0 = ( node1['e0'] + node2['e0'] + node3['e0'] ) / 3.0
                        xi1 = ( node1['e1'] + node2['e1'] + node3['e1'] ) / 3.0

                        # Calculate area of the element
                        area = 0.5 * abs( (node1['x']-node3['x'])*(node2['y']-node1['y']) - (node1['x']-node2['x'])*(node3['y']-node1['y']) )

                        # Calculate Qnets
                        Qnet0 = 0
                        Qnet1 = 0
                        for edge in [ e1, e2, e3 ]:

                            # Calculate edge length
                            l = math.sqrt( ( edge[1]['x'] - edge[0]['x'] )**2 + ( edge[1]['y'] - edge[0]['y'] )**2 )

                            # Calculate normal vector
                            norm = ( ( edge[1]['y'] - edge[0]['y'] ) / l, -( edge[1]['x'] - edge[0]['x'] ) / l )

                            # Calculate normalized velocities at nodes
                            U0n0 = edge[0]['u0'] * norm[0] + edge[0]['v0'] * norm[1]
                            U0n1 = edge[1]['u0'] * norm[0] + edge[1]['v0'] * norm[1]
                            U1n0 = edge[0]['u1'] * norm[0] + edge[0]['v1'] * norm[1]
                            U1n1 = edge[1]['u1'] * norm[0] + edge[1]['v1'] * norm[1]

                            # Calculate water column depth at each node
                            H0n0 = edge[0]['z'] + edge[0]['e0']
                            H0n1 = edge[1]['z'] + edge[1]['e0']
                            H1n0 = edge[0]['z'] + edge[0]['e1']
                            H1n1 = edge[1]['z'] + edge[1]['e1']

                            # Add contribution to Qnets
                            Qnet0 += ( l / 6.0 ) * ( 2*H0n0*U0n0 + H0n0*U0n1 + H0n1*U0n0 + 2*H0n1*U0n1 )
                            Qnet1 += ( l / 6.0 ) * ( 2*H1n0*U1n0 + H1n0*U1n1 + H1n1*U1n0 + 2*H1n1*U1n1 )

                        # Calculate approximation of time integral to get Qnet
                        Qnet = 0.5 * ( Qnet0 + Qnet1 ) * dt

                        # Calculate residal
                        residual = area * ( xi1 - xi0 ) + Qnet

                        # Write residual value to file
                        w.write( '{}\t{}\n'.format( element, residual ) )

                    current = 0

if __name__ == '__main__':

    calculate_residuals( sys.argv[1], sys.argv[2], sys.argv[3] )