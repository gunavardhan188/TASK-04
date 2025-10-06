"""
visible_keylogger.py  — SAFE demo for development / accessibility / debugging.
- Logs keystrokes ONLY while the application's window is focused.
- Visible GUI, user can choose log file path.
- DO NOT use this to capture keystrokes from other people or run stealthily.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
import os

DEFAULT_LOG = "visible_key_log.txt"

class VisibleKeyLogger:
    def __init__(self, root):
        self.root = root
        root.title("Visible Key Logger (Focus Only)")
        root.geometry("700x420")

        # Info / disclaimer
        info = (
            "This application logs keystrokes ONLY when this window is focused.\n"
            "Use responsibly and only with explicit consent.\n"
        )
        tk.Label(root, text=info, padx=10, pady=8, justify="center").pack()

        # Text area showing captured events
        self.text = tk.Text(root, wrap="word", height=14, state="normal")
        self.text.pack(fill="both", expand=True, padx=12, pady=8)
        self.text.insert("end", "Keystrokes will appear here when window has focus.\n\n")

        # Buttons area
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=6)

        tk.Button(btn_frame, text="Clear Display", command=self.clear_display).grid(row=0, column=0, padx=6)
        tk.Button(btn_frame, text="Save Log As...", command=self.save_log_as).grid(row=0, column=1, padx=6)
        tk.Button(btn_frame, text="Open Log Folder", command=self.open_log_folder).grid(row=0, column=2, padx=6)
        tk.Button(btn_frame, text="Show Current Log File", command=self.show_log_location).grid(row=0, column=3, padx=6)

        # Log file path
        self.logfile = DEFAULT_LOG
        self.log_label = tk.Label(root, text=f"Log file: {os.path.abspath(self.logfile)}", fg="gray")
        self.log_label.pack(pady=(4,8))

        # Bind key events application-wide but we check focus before logging
        # We bind to the root so key presses inside widgets are also captured, but only when focused
        root.bind_all("<Key>", self.on_key)

    def clear_display(self):
        self.text.delete("1.0", "end")

    def save_log_as(self):
        path = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if path:
            self.logfile = path
            self.log_label.config(text=f"Log file: {os.path.abspath(self.logfile)}")
            messagebox.showinfo("Saved", f"Log will be written to:\n{self.logfile}")

    def open_log_folder(self):
        folder = os.path.dirname(os.path.abspath(self.logfile))
        try:
            if os.name == 'nt':
                os.startfile(folder)
            elif os.uname().sysname == 'Darwin':
                os.system(f'open "{folder}"')
            else:
                os.system(f'xdg-open "{folder}"')
        except Exception:
            messagebox.showinfo("Open Folder", f"Log folder: {folder}")

    def show_log_location(self):
        messagebox.showinfo("Log File", f"Current log file:\n{os.path.abspath(self.logfile)}")

    def on_key(self, event):
        # Only log when our window or one of its widgets currently has focus
        if self.root.focus_get() is None:
            return

        # Build a readable record
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        keysym = getattr(event, "keysym", "")
        char = getattr(event, "char", "")
        keycode = getattr(event, "keycode", "")

        # For readability: show printable char or descriptive name
        printable = repr(char) if char and char.strip() != "" else f"<{keysym}>"

        record = f"{timestamp}\t{printable}\tkeysym={keysym}\tkeycode={keycode}\n"

        # Append to GUI
        self.text.insert("end", record)
        self.text.see("end")

        # Append to file (handle errors gracefully)
        try:
            with open(self.logfile, "a", encoding="utf-8") as f:
                f.write(record)
        except Exception as e:
            # Show an error once and disable file writes
            messagebox.showerror("File Write Error", f"Could not write to log file:\n{e}")
            self.logfile = None
            self.log_label.config(text="Log file: (disabled)")

if __name__ == "__main__":
    root = tk.Tk()
    app = VisibleKeyLogger(root)
    root.mainloop()
