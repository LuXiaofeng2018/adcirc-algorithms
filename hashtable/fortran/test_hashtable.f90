program test
    use hashtable
    implicit none

    integer :: i
    type(item), allocatable, target, dimension(:) :: d

    call dict( d, 20 )
    call add_item( d, 'test', 4 )
    call add_item( d, 'tristan', 123 )
    call add_item( d, 'asdf', 432 )
    call add_item( d, 'this is cool', 1893 )
    call add_item( d, 'hi my name is tristan', 0 )

    write(*,*) find( d, 'this is cool' )
    write(*,*) find( d, 'tristan' )
    ! call print_dict( d )

    call close_dict( d )
	! type(item), dimension(:) :: d
	! integer :: num_items = 10
	! d = dict( num_items )
!	call add_item

end program test
