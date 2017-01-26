module io
use hashtable
implicit none

private
public read14

contains

subroutine read14 ( file, nodes, d )
    character(len=*) :: file
    real(8), allocatable, dimension(:,:), intent(inout) :: nodes
    type(item), allocatable, target, dimension(:) :: d

    character(len=80) agrid
    character(len=24) node_label
    integer :: num_elements, num_nodes, i

    open(unit=14, file=file, action='read')

    ! Read agrid
    read(14, fmt='(a80)') agrid

    ! Read info line
    read(14, fmt=*) num_elements, num_nodes

    write(*,*) 'Reading fort.14'
    write(*,*) num_nodes, ' nodes'
    write(*,*) num_elements, ' elements'

    ! Allocate arrays
    allocate(nodes(num_nodes, 3))
    call dict(d, num_nodes)

    ! Read the nodes
    do i = 1, num_nodes
        read(14, fmt=*) node_label, nodes(i,1), nodes(i,2), nodes(i,3)
        call add_item(d, node_label, i)
    enddo

    call print_dict( d )

    ! Deallocate arrays
    deallocate(nodes)
    call close_dict(d)

    close(14)

end subroutine read14

end module io
