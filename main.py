import time
from time import strftime
from tkinter import *
from tkinter import messagebox
from tkinter import Toplevel
import threading


# import datetime


def update_time():
    time_label.config(text=strftime("%T %p"))
    day_label.config(text=strftime("%A"))
    date_label.config(text=strftime("%d.%m.%Y"))
    root.after(1000, update_time)


"""
COUNTDOWN CODE IS HERE:
"""


class CountdownWindow:
    def __init__(self):
        """
        # CREATE THE WINDOW ITSELF
        """
        self.cd_root = Toplevel(root)
        self.cd_root.title('GT\'S COUNTDOWN')
        self.cd_root.geometry("480x380")
        self.cd_root.iconbitmap('my_clock.ico')
        """
        # CREATE THE MAIN FRAME
        """
        self.cd_frame = Frame(self.cd_root, bg='black')
        self.cd_frame.pack(fill=BOTH, expand=YES)
        """
        # TITLE
        """
        self.cd_title_label = Label(self.cd_frame, text="Countdown", font=('System', 50), fg='#00ff09', bg='black',
                                    width=10, pady=5)
        self.cd_title_label.pack(side=TOP)
        """
        # DECORATION LINE
        """
        self.cd_line_canvas = Canvas(self.cd_frame, highlightthickness=0, background='black', height=15)
        self.cd_line_canvas.create_line(0, 0, 500000, 0, width=5, fill='white')
        self.cd_line_canvas.pack(side=TOP, fill=X)
        # CREATE THE ENTRY BOX AND THE TIME LABEL
        self.border_color_1 = Frame(self.cd_frame, background="#00ff09")
        self.border_color_1.pack(pady=10)
        self.cd_time_entry = Entry(self.border_color_1, font=('Courier', 20), width=10, bd=0, bg='black', fg='#00ff09')
        self.cd_time_entry.pack(padx=2, pady=2)
        self.border_color_2 = Frame(self.cd_frame, background="#00ff09")
        self.border_color_2.pack(pady=4)
        self.cd_time_label = Label(self.border_color_2, text="Time: 00:00:00", font=('Courier', 30), width=15,
                                   bg='black', fg='#00ff09')
        self.cd_time_label.pack(padx=2, pady=2)
        # INFO LABEL
        self.border_color_3 = Frame(self.cd_frame, background="#00ff09")
        self.border_color_3.pack(pady=4)
        self.cd_info_label = Label(self.border_color_3, text="Valid input is: \"hours:minutes:seconds\"", bg='black',
                                   fg='#00ff09', font=('Courier', 10))
        self.cd_info_label.pack(padx=2, pady=2)
        # CREATE THE BUTTONS
        self.cd_button_frame = Frame(self.cd_frame, bg='black')
        self.cd_button_frame.pack(side=BOTTOM, pady=15)
        self.cd_start_button = Button(self.cd_button_frame, text='Start', font=('Courier', 20), command=self.start_cd,
                                      width=7, bd=5, fg='#8300ff', activeforeground='#8300ff')
        self.cd_stop_button = Button(self.cd_button_frame, text='Stop', font=('Courier', 20), command=self.stop,
                                     width=7, bd=5, fg='#8300ff', activeforeground='#8300ff')
        self.cd_pause_button = Button(self.cd_button_frame, text='Pause', font=('Courier', 20), command=self.pause,
                                      width=7, bd=5, fg='#8300ff', activeforeground='#8300ff')
        self.cd_start_button.pack(side=LEFT, padx=10)
        self.cd_pause_button.pack(side=LEFT, padx=10)
        self.cd_stop_button.pack(side=RIGHT, padx=10)
        # BOOLEAN THAT REPRESENTS WHETHER OR NO THE COUNTDOWN SHOULD BE GOING
        # TRUE = GOING
        self.stop_loop = True
        self.pause_check = 1
        self.cd_time = 0

    def start_thread(self):
        t = threading.Thread(target=self.start_cd, daemon=True)
        self.stop_loop = True
        self.pause_check = 1
        t.start()

    def start_cd(self):
        self.stop_loop = True
        self.pause_check = 1
        # WE SPLIT THE ENTRY BOX BY THE SEPARATOR ":" AND STORE THE VALUES IN A LIST
        hours, minutes, seconds = 0, 0, 0
        string_split = self.cd_time_entry.get().split(":")
        if len(string_split) == 3:
            try:
                hours = int(string_split[0])
                minutes = int(string_split[1])
                seconds = int(string_split[2])
            except ValueError:
                messagebox.showerror(title='Error', message='You didn\'t enter a valid time!')
                self.stop_loop = False
        elif len(string_split) == 2:
            try:
                minutes = int(string_split[0])
                seconds = int(string_split[1])
            except ValueError:
                messagebox.showerror(title='Error', message='You didn\'t enter a valid time!')
                self.stop_loop = False
        elif len(string_split) == 2:
            try:
                seconds = int(string_split[0])
            except ValueError:
                messagebox.showerror(title='Error', message='You didn\'t enter a valid time!')
                self.stop_loop = False
        else:
            messagebox.showerror(title='Error', message='You didn\'t enter a valid time!')
            self.stop_loop = False
        self.cd_time = hours * 3600 + minutes * 60 + seconds
        while self.cd_time > 0 and self.stop_loop:
            # DIVMOD -> RETURNS THE QUOTIENT AND THE REMAINDER OF A DIVISION ( NUMERATOR, DENOMINATOR
            minutes, seconds = divmod(self.cd_time, 60)
            hours, minutes = divmod(minutes, 60)
            # FORMATS THE TIME LABEL TO BE 00:00 EVEN IF THERE ARE ONLY SECONDS LEFT
            self.cd_time_label.config(text=f"Time: {hours:02d}:{minutes:02d}:{seconds:02d}")
            self.cd_root.update()
            time.sleep(1)
            self.cd_time -= 1
            while self.pause_check == -1:
                time.sleep(1)
                self.cd_root.update()
        if self.stop_loop:
            # IF STOP_LOOP IS STILL TRUE THEN THE COUNTDOWN STOPPED BY ITSELF
            messagebox.showinfo('', 'Your time is up!')
        self.cd_time_label.config(text="Time: 00:00:00")
        self.cd_time_entry.delete(0, END)
        self.cd_time_entry.config(state=NORMAL)

    def stop(self):
        self.stop_loop = False
        self.cd_time = 0
        self.cd_time_label.config(text="Time: 00:00:00")
        self.cd_time_entry.delete(0, END)

    def pause(self):
        self.pause_check = -self.pause_check


