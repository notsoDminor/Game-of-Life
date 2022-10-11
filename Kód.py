import tkinter as tk
import numpy as np
from tkinter import filedialog as fd
win = tk.Tk()

WIDTH = 500
HEIGHT = 500
vs = 10 #veľkosť bunky
abvs = vs
cells = np.zeros((WIDTH // vs, HEIGHT // vs), dtype = int) #dvojrozmerný zoznam
cells_new = np.zeros((WIDTH // vs, HEIGHT // vs), dtype = int)

def create_stage():
    for x in range(WIDTH // vs):
        canvas.create_line(x * vs, 0, x * vs, HEIGHT)
    for y in range(HEIGHT // vs):
        canvas.create_line(0, y * vs, WIDTH, y * vs)

def get_neighbours(x, y):
    total = 0
    if x > 0:
        total += cells[x - 1, y]
    if x > 0 and y > 0:
        total += cells[x - 1, y - 1]
    if x < (WIDTH // abvs - 1) and y < (HEIGHT // abvs - 1):
        total += cells[x + 1, y + 1]
    if x > 0 and y < (HEIGHT // abvs - 1):
        total += cells[x - 1, y + 1]
    if x < (WIDTH // abvs - 1):
        total += cells[x + 1, y]
    if y > 0:
        total += cells[x, y - 1]
    if y < (HEIGHT // abvs - 1):
        total += cells[x, y + 1]
    if y > 0 and x < (WIDTH // abvs - 1):
        total += cells[x + 1, y - 1]
    return total

def recalculate():
    global cells, cells_new
    for y in range(HEIGHT // abvs):
        for x in range(WIDTH // abvs):
            temp = get_neighbours(x, y)
            if temp == 2 and cells[x, y] == 1:
                cells_new[x, y] = 1
            if temp == 3:
                cells_new[x, y] = 1
            if temp < 2 or temp > 3:
                cells_new[x, y] = 0
    cells = cells_new.copy()
    canvas.delete("all")
    create_stage()
    redraw_cell()

def slider_changer(e):
    global vs
    canvas.delete("all")
    vs = w.get()
    create_stage()
    redraw_cell()

def create_cell(e):
    global cells
    tx = e.x // vs
    ty = e.y // vs
    x = tx * vs
    y = ty * vs
    canvas.create_oval(x + vs//5, y + vs//5, x+vs - vs//5, y+vs - vs//5, fill = "purple")
    cells[tx, ty] = 1
    #print(get_neighbours(tx, ty))
    #print(cells)

def redraw_cell():
    for x in range(WIDTH // vs):
        for y in range(HEIGHT // vs):
            if cells[x, y] == 1:
                canvas.create_oval(x * vs + vs//5, y * vs + vs//5, x * vs + vs - vs//5, y * vs + vs - vs//5, fill = "purple")

def loop():
    if b_stop.config("text")[4] == "STOP":
        recalculate()
        win.after(300, loop)

def start_the_loop():
    if b_stop.config("text")[4] == "START":
        b_stop.config(text = "STOP")
        loop()
    else:
        b_stop.config(text = "START")

def openfile():
    global cells, cells_new
    file = fd.askopenfile()
    new_input = []
    counter = 0
    for line in file:
        line = line.split()
        for character in line:
            new_input.append(character)
            counter += 1

    if counter <= 2500:
        for i in range(counter):
            for j in range(len(new_input[i])):
                if new_input[i][j] == "1":
                    cells_new[i, j] = 1
                else:
                    cells_new[i, j] = 0
        cells = cells_new.copy()
        canvas.delete("all")
        create_stage()
        redraw_cell()
    else:
        print("ERROR: File size must be less than 50x50")


canvas = tk.Canvas(width = WIDTH, height = HEIGHT, bg = "white")
canvas.pack()

w = tk.Scale(win, from_= 10, to = 50, orient = "horizontal", command = slider_changer, length = 500)
w.pack()

b_next_gen = tk.Button(win, text = "NEXT GENERATION", command = recalculate)
b_next_gen.pack(side = tk.LEFT)

b_file = tk.Button(win, text = "OPEN MY GAME FILE", command = openfile)
b_file.pack(side = tk.RIGHT)

b_stop = tk.Button(win, text = "START", command = start_the_loop)
b_stop.pack(side = tk.BOTTOM)

create_stage()
canvas.bind("<Button-1>", create_cell)

win.mainloop()
