import customtkinter as ctk
from tkinter import messagebox
from services.auth_service import login
from gui.dashboard import DashboardWindow

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class LoginWindow(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("IDWMS - Login")
        self.geometry("560x560")
        self.resizable(False, False)

        self.create_ui()

    def create_ui(self):

        # Top header
        header = ctk.CTkFrame(self, fg_color="#2563EB", height=100, corner_radius=0)
        header.pack(fill="x")

        ctk.CTkLabel(
            self,
            text="Intelligent Document &\nWorkflow Management System",
            font=(None, 24, "bold"),
            text_color="#1E3A8A",
            justify="center"
        ).pack(pady=(30, 10))

        ctk.CTkLabel(
            self,
            text="Secure Enterprise Login Portal",
            font=(None, 16),
            text_color="gray40"
        ).pack(pady=(0, 25))

        # Login card
        card = ctk.CTkFrame(self, width=420, height=280, corner_radius=18)
        card.pack(pady=10)
        card.pack_propagate(False)

        ctk.CTkLabel(
            card,
            text="Sign In",
            font=(None, 22, "bold")
        ).pack(pady=(25, 20))

        self.username = ctk.CTkEntry(
            card,
            width=340,
            height=45,
            placeholder_text="Username"
        )
        self.username.pack(pady=10)

        self.password = ctk.CTkEntry(
            card,
            width=340,
            height=45,
            placeholder_text="Password",
            show="*"
        )
        self.password.pack(pady=10)

        ctk.CTkButton(
            card,
            text="Sign In",
            width=340,
            height=48,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            command=self.do_login
        ).pack(pady=20)

        ctk.CTkLabel(
            self,
            text="Enterprise Secure Authentication | Version 2.0",
            font=(None, 12),
            text_color="gray50"
        ).pack(side="bottom", pady=18)

    def do_login(self):

        username = self.username.get().strip()
        password = self.password.get().strip()

        if username == "" or password == "":
            messagebox.showwarning(
                "Warning",
                "Enter username and password"
            )
            return

        user = login(username, password)

        if not user:
            messagebox.showerror(
                "Login Failed",
                "Invalid username or password"
            )
            return

        messagebox.showinfo(
            "Login Successful",
            f"Welcome {user['full_name']} ({user['role']})"
        )

        self.destroy()

        dashboard = DashboardWindow(
            user["user_id"],
            user["full_name"],
            user["role"]
        )

        dashboard.mainloop()


if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()