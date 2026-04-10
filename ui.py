import pyautogui
import threading

import tkinter as tk

from PIL import Image
from pynput import mouse
from automation import action_lists
from automation import clicking
from state import Action

FONT_TITLE = ("Segoe UI", 14, "bold")
FONT_NORMAL = ("Segoe UI", 10)
FONT_MONO = ("Courier New", 9)
FONT_STATUS = ("Segoe UI", 10, "bold")


class AutoClicker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ClickWise")
        self.root.iconbitmap("app.ico")
        self.root.geometry('480x420')
        self.frames: dict[str, tk.Frame] = {}
        self.inputerror = False
        self.errorshown = False
        self.home()

    def home(self):
        for frame in self.frames.keys():
            self.frames[frame].pack_forget()
        # ===========================Input Error Handling===========================#
        f = tk.Frame(self.root)
        self.frames['home'] = f

        if self.inputerror:
            if not self.errorshown:
                self.message = tk.Label(
                    self.root, text='Insert a positive integer', font=FONT_TITLE, fg='red')
                self.message.pack(pady=[10, 0], padx=[10, 0])
                self.root.deiconify()
                self.errorshown = True
            else:
                self.root.deiconify()
            self.inputerror = False  # This is needed for handling several error inputs in a row
        else:
            if self.errorshown:
                self.message.pack_forget()
                self.errorshown = False

        # ==============================Actions List================================#
        list_frame = tk.Frame(f)
        list_frame.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        logs = tk.Text(list_frame, font=FONT_MONO,
                       yscrollcommand=scrollbar.set, height=9)
        logs.pack(pady=[5, 0], padx=[5, 0],
                  side="left", fill="both", expand=True)

        scrollbar.config(command=logs.yview)

        for state in action_lists:
            logs.insert(
                tk.END, f'{state.mode} - Delay:{state.delay}s, click on {state.click_pos}\n')

        logs.config(state=tk.DISABLED)

        tk.Button(f, text="✕  Remove Selected", font=FONT_NORMAL,
                  command=self._remove_action).pack(pady=(10, 0))
        # ==============================Delay insertion=============================#
        time_entry = tk.Frame(f)
        time_entry.pack(pady=[10, 0])
        time_entry_description = tk.Label(
            time_entry, text='insert a (+) integer as your in between clicks delay', font=FONT_NORMAL)
        time_entry_description.pack(side='left', pady=[10, 0], padx=[0, 0])
        time_entry_box = tk.Entry(time_entry)
        time_entry_box.pack(side='left', padx=[10, 0], pady=[10, 0])
        # ==============================Action Buttons==============================#
        buttons = tk.Frame(f)
        buttons.pack(pady=[10, 0])
        tk.Button(buttons, text='Time', font=FONT_NORMAL, command=lambda: self._time_mode(time_entry_box),).pack(
            side='left', pady=[10, 0], padx=[10, 0])
        tk.Button(buttons, text='Screen Shot', font=FONT_NORMAL, command=lambda: self._screen_mode(time_entry_box),).pack(
            side='left', pady=[10, 0], padx=[10, 0])
        tk.Button(buttons, text='Finish The process', font=FONT_NORMAL, command=self._finish_mode,).pack(
            side='left', pady=[10, 0], padx=[10, 0])

        self.frames['home'].pack()
