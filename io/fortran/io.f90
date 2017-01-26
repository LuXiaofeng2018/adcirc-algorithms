module io
use hashtable
implicit none

private
public read14
public close14

contains

subroutine read14 ( file, agrid, np, ne, x, y, dp, d )
    implicit none
    character(len=*), intent(in) :: file
    character(len=80), intent(inout) :: agrid
    integer, intent(inout) :: np
    integer, intent(inout) :: ne
    real(8), allocatable, intent(inout) :: x(:)
    real(8), allocatable, intent(inout) :: y(:)
    real(8), allocatable, target, intent(inout) :: dp(:)
    type(item), allocatable, target, intent(inout) :: d(:)

    character(len=24) :: node_label
    integer :: i

    open(unit=14, file=file, action='read')

    ! Read agrid
    read(14, fmt='(a80)') agrid

    ! Read info line
    read(14, fmt=*) ne, np

    write(*,*) 'Reading fort.14'
    write(*,*) np, ' nodes'
    write(*,*) ne, ' elements'

    ! Allocate arrays
    allocate(x(np), y(np), dp(np))
    call dict(d, np)

    ! Read the nodes
    do i = 1, np
        read(14, fmt=*) node_label, x(i), y(i), dp(i)
        call add_item(d, node_label, i)
    enddo

    call print_dict( d )

    close(14)

end subroutine read14

subroutine close14 ( x, y, dp, d )
    implicit none
    real(8), allocatable, intent(inout) :: x(:)
    real(8), allocatable, intent(inout) :: y(:)
    real(8), allocatable, target, intent(inout) :: dp(:)
    type(item), allocatable, target, intent(inout) :: d(:)
    deallocate(x, y, dp)
    call close_dict(d)
end subroutine close14

end module io
