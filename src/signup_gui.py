import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os
import re
from db_manager import DatabaseManager

class SignupApp:
    def __init__(self, window):
        self.window = window
        self.window.title("BridgeTalk - Create Account")
        self.window.geometry("900x700")
        self.db_manager = DatabaseManager()

        # State for accessibility
        self.large_text_mode = False
        self.high_contrast_mode = False
        self.voice_assist_on = False

        # Fonts
        self.def_font = ("Helvetica", 11)
        self.header_font = ("Helvetica", 24, "bold")
        self.sub_font = ("Helvetica", 12)
        
        # Colors (Standard)
        self.colors = {
            "bg_top": "#2193b0", # Gradient start
            "bg_bottom": "#6dd5ed", # Gradient end
            "card_bg": "white",
            "text": "#333333",
            "input_bg": "#f9f9f9",
            "accent": "#00838F",
            "error": "#d32f2f"
        }

        self.setup_ui()

    def setup_ui(self):
        # Main Container (Canvas for gradient)
        self.canvas = tk.Canvas(self.window, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        self.draw_gradient()

        # Main Frame (Card)
        self.card = tk.Frame(self.window, bg=self.colors["card_bg"], padx=40, pady=40)
        self.card.place(relx=0.5, rely=0.5, anchor="center")

        # Header
        self.lbl_logo = tk.Label(self.card, text="BridgeTalk", font=self.header_font, fg=self.colors["accent"], bg=self.colors["card_bg"])
        self.lbl_logo.pack(pady=(0, 5))
        
        self.lbl_sub = tk.Label(self.card, text="Connect without barriers. Communicate freely.", font=("Helvetica", 10, "italic"), fg="#666", bg=self.colors["card_bg"])
        self.lbl_sub.pack(pady=(0, 20))

        # Form Container
        self.form_frame = tk.Frame(self.card, bg=self.colors["card_bg"])
        self.form_frame.pack(fill="x")

        # Inputs
        self.entries = {}
        self.add_input_field("Full Name", "full_name")
        self.add_input_field("Email Address", "email")
        self.add_input_field("Mobile Number", "mobile")
        
        # Gender Selector
        tk.Label(self.form_frame, text="Gender", font=self.def_font, bg=self.colors["card_bg"], fg=self.colors["text"]).pack(anchor="w", pady=(5, 2))
        self.gender_var = tk.StringVar(value="Male")
        gender_frame = tk.Frame(self.form_frame, bg=self.colors["card_bg"])
        gender_frame.pack(fill="x", pady=(0, 5))
        
        for g in ["Male", "Female", "Other"]:
            tk.Radiobutton(gender_frame, text=g, variable=self.gender_var, value=g,
                           bg=self.colors["card_bg"], font=self.def_font, activebackground=self.colors["card_bg"]).pack(side="left", padx=(0, 10))

        # Role Selector
        tk.Label(self.form_frame, text="I am a...", font=self.def_font, bg=self.colors["card_bg"], fg=self.colors["text"]).pack(anchor="w", pady=(10, 2))
        self.role_var = tk.StringVar(value="Hearing User")
        self.role_combo = ttk.Combobox(self.form_frame, textvariable=self.role_var, values=["Hearing User", "Deaf / Mute User"], state="readonly", font=self.def_font)
        self.role_combo.pack(fill="x", pady=(0, 5))

        self.add_input_field("Password", "password", show="*")
        self.add_input_field("Confirm Password", "confirm_password", show="*")

        # Show Passwords Toggle
        self.show_pwds_var = tk.BooleanVar(value=False)
        self.btn_show_pwds = tk.Button(self.form_frame, text="👁 Show Passwords", bd=0,
                                       bg=self.colors["card_bg"], fg=self.colors["text"],
                                       command=self.toggle_passwords, font=("Helvetica", 10), 
                                       activebackground=self.colors["card_bg"], cursor="hand2")
        self.btn_show_pwds.pack(anchor="w", pady=(0, 10))

        # Accessibility Options
        self.acc_frame = tk.Frame(self.card, bg=self.colors["card_bg"])
        self.acc_frame.pack(fill="x", pady=15)
        
        self.btn_large_text = tk.Button(self.acc_frame, text="A+", command=self.toggle_large_text, relief="flat", bg="#eee")
        self.btn_large_text.pack(side="left", padx=2)
        
        self.btn_contrast = tk.Button(self.acc_frame, text="👁", command=self.toggle_contrast, relief="flat", bg="#eee")
        self.btn_contrast.pack(side="left", padx=2)
        
        self.btn_voice = tk.Button(self.acc_frame, text="🎤", command=self.toggle_voice, relief="flat", bg="#eee")
        self.btn_voice.pack(side="left", padx=2)

        # Buttons
        self.btn_signup = tk.Button(self.card, text="Sign Up", font=("Helvetica", 12, "bold"), bg=self.colors["accent"], fg="white", relief="flat", padx=20, pady=10, cursor="hand2", command=self.process_signup)
        self.btn_signup.pack(fill="x", pady=10)

        # Links
        link_frame = tk.Frame(self.card, bg=self.colors["card_bg"])
        link_frame.pack(fill="x")
        
        self.btn_login = tk.Button(link_frame, text="Already have an account? Log in", font=("Helvetica", 9, "underline"), fg=self.colors["accent"], bg=self.colors["card_bg"], relief="flat", bd=0, cursor="hand2", command=self.go_to_login)
        self.btn_login.pack()

        # Trust Indicators
        trust_frame = tk.Frame(self.card, bg=self.colors["card_bg"])
        trust_frame.pack(fill="x", pady=(20, 0))
        tk.Label(trust_frame, text="🔒 Secure | Privacy Policy | Terms", font=("Helvetica", 8), fg="#999", bg=self.colors["card_bg"]).pack()

    def add_input_field(self, label, key, show=None):
        tk.Label(self.form_frame, text=label, font=self.def_font, bg=self.colors["card_bg"], fg=self.colors["text"]).pack(anchor="w", pady=(5, 2))
        entry = tk.Entry(self.form_frame, font=self.def_font, show=show, relief="flat", highlightbackground="#ddd", highlightcolor=self.colors["accent"], highlightthickness=1, bg=self.colors["input_bg"])
        entry.pack(fill="x", pady=(0, 5), ipady=5)
        self.entries[key] = entry

    def draw_gradient(self):
        # Simulated gradient
        width = 900
        height = 700
        # Just simple efficient gradient simulation
        limit = height
        r1, g1, b1 = self.hex_to_rgb(self.colors["bg_top"])
        r2, g2, b2 = self.hex_to_rgb(self.colors["bg_bottom"])
        
        for i in range(limit):
             nr = int(r1 + (r2 - r1) * i / limit)
             ng = int(g1 + (g2 - g1) * i / limit)
             nb = int(b1 + (b2 - b1) * i / limit)
             color = "#%02x%02x%02x" % (nr, ng, nb)
             self.canvas.create_line(0, i, width, i, fill=color)

    def hex_to_rgb(self, hex_val):
        hex_val = hex_val.lstrip('#')
        return tuple(int(hex_val[i:i+2], 16) for i in (0, 2, 4))
    
    def toggle_passwords(self):
        self.show_pwds_var.set(not self.show_pwds_var.get())
        show_char = "" if self.show_pwds_var.get() else "*"
        self.entries["password"].config(show=show_char)
        self.entries["confirm_password"].config(show=show_char)
        
        btn_text = "🙈 Hide Passwords" if self.show_pwds_var.get() else "👁 Show Passwords"
        self.btn_show_pwds.config(text=btn_text)

    def toggle_large_text(self):
        self.large_text_mode = not self.large_text_mode
        size_adj = 4 if self.large_text_mode else 0
        
        self.def_font = ("Helvetica", 11 + size_adj)
        self.header_font = ("Helvetica", 24 + size_adj, "bold")
        
        # Re-apply fonts
        self.lbl_logo.config(font=self.header_font)
        for child in self.form_frame.winfo_children():
            if isinstance(child, tk.Label):
                child.config(font=self.def_font)
            elif isinstance(child, tk.Entry):
                child.config(font=self.def_font)
        self.role_combo.config(font=self.def_font)
        
    def toggle_contrast(self):
        self.high_contrast_mode = not self.high_contrast_mode
        if self.high_contrast_mode:
            self.card.config(bg="black")
            self.lbl_logo.config(bg="black", fg="yellow")
            self.lbl_sub.config(bg="black", fg="white")
            self.form_frame.config(bg="black")
            for child in self.form_frame.winfo_children():
                 if isinstance(child, tk.Label):
                     child.config(bg="black", fg="yellow")
                 elif type(child) is tk.Entry:
                     child.config(bg="#333", fg="white", insertbackground="white")
            self.btn_signup.config(bg="yellow", fg="black")
        else:
            # Revert (Simplified revert logic)
            self.card.config(bg=self.colors["card_bg"])
            self.lbl_logo.config(bg=self.colors["card_bg"], fg=self.colors["accent"])
            self.lbl_sub.config(bg=self.colors["card_bg"], fg="#666")
            self.form_frame.config(bg=self.colors["card_bg"])
            for child in self.form_frame.winfo_children():
                 if isinstance(child, tk.Label):
                     child.config(bg=self.colors["card_bg"], fg=self.colors["text"])
                 elif type(child) is tk.Entry:
                     child.config(bg=self.colors["input_bg"], fg="black", insertbackground="black")
            self.btn_signup.config(bg=self.colors["accent"], fg="white")

    def toggle_voice(self):
        self.voice_assist_on = not self.voice_assist_on
        state = "ON" if self.voice_assist_on else "OFF"
        messagebox.showinfo("Voice Assistant", f"Voice Assistance is now {state}\n(Placeholder for TTS integration)")

    def process_signup(self):
        data = {k: v.get() for k, v in self.entries.items()}
        role = self.role_var.get()
        gender = self.gender_var.get()
        
        # Validation
        if not all(data.values()):
            messagebox.showwarning("Missing Info", "Please fill in all fields.")
            return

        if not re.match(r"[^@]+@[^@]+\.[^@]+", data["email"]):
             messagebox.showwarning("Invalid Email", "Please enter a valid email address.")
             return

        if not data["mobile"].isdigit() or len(data["mobile"]) < 10:
             messagebox.showwarning("Invalid Mobile", "Please enter a valid mobile number.")
             return

        if len(data["password"]) < 4:
            messagebox.showwarning("Weak Password", "Password must be at least 4 characters.")
            return

        if data["password"] != data["confirm_password"]:
            messagebox.showerror("Mismatch", "Passwords do not match.")
            return

        # Map role to DB value
        db_role = "Disable" if "Deaf" in role else "Normal"
        
        # Username generation (using email prefix for now to simplify)
        username = data["email"].split("@")[0]
        
        success, msg = self.db_manager.add_user(
            username=username,
            password=data["password"],
            full_name=data["full_name"],
            email=data["email"],
            mobile_number=data["mobile"],
            gender=gender,
            user_type=db_role
        )
        
        if success:
            messagebox.showinfo("Success", f"Account created for {username}!\nPlease log in.")
            self.go_to_login()
        else:
            messagebox.showerror("Error", msg)

    def go_to_login(self):
        self.window.destroy()
        try:
            subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__), "login_gui.py")])
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SignupApp(root)
    root.mainloop()
