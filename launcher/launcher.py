import tkinter as tk
from tkinter import ttk, messagebox
import requests
import webbrowser
import subprocess
import sys
from PIL import Image, ImageTk
import multiprocessing

class GameLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Launcher")
        self.root.geometry("400x600")

        # Favicon
        #favicon = tk.PhotoImage(file="favicon.png")
        #self.root.iconphoto(True, favicon)

        # Encabezado
        self.header_label = tk.Label(root, text="Game Launcher", font=("Helvetica", 16, "bold"))
        self.header_label.pack(pady=10)

        # Sección de usuario
        self.user_frame = tk.Frame(root)
        self.user_frame.pack(pady=20)

        self.username_label = tk.Label(self.user_frame, text="Username:")
        self.username_label.grid(row=0, column=0, padx=10, pady=5)

        self.username_entry = tk.Entry(self.user_frame)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)

        self.password_label = tk.Label(self.user_frame, text="Password:")
        self.password_label.grid(row=1, column=0, padx=10, pady=5)

        self.password_entry = tk.Entry(self.user_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        self.login_button = ttk.Button(self.user_frame, text="Login", command=self.login)
        self.login_button.grid(row=2, columnspan=2, pady=10)
        # Conectar la pulsación de la tecla "Enter" al evento de clic del botón "Login"
        self.root.bind('<Return>', lambda event=None: self.login())
        # Sección de opciones
        self.options_frame = tk.Frame(root)
        self.options_frame.pack(pady=20)

        self.logout_button = ttk.Button(self.options_frame, text="Logout", command=self.logout)
        self.logout_button.grid(row=0, column=0, padx=10, pady=5)

        self.save_score_button = ttk.Button(self.options_frame, text="Save Score", command=self.save_score)
        self.save_score_button.grid(row=0, column=1, padx=10, pady=5)

        self.top_scores_button = ttk.Button(self.options_frame, text="Top Scores", command=self.get_top_scores)
        self.top_scores_button.grid(row=0, column=2, padx=10, pady=5)

        # Notas de la versión
        self.notes_button = ttk.Button(root, text="Release Notes", command=self.open_release_notes)
        self.notes_button.pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        response = requests.post('http://127.0.0.1:5000/login', json={'username': username, 'password': password}, cookies={'session': 'cookie'})

        if response.status_code == 200 and response.json().get('success', False):
            print("Login successful.")

            # Iniciar el juego en un proceso separado
            game_process = multiprocessing.Process(target=self.start_game)
            game_process.start()

            # Cerrar el launcher y salir del programa principal
            self.root.destroy()
            sys.exit()
        else:
            print("Login failed. Please try again.")

    def start_game(self):
        # Ejecutar el menú en el nuevo proceso
        subprocess.run(["python", "menu.py"])

    def logout(self):
        response = requests.post('http://127.0.0.1:5000/logout', cookies={'session': 'cookie'})
        messagebox.showinfo("Logout", response.json())

    def save_score(self):
        score = input("Enter your score: ")
        response = requests.post('http://127.0.0.1:5000/save_score', json={'score': int(score)}, cookies={'session': 'cookie'})
        messagebox.showinfo("Save Score", response.json())

    def get_top_scores(self):
        response = requests.get('http://127.0.0.1:5000/get_top_scores')
        messagebox.showinfo("Top Scores", response.json())

    def open_release_notes(self):
        webbrowser.open("https://example.com/release_notes")  # Reemplaza con tu enlace de notas de versión

if __name__ == "__main__":
    root = tk.Tk()
    launcher = GameLauncher(root)
    root.mainloop()
