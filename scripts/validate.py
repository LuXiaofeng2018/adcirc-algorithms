import sys

check = '  ' + u'\u2713'
x = '  ' + u'\u2718'

def invalidated( line_number ):
    print x, 'Data is not identical'
    print x, 'Mismatch found on line', line_number

def validate( file1, file2 ):

    e1 = file1.split('.')[-1]
    e2 = file2.split('.')[-1]

    if e1 != e2:
        print 'Files must have same extension'
        return

    if e1 == '14':
        validate14( file1, file2 )
    if e1 == '63':
        validate63( file1, file2 )
    if e1 == '64':
        validate64( file1, file2 )

def validate14( file1, file2 ):

    print 'Validating fort.14 files...'

    with open( file1 , 'r' ) as f1, open( file2, 'r' ) as f2:

        f1.readline()
        f2.readline()

        info1 = f1.readline().split()
        info2 = f2.readline().split()

        num_nodes_1 = int( info1[1] )
        num_nodes_2 = int( info2[1] )
        num_elements_1 = int( info1[0] )
        num_elements_2 = int( info2[0] )

        if num_nodes_1 != num_nodes_2:
            print x, 'Meshes have different number of nodes'
            return

        if num_elements_1 != num_elements_2:
            print x, 'Meshes have different number of elements'
            return

        print check, 'Identical number of nodes and elements'

        nodes_1 = dict()
        nodes_2 = dict()

        for l in range( num_nodes_1 ):

            line = f1.next().split()
            n = int( line[0] )
            nodes_1[ n ] = float(line[1]), float(line[2]), float(line[3])

        for l in range( num_nodes_2 ):

            line = f2.next().split()
            n = int( line[0] )
            nodes_2[ n ] = float(line[1]), float(line[2]), float(line[3])

        elements_1 = dict()
        elements_2 = dict()

        for l in range( num_elements_1 ):

            line = f1.next().split()
            e = int( line[0] )
            n1 = int( line[2] )
            n2 = int( line[3] )
            n3 = int( line[4] )
            x1, y1, z1 = nodes_1[ n1 ]
            x2, y2, z2 = nodes_1[ n2 ]
            x3, y3, z3 = nodes_1[ n3 ]

            element = (x1, y1, z1, x2, y2, z2, x3, y3, z3)
            elements_1[ element ] = e

        for l in range( num_elements_2 ):

            line = f2.next().split()
            e = int( line[0] )
            n1 = int( line[2] )
            n2 = int( line[3] )
            n3 = int( line[4] )
            x1, y1, z1 = nodes_2[ n1 ]
            x2, y2, z2 = nodes_2[ n2 ]
            x3, y3, z3 = nodes_2[ n3 ]

            element = (x1, y1, z1, x2, y2, z2, x3, y3, z3)
            elements_2[ element ] = e

        for element, e in elements_1.iteritems():

            if element not in elements_2:

                print x, 'Element', e, 'from', file1, 'is not in', file2
                return

        print check, 'Meshes are identical'

        nope_1 = int( f1.next().split()[0] )
        nope_2 = int( f2.next().split()[0] )

        if nope_1 != nope_2:
            print x, 'Meshes have different number of elevation boundary segments'
            return

        neta_1 = int( f1.next().split()[0] )
        neta_2 = int( f2.next().split()[0] )

        if neta_1 != neta_2:
            print x, 'Meshes have different number of elevation boundary nodes'
            return

        for segment in range( nope_1 ):

            segnodes_1 = int( f1.next().split()[0] )
            segnodes_2 = int( f2.next().split()[0] )

            if segnodes_1 != segnodes_2:
                print x, 'Elevation segment', segment+1, 'has different number of nodes'
                return

            for segnode in range( segnodes_1 ):

                n1 = int( f1.next().split()[0] )
                n2 = int( f2.next().split()[0] )

                n1 = nodes_1[ n1 ]
                n2 = nodes_2[ n2 ]

                if n1 != n2:
                    print x, 'Boundary node', segnode+1, 'of elevation segment', segment+1, 'does not match'
                    return

        print check, 'Elevation boundary segments are identical'

        nbou_1 = int( f1.next().split()[0] )
        nbou_2 = int( f2.next().split()[0] )

        if nbou_1 != nbou_2:
            print x, 'Meshes have different number of flow boundary segments'
            return

        nvel_1 = int( f1.next().split()[0] )
        nvel_2 = int( f2.next().split()[0] )

        if nvel_1 != nvel_2:
            print x, 'Meshes have different number of flow boundary nodes'
            return

        for segment in range( nbou_1 ):

            segnodes_1 = int( f1.next().split()[0] )
            segnodes_2 = int( f2.next().split()[0] )

            if segnodes_1 != segnodes_2:
                print x, 'Flow segment', segment+1, 'has different number of nodes'
                return

            for segnode in range( segnodes_1 ):

                n1 = int( f1.next().split()[0] )
                n2 = int( f2.next().split()[0] )

                n1 = nodes_1[ n1 ]
                n2 = nodes_2[ n2 ]

                if n1 != n2:
                    print x, 'Boundary node', segnode+1, 'of flow segment', segment+1, 'does not match'
                    return

        print check, 'Flow boundary segments are identical'

def validate64( file1, file2 ):

    print 'Validating fort.64 files...'

    with open( file1 ) as f1, open( file2 ) as f2:

        line = 1

        # First line identical
        if not validate_line(f1, f2, line ):
            return
        line += 1

        # Second line identical
        a1 = f1.readline()
        b1 = f2.readline()
        line += 1
        if a1 != b1:
            invalidated(line)
            return

        # Num nodes and timesteps from second line
        info = a1.split()
        num_ts = int(info[0])
        num_nodes = int(info[1])

        # Loop through timesteps
        for ts in range(num_ts):
            line += 1
            if not validate_line(f1, f2, line ):
                return
            line += 1
            for node in range(num_nodes):
                n1 = f1.readline()
                n2 = f2.readline()
                line += 1
                d1 = n1.split()
                d2 = n2.split()
                x1 = float(d1[1])
                x2 = float(d2[1])
                y1 = float(d1[2])
                y2 = float(d2[2])
                if x1 != x2 or y1 != y2:
                    invalidated(line)
                    return

        if not validate_line(f1, f2, line ):
            return
        line += 1

    print check, 'Validated. Data is identical.'

def validate63( file1, file2 ):

    print 'Validating fort.63 files...'

    with open( file1 ) as f1, open( file2 ) as f2:

        line = 1

        # First line identical
        if not validate_line(f1, f2, line ):
            return
        line += 1

        # Second line identical
        a1 = f1.readline()
        b1 = f2.readline()
        line += 1
        if a1 != b1:
            invalidated(line)
            return

        # Num nodes and timesteps from second line
        info = a1.split()
        num_ts = int(info[0])
        num_nodes = int(info[1])

        # Loop through timesteps
        for ts in range(num_ts):
            line += 1
            if not validate_line(f1, f2, line ):
                return
            line += 1
            for node in range(num_nodes):
                n1 = f1.readline()
                n2 = f2.readline()
                line += 1
                d1 = float(n1.split()[1])
                d2 = float(n2.split()[1])
                if d1 != d2:
                    invalidated(line)
                    return

        if not validate_line(f1, f2, line ):
            return
        line += 1

    print check, 'Validated. Data is identical.'

def validate_line( f1, f2, line ):
    if f1.readline() != f2.readline():
        invalidated(line)
        return False
    return True

if __name__ == '__main__':

    if len( sys.argv ) == 3:

        validate( sys.argv[1], sys.argv[2] )