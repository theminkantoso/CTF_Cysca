import socket
import select
import sys
 
WEST = "west"
NORTH = "north"
EAST = "east"
SOUTH = "south"
UP = "up"
DOWN = "down"
 
DIRECTIONS = [WEST, NORTH, EAST, SOUTH]
OPPOSITES = {
    WEST: EAST,
    NORTH: SOUTH,
    EAST: WEST,
    SOUTH: NORTH,
    UP: DOWN,
    DOWN: UP
}
 
 
class Position(object):
    def __init__(self, north=-1, east=-1, south=-1, west=-1, up=-1, down=-1):
        self.north = north
        self.west = west
        self.south = south
        self.east = east
        self.up = up
        self.down = down
        self.back = ""  # direction
        self.g_cost = -1
        self.h_cost = -1
        self.parent = -1
 
    def f_cost(self):
        return self.g_cost + self.h_cost
 
    def is_dead_end(self):
        count = 0
        if self.north == -2:
            count += 1
        if self.east == -2:
            count += 1
        if self.west == -2:
            count += 1
        if self.south == -2:
            count += 1
        return count == 3
 
    def status(self, direction):
        if hasattr(self, direction):
            return getattr(self, direction)
     
    def set_status(self, direction, index):
        if hasattr(self, direction):
            return setattr(self, direction, index)
 
    def set_opposite_status(self, direction, index):
        opposite = OPPOSITES[direction]
        self.back = opposite
        self.set_status(opposite, index)
 
    def direction_for(self, index):
        if self.east == index:
            return EAST
        elif self.west == index:
            return WEST
        elif self.north == index:
            return NORTH
        elif self.south == index:
            return SOUTH
        return "unknown"
 
 