"""
STOPWATCH CODE IS HERE:
"""


class StopwatchWindow:
    def __init__(self):
        """
        # CREATE THE WINDOW ITSELF
        """
        self.sw_root = Toplevel(root)
        self.sw_root.title('GT\'S COUNTDOWN')
        self.sw_root.geometry("480x380")
        self.sw_root.iconbitmap('my_clock.ico')
        """
        # CREATE THE MAIN FRAME
        """
        self.sw_frame = Frame(self.sw_root, bg='black')
        self.sw_frame.pack(fill=BOTH, expand=YES)
        """ 
        # TITLE
        """
        self.sw_title_label = Label(self.sw_frame, text="Stopwatch", font=('System', 50), fg='#fff130', bg='black',
                                    width=10, pady=5)
        self.sw_title_label.pack(side=TOP)
        """
        # DECORATION LINE
        """
        self.sw_line_canvas = Canvas(self.sw_frame, highlightthickness=0, background='black', height=15)
        self.sw_line_canvas.create_line(0, 0, 500000, 0, width=5, fill='white')
        self.sw_line_canvas.pack(side=TOP, fill=X)
        """
        # TIME CHECKER
        """
        self.sw_stop_timer = 1
        """
        # TIME LABEL
        """
        self.border_color_1 = Frame(self.sw_frame, bg='#fff130', border=5)
        self.border_color_1.pack()
        self.sw_time_label = Label(self.border_color_1, background='black', fg='#fff130', text='00:00:00',
                                   font=('Courier', 40))
        self.sw_time_label.pack(side=TOP)
        self.sw_button_frame = Frame(self.sw_frame, bg='black')
        self.sw_button_frame.pack(side=BOTTOM, pady=15)
        self.sw_start_button = Button(self.sw_button_frame, text='Start', font=('Courier', 20), bd=5, fg='#8300ff',
                                      command=self.start_sw_thread, width=7, activeforeground='#8300ff')
        self.sw_start_button.pack(side=LEFT, padx=5)
        self.sw_pause_button = Button(self.sw_button_frame, text='Pause', font=('Courier', 20),
                                      command=self.pause_sw, width=7, bd=5, fg='#8300ff', activeforeground='#8300ff')
        self.sw_pause_button.pack(side=LEFT, padx=5)
        self.sw_pause_button = Button(self.sw_button_frame, text='Stop', font=('Courier', 20),
                                      command=self.stop_sw, width=7, bd=5, fg='#8300ff', activeforeground='#8300ff')
        self.sw_pause_button.pack(side=RIGHT, padx=5)
        self.pause = 1

    def start_sw_thread(self):
        self.stop_sw()
        self.pause = 1
        t = threading.Thread(target=self.start_sw(), daemon=True)
        t.start()

    def start_sw(self):
        self.sw_stop_timer = 1
        self.pause = 1
        sw_h = 0
        sw_m = 0
        sw_s = 0
        time.sleep(1)
        # print(sw_time_s)
        while self.sw_stop_timer == 1:
            while self.pause == -1:
                time.sleep(1)
                self.sw_root.update()
            sw_s += 1
            timer = sw_s + 60 * sw_m + 3600 * sw_h
            sw_m, sw_s = divmod(timer, 60)
            sw_h, sw_m = divmod(sw_m, 60)
            self.sw_time_label.config(
                text=f"{sw_h:02d}:{sw_m:02d}:{sw_s:02d}")
            self.sw_root.update()
            time.sleep(1)

    def pause_sw(self):
        self.pause = -self.pause
        self.sw_root.update()

    def stop_sw(self):
        self.sw_stop_timer = 0
        self.sw_time_label.config(text='00:00:00')
        self.sw_root.update()


