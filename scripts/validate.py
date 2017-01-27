import sys

def invalidated( line_number ):
    print 'Data is not identical'
    print 'Mismatch found on line', line_number

def validate( file1, file2 ):

    e1 = file1.split('.')[-1]
    e2 = file2.split('.')[-1]

    if e1 != e2:
        print 'Files must have same extension'
        return

    if e1 == '63':
        validate63( file1, file2 )
    if e1 == '64':
        validate64( file1, file2 )

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

    print 'Validated. Data is identical.'

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

    print 'Validated. Data is identical.'

def validate_line( f1, f2, line ):
    if f1.readline() != f2.readline():
        invalidated(line)
        return False
    return True

if __name__ == '__main__':

    if len( sys.argv ) == 3:

        validate( sys.argv[1], sys.argv[2] )