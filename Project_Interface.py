from tkinter import *
from PIL import ImageTk,Image
from tkinter import filedialog
from Interpolation import *

root = Tk()
root.title("Image Interpolation")
root.geometry("1250x770")

#Definitions for buttons
#temp - current displaying image
#temp1 - temporary variable used to store prev image for Undo
#original - Original image accessed when clicked Original button 
def Open():
	global org_img
	global org_img_label
	global original
	global temp
	org_filename = filedialog.askopenfilename(initialdir = " ", title = "Open", filetypes = (("jpg files","*.jpg"),("all files","*.*")))
	org_img = Image.open(org_filename)
	original = org_img.copy()
	temp = org_img.copy()
	temp1 = org_img.copy()
	org_img = ImageTk.PhotoImage(org_img)
	org_img_label = Label(root, image = org_img)
	org_img_label.grid(row = 1, column =0, columnspan = 5, rowspan = 3)

def Save():
	global temp
	#Saves files in jpeg format
	file_name = s.get()
	if temp.mode != "RGB":
		temp = temp.convert("RGB")
	temp.save(file_name+ '.jpeg')

def Undo():
	global temp2
	global temp
	global temp2_label
	temp = temp1
	temp2 = ImageTk.PhotoImage(temp)
	temp2_label = Label(root, image = temp2)
	temp2_label.grid(row = 1, column =0, columnspan = 5, rowspan = 3)

def Original():
	global init_img
	global init_img_label
	global temp
	init_img = original
	temp = original
	temp1 = original
	init_img = ImageTk.PhotoImage(init_img)
	init_img_label = Label(root, image = init_img)
	init_img_label.grid(row = 1, column = 0, columnspan = 5, rowspan = 3)

def Nearest():
	global n_temp_label
	global n_temp
	global temp1
	global temp
	temp1 = temp #Used to acces while doing Undo
	temp = nearest_neighbour(temp1, scale = 4)
	n_temp = ImageTk.PhotoImage(temp)
	n_temp_label = Label(root, image = n_temp)
	n_temp_label.grid(row = 1, column =0, columnspan = 5, rowspan = 3)

def Bilinear():
	global b_temp_label
	global b_temp
	global temp1
	global temp
	temp1 = temp
	temp = bilinear(temp1, scale = 4)
	b_temp = ImageTk.PhotoImage(temp)
	b_temp_label = Label(root, image = b_temp)
	b_temp_label.grid(row = 1, column =0, columnspan = 5, rowspan = 3)

def FRS():
	global f_temp_label
	global f_temp
	global temp1
	global temp
	temp1 = temp
	temp = fsrcnn_infer(temp1)
	f_temp = ImageTk.PhotoImage(temp)
	f_temp_label = Label(root, image = f_temp)
	f_temp_label.grid(row = 1, column =0, columnspan = 5, rowspan = 3)

def Compare():
	global c_temp_label
	global c_temp
	global temp1
	global temp
	temp1 = temp
	temp = compare(temp1)
	c_temp = ImageTk.PhotoImage(temp)
	c_temp_label = Label(root, image = c_temp)
	c_temp_label.grid(row = 1, column =0, columnspan = 5, rowspan = 3)



#Buttons
button_open = Button(root,text = "Open", command = Open)
button_save = Button(root, text = "Save", command = Save)
button_undo = Button(root, text = "Undo", command = Undo)
button_original = Button(root, text = "Original", command = Original)

button_nn = Button(root, text = "Nearest\nNeighbor", command = Nearest)
button_bilinear = Button(root, text = "Bilinear", command =  Bilinear)
button_compare = Button(root, text = "Compare", command =  Compare)
button_frscnn = Button(root, text = "FRSCNN", command = FRS)

#Placing of Buttons
button_open.grid(row = 0, column = 0)
button_undo.grid(row = 0, column = 3)
button_original.grid(row = 0, column = 4)

button_nn.grid(row = 1, column = 5)
button_bilinear.grid(row = 2, column = 5)
button_frscnn.grid(row = 3, column = 5)
button_compare.grid(row = 4, column = 0, rowspan = 2)

button_save.grid(row = 5, column = 5)

#Save File Name Input
s = Entry(root)
s.grid(row = 4, column = 5)


#Empty Space Widgets
label_empty = Label(root)
label_empty.grid(row = 0, column = 1,columnspan = 2)

label_empty2 = Label(root)
label_empty2.grid(row = 4, column = 2)

label_empty3 = Label(root)
label_empty3.grid(row = 4, column = 4)

label_empty4 = Label(root)
label_empty4.grid(row = 4, column = 1, rowspan = 2, columnspan = 2)

#Quit Button
button_quit = Button(root, text = "Quit", command = root.quit)
button_quit.grid(row = 0, column = 5)

root.mainloop()