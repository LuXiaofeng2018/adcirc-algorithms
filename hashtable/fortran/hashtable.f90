module hashtable
implicit none

type :: item
    character(len=24) :: key
    integer :: value
    type(item), pointer :: next
end type item

contains
function dict ( num_items )
    implicit none
    integer :: num_items
    type(item), dimension(num_items) :: dict
end function dict

integer function hash ( key_str )
    implicit none
    character(len=*) :: key_str
    integer :: n, i
    n = len( key_str )
    hash = 7
    do i = 1, n
        hash = hash*31 + ichar( key_str(i:i) )
    end do
end function hash

subroutine add_item ( d, key, value )
    implicit none
    type(item), dimension(:) :: d
    character(len=*) :: key
    integer :: value
    integer :: hash_value
    hash_value = hash( key )
    write(*,*) hash_value
end subroutine add_item

end module hashtable
