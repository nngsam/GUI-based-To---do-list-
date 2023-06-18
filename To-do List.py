########################################### To-do list Final Python Project KN11203041 ###########################################
import datetime #module datetime to work with dates as date objects.
import  sqlite3 #to connect the Python script to the SQL database #Pip install sqlite3
from tkcalendar import DateEntry #to enter a date - install tkcalender if code does not run #Pip install tkcalendar
import tkinter as tk 
from tkinter import * #create the GUI 
import tkinter.messagebox as mb #to display boxes
import tkinter.ttk as ttk #for Ttk.Treeview: display a table in the GUI window
# Connecting to the Database
connector = sqlite3.connect("To do list.db") #creating a connection object
cursor = connector.cursor() #create cursor object
connector.execute(
	'CREATE TABLE IF NOT EXISTS FinalProject (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, Due DATETIME, Task TEXT, Description TEXT, Priority TEXT, Mode Text)'
) #tạo bảng trong database
connector.commit() #This method sends a COMMIT statement to the MySQL server, committing the current transaction. Since by default Connector/Python does not autocommit, it is important to call this method after every transaction that modifies data for tables that use transactional storage engines
# Functions
def list_all_tasks():
	global connector, table
	table.delete(*table.get_children()) #The get_children() returns a list of item IDs, one for each child. The item method of the treeview will return a dictionary of data for a given item. Thus, you can iterate over the values 
	all_data = connector.execute('SELECT * FROM FinalProject')
	data = all_data.fetchall() #fetchall() trả về dữ liệu được lưu trữ bên trong bảng dưới dạng các hàng. 
	for values in data:
		table.insert('', END, values=values)
def clear_fields(): #Clear fields in dataentry frame
	global task, description, priority, mode, due, table
	today_date = datetime.datetime.now().date()
	task.set('') ; description.set('') ;  priority.set(''), mode.set(''), due.set_date(today_date)
	table.selection_remove(*table.selection())
def remove_task():
	if not table.selection():
		mb.showerror('No selected!', 'Please select to delete!')
		return
	current_selected_task = table.item(table.focus())
	values_selected = current_selected_task['values']
	surety = mb.askyesno('Are you sure?', f'Are you sure that you want to delete {values_selected[2]}')
	if surety:
		connector.execute('DELETE FROM FinalProject WHERE ID=%d' % values_selected[0])
		connector.commit()
		list_all_tasks()
		mb.showinfo('Deleted successfully!', 'Deleted successfully')
def remove_all_tasks():
	surety = mb.askyesno('Are you sure?', 'Are you sure that you want to delete all the tasks from the database?', icon='warning')
	if surety:
		table.delete(*table.get_children())
		connector.execute('DELETE FROM FinalProject')
		connector.commit()
		clear_fields()
		list_all_tasks()
		mb.showinfo('All Tasks deleted', 'All the tasks were successfully deleted')
	else:
		mb.showinfo('Ok then', 'The action was aborted and no task was deleted!')
def add_another_task():
	global due, task, description, priority, mode
	global connector
	if not due.get() or not task.get() or not description.get() or not priority.get() or not mode.get():
		mb.showerror('Fields empty!', "Please fill all the missing fields before pressing the add button!")
	else:
		connector.execute(
		'INSERT INTO FinalProject (Due, Task, Description, Priority, Mode) VALUES (?, ?, ?, ?, ?)',
		(due.get_date(), task.get(), description.get(), priority.get(), mode.get())
		)
		connector.commit()
		clear_fields()
		list_all_tasks()
		mb.showinfo('Task added', 'The task whose details you just entered has been added to the database')
def task_to_words_before_adding():
	global due, task, description, priority, mode
	if not due or not task or not description or not priority or not mode:
		mb.showerror('Incomplete data', 'The data is incomplete, meaning fill all the fields first!')
	message = f'Your task : \n"{task.get()} - {description.get()} is dued to {due.get_date()} with priority order is {priority.get()}"'
	add_question = mb.askyesno('Read your record like: ', f'{message}\n\nShould I add it to the database?')
	if add_question:
		add_another_task()
	else:
		mb.showinfo('Ok', 'Please take your time to add this record')
