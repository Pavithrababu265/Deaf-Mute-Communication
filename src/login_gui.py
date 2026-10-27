import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
import os
import sys
import socket
from db_manager import DatabaseManager

class LoginApp:
    def __init__(self, window):
        self.window = window
        self.window.title("EchoHands - Access")
        self.window.geometry("500x750")
        
        # Soft Gradient-like Background
        self.bg_color = "#E0F7FA"
        self.window.configure(bg=self.bg_color)
        
        self.db_manager = DatabaseManager()
        
        self.setup_styles()
        
        # Container - Card Like
        self.main_frame = tk.Frame(self.window, bg="white", padx=40, pady=40, highlightbackground="#B2EBF2", highlightthickness=1)
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center", width=420)
        
        self.show_login_frame()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Button Style
        self.style.configure("TButton", padding=10, relief="flat", background="#00BCD4", foreground="white", font=("Helvetica", 11, "bold"))
        self.style.map("TButton", background=[('active', '#0097A7')])
        
        # Frame Style
        self.style.configure("TFrame", background="white")

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def add_label_entry(self, parent, text, show=None):
        tk.Label(parent, text=text, bg="white", fg="#006064", font=("Helvetica", 10, "bold")).pack(anchor="w", pady=(15, 5))
        entry = tk.Entry(parent, font=("Helvetica", 12), show=show, bg="#FAFAFA", relief="flat", highlightthickness=1, highlightbackground="#B2EBF2")
        entry.pack(fill="x", ipady=8)
        return entry

    def show_login_frame(self):
        self.clear_frame()
        
        # Header
        # Logo placeholder
        tk.Label(self.main_frame, text="👐", font=("Segoe UI Emoji", 40), bg="white").pack(pady=(0, 10))
        tk.Label(self.main_frame, text="Sign In", font=("Helvetica", 24, "bold"), bg="white", fg="#006064").pack(pady=(0, 5))
        
        self.entry_user = self.add_label_entry(self.main_frame, "Username")
        
        # Password Field with Eye Icon
        pwd_frame = tk.Frame(self.main_frame, bg="white")
        pwd_frame.pack(fill="x")
        tk.Label(pwd_frame, text="Password", bg="white", fg="#006064", font=("Helvetica", 10, "bold")).pack(anchor="w", pady=(15, 5))
        
        input_frame = tk.Frame(pwd_frame, bg="white", highlightthickness=1, highlightbackground="#B2EBF2")
        input_frame.pack(fill="x")
        self.entry_pass = tk.Entry(input_frame, font=("Helvetica", 12), show="*", bg="#FAFAFA", relief="flat")
        self.entry_pass.pack(side="left", fill="x", expand=True, ipady=8)
        
        self.show_pwd_var = tk.BooleanVar(value=False)
        self.btn_show_pwd = tk.Button(input_frame, text="👁", bg="#FAFAFA", bd=0, font=("Helvetica", 12), cursor="hand2", command=self.toggle_password)
        self.btn_show_pwd.pack(side="right", padx=5)
        
        # Server Config
        try:
            # Get local IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            ip_text = f"My IP: {local_ip}"
        except:
            ip_text = "My IP: Unavailable"

        tk.Label(self.main_frame, text=ip_text, bg="white", fg="#00838F", font=("Helvetica", 10, "bold")).pack(pady=(10, 5))
        
        tk.Label(self.main_frame, text="Server IP", bg="white", fg="gray", font=("Helvetica", 8)).pack(anchor="w", pady=(0, 0))
        self.entry_host = tk.Entry(self.main_frame, font=("Helvetica", 10), bg="#FAFAFA",  relief="flat", highlightthickness=1, highlightbackground="#E0E0E0")
        self.entry_host.insert(0, "127.0.0.1")
        self.entry_host.pack(fill="x", ipady=4, pady=(2, 10))

        self.entry_pass.bind('<Return>', self.login)
        
        # CTA Button
        btn_login = ttk.Button(self.main_frame, text="Sign In", command=self.login, cursor="hand2")
        btn_login.pack(fill="x", pady=10)
        
        # Secondary Link
        btn_signup_link = tk.Button(self.main_frame, text="Don’t have an account? Sign Up", 
                                    font=("Helvetica", 10), fg="#00ACC1", bg="white", bd=0, cursor="hand2", 
                                    activebackground="white", activeforeground="#00838F",
                                    command=self.launch_signup)
        btn_signup_link.pack(pady=10)

    def toggle_password(self):
        self.show_pwd_var.set(not self.show_pwd_var.get())
        if self.show_pwd_var.get():
            self.entry_pass.config(show="")
            self.btn_show_pwd.config(text="🙈")
        else:
            self.entry_pass.config(show="*")
            self.btn_show_pwd.config(text="👁")


    def launch_signup(self):
        self.window.destroy()
        try:
             subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__), "signup_gui.py")])
        except Exception as e:
            messagebox.showerror("Error", f"Could not launch Sign Up: {e}")

    def login(self, event=None):
        username = self.entry_user.get().strip()
        password = self.entry_pass.get().strip()
        host = self.entry_host.get().strip() or "127.0.0.1"
        
        if not username or not password:
            messagebox.showwarning("Input Error", "Please fill in all fields")
            return
            
        success, message, user_type = self.db_manager.validate_user(username, password)
        if success:
            self.launch_main_app(username, user_type, host)
        else:
            messagebox.showerror("Login Failed", message)

    def launch_main_app(self, username, user_type, host):
        self.window.destroy()
        try:
            # Pass arguments to main_gui.py
            cmd = [sys.executable, os.path.join(os.path.dirname(__file__), "main_gui.py"), 
                   "--username", username, 
                   "--role", user_type,
                   "--host", host]
            subprocess.Popen(cmd)
        except Exception as e:
            messagebox.showerror("Launcher Error", f"Failed to launch application: {e}")



if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