class Buddy(object):
    def __init__(self):
        self.position = Position()
        self.maze = [self.position]
        self.coords = {"1000,1000,5": 0}
        self.direction = NORTH
        self.index = 0  # index of position in maze
        self.x = 1000
        self.y = 1000
        self.z = 5
        self.floors = {}
        self.has_key = False
        self.escape_index = -1
        self.key_index = -1
 
        self.s = socket.socket()
        self.s.connect(("192.168.100.210", 7788))
        self.s.recv(1024)  # Please wait...
        self.s.recv(1024)  # Map loaded
        self.s.setblocking(0)
        #self.receive()
 
    def get_key(self):
        self.send("pickup")
        lines = self.receive()
        if "You picked up the key." in lines:
            self.has_key = True
        print lines
 
    def escape(self):
        self.send("escape")
        lines = self.receive()
        if not 'No door here.' in lines:
            print lines
 
    def receive(self):
        lines = []
        for __ in range(2):
            ready = select.select([self.s], [], [], 5 if not lines else 0.1)
            if ready[0]:
                buff = self.s.recv(1024).strip()
                if (not "You moved" in buff and
                        not "There is a wall" in buff and
                        not "No key here." in buff and
                        not "There are stairs heading" in buff and
                        not "Get out of here!" in buff and
                        not "No door here." in buff and
                        not "There is a key here." in buff):
                    print buff
                lines.append(buff)
        if "You are dead." in lines:
            sys.exit()
        return lines
 
    def send(self, data):
        while True:
            ready = select.select([], [self.s], [], 0.1)
            if ready[1]:
                self.s.send(data)
                break
 
    def update_coords(self):
        if self.direction == NORTH:
            self.y += 1
        elif self.direction == SOUTH:
            self.y -= 1
        elif self.direction == WEST:
            self.x -= 1
        elif self.direction == EAST:
            self.x += 1
        elif self.direction == UP:
            self.z += 1
        elif self.direction == DOWN:
            self.z -= 1
        coordinates = "{0},{1},{2}".format(self.x, self.y, self.z)
        if coordinates not in self.coords:
            self.coords[coordinates] = self.index
 
    def move_direction(self, new_direction):
        new_position = None
        lines = []
 
        if new_direction in DIRECTIONS:  # same floor
            new_index = self.position.status(new_direction)
            if new_index >= 0:
                # already known position
                new_position = self.maze[new_index]
                self.index = new_index
                # but we still have to move on the server
                self.send(new_direction + "\n")
                lines = self.receive()
            elif new_index == -2:
                # known dead end
                return False
            else:
                # unknown direction : we try to move
                self.send(new_direction + "\n")
                lines = self.receive()
                if "You moved {0}.".format(new_direction) in lines:
                    new_position = Position()
                    new_position.set_opposite_status(new_direction, self.index)
                    self.index = len(self.maze)
                    self.position.set_status(new_direction, self.index)
                    self.maze.append(new_position)
                    if "There are stairs heading upward." in lines and self.position.status(UP) == -1:
                        up_position = Position()
                        up_position.set_status(DOWN, self.index)
                        up_position.set_status("back", DOWN)
                        new_position.up = len(self.maze)
                        self.maze.append(up_position)
                        print "Found stairs going up."
                    if "There are stairs heading downward." in lines and self.position.status(DOWN) == -1:
                        down_position = Position()
                        down_position.set_status(UP, self.index)
                        down_position.set_status("back", UP)
                        new_position.down = len(self.maze)
                        self.maze.append(down_position)
                        print "Found stairs going down."
                elif "There is a wall there." in lines:
                    # new dead end
                    self.position.set_status(new_direction, -2)
                    return False
                else:
                    print "Uhoh"
                    print lines
                    sys.exit()
        elif new_direction == UP:
            if self.position.up >= 0:
                print "Moving upstair"
                self.send("up\n")
                lines = self.receive()
                if "You moved upstairs." in lines:
                    new_index = self.position.up
                    new_position = self.maze[new_index]
                    print "New upstair position:", new_position
                    self.index = new_index
                else:
                    print "No upstair :("
                    sys.exit()
            else:
                print "UP fail"
                sys.exit()
        elif new_direction == DOWN:
            if self.position.down >= 0:
                print "Moving downstair"
                self.send("down\n")
                lines = self.receive()
                if "You moved downstairs." in lines:
                    new_index = self.position.down
                    new_position = self.maze[new_index]
                    print "New downstair position:", new_position
                    self.index = new_index
                else:
                    print "No downstair :("
                    sys.exit()
            else:
                print "DOWN fail"
                sys.exit()
 
        # On success
        self.position = new_position
        self.direction = new_direction
        print self.direction
 
        self.update_coords()
        new_coords = "{0},{1},{2}".format(self.x, self.y, self.z)
 
        if self.z not in self.floors:
            self.floors[self.z] = {}
 
        if "There is a key here." in lines:
            self.floors[self.z]["key"] = new_coords
        if "There is a locked door here." in lines:  # You need the key to unlock the door.
            self.escape_index = self.index
            self.floors[self.z]["escape"] = new_coords
            self.escape()
        if "There are stairs heading upward." in lines:
            self.floors[self.z]["up"] = new_coords
        if "There are stairs heading downward." in lines:
            self.floors[self.z]["down"] = new_coords
 
        self.fix_map()
        return True
 
    def myself(self):
        return "{0},{1},{2}".format(self.x, self.y, self.z)
 
    def move_tremeaux(self):
        # UP and DOWN are "one-time" directions
        if self.direction == UP or self.direction == DOWN:
            self.direction = NORTH
 
        if True or not self.has_key:
            if False and self.position.down >= 0 and self.z + 1 < 9 not in self.floors:  # NICO up
                self.move_direction(DOWN)  # UP
            else:
                index = DIRECTIONS.index(self.direction)
                for i in range(3, 7):
                    direction = DIRECTIONS[(index + i) % 4]
                    # Only go to unknown directions
                    if self.position.status(direction) == -1:
                        if self.move_direction(direction):
                            break
                else:
                    # if self.position.back:
                    if self.position.back and self.position.back != UP and self.position.back != DOWN:
                        print "Going back to", self.position.back
                        if self.position.back == DOWN:
                            self.floors.append(self.z)
                        if not self.move_direction(self.position.back):
                            print "Error going back :("
                            sys.exit()
                    else:
                        print "Oups, can't go back, position: {0},{1},{2}".format(self.x, self.y, self.z)
                        return False
        else:
            self.move_direction(self.position.back)
        return True
 
    def fix_map(self):
        if self.position.north == -1:
            next_north = "{0},{1},{2}".format(self.x, self.y + 1, self.z)
            if next_north in self.coords:
                self.position.north = self.coords[next_north]
                north_position = self.maze[self.position.north]
                north_position.south = self.index
                print "Already known cell at north ({0}) : {1}".format(next_north, self.position.north)
        if self.position.south == -1:
            next_south = "{0},{1},{2}".format(self.x, self.y - 1, self.z)
            if next_south in self.coords:
                self.position.south = self.coords[next_south]
                south_position = self.maze[self.position.south]
                south_position.north = self.index
                print "Already known cell at south ({0}) : {1}".format(next_south, self.position.south)
        if self.position.west == -1:
            next_west = "{0},{1},{2}".format(self.x - 1, self.y, self.z)
            if next_west in self.coords:
                self.position.west = self.coords[next_west]
                west_position = self.maze[self.position.west]
                west_position.east = self.index
                print "Already known cell at west ({0}) : {1}".format(next_west, self.position.west)
        if self.position.east == -1:
            next_east = "{0},{1},{2}".format(self.x + 1, self.y, self.z)
            if next_east in self.coords:
                self.position.east = self.coords[next_east]
                east_position = self.maze[self.position.east]
                east_position.west = self.index
                print "Already known cell at east ({0}) : {1}".format(next_east, self.position.east)
 
    def print_floor(self, level):
        min_x = 7000
        min_y = 7000
        max_x = 0
        max_y = 0
        for coord in self.coords:
            x, y, z = [int(x) for x in coord.split(',')]
            if z == level:
                if x < min_x:
                    min_x = x
                if x > max_x:
                    max_x = x
                if y < min_y:
                    min_y = y
                if y > max_y:
                    max_y = y
        print
        print "min_x = {0}, min_y = {1}".format(min_x, min_y)
 
        for y in xrange(max_y + 1, min_y - 2, -1):
            for x in xrange(min_x - 1, max_x + 2):
                coord = "{0},{1},{2}".format(x, y, level)
                if coord in self.coords:
                    floor = self.floors[level]
 
                    if coord == floor.get("key"):
                        sys.stdout.write("(")
                    elif coord == floor.get("escape"):
                        sys.stdout.write("?")
                    elif coord == floor.get("up"):
                        sys.stdout.write(">")
                    elif coord == floor.get("down"):
                        sys.stdout.write("<")
                    elif coord == self.myself():
                        sys.stdout.write("@")
                    else:
                        sys.stdout.write(" ")
                else:
                    sys.stdout.write("#")
            sys.stdout.write('\n')
        print ''
 
    def find_short_path(self, start, end):
        x_end, y_end, z_end = [int(x) for x in end.split(',')]
 
        # set H-cost for every nodes on the same floor
        for coord in self.coords:
            x, y, z = [int(x) for x in coord.split(',')]
            if z == z_end:
                position = self.maze[self.coords[coord]]
                position.h_cost = abs(x_end - x) + abs(y_end - y)
                # force reinit
                position.parent = -1
                position.g_cost = -1
 
        end_position = self.maze[self.coords[end]]
        start_position = self.maze[self.coords[start]]
        start_position.g_cost = 0
 
        open_nodes = [start_position]
        closed_nodes = []
 
        print start, "->", end
        while True:
            min_cost = 7000
            min_position = None
            for position in open_nodes:
                if position.f_cost() < min_cost:
                    min_position = position
                    min_cost = min_position.f_cost()
            open_nodes.remove(min_position)
            closed_nodes.append(min_position)
 
            if min_position == end_position:
                print "done"
                commands = []
                while min_position.parent != -1:
                    commands.append(OPPOSITES[min_position.direction_for(min_position.parent)])
                    min_position = self.maze[min_position.parent]
                return commands[::-1]
 
            neighbors_idx = [min_position.east,
                             min_position.south,
                             min_position.north,
                             min_position.west]
 
            for neighbor_idx in neighbors_idx:
                if neighbor_idx < 0:
                    continue
                neighbor = self.maze[neighbor_idx]
                if neighbor in closed_nodes:
                    continue
 
                if neighbor not in open_nodes or (neighbor.f_cost() > min_position.f_cost() + 1):
                    neighbor.parent = self.maze.index(min_position)
                    neighbor.g_cost = min_position.f_cost() + 1
                    if neighbor not in open_nodes:
                        open_nodes.append(neighbor)
 
 
