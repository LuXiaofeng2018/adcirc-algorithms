import sys
import inflect

def genlabels ( infile, outfile ):
    print 'Converting node numbers to labels'
    print infile, ' -> ', outfile

    nodes = []
    elements = []

    with open( infile, 'r' ) as f:

        h1 = f.readline()
        h2 = f.readline()
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

    with open( outfile, 'w' ) as f:

        p = inflect.engine()
        f.write( h1 )
        f.write( h2 )

        for n, x, y, z in nodes:

            f.write('{}\t{}\t{}\t{}\n'.format(
                p.number_to_words(n),
                x, y, z
            ))

        for e, n1, n2, n3 in elements:

            f.write('{}\t3\t{}\t{}\t{}\n'.format(
                e,
                p.number_to_words(n1),
                p.number_to_words(n2),
                p.number_to_words(n3)
            ))

if __name__ == '__main__':

    if len(sys.argv) == 3:

        genlabels(sys.argv[1], sys.argv[2])
