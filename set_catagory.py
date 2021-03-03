from tkinter import *
from tkinter import Tk, Frame, Button, Label, Canvas, Text, Toplevel, Menu, LabelFrame

import bind as bind

from question_database import *
# create a root window.


root = Tk()



# create listbox object
listbox = Listbox(root, height = 50,
                  width = 35,
                  bg = "grey",
                  activestyle = 'dotbox',
                  font = "Helvetica",
                  fg = "yellow")
# Define the size of the window.
root.geometry("350x300")
# Adding Listbox to the left
# side of root window
listbox.pack(side = LEFT, fill = BOTH)

# Creating a Scrollbar and
# attaching it to root window
scrollbar = Scrollbar(root)

# Adding Scrollbar to the right
# side of root window
scrollbar.pack(side=RIGHT, fill=BOTH)

# Define a label for the list.
label = Label(root, text="Catagory")




# insert elements by their
# index and names.
listbox.insert(1, "General Knowledge")
listbox.insert(2, "Entertainment:Books")
listbox.insert(3, "Entertainment:Film")
listbox.insert(4, "Entertainment:Music")
listbox.insert(5, "Entertainment:Musicals & Theatres")
listbox.insert(6, "Entertainment:Television")
listbox.insert(7, "Entertainment:Video Games")
listbox.insert(8, "Entertainment:Board Games")
listbox.insert(9, "Science & nature")
listbox.insert(10, "Science:Computers")
listbox.insert(11, "Science:Mathematics")
listbox.insert(12, "Mythology")
listbox.insert(13, "Sports")
listbox.insert(14, "Geography")
listbox.insert(15, "History")
listbox.insert(16, "Politics")
listbox.insert(17, "Art")
listbox.insert(18, "Celebrities")
listbox.insert(19, "Animals")
listbox.insert(20, "vehicles")
listbox.insert(21, "Entertainment:Comics")
listbox.insert(22, "Science:Gadgets")
listbox.insert(23, "Entertainment:Japanese Anime & Manga")
listbox.insert(24, "Entertainment:Cartoon & Animations")
# Attaching Listbox to Scrollbar
# Since we need to have a vertical
# scroll we use yscrollcommand
listbox.config(yscrollcommand=scrollbar.set)

# setting scrollbar command parameter
# to listbox.yview method its yview because
# we need to have a vertical view
scrollbar.config(command=listbox.yview)

root.mainloop()




