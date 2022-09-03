import random

def counter(lst):
	ctr=0
	for i in lst:
		for j in i:
			if j=='':
				ctr+=1
	return(ctr)

matrix_nominal=[
['','8','1',  '2','','4',  '','',''],
['6','','',  '','','',  '3','',''],
['','','' , '','1','6',  '','','2'],

['','3','6',  '','7','',  '2','',''],
['1','5','',  '','','',  '7','','8'],
['','','',  '4','','',  '','','1'],

['','','',  '8','','',  '','5','3'],
['8','9','3',  '','5','1',  '','2','7'],
['2','1','',  '3','4','7',  '','6','9']]

matrix=matrix_nominal





matrix_temp=[
['','','',  '','','',  '','',''],
['','','',  '','','',  '','',''],
['','','' , '','','',  '','',''],

['','','',  '','','',  '','',''],
['','','',  '','','',  '','',''],
['','','',  '','','',  '','',''],

['','','',  '','','',  '','',''],
['','','',  '','','',  '','',''],
['','','',  '','','',  '','','']]

k_v=[
['0.0', '0.1', '0.2', '1.0', '1.1', '1.2', '2.0', '2.1', '2.2'], 
['0.3', '0.4', '0.5', '1.3', '1.4', '1.5', '2.3', '2.4', '2.5'],
['0.6', '0.7', '0.8', '1.6', '1.7', '1.8', '2.6', '2.7', '2.8'],

['3.0', '3.1', '3.2', '4.0', '4.1', '4.2', '5.0', '5.1', '5.2'], 
['3.3', '3.4', '3.5', '4.3', '4.4', '4.5', '5.3', '5.4', '5.5'], 
['3.6', '3.7', '3.8', '4.6', '4.7', '4.8', '5.6', '5.7', '5.8'],

['6.0', '6.1', '6.2', '7.0', '7.1', '7.2', '8.0', '8.1', '8.2'], 
['6.3', '6.4', '6.5', '7.3', '7.4', '7.5', '8.3', '8.4', '8.5'], 
['6.6', '6.7', '6.8', '7.6', '7.7', '7.8', '8.6', '8.7', '8.8']]



def solver(pos_x,pos_y,matrix):
	
	int_to_str="%i.%i"%(pos_x,pos_y) # convert indexes into str to later check with cube matrix temp
	# we start checking in normal matrix, rev matrix and cube matrix.
	
	for repeat_times in range(2000):

		rnd_num_to_test=(random.randint(1,9)) # we take a random numb and try it in all 3 matrixes
		
		list_rev=[] # form a list for rev matrix to check it later with rnd_num_to_test
		for idx_x_for_rev_matrix in range(9):
			list_rev.append(matrix[idx_x_for_rev_matrix][pos_y])


		list_coube=[] # new list for cube matrix k_v is a templ
		for j in k_v:
			if int_to_str in j:
				for s in j:
					x_int,y_int=int(s[0]),int(s[2])
					list_coube.append(matrix[x_int][y_int])
		
		if rnd_num_to_test not in matrix[pos_x] and rnd_num_to_test not in list_rev and rnd_num_to_test not in list_coube :

			matrix[pos_x][pos_y]=rnd_num_to_test
	# print("rev_list: ",list_rev)

		

def findWhereToStart(matrix_int_2):
	list_of_sum_horiz=[]
	max_temp=0
	max_coord=0
	for i in matrix_int_2:
		temp_int_2=0
		for j in i:
			if j!='':
				temp_int_2+=1
		list_of_sum_horiz.append(temp_int_2)
	for idx_ii,ii in enumerate(list_of_sum_horiz):
		if ii>max_temp and ii!=9:
			max_temp=ii
			max_coord=idx_ii


	return(max_coord)


	
def start(matrix_int_1):
	
	
	for idx_i,i in enumerate(matrix_int_1): #  we convert all the element of matrix_int_1 into int
		for idx_p,p in enumerate(i):
			if p!='':
				p=int(p)
				matrix_int_1[idx_i][idx_p]=p
	for counter_int_1 in range(100):
		where_to_start_idx=findWhereToStart(matrix_int_1)
		for idx_elem, elem in enumerate(matrix_int_1[where_to_start_idx]):
			if elem=='':
				# print(where_to_start_idx,idx_elem,matrix_int_1)
				solver(where_to_start_idx,idx_elem,matrix_int_1)




	# for idx_l,l in enumerate(matrix_int_1): # looking up for the first '' element and passing it into def solver.8
	# 	for idx_elem,elem in enumerate(l):
	# 		# print(l)
	# 		if elem=='':
				# print(idx_l,idx_elem, matrix_int_1)
				# solver((idx_l),(idx_elem),matrix_int_1)
				# pass



start(matrix)

for ii in matrix:
	print(ii)


# count=0
# for m in matrix:
# 	for n in m:
# 		if n=='':
# 			count+=1
# print("count: ",count)
# if count:
# 	# matrix=matrix_nominal
# 	print('hereeee')
# 	print(matrix)
# 	# print(matrix_nominal)
# 	start()
# else:
# 	print(matrix)


