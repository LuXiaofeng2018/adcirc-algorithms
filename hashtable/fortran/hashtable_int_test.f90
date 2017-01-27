program test
    use hashtable_int
    implicit none

    integer :: i
    type(item), allocatable, target :: d(:)

    call dict( d, 20 )
    call add_item( d, 1, 4 )
    call add_item( d, 2, 123 )
    call add_item( d, 3, 432 )
    call add_item( d, 4, 1893 )
    call add_item( d, 5, 0 )

    write(*,*) find( d, 1 )
    write(*,*) find( d, 5 )

    call close_dict( d )

end program test
