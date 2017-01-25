program test
    use hashtable
    implicit none

	type(item), dimension(:) :: d
	integer :: num_items = 10
	d = dict( num_items )
!	call add_item

end program test
