program io_normal
implicit none

! Mimic mesh.F from adcirc
character(len=80) :: agrid
integer :: np                           ! number of nodes in the mesh
integer :: ne                           ! number of elements in the mesh
real(8), allocatable :: x(:)            ! x-values
real(8), allocatable :: y(:)            ! y-values
real(8), allocatable, target :: dp(:)   ! z-values
integer, allocatable :: nm(:,:)         ! element table
integer :: lineNum                      ! the current line number
integer :: jn, je, nhy, k, j

! The fort.14 file location
character(len=4096) :: fileloc

! Timing and formatting variables
real :: start, finish
300 FORMAT (4X, F6.3, A, 4X, A)

if ( iargc() == 1 ) then

    call getarg(1, fileloc)
    fileloc = trim(fileloc)
    lineNum = 1

    write(*,*) 'Reading fort.14....'

    ! Read data from fort.14 using adcirc's current method
    open(unit=14, file=fileloc, action='read')

    ! Read agrid
    read(14, fmt='(a80)') agrid
    lineNum = lineNum + 1

    ! Read info line
    read(14, fmt=*) ne, np
    lineNum = lineNum + 1

    write(*,*) '    ', np, ' nodes'
    write(*,*) '    ', ne, ' elements'

    ! allocate
    call cpu_time(start)
    allocate( x(np), y(np), dp(np) )
    allocate( nm(ne,3) )
    call cpu_time(finish)
    write(*,300) finish-start, 's', 'Allocating arrays'

    ! Read nodes
    call cpu_time(start)
    do k = 1, np
        read(14, fmt=*) jn, x(k), y(k), dp(k)
        lineNum = lineNum + 1
    enddo
    call cpu_time(finish)
    write(*,300) finish-start, 's', 'Reading nodes'

    ! Read elements
    call cpu_time(start)
    do k = 1, ne
        read(14, fmt=*) je, nhy, ( nm(k,j), j = 1, 3 )
        lineNum = lineNum + 1
    enddo
    call cpu_time(finish)
    write(*,300) finish-start, 's', 'Reading elements'

    ! deallocate
    call cpu_time(start)
    deallocate( x, y, dp, nm )
    call cpu_time(finish)
    write(*,300) finish-start, 's', 'Deallocating'

    write(*,*) 'Done.'

else

    write(*,*) 'io_normal [fort.14]'

endif

end program io_normal
