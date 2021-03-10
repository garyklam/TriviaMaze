
class Room:

    def __init__(self, row, column):
        self._position = (row, column)
        self._doors = {"north": True,
                       "south": True,
                       "east": True,
                       "west": True}
        self.answers = {
            "north": 'not set',
            "south": 'not set',
            "east": 'not set',
            "west": 'not set'
        }

    def doors(self):
        return self._doors

    def set_north_border(self):
        self._doors["north"] = False

    def set_south_border(self):
        self._doors["south"] = False

    def set_east_border(self):
        self._doors["east"] = False

    def set_west_border(self):
        self._doors["west"] = False

    def lock_door(self, direction):
        self._doors[direction] = False

    def set_answer(self, direction, answer):
        # answer could be correct or wrong
        self.answers[direction] = answer

    def game_over(self):
        if self.answers["north"] == 'wrong':
            self._doors['north']=False
        if self.answers["south"] == 'wrong':
            self._doors['south']=False
        if self.answers["east"] == 'wrong':
            self._doors['east']=False
        if self.answers["west"] == 'wrong':
            self._doors['west']=False
        for door, value in self.doors().items():
            if(value ==  True):
                return  False
        return True


class Maze:

    def __init__(self, rows, columns):
        self.rows = rows
        self.cols = columns
        self.grid = [[Room(r, c) for c in range(self.cols)] for r in range(self.rows)]
        self.set_borders()
        self.exit = self.get_room(self.rows - 1, self.cols - 1)
        self.player_location = [0, 0]
        self.visited_rooms = []
        self.questions = [0, 0]




    def get_room(self, row, col):
        """Returns room object located at the given row and column."""
        return self.grid[row][col]

    def set_borders(self):
        """Sets the door values of the rooms on the edge of the dungeon to be walls."""
        for room in self.grid[0]:
            room.set_north_border()
        for room in self.grid[self.rows - 1]:
            room.set_south_border()
        for row in self.grid:
            row[0].set_west_border()
            row[self.cols - 1].set_east_border()

    def move_player(self, direction):
        if direction == "north" and self.player_location[0] > 0:
            self.player_location[0] = self.player_location[0] - 1
        elif direction == "south" and self.player_location[0] < self.rows - 1:
            self.player_location[0] = self.player_location[0] + 1
        elif direction == "west" and self.player_location[1] > 0:
            self.player_location[1] = self.player_location[1] - 1
        elif direction == "east" and self.player_location[1] < self.cols - 1:
            self.player_location[1] = self.player_location[1] + 1
        else:
            pass

    def lock_door(self, direction):
        room = self.get_room(self.player_location[0], self.player_location[1])
        room.lock_door(direction)

    def check_traversal(self, row, col):
        """
        Checks if it is possible to reach the exit and all of the pillars from the initial location passed in. Keeps a
        list of rooms that have been visited to avoid an infinite loop. The list of unique rooms used to place the
        pillars, entrance, and exit is used to check if the all of the rooms have been visited.
        """
        found_path = False
        if self.grid[row][col] not in self.visited_rooms:
            self.visited_rooms.append(self.grid[row][col])
            if self.exit in self.visited_rooms:
                found_path = True
            else:
                if not found_path and self.check_north(row, col):
                    found_path = self.check_traversal(row - 1, col)
                if not found_path and self.check_west(row, col):
                    found_path = self.check_traversal(row, col - 1)
                if not found_path and self.check_south(row, col):
                    found_path = self.check_traversal(row + 1, col)
                if not found_path and self.check_east(row, col):
                    found_path = self.check_traversal(row, col + 1)
        return found_path

    def in_bounds(self, row, col):
        """
        Checks if the given row and column are within the bounds of the dungeon, returns true if it is, returns
        false if it is not
        """
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return True
        else:
            return False

    def check_north(self, row, col):
        """Checks to see if the given room has a room to the "north" and if it is possible to travel to the room.
        If the given room has an "open" north door or if the northern room has an "open" south door, then it is
        possible to travel between the two rooms."""
        if self.in_bounds(row - 1, col):
            curr = self.get_room(row, col)
            doors1 = curr.doors()
            south = self.get_room(row - 1, col)
            doors2 = south.doors()
            if doors1["north"] and doors2["south"]:
                return True
        else:
            return False

    def check_south(self, row, col):
        """Checks to see if the given room has a room to the "south" and if it is possible to travel to the room.
            If the given room has an "open" south door or if the southern room has an "open" north door, then it is
            possible to travel between the two rooms."""
        if self.in_bounds(row + 1, col):
            curr = self.get_room(row, col)
            doors1 = curr.doors()
            north = self.get_room(row + 1, col)
            doors2 = north.doors()
            if doors1["south"] and doors2["north"]:
                return True
        else:
            return False

    def check_east(self, row, col):
        """Checks to see if the given room has a room to the "east" and if it is possible to travel to the room.
            If the given room has an "open" east door or if the eastern room has an "west" south door, then it is
            possible to travel between the two rooms."""
        if self.in_bounds(row, col + 1):
            curr = self.get_room(row, col)
            doors1 = curr.doors()
            west = self.get_room(row, col + 1)
            doors2 = west.doors()
            if doors1["east"] and doors2["west"]:
                return True
        else:
            return False

    def check_west(self, row, col):
        """Checks to see if the given room has a room to the "west" and if it is possible to travel to the room.
            If the given room has an "open" west door or if the western room has an "open" west door, then it is
            possible to travel between the two rooms."""
        if self.in_bounds(row, col - 1):
            curr = self.get_room(row, col)
            doors1 = curr.doors()
            east = self.get_room(row, col - 1)
            doors2 = east.doors()
            if doors1["west"] and doors2["east"]:
                return True
        else:
            return False

    def check_game_over(self, row, col):
        room = self.grid[row][col]
        return room.game_over()
    def game_statistic(self):
        self.C_ans = 0
        self.W_ans = 0
        self.points = 0
        for room in self.grid[0]:

            if room.answers["north"] == 'correct':
                self.C_ans += 1
                self.points += 2
            if room.answers["north"] == 'wrong':
               self.W_ans +=1
            if room.answers["south"] == 'correct':
                self.C_ans += 1
                self.points += 2
            if room.answers["south"] == 'wrong':
               self.W_ans +=1
            if room.answers["east"] == 'correct':
                self.C_ans +=1
                self.points += 2
            if room.answers["east"] == 'wrong':
               self.W_ans +=1
            if room.answers["west"] == 'correct':
                self.C_ans += 1
                self.points += 2
            if room.answers["west"] == 'wrong':
               self.W_ans +=1
        self.total_ans_que = self.C_ans + self.W_ans
        A = ' Correct Answers ', self.C_ans
        B = ' Wrong Answers ', self.W_ans
        C = ' Total Answered que', self.total_ans_que
        D = 'Total Points Earned',self.points
        return f'{A[0]}: {A[1]}\n {B[0]}: {B[1]} \n {C[0]}: {C[1]} \n {D[0]}: {D[1]}'




if __name__ == '__main__':
    test = Maze(1, 1)
    print(test.check_traversal(test.player_location[0], test.player_location[0]))
    movements = ["north", "south", "north", "west", "east", "east", "east", "east", "east"]
    for direction in movements:
        test.move_player(direction)
        print(test.player_location)
    test.lock_door("south")
    print(test.check_traversal(test.player_location[0], test.player_location[1]))
    test.lock_door("west")
    print(test.check_traversal(test.player_location[0], test.player_location[1]))
    print('Testing Game over method')
    movements = ["east", "south"]
    test.get_room(0, 0).answers['east'] = 'wrong'
    test.get_room(0, 0).answers['south'] = 'wrong'
    test.get_room(0, 0).answers['north'] = 'correct'
    print('Is game over ' + str(test.check_game_over(0, 0)))

    print(test.game_statistic())