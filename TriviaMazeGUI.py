from maze import Maze
from MazeDrawer import Drawer
from question_database import SQLDatabase
from tkinter import Tk, Frame, Button, Label, Canvas, Text, Toplevel, Menu
from tkinter.constants import END, W
import sqlite3
import html


class MazeGUI:
    def __init__(self):
        self.maze = Maze(4, 4)
        self.root = Tk()
        self.gamescreen = Frame(self.root)
        self.startmenu = Frame(self.root)
        self.db = None
        self.display = None
        self.drawer = None
        self.stats = None
        self.root.resizable(False, False)
        self.root.title("TriviaMaze")
        self.start_menu_init()
        self.startmenu.grid(row=0, column=0)
        self.gamescreen.grid_forget()
        self.root.mainloop()

    """Start menu"""
    def start_menu_init(self):
        """Builds the start menu for the game. Has a button to start a new game, display instructions and exit the
        program."""
        def set_difficulty(difficulty):
            if difficulty == "Hard":
                maze.resize_dungeon(8, 8)
                maze.set_difficulty("hard")
                easy_button["relief"] = "raised"
                medium_button["relief"] = "raised"
                hard_button["relief"] = "sunken"
            elif difficulty == "Medium":
                maze.resize_dungeon(6, 6)
                maze.set_difficulty("medium")
                easy_button["relief"] = "raised"
                medium_button["relief"] = "sunken"
                hard_button["relief"] = "raised"
            elif difficulty == "Easy":
                maze.resize_dungeon(4, 4)
                maze.set_difficulty("easy")
                easy_button["relief"] = "sunken"
                medium_button["relief"] = "raised"
                hard_button["relief"] = "raised"
            else:
                pass

        maze = self.maze
        self.startmenu.grid(row=0, column=0)
        menu_spacer = Frame(self.startmenu, height=100, width=600)
        menu_spacer.grid(row=0, column=0, columnspan=3)
        menu_spacer2 = Frame(self.startmenu, height=400, width=100)
        menu_spacer2.grid(row=2, column=1)
        menu_spacer3 = Frame(menu_spacer2)
        menu_spacer3.grid(row=4, column=1)
        title = Label(self.startmenu, text="504 TriviaMaze", font="Times 40", pady=50)
        title.grid(row=1, column=0, columnspan=4)
        new_game_button = Button(menu_spacer2, text="New Game", font="Times 20",
                                 command= self.start_game)
        new_game_button.grid(row=3, column=1, sticky=W)
        hard_button = Button(menu_spacer3, text="Hard", font="Times 12", command=lambda: set_difficulty("Hard"))
        hard_button.grid(row=0, column=0, sticky=W)
        medium_button = Button(menu_spacer3, text="Medium", font="Times 12",
                               command=lambda: set_difficulty("Medium"))
        medium_button.grid(row=1, column=0, sticky=W)
        easy_button = Button(menu_spacer3, text="Easy", font="Times 12", relief="sunken",
                             command=lambda: set_difficulty("Easy"))
        easy_button.grid(row=2, column=0, sticky=W)
        continue_game_button = Button(menu_spacer2, text="Continue Game", font="Times 20",
                                      command=self.load_game())
        continue_game_button.grid(row=5, column=1, columnspan=2, sticky=W)
        instructions_button = Button(menu_spacer2, text="Instructions", font="Times 20",
                                     command=self.display_instructions)
        instructions_button.grid(row=6, column=1, columnspan=2, sticky=W)
        exit_button = Button(menu_spacer2, text="Exit", font="Times 20", command=self.root.destroy)
        exit_button.grid(row=7, column=1, columnspan=2, sticky=W)

    def display_instructions(self):
        """Displays basic instructions for the game. Hides the start menu and replaces it with a screen containing
        text from a separate text file. Creates a button that will return the user to the start menu."""
        self.startmenu.grid_forget()
        instruction_file = open("triviamaze_instructions.txt", 'r')
        instruction_text = instruction_file.read()
        instruct_frame = Frame(self.root, height=600, width=600)
        instruct_frame.grid(row=0, column=0)
        t = Text(instruct_frame, wrap="word", font="Times 16")
        t.grid(row=0, column=0)
        t.insert("1.0", instruction_text)
        instruction_file.close()
        back_button = Button(instruct_frame, text="Back", font="Times 20",
                             command=lambda: self.screen_switch(instruct_frame, self.startmenu)).grid(row=1, column=0)

    def load_game(self):
        """Set maze fields to the save state, self.start_game"""
        pass

    def start_game(self):
        self.game_display_init()
        db = SQLDatabase(self.maze.category, self.maze.difficulty, self.maze.get_total_rooms())
        db.build_database()
        self.db = sqlite3.connect('trivia_maze_questions.db')
        self.screen_switch(self.startmenu, self.gamescreen)

    def screen_switch(self, curr_frame, new_frame):
        curr_frame.grid_forget()
        new_frame.grid(row=0, column=0)

    """Game Screen"""
    def game_display_init(self):
        self.maze.construct()
        self._menu_init()
        self._movement_interface_init()
        size = self.maze.get_size()
        self.display = Canvas(self.gamescreen, height=size[0]*100, width=size[1]*100, bg="white")
        self.drawer = Drawer(self.maze, self.display)
        self.drawer.draw()
        self.display.grid(row=0, column=0, columnspan=4)
        self.stats = {"Rooms explored": 0,
                      "Rooms traversed": 0,
                      "Damage taken": 0,
                      "Pits fell in": 0,
                      "Health healed": 0,
                      "Healing potions found": 0,
                      "Vision potions found": 0,
                      "Vision potions used": 0}

    def _menu_init(self):
        """Creates the menu bar and contains the methods that the menu options call. Includes the entire map display
        button if the adventurer name is either "Tom" or "Kevin"."""

        def confirm_exit(root):
            """Creates a popup that makes sure the user wishes to exit the program."""

            def close():
                root.destroy()

            def back():
                warning.destroy()

            warning = Toplevel()
            warning_text = Label(warning, font="Times 16", pady=10, text="Are you sure you wish to exit? \n"
                                                                         "Progress in the dungeon will not be saved")
            warning_text.grid(row=0, column=0, columnspan=4)
            ok_button = Button(warning, text="Ok", command=close).grid(row=1, column=1)
            back_button = Button(warning, text="Back", command=back).grid(row=1, column=2)

        def display_help():
            """Prints out the instruction text from the in the text display."""
            pass

        def save():
            pass

        def load():
            pass

        menubar = Menu(self.root)
        menubar.add_command(label="Help", command=display_help())
        menubar.add_command(label="Save", command=lambda: save())
        menubar.add_command(label="Load", command=lambda: load())
        menubar.add_command(label="Exit", command=lambda: confirm_exit(self.root))
        self.root.config(menu=menubar)

    def _movement_interface_init(self):
        """Creates the interface containing player actions, including movement, using potions and displaying player
        info."""
        self.text_display = Frame(self.gamescreen, height=200, width=600, borderwidth=1)
        self.text_display.grid_propagate(0)
        self.text_display.grid(row=1, column=0)
        movementframe = Frame(self.gamescreen)
        self.north = Button(movementframe, text="North", command=lambda: self.display_question("north"), pady=5)
        self.north.grid(row=1, column=2, columnspan=2)
        self.south = Button(movementframe, text="South", command=lambda: self.display_question("south"), pady=5)
        self.south.grid(row=3, column=2, columnspan=2)
        self.east = Button(movementframe, text="East", command=lambda: self.display_question("east"), pady=5)
        self.east.grid(row=2, column=4)
        self.west = Button(movementframe, text="West", command=lambda: self.display_question("west"), pady=5)
        self.west.grid(row=2, column=1)
        movementframe.grid(row=1, column=1)
        self._set_move_button_state()
        self.gamescreen.bind('<Left>', self.leftKey)
        self.gamescreen.bind('<Right>', self.rightKey)
        self.gamescreen.bind('<Up>', self.upKey)
        self.gamescreen.bind('<Down>', self.downKey)
        self.gamescreen.focus_set()

    def leftKey(self, event):
        if self.maze.check_west(self.maze.player_location[0], self.maze.player_location[1]):
            self.display_question("west")
        else:
            pass

    def rightKey(self, event):
        if self.maze.check_east(self.maze.player_location[0], self.maze.player_location[1]):
            self.display_question("east")
        else:
            pass

    def upKey(self, event):
        if self.maze.check_north(self.maze.player_location[0], self.maze.player_location[1]):
            self.display_question("north")
        else:
            pass

    def downKey(self, event):
        if self.maze.check_south(self.maze.player_location[0], self.maze.player_location[1]):
            self.display_question("south")
        else:
            pass

    def _set_move_button_state(self):
        """Sets the state of the movement buttons depending on if the adjacent rooms can be reached from the current
        room or not."""
        row, col = self.maze.player_location[0], self.maze.player_location[1]
        if self.maze.check_north(row, col):
            self.north["state"] = "normal"
        else:
            self.north["state"] = "disabled"
        if self.maze.check_south(row, col):
            self.south["state"] = "normal"
        else:
            self.south["state"] = "disabled"
        if self.maze.check_east(row, col):
            self.east["state"] = "normal"
        else:
            self.east["state"] = "disabled"
        if self.maze.check_west(row, col):
            self.west["state"] = "normal"
        else:
            self.west["state"] = "disabled"

    def _move_player(self, event, direction, correct=True):
        """Changes the adventurer's location depending on the passed in direction. Conducts the room check then
        changes the drawer's location and redraws the game display. Then resets the move buttons."""

        if correct:
            self.stats["Rooms traversed"] += 1
            self.maze.move_player(direction)
            self.maze.visited_rooms.append(self.maze.player_location)
            print(f'{self.maze.visited_rooms}')
        else:
            self.maze.lock_door(direction)
        self.drawer.draw()
        self._set_move_button_state()
        for item in self.text_display.winfo_children():
            item.destroy()

    def display_question(self, direction):
        destination = self.maze.player_location
        if direction == "north":
            destination = [destination[0]-1, destination[1]]
        elif direction == "south":
            destination = [destination[0] + 1, destination[1]]
        elif direction == "east":
            destination = [destination[0], destination[1] + 1]
        elif direction == "west":
            destination = [destination[0], destination[1] - 1]
        if destination in self.maze.visited_rooms:
            print(f'destination:{destination}\nin:{self.maze.visited_rooms}')
            self._move_player(direction)
        else:
            c = self.db.cursor()
            c.execute("SELECT * FROM questions ORDER BY RANDOM() LIMIT 1;")
            question = c.fetchone()
            question_text = Label(self.text_display, text=f'{html.unescape(question[1])}', font="Times 16", wraplength=600)
            question_text.grid(row=0, column=0)
            correct_answer = Label(self.text_display, text=f'\t{html.unescape(question[2])}', font="Times 14")
            correct_answer.bind('<Button-1>', lambda event: self._move_player(event, direction))
            correct_answer.grid(row=1, column=0, sticky=W)
            incorrect1 = Label(self.text_display, text=f'\t{html.unescape(question[3])}', font="Times 14")
            incorrect1.bind('<Button-1>', lambda event: self._move_player(event, direction, correct=False))
            incorrect1.grid(row=2, column=0, sticky=W)
            if question[0] == "multiple":
                incorrect2 = Label(self.text_display, text=f'\t{html.unescape(question[4])}', font="Times 14")
                incorrect2.bind('<Button-1>', lambda event: self._move_player(event, direction, correct=False))
                incorrect2.grid(row=3, column=0, sticky=W)
                incorrect3 = Label(self.text_display, text=f'\t{html.unescape(question[5])}', font="Times 14")
                incorrect3.bind('<Button-1>', lambda event: self._move_player(event, direction, correct=False))
                incorrect3.grid(row=4, column=0, sticky=W)




if __name__ == '__main__':
    game = MazeGUI()

