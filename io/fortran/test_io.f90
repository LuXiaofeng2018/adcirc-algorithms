program test
use hashtable
use io
implicit none

! The fort.14 file location
character(len=4096) :: fileloc
character(len=4096) :: outfileloc

! Mimic mesh.F from adcirc
character(len=80) :: agrid
integer :: np                           ! number of nodes in the mesh
integer :: ne                           ! number of elements in the mesh
real(8), allocatable :: x(:)            ! x-values
real(8), allocatable :: y(:)            ! y-values
real(8), allocatable, target :: dp(:)   ! z-values
integer, allocatable :: nm(:,:)         ! element table

! Mapping from node numbers to node labels, used when writing output
character(len=24), allocatable :: labels(:)
integer :: i

! Get fort.14 file location from command line
if ( iargc() >= 1 ) then

    call getarg(1, fileloc)
    fileloc = trim(fileloc)

    write(*,*) 'Reading fort.14....'
    call read14( fileloc, agrid, np, ne, x, y, dp, nm, labels )

    if ( iargc() == 2) then

        call getarg(2, outfileloc)
        outfileloc = trim(outfileloc)

        open(unit=144, file=outfileloc, status='replace', action='write')
        write(*,*) 'Writing output....'
        do i = 1, np
            write(144,*) i, x(i), y(i), dp(i)
        enddo
        do i = 1, ne
            write(144,*) i, nm(i,1), nm(i,2), nm(i,3)
        enddo
        close(144)

    endif

    write(*,*) 'Freeing memory....'
    call close14( x, y, dp, nm, labels )

else

    write(*,*) 'io [fort.14] [output.txt]'

endif

end program test
