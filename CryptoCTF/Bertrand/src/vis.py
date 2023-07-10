def sox(n, d):
	x, y, t = 0, 0, d
	for s in range(n - 1):
		u = 1 & t // 2
		v = 1 & t ^ u
		x, y = spin(2**s, x, y, u, v)
		x += 2**s * u
		y += 2**s * v
		t = t // 4
	return x, y

def spin(n, x, y, u, v):
	if v == 0:
		if u == 1:
			x = n - 1 - x
			y = n - 1 - y
		x, y = y, x
	return x, y

n = 256
def gen():
    for i in range(n**2):
        yield sox(n, i)
	
import turtle

def draw_path(_, square_size):
    screen = turtle.Screen()
    screen.setup(800, 800)

    turtle.penup()
    turtle.speed(0)

    for point in gen():
        x = point[0] * square_size + square_size / 2
        y = point[1] * square_size + square_size / 2

        off = 10 * square_size
        turtle.goto(x - off, y - off)
        turtle.pendown()
        turtle.dot(2)

    turtle.hideturtle()
    turtle.done()

draw_path(..., 4)