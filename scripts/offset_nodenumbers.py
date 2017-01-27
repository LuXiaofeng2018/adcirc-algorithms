import sys

def offset_nodenumbers ( infile, outfile, offset ):
    print 'Offsetting node numbers by', offset
    print infile, ' -> ', outfile

    nodes = []
    elements = []
    open_segments = []
    land_segments = []
    offset = int(offset)

    with open( infile, 'r' ) as f:

        h1 = f.readline().strip()
        h2 = f.readline().strip()
        dat_line = h2.split()
        num_elements = int( dat_line[0] )
        num_nodes = int( dat_line[1] )

        for l in range( num_nodes ):

            line = f.next().split()
            n = int( line[0] )
            x = float( line[1] )
            y = float( line[2] )
            z = float( line[3] )

            nodes.append((n, x, y, z))

        for l in range( num_elements ):

            line = f.next().split()
            e = int( line[0] )
            n1 = int( line[2] )
            n2 = int( line[3] )
            n3 = int( line[4] )

            elements.append((e, n1, n2, n3))

        nope = f.next().lstrip()
        neta = f.next().lstrip()
        num_segments = int( nope.split()[0] )

        for segment in range(num_segments):

            seg_header = f.next().lstrip()
            num_segnodes = int( seg_header.split()[0] )
            segment = (seg_header, [])

            for segnode in range( num_segnodes ):

                l = f.next().split()
                segment[1].append((int(l[0]), ' '.join(l[1:])))

            open_segments.append( segment )

        nbou = f.next().lstrip()
        nvel = f.next().lstrip()
        num_segments = int( nbou.split()[0] )

        for segment in range(num_segments):

            seg_header = f.next().lstrip()
            num_segnodes = int( seg_header.split()[0] )
            segment = (seg_header, [])

            for segnode in range( num_segnodes ):

                l = f.next().split()
                segment[1].append( ( int(l[0]), ' '.join(l[1:] ) ) )

            land_segments.append( segment )

    with open( outfile, 'w' ) as f:

        f.write( h1 + '\n' )
        f.write( h2 + '\n' )

        for n, x, y, z in nodes:

            f.write('{}\t{}\t{}\t{}\n'.format(
                n+offset,
                x, y, z
            ))

        for e, n1, n2, n3 in elements:

            f.write('{}\t3\t{}\t{}\t{}\n'.format(
                e,
                n1+offset,
                n2+offset,
                n3+offset
            ))

        f.write( nope )
        f.write( neta )

        for header, nodes in open_segments:

            f.write( header )

            for node, rest_of_line in nodes:

                f.write('{}\t{}\n'.format( node+offset, rest_of_line) )

        f.write( nbou )
        f.write( nvel )

        for header, nodes in land_segments:

            f.write( header )

            for node, rest_of_line in nodes:

                f.write('{}\t{}\n'.format(node+offset, rest_of_line))

if __name__ == '__main__':

    if len(sys.argv) == 4:

        offset_nodenumbers(sys.argv[1], sys.argv[2], sys.argv[3])
