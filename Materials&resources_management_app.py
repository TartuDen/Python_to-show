from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import random
import time
import calendar
import datetime
import get_materials_from_GMP_regist as get_mat 
import auto_completing_General_in_TBD as auto_comp_TBD 
import calend

for f in (get_mat.list_of_reagents()):
	print(f)



class Selector():
	def __init__(self,master):
		self.dic_consumption_general={'IP.11':2,'DMS':1.6,'K2CO3':3.25,'Acetone':10,'Na2CO3':0.6,
						'EtOAc':7,'MgSO4_tp4':1.5,'MgSO4_tp1':1,
						'H2O_tp4':31.5,'H2O_tp1':12.7,'H2O_tp3':12.1,'NaCl_tp1':0.56,'NaCl_tp4':3.5,
						'HCl':0.244,'IP.12cr':1.4,'IP.7':1,'STAB':0.9,
						'DCM_tp4':17.65,'DCM_tp3':12.5,'iPrOH_tp4':16,'iPrOH_tp5':51,'NaHCO3':0.91,
						'IP.6':2,'MSA':0.74,'MeOH':10,'Pd/C':84,'Celite':0.13,'NaOH':0.245,'EtOH':8.0}

		self.dic_consumption_tp245={'IP.12cr':1.4,'IP.7':1,'STAB':0.8,'DCM':17.65,'H2O':31.5,
						'iPrOH_tp4':16,'iPrOH_tp5':17,'MgSO4':1.5,'NaCl':3.5,'NaHCO3':0.91}

		self.dic_consumption_tp1={'IP.11':2,'DMS':1.6,'K2CO3':3.25,'Acetone':10,'Na2CO3':0.6,
						'EtOAc':7,'MgSO4':1,'H2O':12.7,'NaCl':0.56,'HCl':0.244}

		self.dic_consumption_tp3={'IP.6':1,'MSA':0.37,'MeOH':5,'Pd/C':40.2,'Celite':0.065,
						'NaOH':0.245,'DCM':12.5,'H2O':12.1,'EtOH':8.0}

		self.dic_consumption_people={}

		def day_week_today(): #here we check if some day was missed, subtract those days.
			def extr_db():
				conn_reag = sqlite3.connect('reagDB.db')
				cur_reag = conn_reag.cursor()
				with conn_reag:
					cur_reag.execute("SELECT * FROM reg_day_table ")
					data=cur_reag.fetchall()
					# print('correct: ',data)
				cur_reag.close()
				conn_reag.close()
				return(data[-1])
			self.last_date_str=extr_db()

			self.last_date=int(((str(self.last_date_str[0]).split('-'))[2]))

			self.currentDayForReg_ = datetime.datetime.now().date()
			self.currentDay_ = datetime.datetime.now().date()
			self.currentDay_ = ((str(self.currentDay_)).split('-'))
			self.currentDay_ = (int(self.currentDay_[-1]))
			self.currentWeekDay_ = datetime.datetime.today().weekday()
			self.currentWeekDay_ = self.currentWeekDay_ + 1
			# self.currentDay_=27
		day_week_today()

		



		def main_selector():

			self.select_var=StringVar()
			self.master = master
			self.selector=ttk.Combobox(self.master, textvariable=self.select_var, value=('People','TP1','TP3','TP2-4-5-6','General','Gen_test'))
			self.selector.place(relx=0.001,rely=0.001,width=70)
			self.selector.bind('<<ComboboxSelected>>', lambda e:self.to_select(self.master,self.select_var,self.currentDayForReg_,self.currentDay_,self.currentWeekDay_))
			self.master.bind('<Escape>', lambda e: self.esc())

			self.select_var.set('General')# to selecte where to start


			# if self.currentDay_-self.last_date>=2:#if some day was missed, run the programm a  couple of times.
			# 	for d in range(self.last_date+1,self.currentDay_+1):
			# self.currentDay_=d
			# self.currentDayForReg_='%d-%d-%s'%(datetime.datetime.now().year,datetime.datetime.now().month,self.currentDay_)					
			# self.to_select(self.master,self.select_var,self.currentDayForReg_,self.currentDay_,self.currentWeekDay_)
			# time.sleep(1)
			# self.master.update()
			# else:
			self.to_select(self.master,self.select_var,self.currentDayForReg_,self.currentDay_,self.currentWeekDay_)
		start_time = time.time()
		main_selector()

	def to_select(self,mast,select,curDForRed,curD,curWD):
		if select.get()=='TP3':
			try:
				self.tp.delete_widgets()
			except Exception as e:
				print(e)
				pass			
			self.tp=Graph(mast,select,self.dic_consumption_tp3,curDForRed,curD,curWD)

		elif select.get()=='TP1':
			try:
				self.tp.delete_widgets()
			except Exception as e:
				print(e)
				pass			
			self.tp=Graph(mast,select,self.dic_consumption_tp1,curDForRed,curD,curWD)

		elif select.get()=='TP2-4-5-6':
			try:
				self.tp.delete_widgets()
			except Exception as e:
				print(e)
				pass			
			self.tp=Graph(mast,select,self.dic_consumption_tp245,curDForRed,curD,curWD)

		elif select.get()=='People':
			try:
				self.tp.delete_widgets()
			except Exception as e:
				print(e)
				pass			
			self.tp=Graph(mast,select,self.dic_consumption_people,curDForRed,curD,curWD)

		elif select.get()=='General':
			try:
				self.tp.delete_widgets()
			except Exception as e:
				print(e)
				pass			
			self.tp=Graph(mast,select,self.dic_consumption_general,curDForRed,curD,curWD)

		elif select.get()=='Gen_test':
			try:
				self.tp.delete_widgets()
			except Exception as e:
				print(e)
				pass			
			self.tp=Graph(mast,select,self.dic_consumption_general,curDForRed,curD,curWD)





