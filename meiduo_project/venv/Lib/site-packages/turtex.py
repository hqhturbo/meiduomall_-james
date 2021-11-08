import turtle
from turtle import *


# Returns nothing. Draws a poly based on the number of sides,
# the length of one side and a turtle object.

def drawpoly(number_of_sides, length, turtle_obj = None):
	
	# Sets default turtle if turtle object is not passed.
	
	if not turtle_obj:
		
		turtle_obj = turtle.Turtle()
	
	# For loop is for the number of sides in the poly.
	
	for i in range(number_of_sides):
		
		turtle_obj.forward(length)
		turtle_obj.lt(360 / number_of_sides)


# Returns nothing. Draws a line, given the starting position, the length of the line,
# the direction in which the line must be drawn and a turtle object.

def draw_line(start_pos, length, direction_in_angle, turtle_obj = None):
	
	# Sets default turtle if turtle object is not passed.
	
	if not turtle_obj:
		
		turtle_obj = turtle.Turtle()
	
	# Goes to the start_pos.
	
	turtle_obj.penup()
	turtle_obj.goto(start_pos[0], start_pos[1])
	turtle_obj.pendown()
	
	# Sets heading according to "direction_in_angle" and
	# goes forward according to the length.
	
	turtle_obj.setheading(direction_in_angle)
	turtle_obj.forward(length)


# Returns nothing. Draws an x shape, given the starting position,
# the length of the lines (4) of the x, a turtle object and the colour of the top left,
# top right, bottom left and the bottom right lines.

def draw_x(start_pos, length, line_colour_top_left, line_colour_top_right, line_colour_bottom_left, line_colour_bottom_right, turtle_obj = None):
	
	# Sets default turtle if turtle object is not passed.
	
	if not turtle_obj:
		
		turtle_obj = turtle.Turtle()
	
	# Top right line.
	
	turtle_obj.color(line_colour_top_right)
	draw_line(start_pos, length, 45, turtle_obj)
	
	# Top left line.
	
	turtle_obj.color(line_colour_top_left)
	draw_line(start_pos, length, 135, turtle_obj)
	
	# Bottom left line.
	
	turtle_obj.color(line_colour_bottom_left)
	draw_line(start_pos, length, 225, turtle_obj)
	
	# Bottom right line.
	
	turtle_obj.color(line_colour_bottom_right)
	draw_line(start_pos, length, 315, turtle_obj)
