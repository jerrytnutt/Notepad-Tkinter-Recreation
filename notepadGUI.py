import tkinter as tk
import tkinter.filedialog
from tkinter import font
from ctypes import windll
from datetime import datetime
import time
import os

class Notebook:
  
  def __init__(self):
    self.windows = 0
    self.current_file = "None"
    self.new_file_type = None
    self.found_str_index = 0
    self.match_locations = []
    self.str_to_find = None
    self.find_direction_down = True
    #self.wrap = True

  def check_text_length(self,new_file_type):
    self.new_file_type = new_file_type
    if len( self.text_field.get("1.0",'end-1c') ) == 0:
      if new_file_type == 'saved':
        return self.open_saved_file()
      else:
        return new_file_type
    return self.save_option_frame.pack()
    
  def dont_save_file(self):
    self.text_field.delete('1.0', 'end-1c')
    self.save_option_frame.pack_forget()
    if self.new_file_type == 'saved':
      return self.open_saved_file()
    self.current_file = None
    return self.new_window.title('Untitled')
   
  def open_saved_file(self):
    self.current_file = tk.filedialog.askopenfilename(filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
    self.new_window.title(os.path.basename(self.current_file))
    try:
      with open(self.current_file, 'r') as saved_file:
        self.text_field.insert('1.0', saved_file.read() )
    except FileNotFoundError:
      self.new_window.title('Untitled')
      return 'File Not Found'
    return self.current_file
  
  def save_file(self):
    if os.path.exists(self.current_file):
      with open(self.current_file, 'w') as curr_file:
        curr_file.write( self.text_field.get("1.0",'end-1c') ) 
    else:
      return self.save_as_file()

  def save_as_file(self):
    try:
      file_save_as = tk.filedialog.asksaveasfile(defaultextension='.txt',filetypes=[("Text file",".txt")])
      self.current_file = str(file_save_as.name)
      with open(self.current_file, 'w') as curr_file:
        curr_file.write( self.text_field.get("1.0",'end-1c') )
      return current_file
    except AttributeError:
      return 'Attribute Error'
  
  def page_setup(self):
    self.text_field.grid(row=0, column=1, padx=50, pady=50)
  def cut(self):
    self.saved_text = self.text_field.get("sel.first", "sel.last")
    self.text_field.delete("sel.first", "sel.last")

  def copy(self, event=None):
    self.saved_text = self.text_field.get("sel.first", "sel.last")

  def paste(self):
    current_position = self.text_field.index(tk.INSERT)
    self.text_field.mark_set('insert',current_position)
    self.text_field.insert('insert', self.saved_text)
  
  def change_find_direction(self,find_direction_down):
    if self.find_direction_down == find_direction_down:
      return 0
    self.find_direction_down = find_direction_down
    found_str_index = self.match_locations[self.found_str_index]
    self.match_locations = self.match_locations[::-1]
    self.found_str_index = self.match_locations.index(found_str_index)
    return self.find_direction_down
    
  def find(self,replace=False):
    self.str_to_find = self.str_txt.get("1.0",'end-1c')
    if len(self.str_to_find) == 0:
      return 'No text'
    start_index = '1.0'
    self.match_locations = []

    while True:
      string_location = self.text_field.search(self.str_to_find, start_index, nocase=1, stopindex='end')
      if string_location != '':
        end_column = int(float(string_location [2:]) + len(self.str_to_find))
        end_column = string_location[0:2]+str(end_column)
        self.match_locations.append([string_location,end_column])
        start_index = end_column
      else:
        if self.find_direction_down == False:
          self.match_locations = self.match_locations[::-1]
        break
   
    if self.match_locations == []:
      return self.cant_find_box()
    
    self.found_str_index = 0
    current_string = self.match_locations[0]
    self.text_field.tag_add('found', current_string[0], current_string[1])
    self.text_field.tag_config('found', background='blue',foreground='white')
    return self.match_locations

  def find_next(self,previous=False):
    if self.str_to_find != self.str_txt.get("1.0",'end-1c') or self.match_locations == []:
      self.text_field.tag_delete('found')
      return self.find()
    print('hey')
    num = 1
    if previous:
      if self.found_str_index == 0:
        return self.cant_find_box()
      self.found_str_index -= num
    else: 
      if (self.found_str_index + 1) == len(self.match_locations):
        #if self.wrap:
          #self.found_str_index = -1
        #else:
        print('return')
        return self.cant_find_box()
      self.found_str_index += num
    
    print('here4')
    current_string = self.match_locations[self.found_str_index]
    self.text_field.tag_delete('found')
    self.text_field.tag_add('found', current_string[0], current_string[1])
    self.text_field.tag_config('found', background='blue',foreground='white')
    
  def cant_find_box(self):
    try:
      print(self.no_match_frame)
      self.no_match_frame.pack()
    except:
      self.no_match_frame = tk.Frame(self.text_field, height=100, width=150,highlightthickness=1,highlightbackground="black")
      self.no_match_frame.pack(anchor='center')
      self.no_match_frame.pack_propagate(0)
      self.text = tk.Label(self.no_match_frame, text="Cannot find {}.".format(self.str_to_find))
      self.text.pack(anchor='center')
      self.ok_button = tk.Button(self.no_match_frame, text ="ok",command=self.no_match_frame.destroy)
      return self.ok_button.pack(side='top')

  def find_mouse_xy(self,event):
    self.row_column.pack_forget()
    self.row_column = tk.Label(self.bottom_widget, text="{}".format(self.text_field.index('insert')),background="white")
    self.row_column.pack(side='right')
    print(self.text_field.index('insert'))
    self.text_field.tag_delete('found')
    self.match_locations = []

  def time_date(self):
    now = datetime.now()
    dt_string = now.strftime("%I:%M %p %d/%m/%Y")
    current_position = self.text_field.index(tk.INSERT)
    self.text_field.mark_set('insert',current_position)
    self.text_field.insert('insert', dt_string)
  
  def go_to(self):
    length_txt = self.length_txt.get("1.0",'end-1c')
    try:
      length_txt = float(length_txt)
    except:
      return 'Enter a number'
    max_row = self.text_field.index('end') 
    max_row = (float(max_row) - 1.0)
    row_number = length_txt
    if float(row_number) > float(max_row):
      return None
   #self.text_field.mark_set('insert',row_number)
    #self.no_length.pack_forget()
    self.text_field.mark_set("insert", '2.0')
    self.text_field.insert('insert', 't')

  def replace(self,all=False):
    if self.match_locations == []:
      return self.find()
    if all:
      self.found_str_index = 0
      while (self.found_str_index + 1) != len(self.match_locations):
        current_string = self.match_locations[self.found_str_index]
        self.text_field.delete(current_string[0], current_string[1])
        replacement_string = self.replace_txt.get("1.0",'end-1c')
        self.text_field.insert(current_string[0], replacement_string)
        self.match_locations = self.find()
      
        
    current_string = self.match_locations[self.found_str_index]
    self.text_field.delete(current_string[0], current_string[1])
    replacement_string = self.replace_txt.get("1.0",'end-1c')
    self.text_field.insert(current_string[0], replacement_string)
    return 0
 
  def select_all(self):
    self.text_field.tag_add('sel', "1.0", 'end-1c')
    self.text_field.mark_set('insert', "1.0")
    
  def new_win(self):
    return create_window()
  def rt(self):
    print(font.families())
    #selection = self.mylist.curselection()
    #print(selection)

  def change_display(self,event):
    print(5)
  
  def set_font(self):
    self.set_font_frame = tk.Frame(self.text_field, height=500, width=550,highlightthickness=1,background="white")
    self.set_font_frame.pack(anchor='center')
    self.set_font_frame.pack_propagate(0)

    

    
    
    self.options_widget = tk.Frame(self.set_font_frame, height=300)
    self.options_widget.pack(anchor='n',fill='x')

    self.font_widget = tk.Frame(self.options_widget, height=300,width=300,background="blue")
    self.font_widget.pack(side='left',padx=10)

    self.font_text_label = tk.Label(self.font_widget, text="Font:",background='white')
    self.font_text_label.pack(anchor='w')

    self.style_widget = tk.Frame(self.options_widget, height=300,width=120,background="blue")
    self.style_widget.pack(side='left',padx=10)
    self.style_text_label = tk.Label(self.style_widget, text="Style:",background='white')
    self.style_text_label.pack(anchor='w')

    self.size_widget = tk.Frame(self.options_widget, height=300,width=220,background="blue")
    self.size_widget.pack(side='left',padx=10)
    self.size_text_label = tk.Label(self.size_widget, text="Size:",background='white')
    self.size_text_label.pack(anchor='w')


    self.example_text_label = tk.Label(self.set_font_frame, height=10, width=30,highlightcolor="black",text="AaBbCcDdEe")
    self.example_text_label.configure(font=("Lucida Console", 14))
    self.example_text_label.pack(side='right')

    #self.save_b = tk.Button(self.set_font_frame, text ="S",command=self.rt,padx=10)
    #self.save_b.pack(side='right')

    


    font_family = ['Modern', 'Roman', 'Script', 'Courier', 'MS Serif', 'MS Sans Serif', 
    'Small Fonts', 'Marlett', 'Arial',  'Calibri',  'Candara',  'Consolas', 'Constantia', 'Corbel', 'Courier New', 
    'Ebrima', 'Franklin Gothic Medium', 'Gabriola', 'Gadugi', 'Georgia',  'Times New Roman','Impact','Broadway', 
    'Castellar', 'Centaur', 'Century',  'Cooper Black', 'Dubai', 'Elephant', 'Forte', 'Franklin Gothic Book',
    'Lucida Sans', 'Magneto','Mistral', 'Onyx',  'Papyrus', 'Pristina', 'Ravie', 
    'Franklin Gothic Demi','Lucida Console']
    font_style = ['bold','normal','italic','roman']
    font_size = [8,9,10,11,12,14,16,18,20,22,24,26,28,36,48,72]
    
    widget_array = [[self.font_widget,font_family],[self.style_widget,font_style],[self.size_widget,font_size]]
    for i in range(len(widget_array)):
      scrollbar = tk.Scrollbar(widget_array[i][0])
      scrollbar.pack(side='right',fill='y')
      
      mylist = tk.Listbox(widget_array[i][0],height=10,width=20, yscrollcommand = scrollbar.set )
      mylist.bind("<Button-1>",self.change_display)
      for line in widget_array[i][1]:
        mylist.insert('end',str(line))
        mylist.pack(side='right')
      scrollbar.config( command = mylist.yview )

    
    
    

  def open_new_window(self):
    self.new_window = tk.Toplevel()
    self.top_menu = tk.Menu(self.new_window)
    self.new_window.config(menu=self.top_menu)
    self.new_window.title('Untitled - Notepad')
    
    file_menu = tk.Menu(self.top_menu,font = ( 12))
    edit_menu = tk.Menu(self.top_menu,font = ( 12))
    self.format_menu = tk.Menu(self.top_menu,font = ( 12))

    self.top_menu.add_cascade(label='File',menu=file_menu)
    self.top_menu.add_cascade(label='Edit',menu=edit_menu)
    self.top_menu.add_cascade(label='Format',menu=self.format_menu)
    file_menu['tearoff'] = 0
    edit_menu['tearoff'] = 0
    self.format_menu['tearoff'] = 0
    
    scroll_y = tk.Scrollbar(self.new_window)
    scroll_x = tk.Scrollbar(self.new_window,orient='horizontal')

    self.bottom_widget = tk.Frame(self.new_window, height=20,width=250,background="grey")
    self.bottom_widget.pack(side='bottom',fill='both')
    self.utf_text = tk.Label(self.bottom_widget, text="UTF-8",background="white")
    self.utf_text.pack(side='right')
    self.crlf_text = tk.Label(self.bottom_widget, text="Windows (CRLF)",background="white")
    self.crlf_text.pack(side='right')

    self.text_field = tk.Text(self.new_window,undo=True,autoseparators=True,maxundo=-1,yscrollcommand=scroll_y.set,xscrollcommand=scroll_x.set,padx=5,pady=5)
    self.text_field.configure(font=("Lucida Console", 14))
    scroll_y.pack(side='right',fill='y')
    scroll_y.config(command=self.text_field.yview)
    scroll_x.pack(side='bottom',fill='x')
    scroll_x.config(command=self.text_field.xview)

    self.find_frame = tk.Frame(self.text_field, height=200, width=300,highlightthickness=1,highlightbackground="black")
    self.no_length = tk.Frame(self.text_field, height=300, width=350,highlightthickness=1,highlightbackground="black")

    self.row_column = tk.Label(self.bottom_widget, text="{}".format(self.text_field.index('insert')),background="white")
    self.row_column.pack(side='right')
   
    file_menu.add_command(label='New..       Ctrl+N',command=lambda: self.check_text_length('new'))
    file_menu.add_command(label='New Window',command=self.new_win)
    file_menu.add_command(label='Open...      Crtl+O',command=lambda: self.check_text_length('saved'))
    file_menu.add_command(label='Save    Ctrl+S',command=self.save_file)
    file_menu.add_command(label='Save as    Crtl+Shift+S',command=self.save_as_file)
    #file_menu.add_command(label='page setip',command=self.page_setup)
    #file_menu.add_command(label='print',command=self.setNum)
    file_menu.add_command(label='Exit',command=self.new_window.destroy)
    
   
    edit_menu.add_command(label='Undo Ctrl+Z',command=self.text_field.edit_undo,foreground="grey")
    edit_menu.add_command(label='Cut     Ctrl+X',command=self.cut)
    edit_menu.add_command(label='Copy   Ctrl+C',command=self.copy)
    edit_menu.add_command(label='Paste     Ctrl+V',command=self.paste)
    edit_menu.add_command(label='Delete      Del',command=lambda: self.text_field.delete("sel.first", "sel.last"))
    edit_menu.add_command(label='Find...      Ctrl+F',command=self.find_frame.pack)
    edit_menu.add_command(label='Find Next...      F3',command=self.find_next)
    edit_menu.add_command(label='Find Previous...      Shift+F3',command=lambda: self.find_next(True))
    edit_menu.add_command(label='replace',command=self.replace)
    edit_menu.add_command(label='Go To...',command=self.no_length.pack)
    edit_menu.add_command(label='Select All',command=self.select_all)
    edit_menu.add_command(label='Time/Date',command=self.time_date)

    self.format_menu.add_command(label='font..',command=self.set_font)
    


    root.bind('<Control-x>',self.cut)
    self.text_field.bind("<Button-1>",self.find_mouse_xy)
    
    
   
    self.text_field.pack(expand=True, fill='both')

    self.save_option_frame = tk.Frame(self.text_field, height=200, width=280,highlightthickness=1,background="white")
    self.save_option_frame.pack(anchor='center')
    self.save_option_frame.pack_propagate(0)

    self.top_widget = tk.Frame(self.save_option_frame, height=20,width=250,background="white")
    self.top_widget.pack(anchor='center',fill='both')
    self.find_text = tk.Label(self.top_widget, text="Find",background="white")
    self.find_text.pack(side='left')
    self.red_xbutton = tk.Button(self.top_widget, text ="X",background="white")
    self.red_xbutton.pack(side='right',fill='both')
    
    self.text = tk.Label(self.save_option_frame, text="Do you want to save changes to Untitled?",fg='blue',font = "Helvetica 10",background="white",pady=30)
    self.text.pack(anchor='w')
    
    self.button_widget = tk.Frame(self.save_option_frame, height=200,width=250,background="grey",pady=10,padx=5)
    self.button_widget.pack(anchor='s',fill='both')
    self.cancel_button = tk.Button(self.button_widget, text ="Cancel",command=self.save_option_frame.pack_forget,padx=10)
    self.cancel_button.pack(side='right')
    self.dontsave_button = tk.Button(self.button_widget, text ="Don't Save",command=self.dont_save_file,padx=10)
    self.dontsave_button.pack(side='right')
    self.save_button = tk.Button(self.button_widget, text ="Save",command=self.save_file,padx=10)
    self.save_button.pack(side='right')
    self.save_option_frame.pack_forget()

    
    self.find_frame.pack(anchor='center')
    self.find_frame.pack_propagate(0)
    self.white_widget = tk.Frame(self.find_frame, height=20,width=250,highlightthickness=1,background='white')
    self.white_widget.pack(anchor='center',fill='x')
    self.find_text = tk.Label(self.white_widget, text="Find",background='white')
    self.find_text.pack(side='left')
    self.red_xbutton = tk.Button(self.white_widget, text ="X",background='white',command=self.find_next)
    self.red_xbutton.pack(side='right',fill='both')

    self.find_frameFour = tk.Frame(self.find_frame, height=120, width=220,highlightthickness=1,highlightbackground="black")
    self.find_frameFour.pack(side="left",fill='x')
    self.find_frameFour.pack_propagate(0)
    
    self.find_widget = tk.Frame(self.find_frameFour, highlightbackground="black")
    self.find_widget.pack(anchor='center',fill='x')
    self.o_text = tk.Label(self.find_widget, text="Find",background='white')
    self.o_text.pack(side='left')
    self.str_txt = tk.Text(self.find_widget,height=1,width=140)
    self.str_txt.pack(side='left')
    
    self.replace_widget = tk.Frame(self.find_frameFour, highlightbackground="black")
    self.replace_widget.pack(anchor='center',fill='x')
    self.f_text = tk.Label(self.replace_widget, text="Find",background='white')
    self.f_text.pack(side='left')
    self.replace_txt = tk.Text(self.replace_widget,height=1,width=40)
    self.replace_txt.pack(side='left')

    text = tk.Label(self.find_frameFour, text="Direction",fg='blue',font = "Helvetica 10")
    text.pack(anchor='center')
    self.v=tk.IntVar()
    self.R1 = tk.Radiobutton(self.find_frameFour, text="Up", variable=self.v, value=1,command=lambda: self.change_find_direction(False) )
    self.R1.pack( anchor ='center' )
    self.R2 = tk.Radiobutton(self.find_frameFour, text="Down", variable=self.v, value=0,command=lambda: self.change_find_direction(True))
    self.R2.pack( anchor ='center' )

    
    
    self.find_frame_right = tk.Frame(self.find_frame, height=120, width=80,highlightthickness=1,highlightbackground="black")
    self.find_frame_right.pack(side="right")
    self.find_frame_right.pack_propagate(0)

    self.text_button = tk.Button(self.find_frame_right, text ="Find Next",command=self.find_next)
    self.text_button.pack(side='top')
    self.replace_button = tk.Button(self.find_frame_right, text ="replace",command=self.replace)
    self.replace_button.pack(side='top')
    self.replace_all_button = tk.Button(self.find_frame_right, text ="replace All",command=lambda: self.replace(True))
    self.replace_all_button.pack(side="top")
    self.cancel_find_button = tk.Button(self.find_frame_right, text ="cancel",command=self.find_frame.pack_forget)
    self.cancel_find_button.pack(side="top")


    self.find_frame_left = tk.Frame(self.find_frame, height=100, width=80,highlightthickness=1,highlightbackground="black")
    self.find_frame_left.pack(side="bottom")
    self.find_frame_left.pack_propagate(0)
    
    self.find_frame.pack_forget()

    
    self.no_length.pack(anchor='center')
    self.no_length.pack_propagate(0)

    self.text_length = tk.Label(self.no_length , text="Line Number")
    self.text_length.pack(anchor='w')

    self.length_txt = tk.Text(self.no_length,height=5,width=10)
    self.length_txt.pack(anchor='w')
    

    self.cancel_go_to = tk.Button(self.no_length, text ="Cancel",command=self.no_length.pack_forget,padx=10)
    self.cancel_go_to.pack(side='right')
    self.go_to_button = tk.Button(self.no_length, text ="Go To",command=self.go_to,padx=10)
    self.go_to_button.pack(side='right')
    

    self.no_length.pack_forget()
    

    self.new_window.geometry('1000x500')
    
    

root = tk.Tk()
windll.shcore.SetProcessDpiAwareness(1)

windows = 0
myNotebook = Notebook()
myNotebook.open_new_window()
def create_window():
  global windows
  windows += 1
  notebookName = ('myNotebook'+str(windows) )
  notebookName = Notebook()
  notebookName.open_new_window()


root.mainloop()