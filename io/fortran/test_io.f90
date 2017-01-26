program test
use hashtable
use io
implicit none

! The fort.14 file location
character(len=4096) :: fileloc

! Mimic mesh.F from adcirc
character(len=80) :: agrid
integer :: np   ! number of nodes in the mesh
integer :: ne   ! number of elements in the mesh
real(8), allocatable :: x(:)
real(8), allocatable :: y(:)
real(8), allocatable, target :: dp(:)

! The new hotness -- a dictionary
type(item), allocatable, target, dimension(:) :: d

! Get fort.14 file location from command line
if ( iargc() == 1 ) then

    call getarg(1, fileloc)
    fileloc = trim(fileloc)

    call read14( fileloc, agrid, np, ne, x, y, dp, d )
    call close14( x, y, dp, d )

else

    write(*,*) 'Specify fort.14 location'

endif

end program test
