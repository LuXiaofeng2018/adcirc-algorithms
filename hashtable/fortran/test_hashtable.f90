program test
    use hashtable
    implicit none

!    type(item) :: t
!    t%key = 'hello, world'
!    t%value = 0
!    nullify(t%next)

    integer :: u
    character(len=4) :: string
    string = 'qi'
    u = hash(string)

    write(*,*) modulo(u, 70)

end program test
