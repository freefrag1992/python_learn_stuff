import tkinter as tk
import copy

PIXEL_SIZE = 20
GRID_SIZE = 16

# Standardfarben für Palette
PALETTE_COLORS = [
    "black", "white", "red", "green", "blue", "yellow",
    "orange", "purple", "pink", "cyan", "brown", "gray"
]

class PixelMatrix:
    def __init__(self, master):
        self.master = master
        self.master.title("20x20 Pixel Matrix")

        # Historie für Undo/Redo
        self.history = []
        self.history_index = -1

        # Farben & aktuelle Farbe
        self.current_color = "black"
        self.drawing = False

        # Buttons für Undo, Redo, Reset
        top_frame = tk.Frame(master)
        top_frame.pack()
        tk.Button(top_frame, text="Undo", command=self.undo).pack(side="left")
        tk.Button(top_frame, text="Redo", command=self.redo).pack(side="left")
        tk.Button(top_frame, text="Reset", command=self.reset).pack(side="left")

        # Farbpalette
        palette_frame = tk.Frame(master)
        palette_frame.pack()
        for color in PALETTE_COLORS:
            btn = tk.Button(palette_frame, bg=color, width=2, command=lambda c=color: self.set_color(c))
            btn.pack(side="left", padx=2)

        # Canvas
        self.canvas = tk.Canvas(master, width=PIXEL_SIZE*GRID_SIZE, height=PIXEL_SIZE*GRID_SIZE)
        self.canvas.pack()

        # Matrix initialisieren (speichert Index in Palette)
        self.matrix = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

        # Rechtecke zeichnen
        self.rects = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                x1, y1 = j*PIXEL_SIZE, i*PIXEL_SIZE
                x2, y2 = x1 + PIXEL_SIZE, y1 + PIXEL_SIZE
                self.rects[i][j] = self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="gray")

        # Mausbindung
        self.canvas.bind("<Button-1>", lambda e: self.start_draw(e))
        self.canvas.bind("<B1-Motion>", lambda e: self.draw_pixel(e))
        self.canvas.bind("<ButtonRelease-1>", lambda e: self.end_draw())

        self.canvas.bind("<Button-3>", lambda e: self.start_draw(e, erase=True))
        self.canvas.bind("<B3-Motion>", lambda e: self.draw_pixel(e, erase=True))
        self.canvas.bind("<ButtonRelease-3>", lambda e: self.end_draw())

    def set_color(self, color):
        self.current_color = color

    def start_draw(self, event, erase=False):
        self.drawing = True
        self.erase = erase
        self.start_matrix = copy.deepcopy(self.matrix)  # Matrix speichern für Undo
        self.draw_pixel(event, erase=erase, save_history=False)

    def draw_pixel(self, event, erase=False, save_history=True):
        if not self.drawing:
            return
        col = event.x // PIXEL_SIZE
        row = event.y // PIXEL_SIZE
        if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
            color = "white" if erase else self.current_color
            if self.matrix[row][col] != color:
                self.matrix[row][col] = color
                self.canvas.itemconfig(self.rects[row][col], fill=color)

    def end_draw(self):
        if self.drawing:
            self.history = self.history[:self.history_index+1]
            self.history.append(self.start_matrix)
            self.history_index += 1
            self.drawing = False

    def undo(self):
        if self.history_index >= 0:
            self.matrix = copy.deepcopy(self.history[self.history_index])
            self.history_index -= 1
            self.update_canvas()

    def redo(self):
        if self.history_index + 1 < len(self.history):
            self.history_index += 1
            self.matrix = copy.deepcopy(self.history[self.history_index])
            self.update_canvas()

    def reset(self):
        self.history = self.history[:self.history_index+1]
        self.history.append(copy.deepcopy(self.matrix))
        self.history_index += 1
        self.matrix = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.update_canvas()

    def update_canvas(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                color = self.matrix[i][j] if self.matrix[i][j] else "white"
                self.canvas.itemconfig(self.rects[i][j], fill=color)

if __name__ == "__main__":
    root = tk.Tk()
    app = PixelMatrix(root)
    root.mainloop()
