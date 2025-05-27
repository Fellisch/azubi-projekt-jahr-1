import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from datetime import datetime
import threading


class DebugWindow:
    _instance = None

    def __init__(self):
        if DebugWindow._instance is not None:
            raise Exception("This class is a singleton!")
        DebugWindow._instance = self

        self.thread = threading.Thread(target=self._start_window, daemon=True)
        self.thread.start()

    _instance_lock = threading.Lock()

    @classmethod
    def get_instance(cls):
        with cls._instance_lock:
            if cls._instance is None:
                cls()
        return cls._instance

    def _start_window(self):
        try:
            self.root = tk.Tk()
            self.root.title("Debug Window")
            self.text_area = ScrolledText(self.root, state='disabled', width=100, height=30, wrap='word')
            self.text_area.pack(expand=True, fill='both')
            clear_button = tk.Button(self.root, text="Clear Log", command=self._clear_log)
            clear_button.pack(fill='x')
            self.root.protocol("WM_DELETE_WINDOW", self._on_close)
            self.root.mainloop()
        except Exception as e:
            print(f"Error launching DebugWindow: {e}")

    def _clear_log(self):
        self.text_area.configure(state='normal')
        self.text_area.delete('1.0', tk.END)
        self.text_area.configure(state='disabled')

    def _on_close(self):
        self.root.destroy()
        DebugWindow._instance = None

    def log(self, message):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        full_message = f"[{timestamp}] {message}"

        def append():
            self.text_area.configure(state='normal')
            self.text_area.insert(tk.END, full_message + '\n')
            self.text_area.configure(state='disabled')
            self.text_area.see(tk.END)

        if hasattr(self, 'text_area'):
            self.text_area.after(0, append)