if __name__ == "__main__":
    bud = Buddy()
    bud_coords = ""
    # go to the lowest level
    while True:
        # explore the whole floor
        while True:
            if not bud.move_tremeaux():
                break
 
        bud_coords = "{0},{1},{2}".format(bud.x, bud.y, bud.z)
        bud.print_floor(bud.z)
        if "down" in bud.floors[bud.z]:
            commands = bud.find_short_path(bud_coords, bud.floors[bud.z]["down"])
            print ", ".join(commands)
            for direction in commands:
                bud.move_direction(direction)
            bud.move_direction(DOWN)
        else:
            # lowest level, we must have found the escape door
            print "Reached end of cave"
            bud.move_direction(UP)
            break
 
    # now go to higher floors
    while True:
        bud_coords = "{0},{1},{2}".format(bud.x, bud.y, bud.z)
        # known floor
        if "up" in bud.floors[bud.z]:
            commands = bud.find_short_path(bud_coords, bud.floors[bud.z]["up"])
            print ", ".join(commands)
            for direction in commands:
                bud.move_direction(direction)
            bud.move_direction(UP)
        else:
            # discover unknown floor
            bud_coords = "{0},{1},{2}".format(bud.x, bud.y, bud.z)
            while True:
                if not bud.move_tremeaux():
                    break
            bud_coords = "{0},{1},{2}".format(bud.x, bud.y, bud.z)
            bud.print_floor(bud.z)
            if "key" in bud.floors[bud.z]:
                commands = bud.find_short_path(bud_coords, bud.floors[bud.z]["key"])
                print ", ".join(commands)
                for direction in commands:
                    bud.move_direction(direction)
                bud.get_key()
                break
            elif "up" in bud.floors[bud.z]:
                commands = bud.find_short_path(bud_coords, bud.floors[bud.z]["up"])
                print ", ".join(commands)
                for direction in commands:
                    bud.move_direction(direction)
                bud.move_direction(UP)
 
            else:
                print "Can't find key nor upstair :("
                break
 
    while True:
        bud_coords = "{0},{1},{2}".format(bud.x, bud.y, bud.z)
        bud.print_floor(bud.z)
        if "escape" in bud.floors[bud.z]:
            print "Go to escape"
            commands = bud.find_short_path(bud_coords, bud.floors[bud.z]["escape"])
            print ", ".join(commands)
            for direction in commands:
                bud.move_direction(direction)
            bud.escape()
            break
        elif "down" in bud.floors[bud.z]:
            commands = bud.find_short_path(bud_coords, bud.floors[bud.z]["down"])
            print ", ".join(commands)
            for direction in commands:
                bud.move_direction(direction)
            bud.move_direction(DOWN)