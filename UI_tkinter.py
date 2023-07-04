import tkinter  # showing the result
import turtle  # animation
import random   # placing of the cities

class TURTLE:
    def __init__(self):
        self.alternatives = None
        self.end_coor = None
        self.start_coor = None
        self.southpoint = None
        self.northpoint = None
        self.eastpoint = None
        self.westpoint = None
        self.new_point = None
        self.default_library_key = 1
        self.halfs_points = []
        self.manhatan_library = {}
        self.east = None
        self.west = None
        self.south = None
        self.north = None
        self.coor = None
        self.root = tkinter.Tk()
        self.canvas = turtle.ScrolledCanvas(self.root)
        self.canvas.pack(side=tkinter.LEFT)
        self.screen = turtle.TurtleScreen(self.canvas)
        self.screen.setworldcoordinates(-10, -10, 110, 110) # grid coordinates (llx, lly, urx, ury)
        self.coord_list = {
            "start": [],
            "mid": [],
            "end": []}
        self.unique_coord = []
        self.roadmap = []
        self.roadmap_x = {}
        self.roadmap_y = {}

    def square(self,size): # single line of grid instruction
        self.turtle = turtle.RawTurtle(self.screen)
        self.turtle.hideturtle()
        self.turtle.speed(0)
        self.turtle.goto(0, 100)
        self.turtle.goto(100, 100)
        self.turtle.goto(100, 0)
        self.turtle.goto(0, 0)

        self.start_point_x = size  # size of small squares
        self.start_point_y = 100  # y-axis starting point
        self.counter = int(round(100/size))  # rows counter

        while self.counter > 0:  # loop for rows creation
            self.start_point_x = size   # refresh dla x-axis
            for x in range(int(round(100/size))):  # draw in reverse L 10 times and size shift
                self.turtle.penup()  # stop drawing
                self.turtle.goto(self.start_point_x, self.start_point_y)  # go to start
                self.turtle.pendown()  # start drawing
                self.turtle.goto(self.start_point_x, self.start_point_y-size) # go bottom
                self.turtle.goto(self.start_point_x-size, self.start_point_y - size)  # go left
                self.start_point_x += size   # change start point x-axis
            self.counter -= 1  # row -1
            self.start_point_y -= size  # change start point y-axis


    def cities(self, cities_number, list_name: str):  # cities creation in number as arg states
        for x in range(cities_number):
            self.turtle = turtle.RawTurtle(self.screen)  # city creation
            self.turtle.shape("circle")  # definition of the characteristics
            self.turtle.penup()
            if list_name == 'start':
                self.turtle.color('red')
            elif list_name == 'mid':
                self.turtle.color('blue')
            elif list_name == 'end':
                self.turtle.color('green')
            self.turtle.shapesize(1, 1)
            self.coordinates = (random.randrange(0,100,10),random.randrange(0,100,10))  # random location
            while self.coordinates in self.unique_coord: # check if that random location is already taken
                self.coordinates = (random.randrange(0, 100, 10), random.randrange(0, 100, 10)) # if yes, then random location again
            self.unique_coord.append(self.coordinates)  # list of unique city coordinates for new city addition
            self.turtle.goto(self.coordinates)  # city visual placement
            self.coord_list[list_name].append((self.turtle.position()))  # city library cataloging


    def roads(self, roads_numb):
        for city in self.unique_coord:
            self.turtle = turtle.RawTurtle(self.screen)  # instance of a turtle creation
            self.turtle.hideturtle()
            self.turtle.pensize(4)
            self.list_visited = [city]  # creation of a list of a visited cities
            for XYZ in range(roads_numb):  # roads number for each city
                self.random_city_coord = random.choice([elem for elem in self.unique_coord if elem not in self.list_visited])
                #  random city end of the road
                self.list_visited.append(self.random_city_coord)  # addition of visited point, so that all the cities might be connected
                self.turtle.penup()
                self.turtle.goto(city)  # road visualisation start
                self.turtle.pendown()
                self.turtle.goto(self.random_city_coord[0],city[1])  # first part of the road creation x-axis
                self.turtle.goto(self.random_city_coord[0],self.random_city_coord[1])  # y-axis part of the road creation
                try:  # add xaxis pat of the road to the library with x-axis as a key
                    self.roadmap_x[f'{self.random_city_coord[0]}'].append({
                        'begining': (self.random_city_coord[0], city[1]),
                        'end': (self.random_city_coord[0], self.random_city_coord[1])})
                except KeyError:  # if there is no key such as x-axis, create new
                    self.roadmap_x[f'{self.random_city_coord[0]}'] = [{
                        'begining': (self.random_city_coord[0], city[1]),
                        'end': (self.random_city_coord[0], self.random_city_coord[1])}]

                try:  # add y-axis pat of the road to the library with x-axis as a key
                    self.roadmap_y[f'{city[1]}'].append({
                            'begining': (city[0], city[1]),
                            'end': (self.random_city_coord[0], city[1])})
                except KeyError:  # if there is no key such as y-axis, create new
                    self.roadmap_y[f'{city[1]}'] = [{
                        'begining': (city[0], city[1]),
                        'end': (self.random_city_coord[0], city[1])}]
        # half-points list creation, important for navigation
        self.halfs_points.extend(self.fives_function(self.roadmap_x, 'x'))
        self.halfs_points.extend(self.fives_function(self.roadmap_y, 'y'))
        self.number_of_moves = 1  # number of moves done counter

    def fives_founder(self, start_point, end_point, axis):  # creator of the half-points
        l1 = []  # local container list
        step = 10
        # intermediates calculated
        if end_point[axis] - start_point[axis] > 0:
            x_values = range(start_point[0], end_point[0] + step, step)
            y_values = range(start_point[1], end_point[1] + step, step)
        else:
            x_values = range(start_point[0], end_point[0] - step, -1 * (step))
            y_values = range(start_point[1], end_point[1] - step, -1 * (step))
        # half-points creation
        intermediate_points = [(x, y) for x in x_values for y in y_values]
        # half-points presentation
        for point in intermediate_points:
            # no need for axis presentation
            try:
                if axis == 1:  # x-axis process tuples rounding
                    new_point = (point[0], round(prev_point[1] + ((point[1] - prev_point[1]) / 2)))
                else:   # y-axis process tuples rounding
                    new_point = (round(prev_point[0] + ((point[0] - prev_point[0]) / 2)), point[1])
                prev_point = point
                l1.append(new_point)
            except NameError:  # acction done at the start, where no prevoius point is in existance
                prev_point = point
        return l1

    def fives_function(self, bibl, axis):  # we need intermediate points to tell where is the road
        # there are situations where roads are parallel and program tries to connect them
        # its impossible with no half-points between them
        if axis == 'x':  # axis determination
            axis_val = 1
        else:
            axis_val = 0
        fives_library = []  # local container list
        for key, value in bibl.items():  #  arg library is beeing looped
            for x in range(len(value)):
                start_point = value[x]['begining']
                end_point = value[x]['end']
                fives_library.extend(self.fives_founder(start_point, end_point, axis_val))
        return fives_library  # returns complete list of navigation points created for current roads

    def manhatan_distance(self, current_loc, key):  # creates movement cost from one point to another
        try:
            cost = abs(current_loc[0] - self.end_coor[0]) + abs(current_loc[1] - self.end_coor[1]) + ((len(self.manhatan_library[key]['road']) - 1) * 10)
            return self.manhatan_library[key]['road'].append((current_loc[0], current_loc[1], cost))
        except KeyError:  # if that key does not exist
            self.manhatan_library[key] = {'road': []}
            cost = abs(current_loc[0] - self.end_coor[0]) + abs(current_loc[1] - self.end_coor[1]) + ((len(self.manhatan_library[key]['road']) - 1) * 10)
            return self.manhatan_library[key]['road'].append((current_loc[0], current_loc[1], cost))

    def a_star_v2(self):  # shortest road finding function
        counter = 0  # counts how many times, function tried to do the next step
        self.turtle = turtle.RawTurtle(self.screen)  # turtle creation with chosen characteristics
        self.turtle.hideturtle()
        self.turtle.penup()
        self.turtle.color('yellow')
        self.turtle.pensize(4)
        self.turtle.speed(5)
        self.start_coor = tuple(round(num, 0) for num in self.coord_list['start'][0])  # read tuple that is a string
        self.end_coor = self.coord_list['end'][0]
        self.been_list = []
        while self.new_point != self.coord_list['end'][0]:  # loop until we reach the destination city
            counter +=1  # counter add 1 each loop for safety switch
            if self.number_of_moves == 1:  # if first move
               self.coor = self.start_coor  # start coordinates
               self.manhatan_distance(self.coor, key = self.default_library_key)
            else:
                self.coor = self.new_point
            self.been_list.append(self.coor)  # add current turtle location as 'been to'
            # checking the way
            for xyy in self.halfs_points:
                # finding points 1-step away from the turtle that it can move to
                if xyy[0] == self.coor[0] and xyy[1] == self.coor[1]+5:
                    self.north = xyy
                if xyy[0] == self.coor[0] and xyy[1] == self.coor[1]-5:
                    self.south = xyy
                if xyy[0] == self.coor[0]+5 and xyy[1] == self.coor[1]:
                    self.east = xyy
                if xyy[0] == self.coor[0]-5 and xyy[1] == self.coor[1]:
                    self.west = xyy

            self.alternatives = []  # alternative directions list creation, that we can choose from half-points
            if self.north is not None:
                self.northpoint = (self.north[0],self.north[1]+5)
                if self.northpoint not in self.been_list:
                    self.alternatives.append(self.northpoint)
            if self.south is not None:
                self.southpoint = (self.south[0],self.south[1]-5)
                if self.southpoint not in self.been_list:
                    self.alternatives.append(self.southpoint)
            if self.east is not None:
                self.eastpoint = (self.east[0]+5,self.east[1])
                if self.eastpoint not in self.been_list:
                    self.alternatives.append(self.eastpoint)
            if self.west is not None:
                self.westpoint = (self.west[0]-5,self.west[1])
                if self.westpoint not in self.been_list:
                    self.alternatives.append(self.westpoint)

            if not self.alternatives:  # if turtle reached end of the road, sets it's price as 9999
                obj_last = self.manhatan_library[self.default_library_key]['road'][len(self.manhatan_library[self.default_library_key]['road'])-1]
                self.manhatan_library[self.default_library_key]['road'].append((obj_last[0], obj_last[1], 9999))


            if len(self.alternatives) == 1:  # if there is only 1 direction available
                self.manhatan_distance(self.alternatives[0], key=self.default_library_key)  # add
            else: # if more than 1 road
                first_iteration = True  # first road has default key value
                for point in self.alternatives:  # all roads check
                    if first_iteration:  # 1st road
                        if (point[0], point[1]) in self.been_list:
                            pass  # no going back safety switch
                        else:  # next step on default key road addition to library
                            self.manhatan_distance(self.alternatives[0], key=self.default_library_key)
                            first_iteration = False
                    else:  # rest of the roads
                        if (point[0],point[1]) in self.been_list: # if the road already exist
                            pass  # no going back safety switch
                        else:  # new road map creation
                            for x in range(1,1000):  # new key creation
                                # check for keyerror to see which one is next empty
                                try:
                                    self.manhatan_library[x]['road'] == self.manhatan_library[x]['road']
                                except KeyError:
                                    self.manhatan_library[x] = {'road': []}  # creates library
                                    for val in range(len(self.manhatan_library[self.default_library_key]['road'])-1):
                                        # adds all the points from the old road (but not last one)
                                        self.manhatan_library[x]['road'].append(self.manhatan_library[self.default_library_key]['road'][val])
                                    self.manhatan_distance(point, x) # adds a point
                                    break  # break because new key was found

                # shortest step search from all key created
            self.lowest = 100000  # random high value to find lower one
            for key, value in self.manhatan_library.items():
                obj1 = value['road'][len(self.manhatan_library[key]['road'])-1]
                if obj1[2] < self.lowest:
                    self.lowest = obj1[2]
                    self.new_point = (obj1[0],obj1[1])
                    self.default_library_key = key

            self.number_of_moves += 1
            if counter > 601:  # safe switch
                print("More than 600 steps, error")
                break
            else:  # closest half-points reset
                self.east = self.west = self.south = self.north = None

        for step in self.manhatan_library[self.default_library_key]['road']:  # display the shortest road
            self.turtle.goto((step[0],step[1]))
            self.turtle.pendown()

        print(f'Turtle reached destination city in {self.number_of_moves-1} units.')  # final message