def view_task_details():
	global table
	global due, task, description, priority, mode
	if not table.selection():
		mb.showerror('No task selected', 'Please select a task from the table to view its details')
	current_selected_task = table.item(table.focus()) #focus(item=None)If item is specified, sets the focus item to item. Otherwise, returns the current focus item, or ‘’ if there is none.
	values = current_selected_task['values']
	task_due = datetime.date(int(values[1][:4]), int(values[1][5:7]), int(values[1][8:]))
	due.set_date(task_due) ; task.set(values[2]) ;description.set(values[3]) ; priority.set(values[4]); mode.set(values[5])
def edit_task(): 
	global table
	def edit_existing_task():
		global due, task, description, priority, mode
		global connector, table
		current_selected_task = table.item(table.focus())
		contents = current_selected_task['values']
		connector.execute('UPDATE FinalProject SET Due = ?, Task = ?, Description = ?, Priority = ?, Mode = ? WHERE ID = ?',
		                  (due.get_date(), task.get(), description.get(), priority.get(), mode.get(), contents[0]))
		connector.commit()
		clear_fields()
		list_all_tasks()
		mb.showinfo('Data edited', 'We have updated the data and stored in the database as you wanted')
		edit_btn.destroy()
		return
	if not table.selection():
		mb.showerror('No task selected!', 'You have not selected any task in the table for us to edit; please do that!')
		return
	view_task_details()
	edit_btn = Button(data_entry_frame, text='Edit task', font=btn_font, width=30,
	                  bg=hlb_btn_bg, command=edit_existing_task)
	edit_btn.place(x=10, y=395)

# Backgrounds and Fonts 
dataentery_frame_bg = 'light cyan' #color of data entry 
buttons_frame_bg = 'mint cream' #color of buttons part
hlb_btn_bg = 'pale turquoise' #color of label
lbl_font = ('Georgia', 13) 
entry_font = 'Times 13 bold' 
btn_font = ('Gill Sans MT', 13) 

# Initializing the GUI window - khởi tạo cửa sổ GUI
root = tk.Tk() 
root.title('Python Final Project KN.11203041') #set title bar
root.geometry('1200x550') #set size of root window
root.resizable() 
Label(root, text='TO DO LIST', font=('Noto Sans CJK TC', 15, 'bold'), bg=hlb_btn_bg).pack(side=TOP, fill=X) 

task = StringVar() 
description = StringVar() 
priority = StringVar(value='*') 
mode = StringVar(value = "N/A")

#Define generally 3 main part: data entry, button, treeview
data_entry_frame = Frame(root, bg=dataentery_frame_bg) #root - frame parent, bg ở đây là màu background của frame 
data_entry_frame.place(x=0, y=30, relheight=0.95, relwidth=0.25) #x,y - độ lệch ngang dọc theo pixel, relw/h - chiều cao và chiều rộng có giá trị trong khoảng [0,1]
buttons_frame = Frame(root, bg=buttons_frame_bg)
buttons_frame.place(relx=0.25, rely=0.05, relwidth=0.75, relheight=0.21)
tree_frame = Frame(root) #default color white
tree_frame.place(relx=0.25, rely=0.26, relwidth=0.75, relheight=0.74)

