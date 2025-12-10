from tkinter import *   # Tuodaan Tkinter-kirjasto graafista käyttöliittymää varten
import random           # Tuodaan random, jotta pallon kimpoaminen voi olla satunnainen

# --- PELIN MITAT JA ASETUKSET ---
WIDTH = 900             # Ikkunan leveys
HEIGHT = 300            # Ikkunan korkeus
PAD_W = 10              # Mailan leveys
PAD_H = 100             # Mailan korkeus
BALL_RADIUS = 40        # Pallon halkaisija
PLAYER_1_SCORE = 0      # Pelaaja 1:n pisteet
PLAYER_2_SCORE = 0      # Pelaaja 2:n pisteet
INITIAL_SPEED = 20      # Pallon alkunopeus

# --- TKINTER-IKKUNA ---
root = Tk()             # Luodaan pääikkuna
root.title("Ping-pong") # Ikkunan otsikko

# --- CANVAS, jossa peli piirretään ---
c = Canvas(root, width=WIDTH, height=HEIGHT, background="#008B8B")  # Pelialusta
c.pack()                        # Näytetään canvas

# --- PIIRRETÄÄN KENTÄN LINJAT ---
c.create_line(PAD_W, 0, PAD_W, HEIGHT, fill="white")                  # Vasemman reunan viiva
c.create_line(WIDTH - PAD_W, 0, WIDTH - PAD_W, HEIGHT, fill="white")  # Oikean reunan viiva
c.create_line(WIDTH / 2, 0, WIDTH / 2, HEIGHT, fill="white")          # Keskiviiva

# --- LUODAAN PALLON GRAFIIKKA ---
BALL = c.create_oval(WIDTH / 2 - BALL_RADIUS / 2,
                     HEIGHT / 2 - BALL_RADIUS / 2,
                     WIDTH / 2 + BALL_RADIUS / 2,
                     HEIGHT / 2 + BALL_RADIUS / 2,
                     fill="#FF4500")    # Pallon väri

# --- LUODAAN MAILAT ---
LEFT_PAD = c.create_line(PAD_W / 2, HEIGHT / 2 - PAD_H / 2,
                         PAD_W / 2, HEIGHT / 2 + PAD_H / 2,
                         width=PAD_W, fill="#DA70D6")    # Vasemman pelaajan maila

RIGHT_PAD = c.create_line(WIDTH - PAD_W / 2, HEIGHT / 2 - PAD_H / 2,
                          WIDTH - PAD_W / 2, HEIGHT / 2 + PAD_H / 2,
                          width=PAD_W, fill="#DA70D6")   # Oikean pelaajan maila

# --- PISTETILASTOT KANKAALLE ---
p_1_text = c.create_text(WIDTH - WIDTH / 6, PAD_H/4,
                         text=PLAYER_1_SCORE,
                         font='Arial 20',
                         fill='aqua')    # Oikean pelaajan pisteet

p_2_text = c.create_text(WIDTH / 6, PAD_H/4,
                         text=PLAYER_2_SCORE,
                         font='Arial 20',
                         fill='aqua')    # Vasemman pelaajan pisteet

# --- MAILOJEN NOPEUS ASETUKSET ---
PAD_SPEED = 20        # Liikkumisnopeus
LEFT_PAD_SPEED = 0    # Vasemman mailan hetkellinen nopeus
RIGHT_PAD_SPEED = 0   # Oikean mailan hetkellinen nopeus

# --- PALLON FYYSIIKKA ---
BALL_SPEED_UP = 1.00     # Pallon nopeuden kasvukerroin mailasta kimpoessa
BALL_MAX_SPEED = 30       # Maksiminopeus
BALL_X_SPEED = 20         # X-suunnan nopeus
BALL_Y_SPEED = 20         # Y-suunnan nopeus

right_line_distance = WIDTH - PAD_W   # Oikean reunan mailan X-sijainti

# --- FUNKTIO: päivitää pisteet ---
def update_score(player):
    global PLAYER_1_SCORE, PLAYER_2_SCORE
    if player == 'right':       # Jos oikea pelaaja menettää pisteen → vasen saa pisteen
        PLAYER_1_SCORE+=1
        c.itemconfig(p_1_text, text=PLAYER_1_SCORE)
    else:                       # Jos vasen pelaaja menettää pisteen
        PLAYER_2_SCORE+=1
        c.itemconfig(p_2_text, text=PLAYER_2_SCORE)

# --- FUNKTIO: palauttaa pallon keskelle ---
def spawn_ball():
    global BALL_X_SPEED
    # Asetetaan pallon koordinaatit takaisin keskelle
    c.coords(BALL,WIDTH/2-BALL_RADIUS/2,
             HEIGHT/2 - BALL_RADIUS/2,
             WIDTH/2+BALL_RADIUS/2,
             HEIGHT/2+BALL_RADIUS/2)
    # Lähetetään pallo liikkeelle oikeaan suuntaan
    BALL_X_SPEED = -(BALL_X_SPEED * -INITIAL_SPEED)/abs(BALL_X_SPEED)

