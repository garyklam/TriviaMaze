from tkinter import PhotoImage


class Drawer:
    """Contains methods to draw the game display for the trivia game."""
    def __init__(self, maze, canvas):
        self.maze = maze
        self.rows = self.maze.rows
        self.cols = self.maze.cols
        self.room_unit = 100
        self.canvas = canvas
        self.player_image = PhotoImage(file='fx/player.gif')
        self.exit_image = PhotoImage(file='fx/exit.gif')

    def draw(self):
        """Draws all of the rooms in the maze along with their contents. Draws walls in a separate loop from the
        doors to avoid overlapping lines causing doors to be obscured in the map. Returns the canvas object after
        drawing all features."""
        self.canvas.delete("all")
        for room in self.maze.visited_rooms:
            self.highlight_room(room)
        for row in self.maze.grid:
            for room in row:
                self.draw_walls(room)
        for room in self.maze.visited_rooms:
            self.draw_door(room)
        self.draw_exit()
        self.draw_player()

    def draw_walls(self, room):
        """Draws a rectangle representing a room in the maze in the canvas that is passed in. Uses the position of
        the room to position the rectangle within the canvas."""
        row, col = room.position[0], room.position[1]
        self.canvas.create_rectangle(self.room_unit * col+4, self.room_unit * row+4, self.room_unit * (col+1),
                                     self.room_unit * (row+1), width=4)

    def draw_player(self):
        location = self.maze.player_location
        row, col = location[0], location[1]
        offset = self.room_unit // 2
        self.canvas.create_image(self.room_unit * col + offset, self.room_unit * row + offset, image=self.player_image)

    def draw_exit(self):
        maze_exit = self.maze.exit
        row, col = maze_exit.position[0], maze_exit.position[1]
        offset = self.room_unit // 2
        self.canvas.create_image(self.room_unit * col + offset, self.room_unit * row + offset, image=self.exit_image)

    def draw_door(self, room):
        """Draws the doors of the rooms in the maze on the canvas that is passed in. Checks if it is possible to
        travel in each direction using the maze's check_direction method and draws a door if it is possible to
        travel in that direction."""
        row, col = room.position[0], room.position[1]
        directions = ["north", "south", "east", "west"]
        cols = [col, col, col+1, col]
        rows = [row, row+1, row, row]
        col_offset, row_offset = [23, 83, 23, 83, -1, 5, -1, 5], [-1, 5, -1, 5, 23, 83, 23, 83]
        for i in range(4):
            if self.maze.check_direction(row, col, directions[i]):
                self.canvas.create_rectangle(self.room_unit * cols[i] + col_offset[i*2], self.room_unit * rows[i] + row_offset[i*2],
                                             self.room_unit * cols[i] + col_offset[i*2+1], self.room_unit * rows[i] + row_offset[i*2+1],
                                             fill="white", outline="")

    def highlight_room(self, room):
        row, col = room.position[0], room.position[1]
        self.canvas.create_rectangle(self.room_unit * col, self.room_unit * row, self.room_unit * (col + 1),
                                     self.room_unit * (row + 1), fill='white', outline="")