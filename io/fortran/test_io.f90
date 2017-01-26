program test
use hashtable
use io
implicit none

real(8), allocatable, dimension(:,:) :: nodes
type(item), allocatable, target, dimension(:) :: d

call read14( 'data/labels.14', nodes, d )

end program test