class Graph():
	def __init__(self,master,select_tp,dic_consumption,curDForRed,curD,curWD):
		self.dic_consumption=dic_consumption
		self.select_tp=select_tp.get()

		self.subtr_com_solv_done=bool()
		self.total_cons=float()
		self.master=master
		self.check_day='Not First Time'
		self.month=datetime.datetime.now().month
		self.currentDay=curD
		self.currentDayForReg=curDForRed
		self.currentWeekDay=curWD
		# print(self.currentDay,self.currentDayForReg,self.currentWeekDay)

		conn_cells = sqlite3.connect('cellsDB.db')
		with conn_cells:
			cur_cells=conn_cells.cursor()
			cur_cells.execute("SELECT * FROM  cells_table_Gen_test")
			# cur_cells.execute("DELETE  FROM  cells_table_Gen_test") #	DELLETTING is here
			# for c in cur_cells.fetchall():
			# 	print(c)
		conn_cells = sqlite3.connect('cellsDB.db')
		with conn_cells:
			cur_cells = conn_cells.cursor()
			try:
				if self.select_tp=='General':
					cur_cells.execute("""CREATE TABLE cells_table_General(
									TP text,
									month text,
									position_v_h text,
									operation text,
									color text)""")

				elif self.select_tp=='Gen_test':
					cur_cells.execute("""CREATE TABLE cells_table_Gen_test(
									TP text,
									month text,
									position_v_h text,
									operation text,
									color text)""")

				elif self.select_tp=='TP1':
					cur_cells.execute("""CREATE TABLE cells_table_tp1(
									TP text,
									month text,
									position_v_h text,
									operation text,
									color text)""")

				elif self.select_tp=='TP3':
					cur_cells.execute("""CREATE TABLE cells_table_tp3(
									TP text,
									month text,
									position_v_h text,
									operation text,
									color text)""")

				elif self.select_tp=='TP2-4-5-6':
					cur_cells.execute("""CREATE TABLE cells_table_tp24(
									TP text,
									month text,
									position_v_h text,
									operation text,
									color text)""")

				elif self.select_tp=='People':
					cur_cells.execute("""CREATE TABLE cells_table_people(
									TP text,
									month text,
									position_v_h text,
									operation text,
									color text,
									people text)""")
				cur_cells.close()
				conn_cells.close()


			except:
				pass

		



		conn_reag = sqlite3.connect('reagDB.db')
		cur_reag = conn_reag.cursor()
		try:
			cur_reag.execute("""CREATE TABLE reagents_table(
							TP text,
							name text,
							batch text,
							amount real,
							status text)""")
		except:
			pass
		finally:
			conn_reag.close()

		conn_reag_people = sqlite3.connect('peopleDB.db')
		cur_reag_people = conn_reag_people.cursor()
		try:
			cur_reag_people.execute("""CREATE TABLE people_table(
							name text,
							working_hours real,
							month text,
							reserve1 text)""")
		except:
			pass
		finally:
			conn_reag_people.close()

		def main_master_fr():
			self.master = master

			self.master.bind('<Escape>', lambda e: self.esc())

			self.canvas = Canvas(self.master, borderwidth=0, background="#ffffff")

			self.frame_main = Frame(self.master, bg='gray35')
			self.frame_main.place(relx=0.16, rely=0.01)

			

			
			def scrolling(canvas,frame):

				def onFrameConfigure( event):
					'''Reset the scroll region to encompass the inner frame'''
					canvas.configure(scrollregion=canvas.bbox("all"))		
				
				vsb = Scrollbar(self.master, orient="horizontal", command=canvas.xview)
				canvas.configure(xscrollcommand=vsb.set)

				vsb.pack(side="bottom", fill="x")
				canvas.place(relx=0.16, rely=0.01)
				canvas.create_window((4,4), window=frame, anchor="nw", tags="frame")

				frame.bind("<Configure>", onFrameConfigure)
			scrolling(self.canvas,self.frame_main)




			if self.select_tp != 'General':
				self.frame_info = Text(self.master, wrap='word')
				self.frame_info.place(relx=0.005, rely=0.67, relwidth=0.155, relheight=0.32)
			self.text_frame_for_reag_from_excel=Text(self.master,wrap='word')
			self.text_frame_for_reag_from_excel.place(x=300, y=730, width=700, height=200)

		main_master_fr()

		def reagent_frame():
			combo_reag_values=set()			    
			if self.select_tp=='General' or self.select_tp=='Gen_test':
				combo_reag_values=('List','IP.11-kg:', 'DMS-kg:', 'K2CO3-kg:', 'Acetone-L:', 'Na2CO3-kg:', 'EtOAc-L:',
									'H2O-L:', 'HCl-kg:','IP.12cr-kg:', 'IP.7-kg:', 'STAB-kg:', 'DCM-L:', 'iPrOH-L:', 'MgSO4-kg:', 
									'NaCl-kg:', 'NaHCO3-kg:','IP.6-kg:', 'MSA-kg:', 'MeOH-L:', 'Pd/C-g:', 'Celite-kg:', 'NaOH-kg:', 'EtOH abs-L:')

			elif self.select_tp=='TP1':
				combo_reag_values=('List','IP.11-kg:', 'DMS-kg:', 'K2CO3-kg:', 'Acetone-L:', 'Na2CO3-kg:', 'EtOAc-L:', 'MgSO4-kg:','H2O-L:', 'NaCl-kg:','HCl-kg:')
			elif self.select_tp=='TP3':
				combo_reag_values=('List','IP.6-kg:', 'MSA-kg:', 'MeOH-L:', 'Pd/C-g:', 'Celite-kg:', 'NaOH-kg:', 'DCM-L:', 'H2O-L:', 'EtOH abs-L:')
			elif self.select_tp=='TP2-4-5-6':
				combo_reag_values=('List','IP.12cr-kg:', 'IP.7-kg:', 'STAB-kg:', 'DCM-L:', 'H2O-L:', 'iPrOH-L:', 'MgSO4-kg:', 'NaCl-kg:', 'NaHCO3-kg:')

			elif self.select_tp=='People':
				combo_reag_values=('List','Vilve A.', 'Allan N.', 'Raul K.', 'Kalev U.', 'Kalmer K.', 'Olena P.', 'Ihor C.', 'Artjom I.', 'Denis M.')


			self.frame_reagents = Frame(self.master, bg='LightGoldenrod1')
			if self.select_tp=='General' or self.select_tp=='Gen_test':
				self.frame_reagents.place(relx=0.0005, rely=0.03, relwidth=0.157, relheight=0.95)
			else:
				self.frame_reagents.place(relx=0.0005, rely=0.03, relwidth=0.157, relheight=0.64)
				# self.name_frame_reagents = Label(self.frame_reagents, text='Reagents', bg='LightGoldenrod1', font=('Arial', 14, 'italic', 'bold'))
				# self.name_frame_reagents.place(relx=0.3, rely=0.01)

			self.reag_names_str_var = StringVar()
			self.combo_reag_name = ttk.Combobox(self.frame_reagents, textvariable=self.reag_names_str_var, value=combo_reag_values)
			self.combo_reag_name.bind('<<ComboboxSelected>>', lambda e:self.DB_list_all_reagents_from_db())

			self.combo_reag_name.place(relx=0.005, y=10, width=70)

			self.entry_reag_batch = Entry(self.frame_reagents)
			self.entry_reag_batch.insert(0, 'batch')
			self.entry_reag_batch.place(relx=0.295, y=10, width=55)

			self.entry_reag_amount = Entry(self.frame_reagents)
			self.entry_reag_amount.insert(0, 'amount')
			self.entry_reag_amount.place(relx=0.525, y=10, width=55)

			def status_botton():
				stat = self.entry_reag_status.cget('text')
				if stat == 'stat':
					self.entry_reag_status.config(text='kar', bg='red')
				elif stat == 'kar':
					self.entry_reag_status.config(text='rel', bg='green')
				elif stat == 'rel':
					self.entry_reag_status.config(text='stat', bg='grey')
			self.entry_reag_status = Button(self.frame_reagents, text='stat', bg='grey', command=status_botton)
			self.entry_reag_status.place(relx=0.75, y=10, width=31, height=19)
			self.entry_reag_ADD = Button(self.frame_reagents, text='+', command=lambda: self.DB_reag_add(self.reag_names_str_var.get(), self.entry_reag_batch.get(), self.entry_reag_amount.get(), self.entry_reag_status.cget('text')))
