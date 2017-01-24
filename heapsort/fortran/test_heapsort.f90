program test
    use heapsort
    implicit none
    integer, parameter :: d = 10000000
    real, dimension(d) :: x
    integer :: i
    do i = 1, d, 1
        x(i) = rand(0)*d
    end do
    call sort( x, d )
    call print_array( x(1:10), 10 )
end program test

subroutine print_array( a, n )
    implicit none
    integer, intent(in) :: n
    real, dimension(n), intent(in) :: a
    integer :: i
    write(*,'(F13.10)')( a(i), i=1,n )
end subroutine print_array