# --- FUNKTIO: pallo kimpoaa ---
def bounce(action):
    global BALL_X_SPEED, BALL_Y_SPEED
    if action == 'strike':             # Pallon kimpoaminen mailasta
        BALL_Y_SPEED = random.randrange(-10, 11)   # Satunnainen kulma
        if abs(BALL_X_SPEED) < BALL_MAX_SPEED:     # Nostetaan nopeutta
            BALL_X_SPEED *= -BALL_SPEED_UP
        else:
            BALL_X_SPEED = -BALL_X_SPEED           # Maksiminopeudessa vain suunnan vaihto
    else:
        BALL_Y_SPEED = -BALL_Y_SPEED               # Kimpoaminen ylä-/alareunasta

# --- FUNKTIO: liikuttaa palloa ---
def move_ball():
    global BALL_X_SPEED, BALL_Y_SPEED
    ball_left, ball_top, ball_right, ball_bottom = c.coords(BALL)  # Pallon rajat
    ball_center = (ball_top + ball_bottom) / 2                      # Pallon keskipiste

    # Normaalitilanne: pallo liikkuu ilman törmäystä
    if ball_right + BALL_X_SPEED < right_line_distance and ball_left + BALL_X_SPEED > PAD_W:
        c.move(BALL, BALL_X_SPEED, BALL_Y_SPEED)

    # Pallo osuu mailaan
    elif ball_right >= right_line_distance or ball_left <= PAD_W:
        if ball_right > WIDTH / 2:   # Oikea maila
            right_pad_coords = c.coords(RIGHT_PAD)
            if right_pad_coords[1] < ball_center < right_pad_coords[3]:
                bounce('strike')      # Osui mailaan
            else:
                update_score('left')  # Ohi → vasen saa pisteen
                spawn_ball()
        else:                         # Vasen maila
            left_pad_coords = c.coords(LEFT_PAD)
            if left_pad_coords[1] < ball_center < left_pad_coords[3]:
                bounce('strike')
            else:
                update_score('right') # Ohi → oikea saa pisteen
                spawn_ball()
    else:
        # Pallo osuu kentän reunaan vajaasti → oikaistaan
        if ball_right > WIDTH / 2:
            c.move(BALL, right_line_distance - ball_right, BALL_Y_SPEED)
        else:
            c.move(BALL, -ball_left + PAD_W, BALL_Y_SPEED)

    # Ylä- ja alareunan kimpoaminen
    if ball_top + BALL_Y_SPEED < 0 or ball_bottom + BALL_Y_SPEED > HEIGHT:
        bounce('ricochet')

# --- FUNKTIO: liikuttaa mailoja ---
def move_pads():
    global LEFT_PAD_SPEED, RIGHT_PAD_SPEED
    PADS = {LEFT_PAD: LEFT_PAD_SPEED,
            RIGHT_PAD: RIGHT_PAD_SPEED}

    for pad in PADS:
        c.move(pad, 0, PADS[pad])   # Liikutetaan mailaa
        if c.coords(pad)[1] < 0:    # Estetään mailaa menemästä yli ylärajan
            c.move(pad, 0, -c.coords(pad)[1])
        elif c.coords(pad)[3] > HEIGHT:  # Estetään alarajan ylitys
            c.move(pad, 0, HEIGHT - c.coords(pad)[3])

# --- PÄÄSILMUKKA: päivittää peliä 30 ms välein ---
def main():
    move_ball()   # Liikuta palloa
    move_pads()   # Liikuta mailoja
    root.after(30, main)  # Kutsu itseään uudelleen

c.focus_set()     # Canvas saa näppäimistöfokuksen

# --- NÄPPÄIMISTÖOHJAUKSET: aloita liike ---
def movement_handler(event):
    global LEFT_PAD_SPEED, RIGHT_PAD_SPEED
    if event.keysym == 'w':        # Vasemman mailan ylös
        LEFT_PAD_SPEED = -PAD_SPEED
    elif event.keysym == 's':      # Vasemman mailan alas
        LEFT_PAD_SPEED = PAD_SPEED
    elif event.keysym == "Up":     # Oikean mailan ylös
        RIGHT_PAD_SPEED = -PAD_SPEED
    elif event.keysym == "Down":   # Oikean mailan alas
        RIGHT_PAD_SPEED = PAD_SPEED

# --- NÄPPÄIMEN PÄÄSTÖ: pysäytä maila ---
def stop_pad(event):
    global LEFT_PAD_SPEED, RIGHT_PAD_SPEED
    if event.keysym in ('w', 's'):
        LEFT_PAD_SPEED = 0
    elif event.keysym in ('Up', 'Down'):
        RIGHT_PAD_SPEED = 0

# --- SIDOTAAN NÄPPÄIMET ---
c.bind("<KeyPress>", movement_handler)  # Kun näppäin painetaan
c.bind("<KeyRelease>", stop_pad)        # Kun näppäin päästetään ylös

main()               # Käynnistetään peli
root.mainloop()      # Tkinterin pääsilmukka (ikkuna on auki)
