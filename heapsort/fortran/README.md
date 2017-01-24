# Heapsort Module for Fortran

A Fortran implementation of the [heapsort](https://en.wikipedia.org/wiki/Heapsort) algorithm.

Available as a Fortran module. To build the module:

```
make heapsort
```

To build the ```test_heapsort``` program, which sorts a random list of 10,000,000 numbers:

```
make
```

## Usage

To use heapsort in your code:

```fortran
program does_sorting
    use heapsort
    implicit none
    integer, parameter :: length_of_array
    real, allocatable :: array(:)
    ...
    call sort( array, length_of_array )
end program does_sorting
