compiler=gfortran

obj_dir=obj
bin_dir=bin

flags=-O3 -fcheck=all

hashtable_src=hashtable/fortran
heapsort_src=heapsort/fortran
io_src=io/fortran

all: hashtable heapsort io

hashtable:
	$(compiler) \
		-c $(hashtable_src)/hashtable.f90 \
		-J$(obj_dir) \
		-o $(obj_dir)/hashtable.o \
		$(flags)

hashtable_tests: hashtable
	$(compiler) \
		$(hashtable_src)/hashtable_test.f90 \
		$(obj_dir)/hashtable.o \
		-I$(obj_dir)  \
	 	-o $(bin_dir)/hashtable \
		$(flags)

heapsort:
	$(compiler) \
		-c $(heapsort_src)/heapsort.f90 \
		-J$(obj_dir) \
		-o $(obj_dir)/heapsort.o \
		$(flags)

heapsort_tests: heapsort
	$(compiler) \
		$(heapsort_src)/heapsort_test.f90 \
		$(obj_dir)/heapsort.o \
		-I$(obj_dir) \
		-o $(bin_dir)/heapsort \
		$(flags)

io: hashtable
	$(compiler) \
		-c $(io_src)/io.f90 \
		-J$(obj_dir) \
		-o $(obj_dir)/io.o \
		$(flags)

io_tests: io
	$(compiler) \
		$(io_src)/io_hash_test.f90 \
		$(obj_dir)/io.o \
		$(obj_dir)/hashtable.o \
		-I$(obj_dir) \
		-o $(bin_dir)/io_hash \
		$(flags)
	$(compiler) \
		$(io_src)/io_normal_test.f90 \
		-o $(bin_dir)/io_normal \
		$(flags)

tests: heapsort_tests hashtable_tests io_tests

clean:
	rm $(obj_dir)/*.mod
	rm $(obj_dir)/*.o

.PHONY: hashtable io heapsort
