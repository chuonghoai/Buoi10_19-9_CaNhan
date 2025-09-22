import tkinter as tk
from PIL import Image, ImageTk
import random
import math

class node:
    def __init__(self, n=8):
        self.n = n
        self.state = []
        self.cost = 0
        
    def random(self):
        self.state = [random.randint(0, self.n-1) for _ in range(self.n)]

    def cost_conflict(self):
        cnt = 0
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if self.state[i] == self.state[j]:
                    cnt += 1
        return cnt

    def create_child(self):
        child = node()
        child.state = self.state[:]
        col = random.randint(0, self.n - 1)
        row = random.randint(0, self.n - 1)
        
        while child.state[row] == col:
            col = random.randint(0, self.n - 1)

        child.state[row] = col
        return child
    
class Image_X:
    def __init__(self):
        self.white = ImageTk.PhotoImage(Image.open("./whiteX.png").resize((60, 60)))
        self.black = ImageTk.PhotoImage(Image.open("./blackX.png").resize((60, 60)))
        self.null = tk.PhotoImage(width=1, height=1)
        
class board:
    def __init__(self, root):  #n: số lượng quân xe (defult = 8)
        self.root = root
        root.title("Simulated Anneling")
        root.config(bg="lightgray")
        self.image = Image_X()
        self.n = node().n
        self.frame_left = self.draw_frame(0, 0)
        self.frame_right = self.draw_frame(0, 1)
        self.buttons_left = self.create_board(self.frame_left)
        self.buttons_right = self.create_board(self.frame_right)

        self.SA_btn = tk.Button(self.root, text="Simulated Anneling")
        self.SA_btn.grid(row=1, column=1, pady=10)
        self.HC_btn = tk.Button(self.root, text="Hill Climbing")
        self.HC_btn.grid(row=2, column=1, pady=10)
        
        self.btn_reset = tk.Button(self.root, text="Reset", bg="red", fg="white", command=self.reset)
        self.btn_reset.grid(row=2, column=0, pady=10)
        
        self.path_btn = tk.Button(self.root, text="Path")
        self.path_btn.grid(row=1, column=0, pady=10)
        
    def draw_frame(self, row, col):
        frame = tk.Frame(self.root, bg="white", relief="solid", borderwidth=1)
        frame.grid(column=col, row=row, padx=10, pady=10)
        return frame
    
    def create_board(self, frame):
        buttons = []
        for i in range(self.n):
            row = []
            for j in range(self.n):
                color = "white" if (i + j) % 2 == 0 else "black"
                img = self.image.null                
                btn = tk.Button(frame, image=img, width=60, height=60, bg=color,
                                relief="flat", borderwidth=0, highlightthickness=0)
                btn.grid(row = i, column = j, padx=1, pady=1)
                row.append(btn)
            buttons.append(row)
        return buttons

    def draw_xa(self,  buttons, state=[]):
        for i in range(self.n):
            for j in range(self.n):
                buttons[i][j].config(image=self.image.null)
        
        for row, col in enumerate(state):
            color = "white" if (row + col) % 2 == 0 else "black"
            img = self.image.white if color == "black" else self.image.black
            buttons[row][col].config(image=img)
    
    def reset(self):
        self.draw_xa(self.buttons_left)
        self.draw_xa(self.buttons_right)

class algorithm(board):
    def __init__(self, root):
        super().__init__(root)
        self.SA_btn.config(command=self.SA_btn_algorithm)
        self.HC_btn.config(command=self.HC_btn_algorithm)
        self.path_btn.config(command=self.path)
        self.path_state = []
        self.state = node()
        self.T = 100
        self.T_min = 1e-6
        self.alpha = 0.99
        
    def SimulatedAnnealing(self):
        state = self.state
        state.random()
        state.cost = state.cost_conflict()
        self.path_state = []
        
        while self.T > self.T_min:
            self.path_state.append(state.state[:])
            
            if state.cost == 0:
                return state.state
            
            state_child = state.create_child()
            state_child.cost = state_child.cost_conflict()
            delta = state_child.cost - state.cost
            
            if delta <= 0:
                state = state_child
            else:
                p = math.exp(-delta / self.T)
                if random.random() < p:
                    state = state_child
            self.T *= self.alpha
        return None

    def SA_btn_algorithm(self):
        self.draw_xa(self.buttons_left)
        self.draw_xa(self.buttons_right)
        self.state = node()
        self.T = 100
        
        state = None
        while state is None:
            state = self.SimulatedAnnealing()
        
        self.draw_xa(self.buttons_right, state)

    def HillClimbing(self):
        state = node()
        state.state = []
        self.path_state = []
        
        for row in range(state.n):
            child_col = None
            child_cost = 9999

            for col in range(state.n):
                child_state = state.state[:] + [col]

                cnt = 0
                for i in range(row):
                    if child_state[i] == col:
                        cnt += 1

                if cnt <= child_cost:
                    child_cost = cnt
                    child_col = col

            state.state.append(child_col)
            self.path_state.append(state.state[:])

        return state.state

    def HC_btn_algorithm(self):
        self.draw_xa(self.buttons_left)
        self.draw_xa(self.buttons_right)
        self.state = node()
        
        state = None
        while state is None:
            state = self.HillClimbing()
        self.draw_xa(self.buttons_right, state)

    def path(self):
        for state in self.path_state:
            print(state)
            self.draw_xa(self.buttons_left, state)
            self.frame_left.update()
            self.root.after(200)

def run_app():
    root = tk.Tk()
    app = algorithm(root)

    root.mainloop()

if __name__ == "__main__":
    run_app()