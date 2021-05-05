import tkinter as tk
import tkinter.filedialog
from tkinter import font
from ctypes import windll
from sys import platform
from datetime import datetime
import time, os


class Notebook:
  
  def __init__(self):
    self.windows = 0
    self.current_file = "None"
    self.new_file_type = None
    self.found_str_index = 0
    self.match_locations = []
    self.str_to_find = None
    self.find_direction_down = True
    self.font = ["Lucida Console",14,"normal"]
    
    #self.wrap = True

  def main_hub(self,new_file_type='Nones'):
    self.new_file_type = new_file_type
    if len( self.text_field.get("1.0",'end-1c') ) == 0:
      if new_file_type == 'saved':
        return self.open_saved_file()
      return 0
    return self.save_option_frame.pack()

  def clear_text(self,option='quit'):
    if option == 'save':
      self.save_file()
    if self.new_file_type == 'new':
      self.text_field.delete('1.0', 'end-1c')
      self.save_option_frame.pack_forget()
      self.new_file_type = 'None'
      return self.new_window.title('Untitled')
    elif self.new_file_type == 'saved':
      self.open_saved_file()
    self.new_file_type = 'None'
    return 'None'

  def open_saved_file(self):
    self.current_file = tk.filedialog.askopenfilename(filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
    self.text_field.delete('1.0', 'end-1c')
    self.save_option_frame.pack_forget()
    self.new_window.title(os.path.basename(self.current_file))
    try:
      with open(self.current_file, 'r') as saved_file:
        self.text_field.insert('1.0', saved_file.read() )
    except FileNotFoundError:
      self.new_window.title('Untitled')
      return 'File Not Found'
    return self.current_file
  
  def save_file(self):
    print(self.current_file)
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
      self.new_window.title(os.path.basename(self.current_file))
    except AttributeError:
      return 'Attribute Error'
  
  
    

  #/////////////////////////////////////////////////////////////////////////
  def cut(self):
    self.saved_text = self.text_field.get("sel.first", "sel.last")
    return self.text_field.delete("sel.first", "sel.last")

  def copy(self, event=None):
    self.saved_text = self.text_field.get("sel.first", "sel.last")
    return self.saved_text

  def paste(self):
    current_position = self.text_field.index(tk.INSERT)
    self.text_field.mark_set('insert',current_position)
    return self.text_field.insert('insert', self.saved_text)
  
  def find(self,replace=False):
    self.str_to_find = self.find_what_text.get("1.0",'end-1c')
    if len(self.str_to_find) == 0:
      return self.str_to_find
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
    if self.str_to_find != self.find_what_text.get("1.0",'end-1c') or self.match_locations == []:
      self.text_field.tag_delete('found')
      return self.find()
    location_int = 1
    if previous:
      if self.found_str_index == 0:
        return self.cant_find_box()
      self.found_str_index -= location_int
    else: 
      if (self.found_str_index + 1) == len(self.match_locations):
        return self.cant_find_box()
      self.found_str_index += location_int
    current_string = self.match_locations[self.found_str_index]
    self.text_field.tag_delete('found')
    self.text_field.tag_add('found', current_string[0], current_string[1])
    self.text_field.tag_config('found', background='blue',foreground='white')

  def change_find_direction(self,find_direction_down):
    if self.find_direction_down == find_direction_down:
      return self.find_direction_down
    self.find_direction_down = find_direction_down
    found_str_index = self.match_locations[self.found_str_index]
    self.match_locations = self.match_locations[::-1]
    self.found_str_index = self.match_locations.index(found_str_index)
    return self.find_direction_down
    
  def cant_find_box(self):
    try:
      self.no_match_frame.pack()
    except:
      self.no_match_frame = tk.Frame(self.text_field, height=100, width=150,highlightthickness=1,highlightbackground="black")
      self.no_match_frame.pack(anchor='center')
      self.no_match_frame.pack_propagate(0)
      self.text = tk.Label(self.no_match_frame, font=(18),text="Cannot find '{}'".format(self.str_to_find))
      self.text.pack(anchor='center')
      self.ok_button = tk.Button(self.no_match_frame, font=(14),text ="Ok",command=self.no_match_frame.destroy)
      return self.ok_button.pack(side='top')

  def display_index_location(self,event):
    current_position = self.text_field.index(tk.INSERT)
    insert_location = self.text_field.index('insert').split(".")
    self.row_column.config( text="Ln {} Col {} ".format(insert_location[0],insert_location[1]))
    self.match_locations = []
    return self.text_field.tag_delete('found')
  
  def replace_found_str(self,all=False):
    if self.match_locations == []:
      return self.find()
    if all:
      self.found_str_index = 0
      while (self.found_str_index + 1) != len(self.match_locations):
        current_string = self.match_locations[self.found_str_index]
        self.text_field.delete(current_string[0], current_string[1])
        self.text_field.insert(current_string[0], self.replace_txt.get("1.0",'end-1c'))
        self.match_locations = self.find()
    current_string = self.match_locations[self.found_str_index]
    self.text_field.delete(current_string[0], current_string[1])
    self.text_field.insert(current_string[0], self.replace_txt.get("1.0",'end-1c'))
    return self.match_locations
 
  def select_all(self):
    self.text_field.tag_add('sel', "1.0", 'end-1c')
    return self.text_field.mark_set('insert', "1.0")

  def time_date(self):
    time_now = datetime.now()
    date_string = time_now.strftime("%I:%M %p %d/%m/%Y")
    current_position = self.text_field.index(tk.INSERT)
    self.text_field.mark_set('insert',current_position)
    return self.text_field.insert('insert', date_string)

  def change_display(self,event):
    self.curr_widget = event.widget
  
  def change_font(self,font_change='current'):
    if self.curr_widget:
      selection = self.curr_widget.get(self.curr_widget.curselection())
      if selection.isdigit():
        self.font[1] = int(selection)
      elif selection[0].isupper():
        self.font[0] = selection
      elif selection[0].islower():
        self.font[2] = selection
      if font_change == 'current':
        return self.text_field.configure(font=(self.font[0],self.font[1],self.font[2])
      return self.example_text_label.configure(font=(self.font[0],self.font[1],self.font[2]))

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


    self.example_text_label = tk.Label(self.set_font_frame, height=5, width=20,highlightcolor="black",text="AaBbCcDdEe")
    self.example_text_label.configure(font=("Lucida Console", 8))
    self.example_text_label.pack(side='right')


    self.bottom_widget = tk.Frame(self.set_font_frame, height=5,width=100,background="green")
    self.bottom_widget.pack(side='left')

    self.cancel_b = tk.Button(self.bottom_widget,height=3,width=10, text ="Preview",command=lambda: self.change_font('preview'),padx=10)
    self.cancel_b.pack(side='right')
    self.save_b = tk.Button(self.bottom_widget,height=3,width=10, text ="Save",command=self.change_font,padx=10)
    self.save_b.pack(side='right')
    

    


    font_family = ['Modern', 'Roman', 'Script', 'Courier', 'MS Serif', 'MS Sans Serif', 
    'Small Fonts', 'Marlett', 'Arial',  'Calibri',  'Candara',  'Consolas', 'Constantia', 'Corbel', 'Courier New', 
    'Ebrima', 'Franklin Gothic Medium', 'Gabriola', 'Gadugi', 'Georgia',  'Times New Roman','Impact','Broadway', 
    'Castellar', 'Centaur', 'Century',  'Cooper Black', 'Dubai', 'Elephant', 'Forte', 'Franklin Gothic Book',
    'Lucida Sans', 'Magneto','Mistral', 'Onyx',  'Papyrus', 'Pristina', 'Ravie', 
    'Franklin Gothic Demi','Lucida Console']
    font_style = ['bold','normal','italic']
    font_size = [8,9,10,11,12,14,16,18,20,22,24,26,28,36,48,72]
    
    widget_array = [[self.font_widget,font_family],[self.style_widget,font_style],[self.size_widget,font_size]]
    self.listArray = [0,1,2]
    for i in range(len(widget_array)):
      print(i)
      self.scrollbar = tk.Scrollbar(widget_array[i][0])
      self.scrollbar.pack(side='right',fill='y')
      
      self.listArray[i] = tk.Listbox(widget_array[i][0],height=10,width=20, yscrollcommand = self.scrollbar.set )
      self.listArray[i].bind("<Button-1>",self.change_display)
      for line in widget_array[i][1]:
        self.listArray[i].insert('end',str(line))
        self.listArray[i].pack(side='right')
      self.scrollbar.config( command = self.listArray[i].yview )

  def zoom(self,command=None):
    if command == 'in':
      print('in')
    elif command == 'out':
      print('out')
    else:
      print('reset')
    return self.zoom_widget.pack_forget()
  
  def open_new_window(self):
    self.new_window = tk.Toplevel()
    self.top_menu = tk.Menu(self.new_window)
    self.new_window.config(menu=self.top_menu)
    self.new_window.title('Untitled - Notepad')
    
    self.file_menu = tk.Menu(self.top_menu,font = ( 12))
    self.edit_menu = tk.Menu(self.top_menu,font = ( 12))
    self.format_menu = tk.Menu(self.top_menu,font = ( 12))
    self.view_menu = tk.Menu(self.top_menu,font = ( 12))

    self.top_menu.add_cascade(label='File',menu=self.file_menu)
    self.top_menu.add_cascade(label='Edit',menu=self.edit_menu)
    self.top_menu.add_cascade(label='Format',menu=self.format_menu)
    self.top_menu.add_cascade(label='View',menu=self.view_menu)
    self.file_menu['tearoff'] = 0
    self.edit_menu['tearoff'] = 0
    self.format_menu['tearoff'] = 0
    self.view_menu['tearoff'] = 0
    
    self.scroll_y = tk.Scrollbar(self.new_window)
    self.scroll_x = tk.Scrollbar(self.new_window,orient='horizontal')

    self.bottom_widget = tk.Frame(self.new_window, height=20,width=250,background="grey")
    self.bottom_widget.pack(side='bottom',fill='both')
    self.utf_text = tk.Label(self.bottom_widget, width=15,text="UTF-8",background="white")
    self.utf_text.pack(side='right')
    self.crlf_text = tk.Label(self.bottom_widget,width=15 ,text="Windows (CRLF)",background="white")
    self.crlf_text.pack(side='right')

    self.text_field = tk.Text(self.new_window,undo=True,autoseparators=True,maxundo=-1,yscrollcommand=self.scroll_y.set,xscrollcommand=self.scroll_x.set,padx=5,pady=5)
    self.text_field.configure(font=("Lucida Console", 14))
    self.scroll_y.pack(side='right',fill='y')
    self.scroll_y.config(command=self.text_field.yview)
    self.scroll_x.pack(side='bottom',fill='x')
    self.scroll_x.config(command=self.text_field.xview)

    self.find_frame = tk.Frame(self.text_field, height=200, width=300,highlightthickness=1,highlightbackground="black")
    self.no_length = tk.Frame(self.text_field, height=300, width=350,highlightthickness=1,highlightbackground="black")

    self.row_column = tk.Label(self.bottom_widget,width=10, text="Ln {} Col {} ".format(0,0),background="white")
    self.row_column.pack(side='right')
   
    self.file_menu.add_command(label='New..       Ctrl+N',command=lambda: self.main_hub('new'))
    self.file_menu.add_command(label='New Window     Crtl+Shift+S',command=self.new_win)
    self.file_menu.add_command(label='Open...      Crtl+O',command=lambda: self.main_hub('saved'))
    self.file_menu.add_command(label='Save    Ctrl+S',command=self.save_file)
    self.file_menu.add_command(label='Save as    Crtl+Shift+S',command=self.save_as_file)
    self.file_menu.add_command(label='Exit',command=self.new_window.destroy)
    
    self.edit_menu.add_command(label='Undo             Ctrl+Z',command=self.text_field.edit_undo)
    self.edit_menu.add_command(label='Cut              Ctrl+X',command=self.cut)
    self.edit_menu.add_command(label='Copy             Ctrl+C',command=self.copy)
    self.edit_menu.add_command(label='Paste            Ctrl+V',command=self.paste)
    self.edit_menu.add_command(label='Delete           Del',command=lambda: self.text_field.delete("sel.first", "sel.last"))
    self.edit_menu.add_command(label='Find...          Ctrl+F',command=self.find_frame.pack)
    self.edit_menu.add_command(label='Find Next...      F3',command=self.find_next)
    self.edit_menu.add_command(label='Find Previous...  Shift+F3',command=lambda: self.find_next(True))
    self.edit_menu.add_command(label='Replace           Ctrl+H',command=self.replace_found_str)
    self.edit_menu.add_command(label='Select All        Ctrl+A',command=self.select_all)
    self.edit_menu.add_command(label='Time/Date         F5',command=self.time_date)

    self.format_menu.add_command(label='font..',command=self.set_font)
    
    self.view_menu.add_command(label='Zoom',command=lambda:  self.zoom_widget.pack(anchor='center'))
    self.zoom_widget = tk.Frame(self.text_field, height=200, width=280,highlightthickness=1,background='grey')
    self.zoom_in = tk.Button(self.zoom_widget, text = "Zoom In",command=lambda: self.zoom('in'))
    self.zoom_in.pack(anchor='n')
    self.zoom_out = tk.Button(self.zoom_widget, text = "Zoom Out",command=lambda: self.zoom('out'))
    self.zoom_out.pack(anchor='n')
    self.restore = tk.Button(self.zoom_widget, text = "Restore Default Zoom",command=self.zoom())
    self.restore.pack(anchor='n')
    
 
   
    
    self.zoom_widget.pack_propagate(0)
    self.zoom_widget.pack_forget()

    root.bind('<Control-x>',self.cut)
    self.text_field.bind("<Button-1>",self.display_index_location)
    
    
   
    self.text_field.pack(expand=True, fill='both')

    self.save_option_frame = tk.Frame(self.text_field, height=200, width=400,highlightthickness=1,background="white")
    self.save_option_frame.pack(anchor='center')
    self.save_option_frame.pack_propagate(0)

    self.save_option_top = tk.Frame(self.save_option_frame, height=20,width=250,background="white")
    self.save_option_top.pack(anchor='center',fill='both')
    self.find_text = tk.Label(self.save_option_top, text="Find",font=(16),background="white",padx=10)
    self.find_text.pack(side='left')
    self.save_option_x = tk.Button(self.save_option_top, text ="X",background="white")
    self.save_option_x.pack(side='right',fill='both')
    
    self.save_option_text = tk.Label(self.save_option_frame, text="Do you want to save changes to Untitled?",fg='#002266',font = (16),background="white",pady=30)
    self.save_option_text.pack(anchor='w')
    
    self.save_option_button = tk.Frame(self.save_option_frame, height=200,width=250,background="#ebebe0",pady=10,padx=5)
    self.save_option_button.pack(anchor='s',fill='both')
    self.save_option_cancel = tk.Button(self.save_option_button, text ="Cancel",command=self.save_option_frame.pack_forget,padx=10)
    self.save_option_cancel.pack(side='right')
    self.dontsave_button = tk.Button(self.save_option_button, text ="Don't Save",command=self.clear_text,padx=10)
    self.dontsave_button.pack(side='right')
    self.save_option_save = tk.Button(self.save_option_button, text ="Save",command=lambda: self.clear_text('save'),padx=10)
    self.save_option_save.pack(side='right')
    self.save_option_frame.pack_forget()

    self.find_frame.pack(anchor='center')
    self.find_frame.pack_propagate(0)
    self.white_widget = tk.Frame(self.find_frame, height=20,width=250,background='white')
    self.white_widget.pack(anchor='center',fill='x')
    self.find_frame_text = tk.Label(self.white_widget, text="Find",background='white')
    self.find_frame_text.pack(side='left')
    self.find_frame_x = tk.Button(self.white_widget, text ="X",background='white',command=self.find_next)
    self.find_frame_x.pack(side='right',fill='both')

    self.find_frame_content = tk.Frame(self.find_frame, height=120, width=220)
    self.find_frame_content.pack(side="left",fill='x')
    self.find_frame_content.pack_propagate(0)
    
    self.find_widget = tk.Frame(self.find_frame_content, highlightbackground="black")
    self.find_widget.pack(anchor='center',fill='x')
    self.find_what = tk.Label(self.find_widget, text="Find What:",background='white')
    self.find_what.pack(side='left')
    self.find_what_text = tk.Text(self.find_widget,height=1,width=140)
    self.find_what_text.pack(side='left')
    
    self.replace_widget = tk.Frame(self.find_frame_content, highlightbackground="black")
    self.replace_widget.pack(anchor='center',fill='x')
    self.replace = tk.Label(self.replace_widget, text="Replace: ",background='white')
    self.replace.pack(side='left')
    self.replace_txt = tk.Text(self.replace_widget,height=1,width=40)
    self.replace_txt.pack(side='left')

    self.direction = tk.Label(self.find_frame_content, text="Direction",font =(10))
    self.direction.pack(anchor='center')
    self.radio_variable=tk.IntVar()
    self.R1 = tk.Radiobutton(self.find_frame_content, text="Up", variable=self.radio_variable, value=1,command=lambda: self.change_find_direction(False) )
    self.R1.pack( anchor ='center' )
    self.R2 = tk.Radiobutton(self.find_frame_content, text="Down", variable=self.radio_variable, value=0,command=lambda: self.change_find_direction(True))
    self.R2.pack( anchor ='center' )

    self.find_frame_right = tk.Frame(self.find_frame, height=120, width=80)
    self.find_frame_right.pack(side="right")
    self.find_frame_right.pack_propagate(0)

    self.find_next_button = tk.Button(self.find_frame_right, text ="Find Next",command=self.find_next)
    self.find_next_button.pack(side='top')
    self.replace_button = tk.Button(self.find_frame_right, text ="Replace..",command=self.replace_found_str)
    self.replace_button.pack(side='top')
    self.replace_all_button = tk.Button(self.find_frame_right, text ="Replace All",command=lambda: self.replace_found_str(True))
    self.replace_all_button.pack(side="top")
    self.cancel_find_button = tk.Button(self.find_frame_right, text ="Cancel",command=self.find_frame.pack_forget)
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
    

    
    

    self.no_length.pack_forget()
    

    self.new_window.geometry('1000x500')
    
if __name__ == "__main__":
  root = tk.Tk()
  window_array = [] 
  my_notebook = Notebook()
  button_label = tk.Button(root, text='Open',font=(14),pady=10,padx=5)
  button_label.pack(anchor='n')
  window_array.append(my_notebook)
  my_notebook.open_new_window()
  if platform == 'win32':
    windll.shcore.SetProcessDpiAwareness(1)
  def create_window():
    new_notebook = Notebook()
    window_array.append(new_notebook)
    new_notebook.open_new_window()
  
  
  root.mainloop()


 