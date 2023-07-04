from UI_tkinter import TURTLE

timmy = TURTLE()  # our turtles name is Timmy (collectively)
timmy.square(10)  # grid creation (with size as an arg)
timmy.cities(1, 'start')  # addition of the start city
timmy.cities(5, 'mid') # add here number of intermediate points
timmy.cities(1, 'end')  # addition of the destination city
timmy.roads(1)  # adds roads between cities in arg declared number (for eg 1 road per city)
timmy.a_star_v2()  # a-star analysis of the shortest road
timmy.screen.mainloop()  # infinite tkinter display loop
