compiler=gfortran

tests: heapsort
	$(compiler) heapsort.o test_heapsort.f90 -O3 -o test_heapsort

heapsort:
	$(compiler) -c heapsort.f90 -O3

clean:
	rm *.o *.mod
	rm test_heapsort
