import tkinter


class Drawer:
    """Contains methods to create map objects for the adventure game."""
    def __init__(self, maze, canvas):
        self.maze = maze
        self.rows = self.maze.rows
        self.cols = self.maze.cols
        self.room_unit = 100
        self.canvas = canvas
        self.player_image = tkinter.PhotoImage(file='player.gif')
        self.exit_image = tkinter.PhotoImage(file='exit.gif')

    def draw(self):
        """Draws all of the rooms in the dungeon along with their contents. Draws walls in a separate loop from the
        doors to avoid overlapping lines causing doors to be obscoured in the map. Returns the canvas object after
        drawing all features."""
        self.canvas.delete("all")
        for row in self.maze.grid:
            for room in row:
                self.draw_walls(room)
        for row in self.maze.grid:
            for room in row:
                self.draw_door(room)
        self.draw_exit()
        self.draw_player()

    def draw_walls(self, room):
        """Draws a rectangle representing a room in the dungeon in the canvas that is passed in. Uses the position of
        the room to position the rectangle within the canvas."""
        position = room.position
        row, col = position[0], position[1]
        self.canvas.create_rectangle(self.room_unit * col+4, self.room_unit * row+4, self.room_unit * (col+1),
                                self.room_unit * (row+1), width=4)

    def draw_player(self):
        location = self.maze.player_location
        row, col = location[0], location[1]
        offset = self.room_unit // 2
        self.canvas.create_image(self.room_unit * col + offset, self.room_unit * row + offset, image=self.player_image)


    def draw_exit(self):
        """Draws the contents of the room passed in. Checks if the room contains the entrance or exit, then checks
        if the room has a pillar, pit, vision potion, or healing potion. Draws the corresponding object if any
        of the checks returns true."""
        maze_exit = self.maze.exit
        position = maze_exit.position
        row, col = position[0], position[1]
        offset = self.room_unit // 2
        self.canvas.create_image(self.room_unit * col + offset, self.room_unit * row + offset, image=self.exit_image)

    def draw_door(self, room):
        """Draws the doors of the rooms in the dungeon on the canvas that is passsed in. Checks if it is possible to
        travel in each direction using the dungeon's check_direction method and draws a door if it is possible to
        travel in that direction."""
        position = room.position
        row, col = position[0], position[1]
        if self.maze.check_north(row, col):
            self.canvas.create_rectangle(self.room_unit * col + 23, self.room_unit * row - 1, self.room_unit * col + 83,
                                    self.room_unit * row + 5, fill="white", outline="")
        if self.maze.check_south(row, col):
            self.canvas.create_rectangle(self.room_unit * col + 23, self.room_unit * (row+1) - 1, self.room_unit * col + 83,
                                    self.room_unit * (row+1) + 5, fill="white", outline="")
        if self.maze.check_west(row, col):
            self.canvas.create_rectangle(self.room_unit * col - 1, self.room_unit * row + 23, self.room_unit * col + 5,
                                    self.room_unit * row + 83, fill="white", outline="")
        if self.maze.check_east(row, col):
            self.canvas.create_rectangle(self.room_unit * (col+1) + 5, self.room_unit * row + 23,
                                    self.room_unit * (col+1) - 1, self.room_unit * row + 83, fill="white", outline="")
