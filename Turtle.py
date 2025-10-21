from tkinter import *

WIDTH = 900
HEIGHT = 300
PAD_W = 10
PAD_H = 100
BALL_RADIUS = 40

root = Tk()
root.title("Ping-pong")

c = Canvas(root, width=WIDTH, height=HEIGHT, background="#008B8B")
c.pack()

c.create_line(PAD_W, 0, PAD_W, HEIGHT, fill="white")
c.create_line(WIDTH - PAD_W, 0, WIDTH - PAD_W, HEIGHT, fill="white")
c.create_line(WIDTH / 2, 0, WIDTH / 2, HEIGHT, fill="white")

BALL = c.create_oval(WIDTH / 2 - BALL_RADIUS / 2,
                     HEIGHT / 2 - BALL_RADIUS / 2,
                     WIDTH / 2 + BALL_RADIUS / 2,
                     HEIGHT / 2 + BALL_RADIUS / 2,
                     fill="#FF4500")

LEFT_PAD = c.create_line(PAD_W / 2, HEIGHT / 2 - PAD_H / 2,
                         PAD_W / 2, HEIGHT / 2 + PAD_H / 2,
                         width=PAD_W, fill="#DA70D6")

RIGHT_PAD = c.create_line(WIDTH - PAD_W / 2, HEIGHT / 2 - PAD_H / 2,
                          WIDTH - PAD_W / 2, HEIGHT / 2 + PAD_H / 2,
                          width=PAD_W, fill="#DA70D6")
PAD_SPEED = 20
LEFT_PAD_SPEED = 0
RIGHT_PAD_SPEED = 0


BALL_X_CHANGE = 5
BALL_Y_CHANGE = 3

def move_ball():
    global BALL_X_CHANGE, BALL_Y_CHANGE
    c.move(BALL, BALL_X_CHANGE, BALL_Y_CHANGE)
    ball_left, ball_top, ball_right, ball_bottom = c.coords(BALL)
    
    if ball_top <= 0 or ball_bottom >= HEIGHT:
        BALL_Y_CHANGE = -BALL_Y_CHANGE

    if ball_left <= 0 or ball_right >= WIDTH:
        BALL_X_CHANGE = -BALL_X_CHANGE

def move_pads():
    PADS = {LEFT_PAD:LEFT_PAD_SPEED,
            RIGHT_PAD:RIGHT_PAD_SPEED}
    for pad in PADS:
        c.move(pad, 0, PADS[pad])
        if c.coords(pad) [1]< 0:
            c.move(pad, 0, -c.coords(pad)[1])
        elif c.coords(pad)[3]>HEIGHT:
            c.move(pad, 0, HEIGHT - c.coords(pad)[3])


def main():
    move_ball()
    move_pads()
    root.after(30, main)
c.focus_set()

def moveent_handler(event):
    global LEFT_PAD_SPEED, RIGHT_PAD_SPEED
    if event.keysym == 'w':
        LEFT_PAD_SPEED = -PAD_SPEED
    elif event.keysym == 's':
        LEFT_PAD_SPEED = PAD_SPEED
    elif event.keysym == "Up":
        RIGHT_PAD_SPEED = -PAD_SPEED
    elif event.keysym == "Down":
        RIGHT_PAD_SPEED = PAD_SPEED
c.bind("<KeyPress>", moveent_handler)

main()
root.mainloop()