# ==============================Clicks Handling=============================#

    def _click_getter(self):
        coords = {}

        def on_click(x, y, button, pressed):
            if pressed:
                coords['pos'] = (x, y)
                return False
        with mouse.Listener(on_click=on_click) as listener:
            listener.join()
        return coords['pos']

    def _time_mode(self, delay):
        self.root.iconify()
        state = Action(None, None, None, None, None)
        pos = self._click_getter()

        try:
            int(delay.get())
            # seems dummy, but these 2 lines are for checking a (+) int input
            (int(delay.get()))**(0.5)
        except:
            self.inputerror = True

        if not self.inputerror:
            if pos:
                self.root.deiconify()
                state = Action('Time', delay.get(), None, None, pos)
            action_lists.append(state)
        self.home()

    def _screen_mode(self, delay):
        self.root.iconify()

        try:
            int(delay.get())
            # seems dummy, but these 2 lines are for checking a (+) int input
            (int(delay.get()))**(0.5)
        except:
            self.inputerror = True
            # if not self.inputerror:
            #     if not self.errorshown:
            #         self.inputerror = True
            #     else:
            #         self.inputerror = False
            # else:
            #     if self.errorshown:
            #         self.errorshown == False

        state = Action('Screenshot', delay.get(), None, (None, None), None)

        overlay = tk.Toplevel(self.root)
        overlay.attributes("-fullscreen", True)
        overlay.attributes("-alpha", 0.1)
        overlay.config(cursor="crosshair")
        overlay.lift()
        overlay.focus_force()

        canvas = tk.Canvas(overlay, bg="grey", highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        start = {}
        rect = [None]

        def on_press(event):
            start['x'] = event.x
            start['y'] = event.y

        def on_drag(event):
            if rect[0]:
                canvas.delete(rect[0])
            rect[0] = canvas.create_rectangle(
                start['x'], start['y'], event.x, event.y,
                outline="red", width=2
            )

        def on_release(event):
            overlay.destroy()
            x1 = min(start['x'], event.x_root)
            y1 = min(start['y'], event.y_root)
            x2 = max(start['x'], event.x_root)
            y2 = max(start['y'], event.y_root)

            screenshot = pyautogui.screenshot(
                region=(x1, y1, x2 - x1, y2 - y1))

            state.image = screenshot
            state.image_pos = (x1, y1)

            def after_click():
                pos = self._click_getter()
                if pos:
                    state.click_pos = pos

                action_lists.append(state)
                self.root.after(0, self.root.deiconify)
                self.root.after(0, self.home)

            if not self.inputerror:
                threading.Thread(target=after_click, daemon=True).start()
            else:
                self.home()

        canvas.bind("<ButtonPress-1>", on_press)
        canvas.bind("<B1-Motion>", on_drag)
        canvas.bind("<ButtonRelease-1>", on_release)

    def _remove_action(self):
        message = tk.Label(
            self.frames['home'], text='For the "Remove" feature \n please ask for the primume version!', font=FONT_TITLE)
        message.pack(padx=[10, 0], pady=[10, 0])

    def _finish_mode(self):
        if 'home' in self.frames.keys():
            self.frames['home'].pack_forget()
        f = tk.Frame(self.root)
        self.frames['finish'] = f
        f.pack()
        interval = tk.Frame(f)
        interval.pack(padx=[10, 0], pady=[10, 0])
        interval_description = tk.Label(
            interval, text='Now choose the interval no.')
        interval_description.pack(padx=[10, 0], pady=[10, 0], side='left')
        interval_no = tk.Entry(interval)
        interval_no.pack(padx=[10, 0], pady=[10, 0], side='left')
        buttons = tk.Frame(f)
        buttons.pack(padx=[10, 0], pady=[10, 0])
        tk.Button(buttons, text='Start Automaiton', font=FONT_NORMAL, command=lambda: self._start(interval_no),).pack(
            side='left', pady=[10, 0], padx=[10, 0])
        tk.Button(buttons, text='Back!', font=FONT_NORMAL, command=self.home,).pack(
            side='left', pady=[10, 0], padx=[10, 0])

    def _start(self, interval_no):
        f = self.frames['finish']
        try:
            for i in range(int(interval_no.get())):
                self.root.iconify()
                clicking()
            self.root.deiconify()
        except:
            self.root.deiconify()
            message = tk.Label(
                f, text='Insert a positive integer', font=FONT_NORMAL)
            message.pack(padx=[10, 0], pady=[10, 0])
