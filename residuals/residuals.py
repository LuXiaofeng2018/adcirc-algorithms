import sys
import math

class FortND:

    def __init__( self, fortnd ):

        self.f = open( fortnd, 'r' )
        self.f.readline()

        info_line = self.f.readline().split()

        self.num_datasets = int( info_line[0] )
        self.num_records = int( info_line[1] )
        self.ts_interval = int( info_line[3] )
        self.ts = float( info_line[2] ) / self.ts_interval
        self.n_dims = int( info_line[4] )

        self.current_dataset = 0

    def dt( self ):

        return self.ts

    def num_nodes( self ):

        return self.num_records

    def next_timestep( self ):

        if self.current_dataset < self.num_datasets:

            data = dict()

            header = self.f.readline().split()
            data[ 'model_time' ] = float( header[0] )
            data[ 'model_timestep' ] = int( header[1] )

            for i in range( self.num_records ):

                dat = self.f.readline().split()

                if self.n_dims == 1:
                    data[ int( dat[0] ) ] = float( dat[1] )
                if self.n_dims == 2:
                    data[ int( dat[0] ) ] = ( float( dat[1] ), float( dat[2] ) )
                if self.n_dims == 3:
                    data[ int( dat[0] ) ] = ( float( dat[1] ), float( dat[2] ), float( dat[2] ) )

            self.current_dataset += 1

            return data

        else:

            return None

    def percent_read( self ):

        return 100 * ( float(self.current_dataset) / float(self.num_datasets) )

    def __del__( self ):

        self.f.close()

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

def calculate_residuals ( f14, prev_ele, curr_ele, prev_vel, curr_vel, output_file ):

    fort14 = Fort14( f14 )
    prev_ele = FortND( prev_ele )
    curr_ele = FortND( curr_ele )
    prev_vel = FortND( prev_vel )
    curr_vel = FortND( curr_vel )

    if prev_ele.dt() == curr_ele.dt() and curr_ele.dt() == prev_vel.dt() and prev_vel.dt() == curr_vel.dt():
        dt = prev_ele.dt()
    else:
        print 'Data files do not have the same timestep'
        return

    if ( prev_ele.num_nodes() != curr_ele.num_nodes() or
         curr_ele.num_nodes() != prev_vel.num_nodes() or
         prev_vel.num_nodes() != curr_vel.num_nodes() ):

        print 'Data files do not have the same number of nodes'
        return

    # Define a check for -99999 values
    def is_dry(node):
        for k in ['e0', 'e1', 'u0', 'u1', 'v0', 'v1']:
            if node[k] == -99999:
                return True
        return False

    with open( output_file, 'w' ) as w:

        p_ele = prev_ele.next_timestep()
        c_ele = curr_ele.next_timestep()
        p_vel = prev_vel.next_timestep()
        c_vel = curr_vel.next_timestep()

        while p_ele is not None and c_ele is not None and p_vel is not None and c_vel is not None:

            print 'Processing dataset ' + str(prev_ele.current_dataset) + '/' + str(prev_ele.num_datasets) + '\t' + str( prev_ele.percent_read() ) + '% complete'

            w.write( 'Timestep {0}\n'.format( p_ele[ 'model_timestep' ] ) )

            for element in fort14.element_keys:

                n1, n2, n3 = fort14.elements[ element ]

                node1 = dict(
                    x = fort14.nodes[ n1 ][0],
                    y = fort14.nodes[ n1 ][1],
                    z = fort14.nodes[ n1 ][2],
                    e0 = p_ele[ n1 ],
                    e1 = c_ele[ n1 ],
                    u0 = p_vel[ n1 ][0],
                    v0 = p_vel[ n1 ][1],
                    u1 = c_vel[ n1 ][0],
                    v1 = c_vel[ n1 ][1]
                )
                node2 = dict(
                    x=fort14.nodes[ n2 ][0],
                    y=fort14.nodes[ n2 ][1],
                    z=fort14.nodes[ n2 ][2],
                    e0=p_ele[ n2 ],
                    e1=c_ele[ n2 ],
                    u0=p_vel[ n2 ][0],
                    v0=p_vel[ n2 ][1],
                    u1=c_vel[ n2 ][0],
                    v1=c_vel[ n2 ][1]
                )
                node3 = dict(
                    x = fort14.nodes[ n3 ][0],
                    y = fort14.nodes[ n3 ][1],
                    z = fort14.nodes[ n3 ][2],
                    e0 = p_ele[ n3 ],
                    e1 = c_ele[ n3 ],
                    u0 = p_vel[ n3 ][0],
                    v0 = p_vel[ n3 ][1],
                    u1 = c_vel[ n3 ][0],
                    v1 = c_vel[ n3 ][1]
                )

                e1 = [ node1, node2 ]
                e2 = [ node2, node3 ]
                e3 = [ node3, node1 ]

                if is_dry( node1 ) or is_dry( node2 ) or is_dry( node3 ):
                    w.write('{0}\t{1}\n'.format(element, -99999))
                    continue

                # Calculate average elevation for each timestep
                xi0 = (node1['e0'] + node2['e0'] + node3['e0']) / 3.0
                xi1 = (node1['e1'] + node2['e1'] + node3['e1']) / 3.0

                # Calculate area of the element
                area = 0.5 * abs((node1['x'] - node3['x']) * (node2['y'] - node1['y']) - (node1['x'] - node2['x']) * (
                node3['y'] - node1['y']))

                # Calculate Qnets
                Qnet0 = 0
                Qnet1 = 0
                for edge in [e1, e2, e3]:
                    # Calculate edge length
                    l = math.sqrt((edge[1]['x'] - edge[0]['x']) ** 2 + (edge[1]['y'] - edge[0]['y']) ** 2)

                    # Calculate normal vector
                    norm = ((edge[1]['y'] - edge[0]['y']) / l, -(edge[1]['x'] - edge[0]['x']) / l)

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
                    Qnet0 += (l / 6.0) * (2 * H0n0 * U0n0 + H0n0 * U0n1 + H0n1 * U0n0 + 2 * H0n1 * U0n1)
                    Qnet1 += (l / 6.0) * (2 * H1n0 * U1n0 + H1n0 * U1n1 + H1n1 * U1n0 + 2 * H1n1 * U1n1)

                # Calculate approximation of time integral to get Qnet
                Qnet = 0.5 * (Qnet0 + Qnet1) * dt

                # Calculate residal
                residual = area * (xi1 - xi0) + Qnet

                # Write residual value to file
                w.write('{0}\t{1}\n'.format(element, residual))

            p_ele = prev_ele.next_timestep()
            c_ele = curr_ele.next_timestep()
            p_vel = prev_vel.next_timestep()
            c_vel = curr_vel.next_timestep()



if __name__ == '__main__':

    # fort.14 fort.6363 fort.63 fort.6464 fort.64 output.txt
    calculate_residuals( sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6] )