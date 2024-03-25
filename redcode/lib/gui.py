from threading import Thread, Timer
from tkinter import ttk, Tk
from time import sleep

class AlarmWindow:
    def __init__(self):
        self.root_frame = None
        self.label_object = None
        self.texts = []
        Thread(target=self._initialize, daemon=True).start()
        sleep(0.3)

    def _initialize(self):
        self.root_frame = Tk()
        self.root_frame.attributes("-topmost", True)
        self.root_frame.overrideredirect(1)
        self.root_frame.withdraw()

        frm = ttk.Frame(self.root_frame, padding=20)
        frm.grid()
        self.label_object = ttk.Label(frm, text="", font=("Arial", 16))
        self.label_object.grid(column=0, row=0)

        self.root_frame.mainloop()

    def _dequeue(self):
        self.texts.pop(0)
        self.change_text("\n".join(self.texts))

    def add_alarm(self, text, is_progressive):
        if is_progressive:
            self.texts += [text]
            Timer(15, self._dequeue).start()
        else:
            self.texts = [text]
        self.change_text("\n".join(self.texts))

    def change_text(self, new_text):
        old_text = self.label_object.cget("text")
        self.label_object.config(text=new_text)
        self.root_frame.update()
        screen_width = self.root_frame.winfo_screenwidth()
        screen_height = self.root_frame.winfo_screenheight()
        r_width = self.root_frame.winfo_reqwidth()
        r_height = self.root_frame.winfo_reqheight()

        self.root_frame.geometry(f"{r_width}x{r_height}+{screen_width - r_width - 10}+{screen_height - r_height - 50}")

        if old_text != "" and new_text == "":
            self.root_frame.withdraw()
        elif old_text == "" and new_text != "":
            self.root_frame.deiconify()