#$
			self.entry_reag_ADD.place(relx=0.89, y=10, width=21, height=19)

			self.frame_details = Text(self.frame_reagents, wrap='word', font=('Arial', 7, 'bold'))
			self.frame_details.place(x=2, y=35, relwidth=0.98, relheight=0.95)
			self.DB_list_all_reagents_from_db()

		reagent_frame()

		def connect():
			self.conn_graph = sqlite3.connect('cellsDB.db')
			self.cur_graph = self.conn_graph.cursor()
		connect()


		def reg_today(): # register first time log in
			conn_reag = sqlite3.connect('reagDB.db')
			cur_reag = conn_reag.cursor()
			try:
				cur_reag.execute("""CREATE TABLE reg_day_table(
								today_check text)""")
			except:
				pass

			conn_reag = sqlite3.connect('reagDB.db')
			cur_reag = conn_reag.cursor()
			with conn_reag:
				cur_reag.execute("SELECT * FROM reg_day_table WHERE today_check=?",(self.currentDayForReg,))
				data=cur_reag.fetchone()
				# print('1',data)
				if data==None:
					cur_reag.execute("INSERT INTO reg_day_table VALUES (?)",(self.currentDayForReg,))
					self.check_day='First Time'


				cur_reag.execute("SELECT * FROM reg_day_table ")
				data=cur_reag.fetchall()
				# print('2',data)
			cur_reag.close()
			conn_reag.close()

		reg_today()

		def main_funct():
			# self.days = self.makeCalendar()
			self.days = calend.calendar_for_TBD()
			self.cells_ = self.buildDayCells(self.days, self.currentDay)

			self.buildingReagCells()
			self.BRalert(self.currentDay,self.cells_)
		main_funct()

	def esc(self):
		return(self.master.destroy())




	def buildDayCells(self, calendar, TodayIs):
		# print('select_tp: ',self.select_tp)
		bg=str()
		if self.select_tp=='General' or self.select_tp=='Gen_test':
			bg='wheat1'
		elif self.select_tp=='TP1':
			bg='wheat1'
		elif self.select_tp=='TP3':
			bg='lightblue'
		elif self.select_tp=='TP2-4-5-6':
			bg='DarkSeaGreen1'
		elif self.select_tp=='People':
			bg='lightgreen'



		try: # destroy prev month when scrolling monthes
			for i in range(len(self.cells_)):
				for j in range(len(self.cells_[i])):
					self.cells_[i][j].destroy()
		except:
			pass

		if self.month==datetime.datetime.now().month:
			Cur_Day_Lab = Label(self.frame_main, background='red', width=2, height=3)
			if self.currentDay==1:
				Cur_Day_Lab.grid(row=0,column=1)
			else:
				Cur_Day_Lab.grid(row=0, column=2) #curent day used to be TodayIs now, since int((day_.split('.'))[0])==(self.currentDay-1) <<week_[day_idx]>=self.currentDay-1 in the past>> it's always second column
		else:
			Cur_Day_Lab = Label(self.frame_main, background=bg, width=2, height=3)
			Cur_Day_Lab.grid(row=0, column=(TodayIs))



		total_width = len(calendar) + 1  # how many columns
		if self.select_tp =='General':
			total_height = 29
		elif self.select_tp=='Gen_test':
			total_height=33
		else:
			total_height=24
		gridList = [[0 for x in range(total_width)]for y in range(total_height)]
		days_count = 0
		if self.select_tp=='General':
			for vert in range(total_height):
				for hor in range(total_width):
					if vert == 0:  # first row for calendars
						if hor > 0:  # start from 1st or 2nd column
							try:
								if 'S' in calendar[days_count]:  # to mark weekends with yellow
									gridList[vert][hor] = (Label(self.frame_main, text='%s' % (calendar[days_count]), font=('Arial', 7, 'bold'), background='lightyellow', width=3, height=3))
								else:
									gridList[vert][hor] = (Label(self.frame_main, text='%s' % (calendar[days_count]), font=('Arial', 7, 'bold'), background=bg, width=3, height=3))
								days_count += 1
							except:
								gridList[vert][hor] = (Label(self.frame_main, background=bg, width=3, height=3))
						else:  # first cell 0;0
							gridList[vert][hor] = (Label(self.frame_main, text='month:\n%s'%(self.month), background='lightgrey', width=3, height=1))
					elif hor == 0:  # first column for batch numbers and reagents
						if vert < 6:  # how many rows with batch numbers
							gridList[vert][hor] = (ttk.Entry(self.frame_main, width=14))
						else:
							gridList[vert][hor] = (Label(self.frame_main, text=' ', background=bg, width=3, height=1))
							
					else:  # the rest of cells
						if vert > 5:
							gridList[vert][hor] = (Label(self.frame_main, background=bg, width=3, height=1))
						else:
							gridList[vert][hor] = (Button(self.frame_main, background=bg, command=lambda v=vert, h=hor: self.CellClick(v, h), width=3, height=1))

					gridList[vert][hor].grid(row=vert, column=hor, stick='nsew', padx=0.5, pady=0.5)
		

		def upd_cell_and_brNumber_from_db():  # from here updating cells with data from cells_table

			

			if self.select_tp=='General':
				self.cur_graph.execute("SELECT * FROM cells_table_General WHERE month=?",(self.month,))
			
			

			db_data = self.cur_graph.fetchall()
			if len(db_data) > 0:
				for cell in db_data:
					print('cell: ', cell)
					v, h, op, color = self.extract_data_from_cell_db(cell,gridList)
					print('v,h,op,color: ',v,h,op,color)
					
					
					if color and h:
						gridList[v][h].config(text=op, background=color,font=('Arial',7,'bold'))
					elif color == None:
						gridList[v][0].insert(0, op)
		upd_cell_and_brNumber_from_db()
		# self.BRalert(self.currentDay,gridList)
		return(gridList)


	def CellClick(self, v_pos, h_pos):
		if self.select_tp=='General':
			operations = ['TP1\n ',' ', 'TP3\n ','  ', 'TP24\n ','   ', 'TP5\n ','    ','TP6\n ']
			colors_operations = ['coral1','coral1', 'gray63','gray63', 'yellow3','yellow3', 'plum1','plum1','sky blue']

		

		if self.select_tp=='General':
			bg='wheat1'
		

		if self.select_tp!='People':
			conn_cells = sqlite3.connect('cellsDB.db')
			with conn_cells:
				batch_number = self.entry_batch_numbers(v_pos, conn_cells)
				cur = conn_cells.cursor()
				day_db_pos=((self.cells_[0][h_pos].cget('text')).split('\n'))[0] #to set day as a ref to the position of operation
				db_position = str(v_pos) + ';' + str(day_db_pos)
				# print('day_db_pos: ',day_db_pos) #8.9
				db_operation = str()
				db_color = str()				
				text_from_cell = self.cells_[v_pos][h_pos].cget('text')#here5
				if text_from_cell:
					idx = operations.index(self.cells_[v_pos][h_pos].cget('text'))
					idx = idx + 1
					if idx > len(operations) - 1:
						self.cells_[v_pos][h_pos].config(text='', background=bg)
						db_operation = ''
						db_color = bg
					else:
						self.cells_[v_pos][h_pos].config(text='%s' % operations[(idx)], background=colors_operations[idx], font=('Arial',7,'bold'))
						db_operation = operations[idx]
						db_color = colors_operations[idx]
				else:
					self.cells_[v_pos][h_pos].config(text='%s' % operations[0], background=colors_operations[0],font=('Arial',7,'bold'))
					db_operation = operations[0]
					db_color = colors_operations[0]
				if self.select_tp=='General':
					cur.execute("SELECT * FROM cells_table_General WHERE position_v_h=? AND month=?", (db_position,self.month))
				elif self.select_tp=='Gen_test':
					cur.execute("SELECT * FROM cells_table_Gen_test WHERE position_v_h=? AND month=?", (db_position,self.month))
				elif self.select_tp=='TP1':
					cur.execute("SELECT * FROM cells_table_tp1 WHERE position_v_h=? AND month=?", (db_position,self.month))
				elif self.select_tp=='TP2-4-5-6':
					cur.execute("SELECT * FROM cells_table_tp24 WHERE position_v_h=? AND month=?", (db_position,self.month))
				elif self.select_tp=='TP3':
					cur.execute("SELECT * FROM cells_table_tp3 WHERE position_v_h=? AND month=?", (db_position,self.month))

				data = cur.fetchone()

				if (data) != None:
					if self.select_tp=='General':
						cur.execute("UPDATE  cells_table_General SET operation=?, color=?  WHERE position_v_h=? AND month=?", (db_operation, db_color, db_position,self.month))
					elif self.select_tp=='Gen_test':
						cur.execute("UPDATE  cells_table_Gen_test SET operation=?, color=?  WHERE position_v_h=? AND month=?", (db_operation, db_color, db_position,self.month))
					elif self.select_tp=='TP1':
						cur.execute("UPDATE  cells_table_tp1 SET operation=?, color=?  WHERE position_v_h=? AND month=?", (db_operation, db_color, db_position,self.month))
					elif self.select_tp=='TP2-4-5-6':
						cur.execute("UPDATE  cells_table_tp24 SET operation=?, color=?  WHERE position_v_h=? AND month=?", (db_operation, db_color, db_position,self.month))
					elif self.select_tp=='TP3':
						cur.execute("UPDATE  cells_table_tp3 SET operation=?, color=?  WHERE position_v_h=? AND month=?", (db_operation, db_color, db_position,self.month))
				else:
					if self.select_tp=='General':
						cur.execute("INSERT INTO cells_table_General VALUES(?,?,?,?,?) ", ('General',self.month, db_position, db_operation, db_color))
					elif self.select_tp=='Gen_test':
						cur.execute("INSERT INTO cells_table_Gen_test VALUES(?,?,?,?,?) ", ('General',self.month, db_position, db_operation, db_color))
					elif self.select_tp=='TP1':
						cur.execute("INSERT INTO cells_table_tp1 VALUES(?,?,?,?,?) ", ('General',self.month, db_position, db_operation, db_color))
					elif self.select_tp=='TP2-4-5-6':
						cur.execute("INSERT INTO cells_table_tp24 VALUES(?,?,?,?,?) ", ('General',self.month, db_position, db_operation, db_color))
					elif self.select_tp=='TP3':
						cur.execute("INSERT INTO cells_table_tp3 VALUES(?,?,?,?,?) ", ('General',self.month, db_position, db_operation, db_color))

		

	def buildingReagCells(self):

		if self.select_tp=='General' or self.select_tp=='Gen_test':
			font_size=7
		else:
			font_size=9

		def retrieve_data_from_reagDB():
			conn_reag = sqlite3.connect('reagDB.db')
			with conn_reag:
				cur_reag = conn_reag.cursor()
				#here to chose from what db will be loaded reagent's data TP='TP1' OR TP='TP234' OR TP='TP3' OR TP='TP24' OR
				cur_reag.execute("SELECT * FROM reagents_table WHERE ( TP='General')")
				data = cur_reag.fetchall()
				temp_rel_list = list()
				temp_kar_list = list()
			for item in data:
				if item[-1] == 'rel':
					temp = list()
					for j in item:
						temp.append(j)
					temp_rel_list.append(temp)
				elif item[-1] == 'kar':
					temp = list()
					for j in item:
						temp.append(j)
					temp_kar_list.append(temp)
			cur_reag.close()
			conn_reag.close()
			return([sorted(temp_rel_list), sorted(temp_kar_list)])

		total_list = retrieve_data_from_reagDB()
		def upd_DB_when_first_time(name,batch,amount):
			print('upd db when first time')
			conn_reag = sqlite3.connect('reagDB.db')
			with conn_reag:
				cur_reag = conn_reag.cursor()
				cur_reag.execute("UPDATE reagents_table SET amount=? WHERE name=? AND batch=?",(amount,name,batch))
			cur_reag.close()
			conn_reag.close()
			conn_reag = sqlite3.connect('reagDB.db')
			# to check
			# with conn_reag:
			# 	cur_reag = conn_reag.cursor()
			# 	cur_reag.execute("SELECT * FROM reagents_table  ")
			# 	for i in (cur_reag.fetchall()):
			# 		print(i)
			# 	print('--------------------')



		def search_for_op(v_target, reag_to_use, op_list, amount_taken):


			v_total=len(self.cells_)# rows (vertical)
			h_total=len(self.cells_[0]) #colums (days)
			for h in range(2,h_total): #used to be from_what_day now it's always 2d column (2d day)

				self.total_cons=0				


				for v in range(v_total):
					cell_op=self.cells_[v][h].cget('text')
					cell_op=cell_op.split('\n')
					cell_op=cell_op[0]
					for one_op in range(len(op_list)):
						if op_list[one_op] in cell_op:

							def searching_total_list():
								leftover=float()
								for i in range(len(total_list)):
									for j in range(len(total_list[i])):
										n = total_list[i][j][1]
										b = total_list[i][j][2]
										am = float(total_list[i][j][3])
										if reag_to_use in n :
											# print('test: ', reag_to_use, n, b)
											if self.check_day=='First Time' and h==2:#used to be h==self.currentDay
												if float(am) >= amount_taken[one_op]:
													if leftover:
														am = round(float(am) + leftover - amount_taken[one_op], 2)
														leftover = float()
													else:
														am = round(float(am) - amount_taken[one_op], 2)


													total_list[i][j][3] = str(am)

													if i == 1:
														self.cells_[v_target][h].config(text='%s\n%s' % (am,b), fg='red', font=('Arial', font_size, 'bold'))
													else:
														self.cells_[v_target][h].config(text='%s\n%s' % (am,b), fg='black', font=('Arial', font_size, 'bold'))
													self.total_cons=self.total_cons+amount_taken[one_op]
													if self.select_tp=='General':
														upd_DB_when_first_time(n,b,am)
													self.DB_list_all_reagents_from_db()

													return()  # we found and fill the cell, continue search another
												elif float(am) < amount_taken[one_op] and float(am) > 0:
													leftover = float(am)
													total_list[i][j][3]=str(0)
												else:
													self.cells_[v_target][h].config(text='OUT!' , fg='red', font=('Arial', font_size, 'bold'))



											elif h==2: #used to be h==self.currentDay
												if i == 1:
													self.cells_[v_target][h].config(text='%s\n%s' % (am,b), fg='red', font=('Arial', font_size, 'bold'))
												else:
													self.cells_[v_target][h].config(text='%s\n%s' % (am,b), fg='black', font=('Arial', font_size, 'bold'))
												return()  # we found and fill the cell, continue search another
											else:#__________________________________________________________


												if float(am) >= amount_taken[one_op]:
													if leftover:
														am = round(float(am) + leftover - amount_taken[one_op], 2)
														leftover = float()
													else:
														am = round(float(am) - amount_taken[one_op], 2)

													total_list[i][j][3] = str(am)

													if i == 1:
														self.cells_[v_target][h].config(text='%s\n%s' % (am,b), fg='red', font=('Arial', font_size, 'bold'))
														
													else:
														self.cells_[v_target][h].config(text='%s\n%s' % (am,b), fg='black', font=('Arial', font_size, 'bold'))
													self.total_cons=self.total_cons+amount_taken[one_op]

													return()
												elif float(am) < amount_taken[one_op] and float(am) > 0:
													leftover = float(am)
													total_list[i][j][3]=str(0)
													self.cells_[v_target][h].config(text='OUT!' , fg='red', font=('Arial', font_size, 'bold'))
												else:
													self.cells_[v_target][h].config(text='OUT!' , fg='red', font=('Arial', font_size, 'bold'))





							searching_total_list()
		if self.select_tp=='General':
			if self.select_tp=='General':
				inc=0
			elif self.select_tp=='Gen_test':
				inc=4
			for v in range(len(self.cells_)):
				for h in range(len(self.cells_[v])):
					if v == 6+inc:
						if h == 0:
							search_for_op(v, 'IP.11', ['TP1'], [self.dic_consumption['IP.11'],self.dic_consumption['IP.11']])
							self.cells_[v][h].config(text='IP.11-kg', bg='lightgrey',font=('Arial',7,'bold'))
							# self.cells_[v][h].bind('<1>',lambda e: self.DB_list_all_reagents_from_db('IP.11-kg:', 6, len(self.cells_[v]) ))
							self.cells_[v][h].bind('<1>',lambda e: self.DB_list_all_reagents_from_db('IP.11-kg:'))

						else:
							self.cells_[v][h].config(bg='lightgrey')
					elif v == 7+inc:
						if h == 0:
							search_for_op(v, 'DMS', ['TP1'], [self.dic_consumption['DMS'],self.dic_consumption['DMS']])
							self.cells_[v][h].config(text='DMS-kg', bg='lightyellow',font=('Arial',7,'bold'))
							self.cells_[v][h].bind('<1>',lambda e: self.DB_list_all_reagents_from_db('DMS-kg:'))
						else:
							self.cells_[v][h].config(bg='lightyellow')
					elif v == 8+inc:
						if h == 0:
							search_for_op(v, 'K2CO3', ['TP1'],[self.dic_consumption['K2CO3'],self.dic_consumption['K2CO3']])
							self.cells_[v][h].config(text='K2CO3-kg', bg='powder blue',font=('Arial',7,'bold'))
							self.cells_[v][h].bind('<1>',lambda e: self.DB_list_all_reagents_from_db('K2CO3-kg:'))
						else:
							self.cells_[v][h].config(bg='powder blue')
					elif v == 9+inc:
						if h == 0:
							search_for_op(v, 'Acetone', ['TP1'], [self.dic_consumption['Acetone'],
								self.dic_consumption['Acetone']])
							self.cells_[v][h].config(text='Acetone-L', bg='sandy brown',font=('Arial',7,'bold'))
							self.cells_[v][h].bind('<1>',lambda e: self.DB_list_all_reagents_from_db('Acetone-L:'))
						else:
							self.cells_[v][h].config(bg='sandy brown')
					elif v == 10+inc:
						if h == 0:
							search_for_op(v, 'Na2CO3', ['TP1'], [self.dic_consumption['Na2CO3'],self.dic_consumption['Na2CO3']])
							self.cells_[v][h].config(text='Na2CO3-kg', bg='ivory2',font=('Arial',7,'bold'))
							self.cells_[v][h].bind('<1>',lambda e: self.DB_list_all_reagents_from_db('Na2CO3-kg:'))
						else:
							self.cells_[v][h].config(bg='ivory2')
					elif v == 11+inc:
						if h == 0:
							search_for_op(v, 'EtOAc', ['TP1'], [self.dic_consumption['EtOAc'],self.dic_consumption['EtOAc']])
							self.cells_[v][h].config(text='EtOAc-L', bg='thistle1',font=('Arial',7,'bold'))
							self.cells_[v][h].bind('<1>',lambda e: self.DB_list_all_reagents_from_db('EtOAc-L:'))
						else:
							self.cells_[v][h].config(bg='thistle1')
					elif v == 12+inc:
						if h == 0:
							search_for_op(v, 'MgSO4', ['TP1','TP24'], [self.dic_consumption['MgSO4_tp1'],
								self.dic_consumption['MgSO4_tp4']])
							self.cells_[v][h].config(text='MgSO4-kg', bg='pale green',font=('Arial',7,'bold'))
							self.cells_[v][h].bind('<1>',lambda e: self.DB_list_all_reagents_from_db('MgSO4-kg:'))
						else:
							self.cells_[v][h].config(bg='pale green')
					elif v == 13+inc:
						if h == 0:
							search_for_op(v, 'H2O', ['TP1','TP24','TP3'], [self.dic_consumption['H2O_tp1'],
								self.dic_consumption['H2O_tp4'],self.dic_consumption['H2O_tp3']])
							self.cells_[v][h].config(text='H2O-L', bg='yellow2',font=('Arial',7,'bold'))
							self.cells_[v][h].bind('<1>',lambda e: self.DB_list_all_reagents_from_db('H2O-L:'))
						else:
							self.cells_[v][h].config(bg='yellow2')
					elif v == 14+inc:
						if h == 0:
							search_for_op(v, 'NaCl', ['TP1','TP24'], 
								[self.dic_consumption['NaCl_tp1'],self.dic_consumption['NaCl_tp4']])
							self.cells_[v][h].config(text='NaCl-kg', bg='cyan2',font=('Arial',7,'bold'))
							self.cells_[v][h].bind('<1>',lambda e: self.DB_list_all_reagents_from_db('NaCl-kg:'))
						else:
							self.cells_[v][h].config(bg='cyan2')
					elif v == 15+inc:
						if h == 0:
							search_for_op(v, 'HCl', ['TP1'], [self.dic_consumption['HCl'],self.dic_consumption['HCl']])
							self.cells_[v][h].config(text='HCl-kg', bg='khaki1',font=('Arial',7,'bold'))
							self.cells_[v][h].bind('<1>',lambda e: self.DB_list_all_reagents_from_db('HCl-kg:'))
						else:
							self.cells_[v][h].config(bg='khaki1')

					elif v == 16+inc:
						if h == 0:
							search_for_op(v, 'IP.6', ['TP3'], [self.dic_consumption['IP.6'],self.dic_consumption['IP.6']])
							self.cells_[v][h].config(text='IP.6-kg', bg='SkyBlue1',font=('Arial',7,'bold'))
							self.cells_[v][h].bind('<1>',lambda e: self.DB_list_all_reagents_from_db('IP.6-kg:'))
						else:
							self.cells_[v][h].config(bg='SkyBlue1')
					elif v == 17+inc:
						if h == 0:
							search_for_op(v, 'MSA', ['TP3'], [self.dic_consumption['MSA'],self.dic_consumption['MSA']])
							self.cells_[v][h].config(text='MSA-kg', bg='plum1',font=('Arial',7,'bold'))
							self.cells_[v][h].bind('<1>',lambda e: self.DB_list_all_reagents_from_db('MSA-kg:'))
						else:
							self.cells_[v][h].config(bg='plum1')
					elif v == 18+inc:
						if h == 0:
							search_for_op(v, 'MeOH', ['TP3'], [self.dic_consumption['MeOH'],self.dic_consumption['MeOH']])
							self.cells_[v][h].config(text='MeOH-L', bg='orange',font=('Arial',7,'bold'))
							self.cells_[v][h].bind('<1>',lambda e: self.DB_list_all_reagents_from_db('MeOH-L:'))
						else:
							self.cells_[v][h].config(bg='orange')
					elif v == 19+inc:
						if h == 0:
							search_for_op(v, 'Pd/C', ['TP3'], [self.dic_consumption['Pd/C'],self.dic_consumption['Pd/C']])
							self.cells_[v][h].config(text='Pd/C-g', bg='LightCyan2',font=('Arial',7,'bold'))
							self.cells_[v][h].bind('<1>',lambda e: self.DB_list_all_reagents_from_db('Pd/C-g:'))
						else:
							self.cells_[v][h].config(bg='LightCyan2')
					elif v == 20+inc:
						if h == 0:
							search_for_op(v, 'Celite', ['TP3'], [self.dic_consumption['Celite'],self.dic_consumption['Celite']])
							self.cells_[v][h].config(text='Celite-kg', bg='green2',font=('Arial',7,'bold'))
							self.cells_[v][h].bind('<1>',lambda e: self.DB_list_all_reagents_from_db('Celite-kg:'))
						else:
							self.cells_[v][h].config(bg='green2')
					elif v == 21+inc:
						if h == 0:
							search_for_op(v, 'NaOH', ['TP3'], [self.dic_consumption['NaOH'],self.dic_consumption['NaOH']])
							self.cells_[v][h].config(text='NaOH-kg', bg='tan1',font=('Arial',7,'bold'))
							self.cells_[v][h].bind('<1>',lambda e: self.DB_list_all_reagents_from_db('NaOH-kg:'))
						else:
							self.cells_[v][h].config(bg='tan1')
					elif v == 22+inc:
						if h == 0:
							search_for_op(v, 'EtOH', ['TP3'], [self.dic_consumption['EtOH'],self.dic_consumption['EtOH']])
							self.cells_[v][h].config(text='EtOH abs-L', bg='SteelBlue1',font=('Arial',7,'bold'))
							self.cells_[v][h].bind('<1>',lambda e: self.DB_list_all_reagents_from_db('EtOH abs-L:'))
						else:
							self.cells_[v][h].config(bg='SteelBlue1')

					elif v == 23+inc:
						if h == 0:
							search_for_op(v, 'IP.12cr', ['TP24'], [self.dic_consumption['IP.12cr'],self.dic_consumption['IP.12cr']])
							self.cells_[v][h].config(text='IP.12cr-kg', bg='pink1',font=('Arial',7,'bold'))
							self.cells_[v][h].bind('<1>',lambda e: self.DB_list_all_reagents_from_db('IP.12cr-kg:'))
						else:
							self.cells_[v][h].config(bg='pink1')
					elif v == 24+inc:
						if h == 0:
							search_for_op(v, 'IP.7', ['TP24'], [self.dic_consumption['IP.7'],self.dic_consumption['IP.7']])
							self.cells_[v][h].config(text='IP.7-kg', bg='snow2',font=('Arial',7,'bold'))
							self.cells_[v][h].bind('<1>',lambda e: self.DB_list_all_reagents_from_db('IP.7-kg:'))
						else:
							self.cells_[v][h].config(bg='snow2')
					elif v == 25+inc:
						if h == 0:
							search_for_op(v, 'STAB', ['TP24'], [self.dic_consumption['STAB'],self.dic_consumption['STAB']])
							self.cells_[v][h].config(text='STAB-kg', bg='yellow2',font=('Arial',7,'bold'))
							self.cells_[v][h].bind('<1>',lambda e: self.DB_list_all_reagents_from_db('STAB-kg:'))
						else:
							self.cells_[v][h].config(bg='yellow2')
					elif v == 26+inc:
						if h == 0:
							search_for_op(v, 'DCM', ['TP24','TP3'], [self.dic_consumption['DCM_tp4'],self.dic_consumption['DCM_tp3']])
							self.cells_[v][h].config(text='DCM-L', bg='RosyBrown1',font=('Arial',7,'bold'))
							self.cells_[v][h].bind('<1>',lambda e: self.DB_list_all_reagents_from_db('DCM-L:'))
						else:
							self.cells_[v][h].config(bg='RosyBrown1')
					elif v == 27+inc:
						if h == 0:
							search_for_op(v, 'NaHCO3', ['TP24'], [self.dic_consumption['NaHCO3'],self.dic_consumption['NaHCO3']])
							self.cells_[v][h].config(text='NaHCO3-kg', bg='snow',font=('Arial',7,'bold'))
							self.cells_[v][h].bind('<1>',lambda e: self.DB_list_all_reagents_from_db('NaHCO3-kg:'))
						else:
							self.cells_[v][h].config(bg='snow')

					elif v == 28+inc:
						if h == 0:
							search_for_op(v, 'iPrOH', ['TP24','TP5'], [self.dic_consumption['iPrOH_tp4'],self.dic_consumption['iPrOH_tp5']])
							self.cells_[v][h].config(text='iPrOH-L', bg='orange2',font=('Arial',7,'bold'))
							self.cells_[v][h].bind('<1>',lambda e: self.DB_list_all_reagents_from_db('iPrOH-L:'))
						else:
							self.cells_[v][h].config(bg='orange2')


							

				

		self.check_day='Not First Time'
		# print('self.check_day: ', self.check_day)

	def BRalert(self, todayIs,gridList):
		# self.currentWeekDay=5
		if self.select_tp == 'TP2-4-5-6':
			with self.conn_graph:
				self.cur_graph.execute("SELECT * FROM cells_table_tp24  WHERE month=? ORDER BY position_v_h",(self.month,)) #in order to sort data in cell, we use ORDER BY
				data = self.cur_graph.fetchall()
				for cell in data:  # print BR
					v, h, op, color = self.extract_data_from_cell_db(cell,gridList)
					br_number_alert = self.cells_[v][0].get()
					day_from_cell=self.cells_[0][h].cget('text')
					num_of_day=day_from_cell.split('\n')
					num_of_day=num_of_day[0]
					if len(br_number_alert) < 2:
						br_number_alert = 'no number'
					if h >=1 and h<=7: #from mond to friday
												

						if ('SAT' in day_from_cell or 'SUN' in day_from_cell) and op == 'DIST':
							self.frame_info.insert(INSERT, '\n%s(TP.2):\n%s: %s - %0.2fkg' % (num_of_day,op,'IP.12cr',self.dic_consumption['IP.12cr']))
							self.frame_info.insert(INSERT, '\n--------------------------')

						
						if ('SAT' in day_from_cell or 'SUN' in day_from_cell) and op =='REACT':
							self.frame_info.insert(INSERT, '\n%s(TP.4):\n%s: %s - %0.2fkg' % (num_of_day,op,'IP.7',self.dic_consumption['IP.7']))
							self.frame_info.insert(INSERT, '\n%s - %0.2fkg' % ('STAB',self.dic_consumption['STAB']))
							self.frame_info.insert(INSERT, '\n%s - %0.2fL' % ('DCM',10))
							self.frame_info.insert(INSERT, '\n--------------------------')

						if ('SAT' in day_from_cell or 'SUN' in day_from_cell) and op =='extr\nMgSO4':
							self.frame_info.insert(INSERT, '\n%s(TP.4):\n%s: %s - %0.2fL' % (num_of_day,'extr / MgSO4','DCM',11))
							self.frame_info.insert(INSERT, '\n%s - %0.2fL' % ('H2O',(self.dic_consumption['H2O']+3)))
							self.frame_info.insert(INSERT, '\n%s - %0.2fkg' % ('NaCl',self.dic_consumption['NaCl']))
							self.frame_info.insert(INSERT, '\n%s - %0.2fkg' % ('NaHCO3',self.dic_consumption['NaHCO3']))
							self.frame_info.insert(INSERT, '\n%s - %0.2fkg' % ('MgSO4',self.dic_consumption['MgSO4']))
							self.frame_info.insert(INSERT, '\n--------------------------')

						
						if ('SAT' in day_from_cell or 'SUN' in day_from_cell) and op =='evap\nrecr':
							self.frame_info.insert(INSERT, '\n%s:\n%s: %s - %0.2fL' % (num_of_day,'evap / recr','iPrOH (TP.4)',(self.dic_consumption['iPrOH_tp4']+2)))
							self.frame_info.insert(INSERT, '\n--------------------------')

						if ('SAT' in day_from_cell or 'SUN' in day_from_cell) and op =='pack\nsample':
							self.frame_info.insert(INSERT, '\n%s:\n%s - %s' % (num_of_day,'TP.4 Packing','2 vials; 2 PE bags; closures'))
							self.frame_info.insert(INSERT, '\n--------------------------')

						if ('SAT' in day_from_cell or 'SUN' in day_from_cell) and op =='TP5\nrecr':
							self.frame_info.insert(INSERT, '\n%s:\n%s: %s - %0.2fL' % (num_of_day,'TP5 / recr','iPrOH (TP.5)',(self.dic_consumption['iPrOH_tp5']+2)))
							self.frame_info.insert(INSERT, '\n--------------------------')

						if ('SAT' in day_from_cell or 'SUN' in day_from_cell) and op =='TP5\npack':
							self.frame_info.insert(INSERT, '\n%s:\n%s - %s' % (num_of_day,'TP.5 Packing','2 vials; 4 PE bags; closures'))
							self.frame_info.insert(INSERT, '\n--------------------------')

						

		elif self.select_tp=='TP3':
			with self.conn_graph:
				self.cur_graph.execute("SELECT * FROM cells_table_tp3  WHERE month=? ORDER BY position_v_h",(self.month,)) #in order to sort data in cell, we use ORDER BY
				data = self.cur_graph.fetchall()
				for cell in data:  # print BR
					v, h, op, color = self.extract_data_from_cell_db(cell,gridList)
					br_number_alert = self.cells_[v][0].get()
					day_from_cell=self.cells_[0][h].cget('text')
					num_of_day=day_from_cell.split('\n')
					num_of_day=num_of_day[0]
					if len(br_number_alert) < 2:
						br_number_alert = 'no number'
					if h >=1 and h<=7: #from mond to friday
												

						if ('SAT' in day_from_cell or 'SUN' in day_from_cell) and op in ['FH', 'SH']:
							self.frame_info.insert(INSERT, '\n%s(TP.3):\n%s: %s - %0.2fkg' % (num_of_day,op,'IP.6',self.dic_consumption['IP.6']))
							self.frame_info.insert(INSERT, '\n%s - %0.2fkg' % ('MSA',self.dic_consumption['MSA']))
							self.frame_info.insert(INSERT, '\n%s - %0.2fL' % ('MeOH',(self.dic_consumption['MeOH']+3)))
							self.frame_info.insert(INSERT, '\n%s - %0.2fg' % ('Pd/C',self.dic_consumption['Pd/C']))
							self.frame_info.insert(INSERT, '\n%s - %0.3fkg' % ('Celite',self.dic_consumption['Celite']))
							self.frame_info.insert(INSERT, '\n--------------------------')

						
						if ('SAT' in day_from_cell or 'SUN' in day_from_cell) and op =='evap\nextr':
							self.frame_info.insert(INSERT, '\n%s(TP.3):\n%s: %s - %0.2fkg' % (num_of_day,'evap / extr','NaOH',self.dic_consumption['NaOH']))
							self.frame_info.insert(INSERT, '\n%s - %0.2fkg' % ('DCM',(self.dic_consumption['DCM']+2)))
							self.frame_info.insert(INSERT, '\n%s - %0.2fL' % ('H2O',(self.dic_consumption['H2O']+2)))
							self.frame_info.insert(INSERT, '\n--------------------------')

						
						if ('SAT' in day_from_cell or 'SUN' in day_from_cell) and op =='filtr':
							self.frame_info.insert(INSERT, '\n%s(TP.3):\n%s: %s - %0.2fkg' % (num_of_day,op,'EtOH abs',self.dic_consumption['EtOH']))
							self.frame_info.insert(INSERT, '\n--------------------------')

						if ('SAT' in day_from_cell or 'SUN' in day_from_cell) and op =='dry':
							self.frame_info.insert(INSERT, '\n%s(TP.3):\n%s: %s - %s' % (num_of_day,op,'Packing','2 vials; 2 PE bags; closures'))
							self.frame_info.insert(INSERT, '\n--------------------------')

						


		elif self.select_tp=='TP1':
			with self.conn_graph:
				self.cur_graph.execute("SELECT * FROM cells_table_tp1  WHERE month=? ORDER BY position_v_h",(self.month,)) #in order to sort data in cell, we use ORDER BY
				data = self.cur_graph.fetchall()
				for cell in data:  # print BR
					v, h, op, color = self.extract_data_from_cell_db(cell,gridList)
					br_number_alert = self.cells_[v][0].get()
					day_from_cell=self.cells_[0][h].cget('text')
					num_of_day=day_from_cell.split('\n')
					num_of_day=num_of_day[0]
					if len(br_number_alert) < 2:
						br_number_alert = 'no number'
					if h >=1 and h<=7: #from mond to friday
												

						if ('SAT' in day_from_cell or 'SUN' in day_from_cell) and op =='K2CO3':
							self.frame_info.insert(INSERT, '\n%s(TP.1):\n%s: %s - %0.2fkg' % (num_of_day,op,'K2CO3',self.dic_consumption['K2CO3']))
							self.frame_info.insert(INSERT, '\n--------------------------')

						
						if ('SAT' in day_from_cell or 'SUN' in day_from_cell) and op =='React':
							self.frame_info.insert(INSERT, '\n%s(TP.1):\n%s: %s - %0.2fkg' % (num_of_day,op,'IP.11',self.dic_consumption['IP.11']))
							self.frame_info.insert(INSERT, '\n%s - %0.2fkg' % ('DMS',self.dic_consumption['DMS']))
							self.frame_info.insert(INSERT, '\n%s - %0.2fL' % ('Acetone',self.dic_consumption['Acetone']))
							self.frame_info.insert(INSERT, '\n--------------------------')

						
						if ('SAT' in day_from_cell or 'SUN' in day_from_cell) and op =='Soda / quench':
							self.frame_info.insert(INSERT, '\n%s(TP.1):\n%s: %s - %0.2fkg' % (num_of_day,op,'Na2CO3',self.dic_consumption['Na2CO3']))
							self.frame_info.insert(INSERT, '\n%s - %0.2fkg' % ('H2O',1.5))
							self.frame_info.insert(INSERT, '\n--------------------------')

						
						if ('SAT' in day_from_cell or 'SUN' in day_from_cell) and op =='Extract.':
							self.frame_info.insert(INSERT, '\n%s(TP.1):\n%s: %s - %0.2fL' % (num_of_day,op,'EtOAc',self.dic_consumption['EtOAc']))
							self.frame_info.insert(INSERT, '\n%s - %0.2fkg' % ('MgSO4',self.dic_consumption['MgSO4']))
							self.frame_info.insert(INSERT, '\n%s - %0.2fkg' % ('NaCl',self.dic_consumption['NaCl']))
							self.frame_info.insert(INSERT, '\n%s - %0.3fL' % ('HCl',self.dic_consumption['HCl']))
							self.frame_info.insert(INSERT, '\n%s - %0.2fL' % ('H2O',self.dic_consumption['H2O']))
							self.frame_info.insert(INSERT, '\n--------------------------')

						if ('SAT' in day_from_cell or 'SUN' in day_from_cell) and op =='Evap':
							self.frame_info.insert(INSERT, '\n%s(TP.1):\n%s: %s - %s' % (num_of_day,op,'Packing','2 vials'))
							self.frame_info.insert(INSERT, '\n--------------------------')




	def entry_batch_numbers(self, v, connection_):
		with connection_:
			cur = connection_.cursor()
			db_position = str(v) + ';' + '0'
			br_number = self.cells_[v][0].get()
			if self.select_tp=='General':
				if len(br_number) == 0 or len(br_number) > 2:
					cur.execute("SELECT * FROM cells_table_General WHERE position_v_h=? AND month=?", (db_position,self.month))
					data = cur.fetchone()
					if (data) is not None:
						cur.execute("UPDATE  cells_table_General SET operation=?, color=?  WHERE position_v_h=? AND month=?", (br_number, None, db_position,self.month))

					else:
						cur.execute("INSERT INTO cells_table_General VALUES(?,?,?,?,?) ", ('General',self.month, db_position, br_number, None))

					return(True)
				else:
					return(False)
			elif self.select_tp=='TP1':
				if len(br_number) == 0 or len(br_number) > 2:
					cur.execute("SELECT * FROM cells_table_tp1 WHERE position_v_h=? AND month=?", (db_position,self.month))
					data = cur.fetchone()
					if (data) is not None:
						cur.execute("UPDATE  cells_table_tp1 SET operation=?, color=?  WHERE position_v_h=? AND month=?", (br_number, None, db_position,self.month))

					else:
						cur.execute("INSERT INTO cells_table_tp1 VALUES(?,?,?,?,?) ", ('General',self.month, db_position, br_number, None))

					return(True)
				else:
					return(False)
			elif self.select_tp=='TP2-4-5-6':
				if len(br_number) == 0 or len(br_number) > 2:
					cur.execute("SELECT * FROM cells_table_tp24 WHERE position_v_h=? AND month=?", (db_position,self.month))
					data = cur.fetchone()
					if (data) is not None:
						cur.execute("UPDATE  cells_table_tp24 SET operation=?, color=?  WHERE position_v_h=? AND month=?", (br_number, None, db_position,self.month))

					else:
						cur.execute("INSERT INTO cells_table_tp24 VALUES(?,?,?,?,?) ", ('General',self.month, db_position, br_number, None))

					return(True)
				else:
					return(False)
			elif self.select_tp=='TP3':
				if len(br_number) == 0 or len(br_number) > 2:
					cur.execute("SELECT * FROM cells_table_tp3 WHERE position_v_h=? AND month=?", (db_position,self.month))
					data = cur.fetchone()
					if (data) is not None:
						cur.execute("UPDATE  cells_table_tp3 SET operation=?, color=?  WHERE position_v_h=? AND month=?", (br_number, None, db_position,self.month))

					else:
						cur.execute("INSERT INTO cells_table_tp3 VALUES(?,?,?,?,?) ", ('General',self.month, db_position, br_number, None))

					return(True)
				else:
					return(False)
	def extract_data_from_cell_db(self, cell,total_cells):
		# print('cells: ', cell)
		pos = (list(cell))[2]
		pos = pos.split(';')
		v=int(pos[0])
		h=int()

		if cell[3] :
			i=0
			while True:
				i+=1
				try: #to prevent it to going over 2 months
					real_date_pos=((total_cells[0][i].cget('text')).split('\n'))[0]
					if pos[1] ==real_date_pos:
						h=i
						# print('pos: ', pos,total_cells[0][i].cget('text'),h)
						break
				except:
					break
		
		op = (list(cell))[3]
		color = (list(cell))[4]
		return(v, h, op, color)

	def DB_reag_add(self, name, batch, amount, status):
		if self.select_tp!='People':
			if amount not in ['d','delete','amount']:
				try:
					check=float(amount)
				except ValueError:
					amount='amount'

			conn_reag = sqlite3.connect('reagDB.db')
			cur_reag = conn_reag.cursor()
			with conn_reag:
				cur_reag.execute("SELECT * FROM reagents_table WHERE TP=? AND name=? AND batch=?", ('General',name, batch))
				data = cur_reag.fetchone()
				if data is None:
					cur_reag.execute("INSERT INTO reagents_table VALUES (?,?,?,?,?)", ('General', name, batch, float((amount)), status))
				else:
					if 'amount' in amount:
						cur_reag.execute("UPDATE  reagents_table SET status=? WHERE name=? AND batch=? ", (status, name, batch))
					elif (amount == 'delete') or (amount =='d'):
						cur_reag.execute("DELETE FROM reagents_table WHERE name=? AND batch=?", (name, batch))

					else:
						cur_reag.execute("UPDATE  reagents_table SET status=?, amount=? WHERE name=? AND batch=? ", (status, amount, name, batch))
			cur_reag.close()
			conn_reag.close()
			if 'amount' not in amount:
				self.buildingReagCells()
		

		elif self.select_tp=='People':
			local_working_hours=int(batch)
			local_working_month=int(amount)
			conn_people = sqlite3.connect('peopleDB.db')
			cur_people = conn_people.cursor()
			with conn_people:
				cur_people.execute("SELECT * FROM people_table WHERE name=? AND month=?",(name, self.month))
				data = cur_people.fetchone()
				print('insert data: ', data)
				if data is None:
					cur_people.execute("INSERT INTO people_table VALUES (?,?,?,?)", (name, local_working_hours, local_working_month, None))
				else:
					# if 'amount' in amount:
					# 	cur_people.execute("UPDATE  people_table SET status=? WHERE name=? AND batch=? ", (status, name, working_hours))
					if (amount == 'delete') or (amount =='d'):
						cur_people.execute("DELETE FROM people_table WHERE name=? AND batch=?", (name, local_working_hours))

					else:
						cur_people.execute("UPDATE  people_table SET name=? WHERE working_hours=? AND month=? ", ( name, local_working_hours,local_working_month))
			cur_people.close()
			conn_people.close()
			if 'amount' not in amount:
				self.buildingReagCells()

		self.DB_list_all_reagents_from_db(name)


	def DB_list_all_reagents_from_db(self, *arg):



		if arg:
			self.arg=arg[0]
			# v=arg[1]
			# tot_h=arg[2]
			self.reag_names_str_var.set(self.arg)
			# print('<<<<<<<<<<<<>>>>>>>>>>>>>',self.arg,v,tot_h)

			# for h in range(tot_h):
			# 	self.cells_[v][h].config(background='red')
		else:
			self.arg='None'
			

		comparing_list=['IP.11', 'DMS', 'K2CO3', 'Acet', 'Na2CO3', 'EtOAc','H2O', 'HCl','IP.12cr', 'IP.7', 'STAB', 'DCM', 'iPrOH', 'MgSO4', 'NaCl', 'NaHCO3',
			'IP.6', 'MSA', 'MeOH', 'Pd', 'Celite', 'NaOH', 'EtOH']

		list_reag_from_DB=['IP.11-kg:', 'DMS-kg:', 'K2CO3-kg:', 'Acetone-L:', 'Na2CO3-kg:', 'EtOAc-L:',
			'H2O-L:', 'HCl-kg:','IP.12cr-kg:', 'IP.7-kg:', 'STAB-kg:', 'DCM-L:', 'iPrOH-L:', 'MgSO4-kg:', 'NaCl-kg:', 'NaHCO3-kg:',
			'IP.6-kg:', 'MSA-kg:', 'MeOH-L:', 'Pd/C-g:', 'Celite-kg:', 'NaOH-kg:', 'EtOH abs-L:']
		element=str()
		list_from_excel=get_mat.list_of_reagents()
		# for k in list_from_excel:
		# 	print(k)
		self.frame_details.config(state='normal')
		conn_reag = sqlite3.connect('reagDB.db')
		self.frame_details.delete('1.0', END)

		print(self.arg,'------------', list_reag_from_DB)


		if self.select_tp=='General' or self.select_tp=='Gen_test':
			if self.reag_names_str_var.get() in list_reag_from_DB or self.arg in list_reag_from_DB:
				# print('we hereee')
				with conn_reag:
					cur_reag = conn_reag.cursor()
					#here select from list reag from General db, used to be TP='TP234' OR TP='TP1' OR TP='TP3' OR TP='TP24'
					if self.arg:
						cur_reag.execute("SELECT *FROM reagents_table WHERE name=? AND (TP='General')",(self.arg,))
					else:
						cur_reag.execute("SELECT *FROM reagents_table WHERE name=? AND (TP='General')",(self.reag_names_str_var.get(),))
					data = cur_reag.fetchall()
					temp_list = list()
					for d in data:
						element=str(d[1])
						d = '%s |b %s| %s| status: %s\n' % (str(d[1]), str(d[2]), str(d[3]), str(d[4]))
						temp_list.append(d)
					temp_list = sorted(temp_list)
					for i in range(len(temp_list)):
						self.frame_details.insert(INSERT, temp_list[i])
						try:
							if ((temp_list[i + 1]).split(':')[0]) != ((temp_list[i]).split(':')[0]):
								self.frame_details.insert(INSERT, '%s\n' % ('-' * 57))
						except:
							pass	
				self.text_frame_for_reag_from_excel.delete('1.0',END)
				macth_set=set()
				for check_element in comparing_list: # this loop is for printing out reagents from excel db when you select them
					if check_element.upper() in (self.reag_names_str_var.get()).upper() or check_element.upper() in self.arg.upper():
						for k in list_from_excel:
							if 'IP.11' in check_element.upper() and 'IP11' in ((k.upper()).split('|'))[0]:
								print(k)
								self.text_frame_for_reag_from_excel.insert(INSERT,k)
								self.text_frame_for_reag_from_excel.insert(INSERT,'\n')
							elif 'IP.6' in check_element.upper() and 'IP6' in ((k.upper()).split('|'))[0]:
								print(k)
								self.text_frame_for_reag_from_excel.insert(INSERT,k)
								self.text_frame_for_reag_from_excel.insert(INSERT,'\n')
							elif 'Pd/C' in check_element.upper() and 'PdC' in ((k.upper()).split('|'))[0]:
								print(k)
								self.text_frame_for_reag_from_excel.insert(INSERT,k)
								self.text_frame_for_reag_from_excel.insert(INSERT,'\n')
							elif check_element.upper() in ((k.upper()).split('|'))[0]:
								print(k)
								self.text_frame_for_reag_from_excel.insert(INSERT,k)
								self.text_frame_for_reag_from_excel.insert(INSERT,'\n')
							
							
							# self.dic_consumption_general[]
							for key in self.dic_consumption:
								if check_element in key:
									if key not in macth_set:
										macth_set.add(key)
										# print(key,' per one batch: ',self.dic_consumption[key])
							# self.text_frame_for_reag_from_excel.insert(INSERT,k)
							# self.text_frame_for_reag_from_excel.insert(INSERT,'\n')
				for elem in macth_set:
					elem='%.2f %s %s'%(self.dic_consumption[elem],'L/kg per one batch ',elem)
					self.text_frame_for_reag_from_excel.insert(INSERT,'==================================\n')
					self.text_frame_for_reag_from_excel.insert(INSERT,elem)
					self.text_frame_for_reag_from_excel.insert(INSERT,'\n')
				print('---------------------')
			else:
				with conn_reag:
					cur_reag = conn_reag.cursor()
					#here List all reag from General db, used to be TP='TP234' OR TP='TP1' OR TP='TP3' OR TP='TP24'
					cur_reag.execute("SELECT *FROM reagents_table WHERE (TP='General' )")
					data = cur_reag.fetchall()
					temp_list = list()
					for d in data:
						d = '%s |b %s| %s| status: %s\n' % (str(d[1]), str(d[2]), str(d[3]), str(d[4]))
						temp_list.append(d)
					temp_list = sorted(temp_list)
					for i in range(len(temp_list)):
						self.frame_details.insert(INSERT, temp_list[i])
						try:
							if ((temp_list[i + 1]).split(':')[0]) != ((temp_list[i]).split(':')[0]):
								self.frame_details.insert(INSERT, '%s\n' % ('-' * 57))
						except:
							pass
		elif self.select_tp=='TP2-4-5-6':

			reag_select=['IP.12cr-kg:', 'IP.7-kg:', 'STAB-kg:', 'DCM-L:', 'H2O-L:', 'iPrOH-L:', 'MgSO4-kg:', 'NaCl-kg:', 'NaHCO3-kg:']

			if self.reag_names_str_var.get() in reag_select:
				
				with conn_reag:
					cur_reag = conn_reag.cursor()
					#here select from list reag from General db, used to be TP='TP234' OR TP='TP1' OR TP='TP3' OR TP='TP24'
					cur_reag.execute("SELECT *FROM reagents_table WHERE name=? AND (TP='General')",(self.reag_names_str_var.get(),))
					data = cur_reag.fetchall()
					temp_list = list()
					for d in data:
						d = '%s |b %s| %s| status: %s\n' % (str(d[1]), str(d[2]), str(d[3]), str(d[4]))
						temp_list.append(d)
					temp_list = sorted(temp_list)
					for i in range(len(temp_list)):
						self.frame_details.insert(INSERT, temp_list[i])
						try:
							if ((temp_list[i + 1]).split(':')[0]) != ((temp_list[i]).split(':')[0]):
								self.frame_details.insert(INSERT, '%s\n' % ('-' * 57))
						except:
							pass		
			else:
				with conn_reag:
					cur_reag = conn_reag.cursor()
					#here List all reag from General db, used to be TP='TP234' OR TP='TP1' OR TP='TP3' OR TP='TP24'
					cur_reag.execute("SELECT *FROM reagents_table WHERE (TP='General' )")
					data = cur_reag.fetchall()
					temp_list = list()
					for d in data:
						if d[1] in reag_select:
							d = '%s |b %s| %s| status: %s\n' % (str(d[1]), str(d[2]), str(d[3]), str(d[4]))
							temp_list.append(d)
					temp_list = sorted(temp_list)
					for i in range(len(temp_list)):
						self.frame_details.insert(INSERT, temp_list[i])
						try:
							if ((temp_list[i + 1]).split(':')[0]) != ((temp_list[i]).split(':')[0]):
								self.frame_details.insert(INSERT, '%s\n' % ('-' * 57))
						except:
							pass
		elif self.select_tp=='TP1':
			reag_select=['IP.11-kg:', 'DMS-kg:', 'K2CO3-kg:', 'Acetone-L:', 'Na2CO3-kg:', 'EtOAc-L:', 'MgSO4-kg:','H2O-L:', 'NaCl-kg:','HCl-kg:']
			if self.reag_names_str_var.get() in reag_select:
				with conn_reag:
					cur_reag = conn_reag.cursor()
					#here select from list reag from General db, used to be TP='TP234' OR TP='TP1' OR TP='TP3' OR TP='TP24'
					cur_reag.execute("SELECT *FROM reagents_table WHERE name=? AND (TP='General')",(self.reag_names_str_var.get(),))
					data = cur_reag.fetchall()
					temp_list = list()
					for d in data:
						d = '%s |b %s| %s| status: %s\n' % (str(d[1]), str(d[2]), str(d[3]), str(d[4]))
						temp_list.append(d)
					temp_list = sorted(temp_list)
					for i in range(len(temp_list)):
						self.frame_details.insert(INSERT, temp_list[i])
						try:
							if ((temp_list[i + 1]).split(':')[0]) != ((temp_list[i]).split(':')[0]):
								self.frame_details.insert(INSERT, '%s\n' % ('-' * 57))
						except:
							pass		
			else:
				with conn_reag:
					cur_reag = conn_reag.cursor()
					#here List all reag from General db, used to be TP='TP234' OR TP='TP1' OR TP='TP3' OR TP='TP24'
					cur_reag.execute("SELECT *FROM reagents_table WHERE (TP='General' )")
					data = cur_reag.fetchall()
					temp_list = list()
					for d in data:
						if d[1] in reag_select:
							d = '%s |b %s| %s| status: %s\n' % (str(d[1]), str(d[2]), str(d[3]), str(d[4]))
							temp_list.append(d)
					temp_list = sorted(temp_list)
					for i in range(len(temp_list)):
						self.frame_details.insert(INSERT, temp_list[i])
						try:
							if ((temp_list[i + 1]).split(':')[0]) != ((temp_list[i]).split(':')[0]):
								self.frame_details.insert(INSERT, '%s\n' % ('-' * 57))
						except:
							pass
		elif self.select_tp=='TP3':
			reag_select=['IP.6-kg:', 'MSA-kg:', 'MeOH-L:', 'Pd/C-g:', 'Celite-kg:', 'NaOH-kg:', 'DCM-L:', 'H2O-L:', 'EtOH abs-L:']
			if self.reag_names_str_var.get() in reag_select:
				with conn_reag:
					cur_reag = conn_reag.cursor()
					#here select from list reag from General db, used to be TP='TP234' OR TP='TP1' OR TP='TP3' OR TP='TP24'
					cur_reag.execute("SELECT *FROM reagents_table WHERE name=? AND (TP='General')",(self.reag_names_str_var.get(),))
					data = cur_reag.fetchall()
					temp_list = list()
					for d in data:
						d = '%s |b %s| %s| status: %s\n' % (str(d[1]), str(d[2]), str(d[3]), str(d[4]))
						temp_list.append(d)
					temp_list = sorted(temp_list)
					for i in range(len(temp_list)):
						self.frame_details.insert(INSERT, temp_list[i])
						try:
							if ((temp_list[i + 1]).split(':')[0]) != ((temp_list[i]).split(':')[0]):
								self.frame_details.insert(INSERT, '%s\n' % ('-' * 57))
						except:
							pass		
			else:
				with conn_reag:
					cur_reag = conn_reag.cursor()
					#here List all reag from General db, used to be TP='TP234' OR TP='TP1' OR TP='TP3' OR TP='TP24'
					cur_reag.execute("SELECT *FROM reagents_table WHERE (TP='General' )")
					data = cur_reag.fetchall()
					temp_list = list()
					for d in data:
						if d[1] in reag_select:
							d = '%s |b %s| %s| status: %s\n' % (str(d[1]), str(d[2]), str(d[3]), str(d[4]))
							temp_list.append(d)
					temp_list = sorted(temp_list)
					for i in range(len(temp_list)):
						self.frame_details.insert(INSERT, temp_list[i])
						try:
							if ((temp_list[i + 1]).split(':')[0]) != ((temp_list[i]).split(':')[0]):
								self.frame_details.insert(INSERT, '%s\n' % ('-' * 57))
						except:
							pass
		elif self.select_tp=='People':
			conn_people = sqlite3.connect('peopleDB.db')

			people_select=['Vilve A.', 'Allan N.', 'Raul K.', 'Kalev U.', 'Kalmer K.', 'Olena P.', 'Ihor C.', 'Artjom I.', 'Denis M.']
			if self.reag_names_str_var.get() in people_select:
				with conn_people:
					cur_people = conn_people.cursor()
					#here select from list reag from General db, used to be TP='TP234' OR TP='TP1' OR TP='TP3' OR TP='TP24'
					cur_people.execute("SELECT *FROM people_table WHERE name=? AND month=? ",(self.reag_names_str_var.get(),self.month))
					data = cur_people.fetchall()
					temp_list = list()
					for d in data:
						d = '%s | %sh| %s| %s\n' % (str(d[0]), str(d[1]), 'None', 'None')
						temp_list.append(d)
					temp_list = sorted(temp_list)
					for i in range(len(temp_list)):
						self.frame_details.insert(INSERT, temp_list[i])
						try:
							if ((temp_list[i + 1]).split(':')[0]) != ((temp_list[i]).split(':')[0]):
								self.frame_details.insert(INSERT, '%s\n' % ('-' * 57))
						except:
							pass		
			else:
				with conn_people:
					cur_people = conn_people.cursor()
					#here List all reag from General db, used to be TP='TP234' OR TP='TP1' OR TP='TP3' OR TP='TP24'
					cur_people.execute("SELECT *FROM people_table WHERE month=?",(self.month,))
					data = cur_people.fetchall()
					temp_list = list()
					for d in data:
						if d[0] in people_select:
							d = '%s | %sh| %s| %s\n' % (str(d[0]), str(d[1]), 'None', 'None')
							temp_list.append(d)
					temp_list = sorted(temp_list)
					for i in range(len(temp_list)):
						self.frame_details.insert(INSERT, temp_list[i])
						try:
							if ((temp_list[i + 1]).split(':')[0]) != ((temp_list[i]).split(':')[0]):
								self.frame_details.insert(INSERT, '%s\n' % ('-' * 57))
						except:
							pass



		self.frame_details.config(state='disabled')


	def delete_widgets(self):
		list_widgets=self.master.place_slaves()

		for i in list_widgets:
			print('<<<<<<<<<<<<',i)
			if 'combobox' not in str(i):
				i.destroy()

