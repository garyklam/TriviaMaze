from maze import Maze
from MazeDrawer import Drawer
from question_database import SQLDatabase
from tkinter import Tk, Frame, Button, Label, Canvas, Text, Toplevel, Menu, LabelFrame, ttk, StringVar, OptionMenu
from tkinter.constants import E, W, N
import pickle
import time
import pygame
import random
from functools import partial


class MazeGUI:
    def __init__(self):
        self.maze = Maze(4, 4)
        self.root = Tk()
        self.gamescreen = Frame(self.root)
        self.startmenu = Frame(self.root)
        self.db = None
        self.display = None
        self.drawer = None
        self.start_time = None
        self.root.resizable(False, False)
        self.root.title("TriviaMaze")
        self.start_menu_init()
        self.startmenu.grid(row=0, column=0)
        self.gamescreen.grid_forget()
        pygame.init()
        pygame.mixer.init()
        self.root.mainloop()

    """Start menu"""
    def start_menu_init(self):
        """Builds the start menu for the game. Has a button to start a new game, continue game, display instructions and
         exit the program. Under the new game button there are options for different game difficulties, with easy as the
         default selection."""
        self.startmenu.grid(row=0, column=0)
        menu_spacer = Frame(self.startmenu, height=80, width=600)
        menu_spacer.grid(row=0, column=0, columnspan=3)
        menu_spacer2 = Frame(self.startmenu, height=420, width=100)
        menu_spacer2.grid(row=2, column=1)
        menu_spacer3 = Frame(menu_spacer2)
        menu_spacer3.grid(row=4, column=1)
        title = Label(self.startmenu, text="504 TriviaMaze", font="Times 40", pady=50)
        title.grid(row=1, column=0, columnspan=4)
        new_game_button = Button(menu_spacer2, text="New Game", font="Times 20",
                                 command=lambda: self.display_new_game_menu())
        new_game_button.grid(row=3, column=1, sticky=W)
        continue_game_button = Button(menu_spacer2, text="Continue Game", font="Times 20",
                                      command=self.display_load_menu)
        continue_game_button.grid(row=6, column=1, columnspan=2, sticky=W)
        instructions_button = Button(menu_spacer2, text="Instructions", font="Times 20",
                                     command=self.display_instructions)
        instructions_button.grid(row=7, column=1, columnspan=2, sticky=W)
        exit_button = Button(menu_spacer2, text="Exit", font="Times 20", command=self.root.destroy)
        exit_button.grid(row=8, column=1, columnspan=2, sticky=W)

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
                             command=lambda: self.screen_switch(instruct_frame, self.startmenu))
        back_button.grid(row=1, column=0)

    def display_new_game_menu(self):
        """Creates and displays the new game menu, allowing the player to choose question difficulty, maze size, and
        trivia category. The default options are easy, 4x4 and no specific category."""
        def set_difficulty(difficulty):
            buttons = {"Easy": easy_button, "Medium": medium_button, "Hard": hard_button}
            for button in buttons.values():
                button['relief'] = 'raised'
            buttons[difficulty]['relief'] = 'sunken'
            maze.set_difficulty(difficulty.lower())

        def set_category(chosen_category, possible_categories):
            """Ensures a valid category is chosen"""
            if chosen_category in possible_categories:
                maze.set_category(chosen_category)
            else:
                invalid_selection = Label(new_game_menu, text="The selected category is invalid, please choose a "
                                                              "different category.", font='Times 16', pady=5)
                invalid_selection.grid(row=5, column=0, columnspan=4)

        new_game_menu = Toplevel(self.root)
        maze = self.maze
        instruction_text = "Please select a category from the provided list.\nChoosing a specific category will reduce " \
                           "the number of\navailable questions and increase the change of repeat questions.\n Selecting" \
                           " no category will pull from all possible categories."
        selection_instruction = Label(new_game_menu, text=instruction_text, font="Times 14", pady=10)
        selection_instruction.grid(row=0, column=0, columnspan=3)

        difficulty_frame = Frame(new_game_menu)
        difficulty_frame.grid(row=1, column=0, columnspan=3)
        difficulty_label = Label(difficulty_frame, text="Question difficulty: ", font="Times 16", pady=15)
        difficulty_label.grid(row=1, column=0)
        hard_button = Button(difficulty_frame, text="Hard", padx=5, font="Times 12",
                             command=lambda: set_difficulty("Hard"))
        hard_button.grid(row=1, column=4)
        medium_button = Button(difficulty_frame, text="Medium", padx=5, font="Times 12",
                               command=lambda: set_difficulty("Medium"))
        medium_button.grid(row=1, column=3)
        easy_button = Button(difficulty_frame, text="Easy", padx=5, font="Times 12",
                             command=lambda: set_difficulty("Easy"))
        easy_button.grid(row=1, column=2)
        set_difficulty("Easy")

        dimension_frame = Frame(new_game_menu)
        dimension_frame.grid(row=2, column=0, columnspan=3)
        dimension_choices = range(3, 11)
        row_label = Label(dimension_frame, text="Row: ", font="Times 16", pady=15)
        row_label.grid(row=2, column=0, sticky=W)
        row_choice = StringVar()
        row_choice.set(4)
        row_select = OptionMenu(dimension_frame, row_choice, *dimension_choices)
        row_select.grid(row=2, column=1)
        col_label = Label(dimension_frame, text="Col: ", font="Times 16")
        col_label.grid(row=2, column=2, sticky=W)
        col_choice = StringVar()
        col_choice.set(4)
        col_select = OptionMenu(dimension_frame, col_choice, *dimension_choices)
        col_select.grid(row=2, column=3)

        db = SQLDatabase()
        category_list = db.request_category_list()
        category_frame = Frame(new_game_menu)
        category_frame.grid(row=3, column=0, columnspan=3)
        category_label = Label(category_frame, text="Category: ", font="Times 16", pady=15).grid(row=3, column=0)
        c = StringVar()
        category_box = ttk.Combobox(category_frame, justify='left', textvariable=c, font='Times 16')
        categories = []
        for key in category_list.keys():
            categories.append(key)
        category_box['values'] = categories
        category_box.grid(row=3, column=1)

        button_frame = Frame(new_game_menu)
        button_frame.grid(row=4, column=1)
        submit = Button(button_frame, text='Start', font='Times 20',
                        command=lambda: [set_category(c.get(), categories),
                                         self.maze.resize_maze(int(row_choice.get()), int(col_choice.get())),
                                         self.start_game(new_game=True),
                                         new_game_menu.destroy()])
        submit.grid(row=4, column=0)
        back_button = Button(button_frame, text='Back', font='Times 20', command=lambda: new_game_menu.destroy())
        back_button.grid(row=4, column=1)

    def prompt(self, savefile, type):
        """Creates a text prompt in the text display of the game screen asking the player to confirm their save/load.
        Prompt message depend on whether the player wishes to save or load. Upon confirming their action the save or
        load is initiated with the indicated save file.
        savefile: name of the save file as a string
        type: type of request, either 'save' or 'load'
        """
        self.clear_text_display()
        if type == "save":
            confirm_text = "Any existing data in this save file will be written over." \
                           "\nAre you sure you wish to continue?"
            ok_button = Button(self.text_display, text="Yes", font='Times 20', command=lambda: self.save_game(savefile))
        else:
            confirm_text = "Any unsaved progress will be lost when loading a save file.\n " \
                           "Are you sure you wish to continue?"
            ok_button = Button(self.text_display, text="Yes", font='Times 20',
                               command=lambda: self.load_game(savefile))
        ok_button.grid(row=1, column=2)
        warning_text = Label(self.text_display, font="Times 18", padx=10, pady=10, text=confirm_text)
        warning_text.grid(row=0, column=1, columnspan=4)
        back_button = Button(self.text_display, text="No", font='Times 20', command=lambda: self.clear_text_display())
        back_button.grid(row=1, column=3)

    def load_game(self, savefile, event=None, load_menu=None):
        """Attempts to open the indicated save file. If it is not found and the load request came from the load menu,
        nothing happens, if the load request came from in game, displays an error message in the text display before
        returning. If the file is found, the maze is set equal to the save file data, the existing display is switched,
        the game restarts with the new maze.
        savefile: name of the save file as a string
        load_menu: load menu frame, used to indicate if the load request came from the load menu or in game,
        default is None
        """
        print(f'loading {savefile}')
        try:
            loadhandle = open(savefile+'.pkl', 'rb')
        except FileNotFoundError:
            if load_menu:
                return
            else:
                self.clear_text_display()
                no_file_found_text = "No save file could be found for this save slot."
                no_file = Label(self.text_display, text=no_file_found_text, font='Times 20', padx=30, pady=40)
                no_file.grid(row=0, column=0)
                continue_button = Button(self.text_display, text='Continue', font='Times 20',
                                         command=self.clear_text_display)
                continue_button.grid(row=1, column=0)
                return
        load_tone = pygame.mixer.Sound('sfx/load_tone.wav')
        pygame.mixer.Sound.play(load_tone)
        mazedata = pickle.load(loadhandle)
        loadhandle.close()
        self.maze = mazedata
        if not load_menu:
            self.display.destroy()
        else:
            load_menu.destroy()
            self.screen_switch(self.startmenu, self.gamescreen)
        self.start_game()
        self.check_end_game()

    def save_game(self, savefile):
        """
        Sets the time elapsed field for the maze and saves the current maze to the indicated save file. Displays a
        message in the text display to tell the player that the save was completed.
        savefile: name of the save file as a string
        """
        self.maze.set_time_elapsed(self.start_time, int(time.time()))
        self.start_time = int(time.time())
        savehandle = open(savefile+'.pkl', 'wb')
        pickle.dump(self.maze, savehandle)
        savehandle.close()
        self.clear_text_display()
        confirmation = Label(self.text_display, font="Times 18", pady=10, padx=120, text="Successfully saved", )
        confirmation.grid(row=0, column=0)
        back_button = Button(self.text_display, text="Continue", font='Times 18', command=self.clear_text_display)
        back_button.grid(row=1, column=0)
        save_tone = pygame.mixer.Sound('sfx/save_tone.wav')
        pygame.mixer.Sound.play(save_tone)

    def display_load_menu(self):
        """
        Builds a load menu that displays the three save slots. Loads the save information if the save file exists and
        uses different maze methods/fields to obtain information about the save such as the maze size, player location,
        trivia category, trivia difficulty, and time spent in game and displays this info.
        """
        saves = Frame(self.root, height=650, width=650, bg='SystemButtonFace')
        saves.grid(row=0, column=0)
        save = []
        load_instruct = "Loading will take a few seconds, and can be inconsistent.\n" \
                        "Wait a moment before clicking a save file again or exit the load menu and try again."
        instruct = Label(saves, text=load_instruct, font='Times 12', pady=10)
        instruct.grid(row=0, column=0)
        for i in range(1, 4):
            savelabel = LabelFrame(saves, height=175, width=550, text=f'Save {i}', cursor='hand1', font='Times 16')
            savelabel.grid(row=i, column=0, sticky=E)
            savelabel.grid_propagate(0)
            try:
                loadhandle = open(f'save_file_{i}.pkl', 'rb')
                maze = pickle.load(loadhandle)
                info = [f'Rows: {maze.get_size()[0]}', f'Columns: {maze.get_size()[1]}',
                        f'Difficulty: {maze.difficulty}', f'Category: {maze.category}',
                        f'Position: {maze.player_location}', f'Time: {maze.get_time()}']
                for j in range(len(info)):
                    label = Label(savelabel, text=info[j], font='Times 14', anchor=W, padx=5, pady=10)
                    label.grid(row=j % 2, column=j // 2, sticky=W)
                loadhandle.close()
                save_file = "save_file_" + str(i)
                savelabel.bind('<Button-1>', partial(self.load_game, save_file, load_menu=saves))
            except FileNotFoundError:
                continue
            save.append(savelabel)
        back_button = Button(saves, text="Back", font='Times 20', anchor=N,
                             command=lambda: self.screen_switch(saves, self.startmenu))
        back_button.grid(row=4, column=0)

    def start_game(self, new_game=False):
        """Builds game screen and database of questions, switches to game screen, saves the current time for use in
        tracking the play time.
        new_game: boolean indicating if the game is being loaded from a save file or if it is a new game
        """
        if new_game:
            self.maze.construct()
            self.screen_switch(self.startmenu, self.gamescreen)
        for item in self.gamescreen.winfo_children():
            item.destroy()
        self._menu_init()
        self._movement_interface_init()
        size = self.maze.get_size()
        self.display = Canvas(self.gamescreen, height=size[0] * 100, width=size[1] * 100, bg="gray")
        self.drawer = Drawer(self.maze, self.display)
        self.drawer.draw()
        self.display.grid(row=0, column=0, columnspan=4)
        self.db = SQLDatabase(self.maze.category, self.maze.difficulty, self.maze.get_total_doors())
        self.db.build_database()
        self.start_time = int(time.time())

    def screen_switch(self, curr_frame, new_frame):
        """Switches the main display from the current frame to the desired frame.
        curr_frame: current frame that is being displayed
        new_frame: the desired frame
        """
        curr_frame.grid_forget()
        new_frame.grid(row=0, column=0)

    """Game Screen"""
    def _menu_init(self):
        """Creates the menubar consisting of options for loading a game, saving the current game, getting instructions,
        or exiting the game."""
        def confirm_exit(root):
            """Creates a popup that makes sure the user wishes to exit the program."""
            def close():
                root.destroy()

            def back():
                warning.destroy()

            warning = Toplevel()
            warning_text = Label(warning, font="Times 20", pady=10, text="Are you sure you wish to exit? \n"
                                                                         "Any unsaved progress will not be kept.")
            warning_text.grid(row=0, column=0, columnspan=4)
            ok_button = Button(warning, text="Ok", font='Times 16', command=close).grid(row=1, column=1)
            back_button = Button(warning, text="Back", font='Times 16', command=back).grid(row=1, column=2)

        def display_help():
            """Prints out the instruction text from the in the text display."""
            instruction_file = open("triviamaze_instructions.txt", 'r')
            instruction_text = instruction_file.read()
            instruction_file.close()
            help_window = Toplevel()
            help_label = Label(help_window, text=instruction_text, font='Times 14')
            help_label.grid(row=0, column=0)

        menubar = Menu(self.root)
        menubar.add_command(label="Help", command=display_help)
        savemenu = Menu(menubar, tearoff=0)
        savemenu.add_command(label="Save 1", command=lambda: self.prompt("save_file_1", "save"))
        savemenu.add_command(label="Save 2", command=lambda: self.prompt("save_file_2", "save"))
        savemenu.add_command(label="Save 3", command=lambda: self.prompt("save_file_3", "save"))
        menubar.add_cascade(label="Save", menu=savemenu)
        loadmenu = Menu(menubar, tearoff=0)
        loadmenu.add_command(label="Load 1", command=lambda: self.prompt("save_file_1", "load"))
        loadmenu.add_command(label="Load 2", command=lambda: self.prompt("save_file_2", "load"))
        loadmenu.add_command(label="Load 3", command=lambda: self.prompt("save_file_3", "load"))
        menubar.add_cascade(label="Load", menu=loadmenu)
        menubar.add_command(label="Exit", command=lambda: confirm_exit(self.root))
        self.root.config(menu=menubar)

    def _movement_interface_init(self):
        """Creates the interface allowing player movement, binds arrow keys to different movements."""
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
        self.gamescreen.bind('<Left>', partial(self.arrowKey, "west"))
        self.gamescreen.bind('<Right>', partial(self.arrowKey, "east"))
        self.gamescreen.bind('<Up>', partial(self.arrowKey, "north"))
        self.gamescreen.bind('<Down>', partial(self.arrowKey, "south"))
        self.gamescreen.focus_set()

    def arrowKey(self, direction, event=None):
        if self.maze.check_direction(self.maze.player_location[0], self.maze.player_location[1], direction):
            self.display_question(direction)
        else:
            pass

    def _set_move_button_state(self):
        """Sets the state of the movement buttons depending on if the adjacent rooms can be reached from the current
        room or not."""
        row, col = self.maze.player_location[0], self.maze.player_location[1]
        directions = ["north", "south", "east", "west"]
        buttons = [self.north, self.south, self.east, self.west]
        for i in range(4):
            if self.maze.check_direction(row, col, directions[i]):
                buttons[i]['state'] = "normal"
            else:
                buttons[i]['state'] = "disabled"

    def _move_player(self, direction, event=None, correct=True):
        """Moves the player if correct. If incorrect, then the corresponding door is locked. In both cases the game
        display is redrawn, the movement buttons are reset and any text that is in the text display is deleted.
        direction: string representing the direction the player is moving
        correct: boolean indicating if the player correctly answered the trivia question"""
        if correct:
            self.maze.move_player(direction)
            walk_sound = pygame.mixer.Sound('sfx/walk.wav')
            pygame.mixer.Sound.play(walk_sound)
        else:
            self.maze.lock_door(direction)
            door_lock_sound = pygame.mixer.Sound('sfx/door_lock.wav')
            pygame.mixer.Sound.play(door_lock_sound)
        self.drawer.draw()
        self._set_move_button_state()
        self.clear_text_display()
        self.check_end_game()

    def check_end_game(self):
        """Checks if either player wins or maze is no longer completable. If either condition is met, the corresponding
        end game screen is displayed and options for exiting and replaying are offered."""
        def close(window):
            window.destroy()

        if self.maze.player_wins():
            text = Label(self.text_display, text=f'Congrats, you have won the game!', font="Times 26", padx=20, pady=10)
            game_win_sound = pygame.mixer.Sound('sfx/game_win.wav')
            pygame.mixer.Sound.play(game_win_sound)
        elif not self.maze.is_completable():
            text = Label(self.text_display, text=f'Game Over\nYou can no longer reach the exit.', font="Times 26",
                         padx=20)
            game_lose_sound = pygame.mixer.Sound('sfx/game_lose.wav')
            pygame.mixer.Sound.play(game_lose_sound)
        else:
            return
        text.grid(row=0, column=0, columnspan=4)
        replay_button = Button(self.text_display, text="Replay", font="Times 20",
                               command=lambda: [self.start_menu_init(),
                                                self.screen_switch(self.gamescreen, self.startmenu)])
        replay_button.grid(row=1, column=1)
        exit_button = Button(self.text_display, text="Exit", font="Times 20", command=lambda: close(self.root))
        exit_button.grid(row=1, column=2)

    def display_question(self, direction):
        """If a question is currently being displayed, pass. If the room that the player is moving too has already been
        visited, then move the player. Otherwise, pull a question from the database, and display it in the text display.
        direction: string representing the direction that the player is attempting to move in
        """
        def highlight_selection(i, event=None):
            answer_list[i]['bg'] = 'gray'

        def unhighlight_selection(i, event=None):
            answer_list[i]['bg'] = 'SystemButtonFace'

        if self.text_display.winfo_children():
            return
        destination = self.maze.find_destination(self.maze.player_location[0], self.maze.player_location[1], direction)
        if destination in self.maze.visited_rooms:
            self.maze.move_player(direction)
            self.drawer.draw()
            self._set_move_button_state()
            walk_short_sound = pygame.mixer.Sound('sfx/walk_short.wav')
            pygame.mixer.Sound.play(walk_short_sound)
        else:
            question = self.db.get_random_question()
            question_text = Label(self.text_display, text=f'{question[1]}', font="Times 16",
                                  justify="left", wraplength=600, anchor=W, width=600)
            question_text.grid(row=0, column=0)
            answer_list = []
            answer_count = len(question)
            positions = [*range(1, answer_count + 1)]
            random.shuffle(positions)
            for i in range(2, answer_count):
                if not question[i]:
                    return
                answer = Label(self.text_display, text=f'\t{question[i]}', font="Times 14", anchor=W)
                answer.grid(row=positions.pop() + 1, column=0, sticky=E + W)
                answer.bind('<Enter>', partial(highlight_selection, i - 2))
                answer.bind('<Leave>', partial(unhighlight_selection, i - 2))
                answer.bind('<Button-1>', partial(self._move_player, direction, correct=(i == 2)))
                answer_list.append(answer)

    def clear_text_display(self):
        """Clears items in the text display."""
        for item in self.text_display.winfo_children():
            item.destroy()


if __name__ == '__main__':
    game = MazeGUI()
