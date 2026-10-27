import tkinter as tk
import subprocess
import os
import sys

class WelcomeApp:
    def __init__(self, window):
        self.window = window
        self.window.title("EchoHands - Welcome")
        self.window.geometry("500x700")
        
        # Soft Gradient-like Background (Solid color for standard Tkinter)
        # Using a soft teal/blue shade
        self.bg_color = "#E0F7FA" 
        self.window.configure(bg=self.bg_color)
        
        self.setup_ui()

    def setup_ui(self):
        # Center Frame to hold elements
        main_frame = tk.Frame(self.window, bg=self.bg_color)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Logo/Icon Placeholder
        # Using a large emoji as a simple logo representation
        logo_label = tk.Label(main_frame, text="👐", font=("Segoe UI Emoji", 80), bg=self.bg_color)
        logo_label.pack(pady=(0, 20))

        # App Name "EchoHands"
        title_label = tk.Label(main_frame, text="EchoHands", font=("Helvetica", 36, "bold"), bg=self.bg_color, fg="#006064")
        title_label.pack(pady=10)
        
        # Tagline / Subtitle
        subtitle = tk.Label(main_frame, text="Bridging Communication", font=("Helvetica", 14), bg=self.bg_color, fg="#00838F")
        subtitle.pack(pady=(0, 40))

        # "Next" Button
        # Large, rounded feel, high contrast
        btn_next = tk.Button(main_frame, text="Next", font=("Helvetica", 16, "bold"), 
                             bg="#00BCD4", fg="white", activebackground="#0097A7", activeforeground="white",
                             bd=0, padx=50, pady=10, cursor="hand2",
                             command=self.go_to_login)
        btn_next.pack(pady=20)
    
    def go_to_login(self):
        self.window.destroy()
        try:
            subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__), "login_gui.py")])
        except Exception as e:
            print(f"Error launching login: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WelcomeApp(root)
    root.mainloop()
