module heapsort
implicit none
contains

integer function i_parent ( i )
    implicit none
    integer :: i
    i_parent = CEILING( (i-1) / 2.0 )
end function i_parent

integer function i_left_child ( i )
    implicit none
    integer :: i
    i_left_child = 2*i
end function i_left_child

integer function i_right_child ( i )
    implicit none
    integer :: i
    i_right_child = 2*i + 1
end function i_right_child

subroutine sift_up ( a, n, s, e )
    implicit none
    integer, intent(in) :: n, s, e
    real, dimension(n), intent(inout) :: a
    integer :: child, parent
    real :: temp
    child = e
    do
        if ( child <= s ) exit
        parent = i_parent( child )
        if ( a( parent ) < a( child ) ) then
            temp = a( parent )
            a( parent ) = a( child )
            a( child ) = temp
            child = parent
        else
            exit
        endif
    enddo
end subroutine sift_up

subroutine sift_down ( a, n, s, e )
    implicit none
    integer, intent(in) :: n, s, e
    real, dimension(n), intent(inout) :: a
    integer :: root, child, swap
    real :: temp
    root = s
    do
        if ( i_left_child( root ) > e ) exit
        child = i_left_child( root )
        swap = root
        if ( a( swap ) < a( child ) ) swap = child
        if ( child + 1 <= e .and. a( swap ) < a( child+1 ) ) swap = child + 1
        if ( swap == root ) then
            exit
        else
            temp = a( root )
            a( root ) = a( swap )
            a( swap ) = temp
            root = swap
        endif
    enddo
end subroutine sift_down

subroutine heapify ( a, n )
    implicit none
    integer, intent(in) :: n
    real, dimension(n), intent(inout) :: a
    integer :: e = 2
    do
        if ( e > n ) exit
        call sift_up( a, n, 1, e )
        e = e + 1
    enddo
end subroutine

subroutine sort ( a, n )
    implicit none
    integer, intent(in) :: n
    real, dimension(n), intent(inout) :: a
    integer :: e
    real :: temp
    e = n
    call heapify( a, n )
    do
        if ( e <= 1 ) exit
        temp = a(e)
        a(e) = a(1)
        a(1) = temp
        e = e - 1
        call sift_down( a, n, 1, e )
    enddo
end subroutine

end module heapsort