root = Tk()

root.title('GT\'S CLOCK')
root.geometry("480x380")
root.iconbitmap('my_clock.ico')
root.config(bg='black')

"""
# CLOCK-FRAME
"""
clock_frame = Frame(root, bg='black')
clock_frame.pack(fill=BOTH, expand=True)

title_label = Label(clock_frame, text="Clock", font=('System', 50), fg='#0efde9', bg='black', width=10, pady=5)
title_label.pack()

line_canvas = Canvas(clock_frame, highlightthickness=0, background='black', height=20)
line_canvas.create_line(0, 0, 500000, 0, width=5, fill='white')
line_canvas.pack(side=TOP, fill=X)

time_label = Label(clock_frame, font=('Operator Mono Bold', 40), fg='#0efde9', bg='black', pady=10)
time_label.pack()
day_label = Label(clock_frame, font=('Operator Mono Bold', 20), fg='white', bg='black')
day_label.pack()
date_label = Label(clock_frame, font=('Operator Mono Bold', 25), fg='white', bg='black')
date_label.pack()

frame_b = Frame(clock_frame, bg='black')
frame_b.pack(side=BOTTOM)
cd_button = Button(frame_b, text='Countdown', font=('Courier', 20), fg='#8300ff', activeforeground='#8300ff', bd=5,
                   command=CountdownWindow)
cd_button.pack(side=LEFT, padx=5, pady=10)
sw_button = Button(frame_b, text='Stopwatch', font=('Courier', 20), fg='#8300ff', activeforeground='#8300ff', bd=5,
                   command=StopwatchWindow)
sw_button.pack(side=RIGHT, padx=5, pady=10)
made_by_label = Label(root, text='Made by: Gulin', font=('Operator Mono Bold', 10), fg='#0efde9', bg='black')
made_by_label.pack(side=BOTTOM)

update_time()

root.mainloop()

# another way to implement stopwatch
"""sw_time_up_h = int(datetime.datetime.now().hour)
            sw_time_up_m = int(datetime.datetime.now().minute)
            sw_time_up_s = int(datetime.datetime.now().second)
            sw_time_up = 3600 * sw_time_up_h + 60 * sw_time_up_m + sw_time_up_s
            timer = sw_time_up - sw_time
            sw_m, sw_s = divmod(timer, 60)
            sw_h, sw_m = divmod(sw_m, 60)
            I'm not using this method anymore; I used this before implementing the Pause option."""
"""sw_time_h = int(datetime.datetime.now().hour)
sw_time_m = int(datetime.datetime.now().minute)
sw_time_s = int(datetime.datetime.now().second)
sw_time = 3600 * sw_time_h + 60 * sw_time_m + sw_time_s
I'm not using this method anymore; I used this before implementing the Pause option."""
"""if self.pause == -1:
    sw_time_h = int(datetime.datetime.now().hour)
    sw_time_m = int(datetime.datetime.now().minute)
    sw_time_s = int(datetime.datetime.now().second)
    sw_time = 3600 * sw_time_h + 60 * sw_time_m + sw_time_s
    self.sw_root.update()
    I'm not using this method anymore; I tried to use this method for the Pause option but it didn't work"""
