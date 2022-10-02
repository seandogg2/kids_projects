import turtle as tt


def init(low_x=-10, low_y=-10, high_x=10, high_y=10):
    tt.setworldcoordinates(low_x, low_y, high_x, high_y)
    tt.speed(0)
    tt.tracer(None)



def line(pnt1, pnt2):
    tt.penup()
    tt.goto(pnt1[0], pnt1[1])
    tt.pendown()
    tt.goto(pnt2[0], pnt2[1])


def Jonathan_test():
    init()
    for i in range(11):
        line((10-i, 0), (0, i))
        line((-10+i, 0), (0, i))
        line((-10+i, 0), (0, -i))
        line((10-i, 0), (0, -i))


def init_room_test():
    init(0, 0, 200, 200)
    draw_room()
    draw_left()
    draw_right()
    draw_front()


def square():
    line((0, 190), (190, 190))
    line((190,190),(190,0))
    line((190,0),(0,0))
    line((0,0),(0,190))


def smallsquare():
    line((40, 40), (40, 150))
    line((40,150), (150,150))
    line((150,150), (150,40))
    line((150,40),(40,40))


def draw_room():
    square()
    smallsquare()
    line((40,150),(0,190))
    line((150, 150),(190,190))
    line((150,40),(190,0))
    line((40,40),(0,0))


def draw_right():
    pass


def draw_left():
    pass


def draw_front():
    pass


if __name__ == '__main__':
    init_room_test()
    input()
