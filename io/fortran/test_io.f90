program test
use hashtable
use io
implicit none

! The fort.14 file location
character(len=4096) :: fileloc

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
if ( iargc() == 1 ) then

    call getarg(1, fileloc)
    fileloc = trim(fileloc)

    call read14( fileloc, agrid, np, ne, x, y, dp, nm, labels )

    do i = 1, np
        write(*,*) i, x(i), y(i), dp(i)
    enddo
    do i = 1, ne
        write(*,*) i, nm(i,1), nm(i,2), nm(i,3)
    enddo

    call close14( x, y, dp, nm, labels )

else

    write(*,*) 'Specify fort.14 location'

endif

end program test
