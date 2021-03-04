from question_database import SQLDatabase
from tkinter import Tk, Frame, Button, ttk, StringVar
import time


def print_out_selection(text, categories):
    if text in categories:
        print(text)
    # maze.set_category(text)


def add_time(start):
    curr = int(time.time())
    diff = curr - start
    hours = diff//3600
    minutes = (diff-hours*3600)//60
    seconds = (diff-hours*3600-minutes*60)
    elapsed = f'{str(hours).zfill(2)}:{str(minutes).zfill(2)}:{str(seconds).zfill(2)}'
    print(elapsed)


time_spent = 0
category_list = SQLDatabase.get_category_list()
root = Tk()
gamescreen = Frame(root, height=400, width=800)
gamescreen.grid()
gamescreen.grid_propagate(0)
n = StringVar()
category_box = ttk.Combobox(gamescreen, width=40, justify='left', textvariable=n, font='Times 20')
categories = []
for key in category_list.keys():
    categories.append(key)
category_box['values'] = categories
category_box.grid(row=0, column=0)
submit = Button(gamescreen, text='Select', font='Times 20', command=lambda: print_out_selection(n.get(), categories))
submit.grid(row=1, column=0)
start = int(time.time())
timer_button = Button(gamescreen, text='Add Time', command=lambda: add_time(start))
timer_button.grid(row=2, column=0)

root.mainloop()