def correct_reg_day():
	day='2020-05-20'
	conn_reag = sqlite3.connect('reagDB.db')
	cur_reag = conn_reag.cursor()
	with conn_reag:
		cur_reag.execute("DELETE FROM reg_day_table WHERE today_check=?",(day,))
		cur_reag.execute("SELECT * FROM reg_day_table ")
		data=cur_reag.fetchall()
		print('correct: ',data)

	cur_reag.close()
	conn_reag.close()

	


def correct_Reag_table():
	conn_reag=sqlite3.connect('reagDB.db')
	cur_reag=conn_reag.cursor()
	with conn_reag:
		cur_reag.execute("DELETE FROM reagents_table WHERE name=? AND batch=?",('IP.12cr-kg:','001'))
		cur_reag.execute("SELECT * FROM reagents_table")
		data=cur_reag.fetchall()
		for i in data:
			print(i)
		print('________________')
	cur_reag.close()
	conn_reag.close()
# correct_Reag_table()

def correct_Cells_table():
	conn_reag=sqlite3.connect('cellsDB.db')
	cur_reag=conn_reag.cursor()
	with conn_reag:
		cur_reag.execute("DELETE FROM cells_table_tp24 WHERE TP=?",('TP3',))
		cur_reag.execute("SELECT * FROM cells_table_tp24")
		data=cur_reag.fetchall()
		for i in data:
			print(i)
		print('________________')
	cur_reag.close()
	conn_reag.close()
# correct_Cells_table()


def main():
	# correct_reg_day()



	root = Tk()
	root.geometry('1550x870+50+20')
	root.resizable(True, True)
	new_object = Selector(root)
	root.mainloop()




main()