# Data Entry Frame
Label(data_entry_frame, text='Due:', font=lbl_font, bg=dataentery_frame_bg).place(x=10, y=25) 
due = DateEntry(data_entry_frame, due=datetime.datetime.now().date(), font=entry_font) 
due.place(x=160, y=50)
Label(data_entry_frame, text='Task:', font=lbl_font, bg=dataentery_frame_bg).place(x=10, y=70)
Entry(data_entry_frame, font=entry_font, width=31, text=task).place(x=10, y=100) #Create the Entry box, which is used to get the user's input
Label(data_entry_frame, text='Description:', font=lbl_font, bg=dataentery_frame_bg).place(x=10, y=160)
Entry(data_entry_frame, font=entry_font, width=35,  text=description).place(x=10, y=190)
Label(data_entry_frame, text='Priority:', font=lbl_font, bg=dataentery_frame_bg).place(x=10, y=250)
dd1 = OptionMenu(data_entry_frame, priority, *['***', '**', '*'])
dd1.place(x=160, y=250); dd1.configure(width=5, font=entry_font)
Label(data_entry_frame, text='Mode:', font=lbl_font, bg=dataentery_frame_bg).place(x=10, y=300)
dd2 = OptionMenu(data_entry_frame, mode, *['In Progress', 'Done', 'Late','N/A'])
dd2.place(x=160, y=300); dd2.configure(width=12, font=entry_font)

Button(data_entry_frame, text='Add task', command=add_another_task, font=btn_font, width=30, bg=hlb_btn_bg).place(x=10, y=395) #đầu tiên là parent window - data_entry_frame, command sẽ chứa method/function - def add_another_task ở trên
Button(data_entry_frame, text='Review before adding',command=task_to_words_before_adding, font=btn_font, width=30, bg=hlb_btn_bg).place(x=10,y=450)  

# Buttons' Frame
Button(buttons_frame, text='Delete task', font=btn_font, width=25, bg=hlb_btn_bg, command=remove_task).place(x=30, y=5)
Button(buttons_frame, text='Clear Fields in DataEntry Frame', font=btn_font, width=25, bg=hlb_btn_bg, command=clear_fields).place(x=335, y=5)
Button(buttons_frame, text='Delete All Tasks', font=btn_font, width=25, bg=hlb_btn_bg, command=remove_all_tasks).place(x=640, y=5)
Button(buttons_frame, text='View Selected Task\'s Details', font=btn_font, width=25, bg=hlb_btn_bg, command=view_task_details).place(x=170, y=65)
Button(buttons_frame, text='Edit Selected Task', command=edit_task, font=btn_font, width=25, bg=hlb_btn_bg).place(x=480,y=65)

# Treeview Frame or Tkinter Treeview widget 
table = ttk.Treeview(tree_frame, selectmode=BROWSE, columns=('ID', 'Due', 'Task', 'Description', 'Priority','Mode')) #creat Treeview widget using ttk.Treeview class
X_Scroller = Scrollbar(table, orient='horizontal', command=table.xview)#table, orient là hướng, horizontal ngang
Y_Scroller = Scrollbar(table, orient='vertical', command=table.yview) #table, verical đứng
X_Scroller.pack(side='bottom', fill='x') #thanh cuộn ở vị trí dưới đáy, fill = 'x' nghĩa là khi widget hiện tại đầy thì nó sẽ fill up theo horizontal - chiều ngang only
Y_Scroller.pack(side='right', fill='y') #thanh cuộn ở vị trí bên phải 
table.config(yscrollcommand=Y_Scroller.set, xscrollcommand=X_Scroller.set) 

table.heading('ID', text='S No.', anchor=CENTER) 
table.heading('Due', text='Due', anchor=CENTER)
table.heading('Task', text='Task', anchor=CENTER)
table.heading('Description', text='Description', anchor=CENTER)
table.heading('Priority', text='Priority', anchor=CENTER)
table.heading('Mode', text='Mode', anchor=CENTER)

#Defining columns
table.column('#0', width=0, stretch=NO) #user can't alter the width when stretch=NO 
table.column('#1', width=50, stretch=NO, anchor=CENTER)
table.column('#2', width=100, stretch=NO, anchor=CENTER)  
table.column('#3', width=200, stretch=NO, anchor=CENTER)  
table.column('#4', width=350, stretch=NO, anchor=CENTER) 
table.column('#5', width=70, stretch=NO, anchor=CENTER)  
table.column('#6', width=130, stretch=NO, anchor=CENTER)  
table.place(relx=0, y=0, relheight=1, relwidth=1) 

list_all_tasks()
# Finalizing the GUI window
root.update() 
root.mainloop() 