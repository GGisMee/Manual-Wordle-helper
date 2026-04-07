import customtkinter as ctk
from engine import solve_wordle


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 1. Global Skalning (Viktigast)
        ctk.set_appearance_mode("dark")
        ctk.set_widget_scaling(1.2)  # Förstorar allt 200%
        ctk.set_window_scaling(1.4)  # Förstorar själva fönstret

        self.title("Wordle Solver")
        self.geometry("800x1000")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)

        # 2. Komponenter med JÄTTE-text
        # Titel
        self.label = ctk.CTkLabel(
            self, text="WORDLE SOLVER", font=("Arial", 40, "bold")
        )
        self.label.grid(row=0, column=0, pady=40, sticky="ew")

        # Grå bokstäver
        self.used_input = ctk.CTkEntry(
            self, placeholder_text="Grå bokstäver...", height=70, font=("Arial", 24)
        )
        self.used_input.grid(row=1, column=0, padx=50, pady=15, sticky="ew")

        # Gröna bokstäver
        self.green_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.green_frame.grid(row=2, column=0, pady=10)
        self.greens = []
        for i in range(5):
            e = ctk.CTkEntry(
                self.green_frame,
                width=100,
                height=100,
                font=("Arial", 32, "bold"),
                justify="center",
                fg_color="#1e5230",  # A shade of green
            )
            e.grid(row=0, column=i, padx=10)
            self.greens.append(e)

        # Gula bokstäver
        self.yellow_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.yellow_frame.grid(row=3, column=0, pady=10)

        self.yellows = []
        for i in range(5):
            e = ctk.CTkEntry(
                self.yellow_frame,
                width=100,
                height=100,
                font=("Arial", 32, "bold"),
                justify="center",
                fg_color="#6b7026",  # A shade of yellow
            )
            e.grid(row=0, column=i, padx=10)
            self.yellows.append(e)

        # Knapp
        self.solve_btn = ctk.CTkButton(
            self,
            text="HITTA ORD",
            command=self.calculate,
            height=80,
            font=("Arial", 28, "bold"),
            fg_color="#27ae60",
        )
        self.solve_btn.grid(row=4, column=0, padx=50, pady=20, sticky="ew")

        # Resultat
        self.res = ctk.CTkTextbox(self, font=("Consolas", 22), border_width=2)
        self.res.grid(row=5, column=0, padx=50, pady=(0, 50), sticky="nsew")

    def calculate(self):
        green_data = {i + 1: self.greens[i].get().lower() for i in range(5)}
        yellow_data = {i + 1: self.yellows[i].get().lower() for i in range(5)}
        results = solve_wordle(self.used_input.get(), yellow_data, green_data)

        self.res.delete("1.0", "end")
        if not results:
            self.res.insert("end", "❌ Inga träffar.")
            return

        # Inställningar
        num_cols = 4
        col_width = 15
        num_items = len(results)

        # Beräkna rader som behövs för vertikal fyllning
        num_rows = (num_items + num_cols - 1) // num_cols

        output = f"Antal ord: {num_items}\n"
        output += "─" * (num_cols * col_width) + "\n\n"

        for r in range(num_rows):
            line = ""
            for c in range(num_cols):
                # Beräkna index för att hämta ord vertikalt
                index = r + (c * num_rows)
                if index < num_items:
                    word = results[index].upper()
                    line += f"{word:<{col_width}}"
            output += line + "\n"

        self.res.insert("end", output)


if __name__ == "__main__":
    App().mainloop()
