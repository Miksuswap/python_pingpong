from tkinter import *
import random

WIDTH = 900
HEIGHT = 300
PAD_W = 10
PAD_H = 100
BALL_RADIUS = 40
PLAYER_1_SCORE = 0
PLAYER_2_SCORE = 0
INITIAL_SPEED = 20

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
p_1_text = c.create_text(WIDTH - WIDTH / 6, PAD_H/4,
                         text=PLAYER_1_SCORE,
                         font='Arial 20',
                         fill='aqua')
p_2_text = c.create_text(WIDTH / 6, PAD_H/4,
                         text=PLAYER_2_SCORE,
                         font='Arial 20',
                         fill='aqua')

PAD_SPEED = 20
LEFT_PAD_SPEED = 0
RIGHT_PAD_SPEED = 0

BALL_SPEED_UP = 1.00
BALL_MAX_SPEED = 30
BALL_X_SPEED = 20
BALL_Y_SPEED = 20

right_line_distance = WIDTH - PAD_W

def update_score(player):
    global PLAYER_1_SCORE, PLAYER_2_SCORE
    if player == 'right':
        PLAYER_1_SCORE+=1
        c.itemconfig(p_1_text, text=PLAYER_1_SCORE)
    else:
        PLAYER_2_SCORE+=1
        c.itemconfig(p_2_text, text=PLAYER_2_SCORE)

def spawn_ball():
    global BALL_X_SPEED
    c.coords(BALL,WIDTH/2-BALL_RADIUS/2,
             HEIGHT/2 - BALL_RADIUS/2,
             WIDTH/2+BALL_RADIUS/2,
             HEIGHT/2+BALL_RADIUS/2)
    BALL_X_SPEED = -(BALL_X_SPEED * -INITIAL_SPEED)/abs(BALL_X_SPEED)
    


def bounce(action):
    global BALL_X_SPEED, BALL_Y_SPEED
    if action == 'strike':
        BALL_Y_SPEED = random.randrange(-10, 11)  
        if abs(BALL_X_SPEED) < BALL_MAX_SPEED:
            BALL_X_SPEED *= -BALL_SPEED_UP
        else:
            BALL_X_SPEED = -BALL_X_SPEED
    else:
        BALL_Y_SPEED = -BALL_Y_SPEED

def move_ball():
    global BALL_X_SPEED, BALL_Y_SPEED
    ball_left, ball_top, ball_right, ball_bottom = c.coords(BALL)
    ball_center = (ball_top + ball_bottom) / 2

    if ball_right + BALL_X_SPEED < right_line_distance and ball_left + BALL_X_SPEED > PAD_W:
        c.move(BALL, BALL_X_SPEED, BALL_Y_SPEED)

    elif ball_right >= right_line_distance or ball_left <= PAD_W:
        if ball_right > WIDTH / 2:
            right_pad_coords = c.coords(RIGHT_PAD)
            if right_pad_coords[1] < ball_center < right_pad_coords[3]:
                bounce('strike')
            else:
                update_score('left')
                spawn_ball()
        else:
            left_pad_coords = c.coords(LEFT_PAD)
            if left_pad_coords[1] < ball_center < left_pad_coords[3]:
                bounce('strike')
            else:
                update_score('right')
                spawn_ball()
    else:
        if ball_right > WIDTH / 2:
            c.move(BALL, right_line_distance - ball_right, BALL_Y_SPEED)
        else:
            c.move(BALL, -ball_left + PAD_W, BALL_Y_SPEED)


    if ball_top + BALL_Y_SPEED < 0 or ball_bottom + BALL_Y_SPEED > HEIGHT:
        bounce('ricochet')

def move_pads():
    global LEFT_PAD_SPEED, RIGHT_PAD_SPEED
    PADS = {LEFT_PAD: LEFT_PAD_SPEED,
            RIGHT_PAD: RIGHT_PAD_SPEED}
    for pad in PADS:
        c.move(pad, 0, PADS[pad])
        if c.coords(pad)[1] < 0:
            c.move(pad, 0, -c.coords(pad)[1])
        elif c.coords(pad)[3] > HEIGHT:
            c.move(pad, 0, HEIGHT - c.coords(pad)[3])

def main():
    move_ball()
    move_pads()
    root.after(30, main)

c.focus_set()

def movement_handler(event):
    global LEFT_PAD_SPEED, RIGHT_PAD_SPEED
    if event.keysym == 'w':
        LEFT_PAD_SPEED = -PAD_SPEED
    elif event.keysym == 's':
        LEFT_PAD_SPEED = PAD_SPEED
    elif event.keysym == "Up":
        RIGHT_PAD_SPEED = -PAD_SPEED
    elif event.keysym == "Down":
        RIGHT_PAD_SPEED = PAD_SPEED

def stop_pad(event):
    global LEFT_PAD_SPEED, RIGHT_PAD_SPEED
    if event.keysym in ('w', 's'):
        LEFT_PAD_SPEED = 0
    elif event.keysym in ('Up', 'Down'):
        RIGHT_PAD_SPEED = 0

c.bind("<KeyPress>", movement_handler)
c.bind("<KeyRelease>", stop_pad)

main()
root.mainloop()
