matrix=[
[9,'',6,8,7,'',3,4,''],
['',5,1,'',4,'',7,'',6],
[4,'','','','',6,'','',''],
['',6,8,'','',7,'','',3],
[3,'',2,'',1,'',6,8,7],
[1,'','','','','','','',''],
['','','','','',2,4,'',9],
[7,'','',5,'',8,1,6,2],
[2,'',9,'','',4,'',3,8]]

l=[[9, '', 4, '', 3, 1, '', 7, 2], 
['', 5, '', 6, '', '', '', '', ''], 
[6, 1, '', 8, 2, '', '', '', 9], 
[8, '', '', '', '', '', '', 5, ''], 
[7, 4, '', '', 1, '', '', '', ''], 
['', '', 6, 7, '', '', 2, 8, 4], 
[3, 7, '', '', 6, '', 4, 1, ''], 
[4, '', '', '', 8, '', '', 6, 3], 
['', 6, '', 3, 7, '', 9, 2, 8]]



def matrix_rev():
	m_rev=[[],[],[],[],[],[],[],[],[]]
	for idx_x,line_ in enumerate(matrix):
		for idx_y,col_ in enumerate( line_):
			m_rev[idx_y].append(col_)
	return(m_rev)
matrix1=(matrix_rev())

def matrix_cube():
	m_cube=[[],[],[],[],[],[],[],[],[]]
	for k in range(1,10):
		print("a ",k)

		for j in range(1,10):
			print("b ",j)
			if j%3==0:
				break
matrix_cube()









def solver(x,y):
	def check_x():
		for idx_l in range(8):
			if idx_l+1 not in matrix[x]:
				# print('a  ',idx_l+1, matrix[x])
				for idx_c in range(8):
					if idx_l+1 != matrix[idx_c][y-1]:
						print(idx_l+1)
				exit()

	check_x()

for i in range(1):
	x=0
	
	for l in matrix:
		x+=1
		y=0
		for elem in l:
			y+=1
			if elem=='':
				# print(x,y)
				# solver(x,y)
				pass






