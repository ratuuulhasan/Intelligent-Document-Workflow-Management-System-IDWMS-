import customtkinter as ctk
from gui.version_history import VersionHistoryWindow

root = ctk.CTk()
root.withdraw()

VersionHistoryWindow(root, 1, "NID TEST")

root.mainloop()