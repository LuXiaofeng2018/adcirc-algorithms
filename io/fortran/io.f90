module io
use hashtable
implicit none

private
public read14
public close14

contains

subroutine read14 ( file, agrid, np, ne, x, y, dp, nm, labels )
    implicit none
    character(len=*), intent(in) :: file
    character(len=80), intent(inout) :: agrid
    integer, intent(inout) :: np
    integer, intent(inout) :: ne
    real(8), allocatable, intent(inout) :: x(:)
    real(8), allocatable, intent(inout) :: y(:)
    real(8), allocatable, target, intent(inout) :: dp(:)
    integer, allocatable, intent(inout) :: nm(:,:)
    character(len=24), allocatable :: labels(:)

    type(item), allocatable, target :: d(:)
    integer :: i
    integer :: element_number, nodes_per_element
    character(len=24) :: n1, n2, n3

    open(unit=14, file=file, action='read')

    ! Read agrid
    read(14, fmt='(a80)') agrid

    ! Read info line
    read(14, fmt=*) ne, np

    write(*,*) 'Reading fort.14'
    write(*,*) np, ' nodes'
    write(*,*) ne, ' elements'

    ! Allocate arrays
    allocate(x(np), y(np), dp(np), labels(np))
    allocate(nm(ne,3))
    call dict(d, np)

    ! Read the nodes
    do i = 1, np
        read(14, fmt=*) labels(i), x(i), y(i), dp(i)
        call add_item(d, labels(i), i)
    enddo

    do i = 1, ne
        read(14, fmt=*) element_number, nodes_per_element, n1, n2, n3
        nm(i,1) = find( d, n1 )
        nm(i,2) = find( d, n2 )
        nm(i,3) = find( d, n3 )
    enddo

    call close_dict( d )

    close(14)

end subroutine read14

subroutine close14 ( x, y, dp, nm, labels )
    implicit none
    real(8), allocatable, intent(inout) :: x(:)
    real(8), allocatable, intent(inout) :: y(:)
    real(8), allocatable, target, intent(inout) :: dp(:)
    integer, allocatable, intent(inout) :: nm(:,:)
    character(len=24), allocatable :: labels(:)
    deallocate(x, y, dp, nm, labels)
end subroutine close14

end module io
