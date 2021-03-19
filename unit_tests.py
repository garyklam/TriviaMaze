import unittest
from maze import Maze, Room
from TriviaMazeGUI import MazeGUI


class UnitTests(unittest.TestCase):

    # Room
    def test_default_room(self):
        room = Room(0, 0)
        open_doors = True
        for door in room.doors().values():
            if not door:
                open_doors = False
        self.assertTrue(open_doors)

    def test_room_lock_door(self):
        room = Room(0, 0)
        directions = ["south", "north", "west", "east"]
        for direction in directions:
            room.lock_door(direction)
            self.assertFalse(room.doors()[direction])

    #Maze
    def test_player_default_location(self):
        maze = Maze(3, 3)
        maze.construct()
        self.assertEqual(maze.player_location, [1, 1])

    def test_maze_get_size(self):
        maze = Maze(5, 7)
        self.assertEqual(maze.get_size(), [5, 7])

    def test_maze_resize(self):
        maze = Maze(3, 3)
        maze.construct()
        maze.resize_maze(8, 4)
        self.assertEqual(maze.get_size(), [8, 4])

    def test_maze_get_room(self):
        maze = Maze(3, 3)
        maze.construct()
        self.assertEqual(maze.get_room(1, 1), maze.grid[1][1])

    def test_find_destination_north(self):
        maze = Maze(3, 3)
        maze.construct()
        self.assertEqual(maze.find_destination(1, 1, "north"), maze.get_room(0, 1))

    def test_find_destination_south(self):
        maze = Maze(3, 3)
        maze.construct()
        self.assertEqual(maze.find_destination(1, 1, "south"), maze.get_room(2, 1))

    def test_find_destination_east(self):
        maze = Maze(3, 3)
        maze.construct()
        self.assertEqual(maze.find_destination(1, 1, "east"), maze.get_room(1, 2))

    def test_find_destination_west(self):
        maze = Maze(3, 3)
        maze.construct()
        self.assertEqual(maze.find_destination(1, 1, "west"), maze.get_room(1, 0))

    def test_find_destination_out_of_bounds_north(self):
        maze = Maze(3, 3)
        maze.construct()
        self.assertIsNone(maze.find_destination(0, 0, "north"))

    def test_find_destination_out_of_bounds_south(self):
        maze = Maze(3, 3)
        maze.construct()
        self.assertIsNone(maze.find_destination(3, 0, "south"))

    def test_find_destination_out_of_bounds_east(self):
        maze = Maze(3, 3)
        maze.construct()
        self.assertIsNone(maze.find_destination(3, 1, "east"))

    def test_find_destination_out_of_bounds_west(self):
        maze = Maze(3, 3)
        maze.construct()
        self.assertIsNone(maze.find_destination(2, 0, "west"))

    def test_check_direction_north_true(self):
        maze = Maze(3, 3)
        maze.construct()
        self.assertTrue(maze.check_direction(1, 1, "north"))

    def test_check_direction_south_true(self):
        maze = Maze(3, 3)
        maze.construct()
        self.assertTrue(maze.check_direction(1, 1, "south"))

    def test_check_direction_east_true(self):
        maze = Maze(3, 3)
        maze.construct()
        self.assertTrue(maze.check_direction(1, 1, "east"))

    def test_check_direction_west_true(self):
        maze = Maze(3, 3)
        maze.construct()
        self.assertTrue(maze.check_direction(1, 1, "west"))

    def test_check_direction_no_destination(self):
        maze = Maze(3, 3)
        maze.construct()
        self.assertFalse(maze.check_direction(0, 1, "north"))

    def test_check_direction_door_locked1(self):
        maze = Maze(3, 3)
        maze.construct()
        maze.lock_door("north")
        self.assertFalse(maze.check_direction(1, 1, "north"))

    def test_check_direction_door_locked2(self):
        maze = Maze(3, 3)
        maze.construct()
        maze.lock_door("north")
        self.assertFalse(maze.check_direction(0, 1, "south"))

    def test_maze_lock_door(self):
        maze = Maze(3, 3)
        maze.construct()
        room = maze.get_room(1, 1)
        directions = ["south", "north", "west", "east"]
        for direction in directions:
            maze.lock_door(direction)
            self.assertFalse(room.doors()[direction])

    def test_maze_move_player_north(self):
        maze = Maze(3, 3)
        maze.construct()
        start = maze.player_location
        maze.move_player("north")
        self.assertEqual(maze.player_location, [start[0]-1, start[1]])

    def test_maze_move_player_south(self):
        maze = Maze(3, 3)
        maze.construct()
        start = maze.player_location
        maze.move_player("south")
        self.assertEqual(maze.player_location, [start[0]+1, start[1]])

    def test_maze_move_player_west(self):
        maze = Maze(3, 3)
        maze.construct()
        start = maze.player_location
        maze.move_player("west")
        self.assertEqual(maze.player_location, [start[0], start[1]-1])

    def test_maze_move_player_east(self):
        maze = Maze(3, 3)
        maze.construct()
        start = maze.player_location
        maze.move_player("east")
        self.assertEqual(maze.player_location, [start[0], start[1]+1])

    def test_default_visited_rooms(self):
        maze = Maze(3, 3)
        maze.construct()
        self.assertEqual([maze.get_room(1, 1)], maze.visited_rooms)

    def test_visited_rooms(self):
        maze = Maze(3, 3)
        maze.construct()
        maze.move_player("north")
        maze.move_player("south")
        maze.move_player("east")
        self.assertEqual(maze.visited_rooms, [maze.get_room(1, 1), maze.get_room(0, 1), maze.get_room(1, 2)])

    def test_maze_is_completable_true1(self):
        maze = Maze(3, 3)
        maze.construct()
        self.assertTrue(maze.is_completable())

    def test_maze_is_completable_true2(self):
        maze = Maze(3, 3)
        maze.construct()
        directions = ["south", "north", "west"]
        for direction in directions:
            maze.lock_door(direction)
        self.assertTrue(maze.is_completable())

    def test_maze_is_completable_false1(self):
        maze = Maze(3, 3)
        maze.construct()
        directions = ["south", "north", "west", "east"]
        for direction in directions:
            maze.lock_door(direction)
        self.assertFalse(maze.is_completable())

    def test_maze_is_completable_false2(self):
        maze = Maze(3, 3)
        maze.construct()
        maze.move_player("north")
        maze.move_player("west")
        directions = ["south", "east"]
        for direction in directions:
            maze.lock_door(direction)
        self.assertFalse(maze.is_completable())

    def test_player_wins_false(self):
        maze = Maze(3, 3)
        maze.construct()
        self.assertFalse(maze.player_wins())

    def test_player_wins_true(self):
        maze = Maze(3, 3)
        maze.construct()
        maze.move_player("south")
        maze.move_player("east")
        self.assertTrue(maze.player_wins())

