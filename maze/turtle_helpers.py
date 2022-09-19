import turtle as tt


def init(low_x=-10, low_y=-10, high_x=10, high_y=10):
    tt.setworldcoordinates(low_x, low_y, high_x, high_y)
    tt.speed(0)


def line(pnt1, pnt2):
    tt.penup()
    tt.goto(pnt1[0], pnt1[1])
    tt.pendown()
    tt.goto(pnt2[0], pnt2[1])


def Jonathan_test():
    init()
    for i in range(11):
        line((10-i,0), (0,i))
        line((-10+i,0),(0,i))
        line((-10+i,0),(0,-i))
        line((10-i,0), (0,-i))