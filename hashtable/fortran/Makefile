compiler=gfortran

tests: hashtable
	$(compiler) hashtable.o test_hashtable.f90 -O3 -o test_hashtable

hashtable:
	$(compiler) -c hashtable.f90 -O3

clean:
	rm *.o *.mod
	rm test_hashtable
