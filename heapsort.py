import random
import timeit

def heapsort( unsorted ):
	
	# Heapify the unsorted list
	heapify( unsorted, len(unsorted) )
	
	# Sort
	end = len(unsorted)-1
	while end > 0:
		unsorted[end], unsorted[0] = unsorted[0], unsorted[end]
		end -= 1
		sift_down( unsorted, 0, end )

def heapsort_bu( unsorted ):
	
	# Heapify the unsorted list
	heapify( unsorted, len(unsorted) )
	
	# Sort
	end = len(unsorted)-1
	while end > 0:
		unsorted[end], unsorted[0] = unsorted[0], unsorted[end]
		end -= 1
		sift_down_bu( unsorted, 0, end )

def i_parent( i ):
	return int( (i-1)/2.0 )

def i_left_child( i ):
	return 2*i + 1

def i_right_child( i ):
	return 2*i + 2

def sift_up( a, start, end ):
	child = end
	while child > start:
		parent = i_parent(child)
		if a[parent] < a[child]:
			a[parent], a[child] = a[child], a[parent]
			child = parent
		else:
			return

def sift_down( a, start, end ):
	root = start
	while i_left_child( root ) <= end:
		child = i_left_child(root)
		swap = root
		
		if a[swap] < a[child]:
			swap = child
		
		if child+1 <= end and a[swap] < a[child+1]:
			swap = child+1
		
		if swap == root:
			return
		
		else:
			a[root], a[swap] = a[swap], a[root]
			root = swap

def sift_down_bu( a, i, end ):
	j = leaf_search( a, i, end )
	while a[i] > a[j]:
		j = i_parent(j)
	x = a[j]
	a[j] = a[i]
	while j > i:
		x, a[i_parent(j)] = a[i_parent(j)], x
		j = i_parent(j)

def heapify( a, count ):
	end = 1
	while end < count:
		sift_up(a, 0, end)
		end += 1

def leaf_search( a, i, end ):
	j = i
	while i_left_child(j) <= end:
		if i_right_child(j) <= end and a[i_right_child(j)] > a[i_left_child(j)]:
			j = i_right_child(j)
		else:
			j = i_left_child(j)
	return j


n = 1000000
print 'Sorting', n, 'values'
print 'Creating arrays...'
l1 = [random.randint(1,n) for i in range(n)]
l2 = l1[:]

def test_l1():
	heapsort(l1)
def test_l2():
	heapsort_bu(l2)

print 'Starting tests...'
print 'Ordinary heapsort:', timeit.timeit( test_l1, number=1 )
print 'Bottom up heapsort:', timeit.timeit( test_l2, number=1 )





