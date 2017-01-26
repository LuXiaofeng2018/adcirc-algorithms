compiler=gfortran

obj_dir=obj
bin_dir=bin

flags=-O3 -fcheck=all

hashtable_src=hashtable/fortran
heapsort_src=heapsort/fortran
io_src=io/fortran

hashtable:
	$(compiler) \
		-c $(hashtable_src)/hashtable.f90 \
		-J$(obj_dir) \
        -o $(obj_dir)/hashtable.o \
		$(flags)

heapsort:
	$(compiler) \
		-c $(heapsort_src)/heapsort.f90 \
		-J$(obj_dir) \
		-o $(obj_dir)/heapsort.o \
		$(flags)

io: hashtable
	$(compiler) \
		-c $(io_src)/io.f90 \
		-J$(obj_dir) \
		-o $(obj_dir)/io.o \
		$(flags)

tests: hashtable heapsort
	$(compiler) \
		$(hashtable_src)/test_hashtable.f90 \
		$(obj_dir)/hashtable.o \
		-I$(obj_dir)  \
	 	-o $(bin_dir)/hashtable \
		$(flags)

	$(compiler) \
		$(heapsort_src)/test_heapsort.f90 \
		$(obj_dir)/heapsort.o \
		-I$(obj_dir) \
		-o $(bin_dir)/heapsort \
		$(flags)

test_io: io
	$(compiler) \
		$(io_src)/test_io.f90 \
		$(obj_dir)/io.o \
		$(obj_dir)/hashtable.o \
		-I$(obj_dir) \
		-o $(bin_dir)/io \
		$(flags)

clean:
	rm $(obj_dir)/*.mod
	rm $(obj_dir)/*.o

.PHONY: hashtable io heapsort
