class Room:

    def __init__(self, row, column):
        self._position = [row, column]
        self._doors = {"north": True,
                        "south": True,
                        "east": True,
                        "west": True}

    def doors(self):
        return self._doors

    def set_as_border(self, direction):
        self._doors[direction.lower()] = False

    def lock_door(self, direction):
        self._doors[direction] = False

    @property
    def position(self):
        return self._position


class Maze:

    def __init__(self, rows, columns):
        self.rows = rows
        self.cols = columns
        self._player_location = [1, 1]
        self._difficulty = "easy"
        self._category = None
        self.grid = None
        self.visited_rooms = []
        self.stats = {}
        self._time_elapsed = 0

    @property
    def player_location(self):
        return self._player_location

    @property
    def difficulty(self):
        return self._difficulty

    @property
    def category(self):
        return self._category

    def get_total_doors(self):
        return self.rows * (self.cols-1) + self.cols * (self.rows-1)

    def get_size(self):
        return [self.rows, self.cols]

    def get_room(self, row, col):
        """Returns room object located at the given row and column."""
        return self.grid[row][col]

    def get_time(self):
        """Returns the time elapsed in digital clock format: (hour:minute:second)"""
        hours = self._time_elapsed // 3600
        minutes = (self._time_elapsed - hours * 3600) // 60
        seconds = (self._time_elapsed - hours * 3600 - minutes * 60)
        return f'{str(hours).zfill(2)}:{str(minutes).zfill(2)}:{str(seconds).zfill(2)}'

    def resize_dungeon(self, row, col):
        """
        Alters dimension fields of the dungeon, does not create a new grid of rooms, needs to call generate to actually
        resize the dungeon.
        """
        self.rows = row
        self.cols = col

    def set_difficulty(self, difficulty):
        self._difficulty = difficulty

    def set_category(self, category):
        self._category = category

    def set_time_elapsed(self, start, current):
        self._time_elapsed += current - start

    def construct(self):
        self.grid = [[Room(r, c) for c in range(self.cols)] for r in range(self.rows)]
        self.set_borders()
        self.exit = self.get_room(self.rows - 1, self.cols - 1)
        row, col = self.player_location[0], self.player_location[1]
        room = self.get_room(row, col)
        self.visited_rooms.append(room)

    def set_borders(self):
        """Sets the door values of the rooms on the edge of the dungeon to be walls."""
        for room in self.grid[0]:
            room.set_as_border("north")
        for room in self.grid[self.rows - 1]:
            room.set_as_border("south")
        for row in self.grid:
            row[0].set_as_border("west")
            row[self.cols - 1].set_as_border("east")

    def move_player(self, direction):
        destination = self.find_destination(self.player_location[0], self.player_location[1], direction)
        self._player_location = destination.position
        self.visited_rooms.append(destination)

    def player_wins(self):
        if self._player_location[0] == self.exit.position[0] \
                and self._player_location[1] == self.exit.position[1]:
            return True
        return False

    def lock_door(self, direction):
        room = self.get_room(self.player_location[0], self.player_location[1])
        room.lock_door(direction)

    def is_completable(self):
        visited = []
        row, col = self.player_location[0], self.player_location[1]
        return self.check_traversal(row, col, visited)

    def check_traversal(self, row, col, visited):
        """
        Checks if it is possible to reach the exit and all of the pillars from the initial location passed in. Keeps a
        list of rooms that have been visited to avoid an infinite loop. The list of unique rooms used to place the
        pillars, entrance, and exit is used to check if the all of the rooms have been visited.
        """
        found_path = False
        if self.grid[row][col] not in visited:
            visited.append(self.grid[row][col])
            if self.exit in visited:
                found_path = True
            else:
                if not found_path and self.check_direction(row, col, "north"):
                    found_path = self.check_traversal(row-1, col, visited)
                if not found_path and self.check_direction(row, col, "west"):
                    found_path = self.check_traversal(row, col-1, visited)
                if not found_path and self.check_direction(row, col, "south"):
                    found_path = self.check_traversal(row+1, col, visited)
                if not found_path and self.check_direction(row, col, "east"):
                    found_path = self.check_traversal(row, col+1, visited)
        return found_path

    def check_direction(self, row, col, direction):
        opposite = {"north": "south", "south": "north", "west": "east", "east": "west"}
        destination = self.find_destination(row, col, direction)
        if destination:
            curr = self.get_room(row, col)
            doors1 = curr.doors()
            doors2 = destination.doors()
            if doors1[direction] and doors2[opposite[direction]]:
                return True
        return False

    def find_destination(self, row, col, direction):
        translation = {"north": [-1, 0], "south": [1, 0], "east": [0, 1], "west": [0, -1]}
        row += translation[direction][0]
        col += translation[direction][1]
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.get_room(row, col)

# if __name__ == '__main__':
#     test = Maze(4, 4)
#     test.construct()
#     print(test.is_completable())
#     movements = ["north", "south", "north", "west", "east", "east", "east", "east", "east"]
#     for direction in movements:
#         test.move_player(direction)
#         print(test.player_location)
#     test.lock_door("south")
#     print(test.is_completable())
#     test.lock_door("west")
#     print(test.is_completable())
