import random
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class AircraftScheduler:
    def __init__(self):
        self.time_table = {}
        self.delayed_planes = {}

    def check_availability(self, arrival_time):
        return all(data[0] != arrival_time for data in self.time_table.values())

    def add_aircraft(self, id, arrival_time, size, on_time, aircraft_class):
        if self.check_availability(arrival_time):
            self.time_table[id] = [arrival_time, size, aircraft_class, on_time]
            return f'ID-{id} aircraft added to the schedule!!'
        else:
            conflicting_aircraft, flag = None, 999
            user_hr, user_min = map(int, arrival_time.split(":"))

            for craft_id, data in self.time_table.items():
                hr, min = map(int, data[0].split(":"))
                if hr == user_hr and user_min in range(min, min + 20) and data[3] == "true":
                    conflicting_aircraft = craft_id
                    flag = 1
                elif hr == user_hr and user_min in range(min, min + 20) and data[3] != "true":
                    conflicting_aircraft = craft_id
                    flag = 0
                    break

            if conflicting_aircraft is not None:
                if flag == 1:
                    delayed_time = '{}:{}'.format(user_hr, user_min + 20)
                    self.time_table[id] = [delayed_time, size, aircraft_class, 'false']
                    return f'Aircraft with ID-{id} added with a delay of 20 minutes.'
                elif flag == 0:
                    if conflicting_aircraft not in self.time_table:
                        return f'Aircraft with conflicting ID={conflicting_aircraft} does not exist in the schedule.'

                    t = self.time_table[conflicting_aircraft][0]
                    if self.time_table[conflicting_aircraft][2] == self.time_table[id][2]:
                        if self.time_table[conflicting_aircraft][1] == self.time_table[id][1]:
                            lucky = random.choice([conflicting_aircraft, id])
                            if lucky == conflicting_aircraft:
                                delayed_time = '{}:{}'.format(user_hr, user_min + 20)
                                self.time_table[id] = [delayed_time, size, aircraft_class, 'false']
                                return f'ID-{conflicting_aircraft} can land at {self.time_table[conflicting_aircraft][0]}'
                            else:
                                delayed_time = '{}:{}'.format(user_hr, user_min + 20)
                                self.time_table[conflicting_aircraft][0] = delayed_time
                                return f'ID-{id} can land at {self.time_table[id][0]}'
                        elif self.time_table[conflicting_aircraft][1] < self.time_table[id][1]:
                            delayed_time = '{}:{}'.format(hr, min + 20)
                            self.time_table[id] = [delayed_time, size, aircraft_class, 'false']
                            return f'ID-{id} can land at {self.time_table[id][0]}'
                        else:
                            self.time_table[id][3] = "False"
                            self.time_table[id][0] = '{}:{}'.format(user_hr, user_min + 20)
                            return f'ID-{id} has to delay by 20 min. Arrival time conflicts with another aircraft. Updated data.'
                    elif data[2] > self.time_table[id][2]:
                        return f'ID-{id} can land at {self.time_table[id][0]}'
                    else:
                        self.time_table[id][3] = "False"
                        self.time_table[id][0] = '{}:{}'.format(user_hr, user_min + 20)
                        return f'ID-{id} has to delay by 20 min. Arrival time conflicts with another aircraft. Updated data.'
            else:
                self.time_table[id] = [arrival_time, size, aircraft_class, on_time]
                return f'ID-{id} aircraft added to the schedule with adjusted time!!'

    def cancel_schedule(self, id):
        if id in self.time_table:
            del self.time_table[id]
            return f'Aircraft ID-{id} schedule has been canceled.'
        else:
            return f'Aircraft ID-{id} not found in the schedule.'


class PopupWindow:
    def __init__(self, root, scheduler, function, on_close_callback):
        self.root = root
        self.scheduler = scheduler
        self.function = function
        self.on_close_callback = on_close_callback
        self.response = ""
        self.popup = tk.Toplevel(root)
        self.popup.title("Add Info")
        self.popup.geometry("200x200")
        self.create_widgets()

    def create_widgets(self):
        self.label_id = tk.Label(self.popup, text="ID:")
        self.label_arivaltime = tk.Label(self.popup, text="Arrival Time:")
        self.label_size = tk.Label(self.popup, text="Size:")
        self.label_ontime = tk.Label(self.popup, text="Ontime:")
        self.label_class = tk.Label(self.popup, text="Class:")

        self.entry_id = tk.Entry(self.popup, width=10)
        self.entry_arivaltime = tk.Entry(self.popup, width=10)
        self.entry_arivaltime.insert(0, "HH:MM")
        self.entry_size = tk.Entry(self.popup, width=10)
        ontime_option = ["True", "False"]
        self.entry_ontime = ttk.Combobox(self.popup, values=ontime_option, width=7)
        self.entry_ontime.set(ontime_option[0])
        class_option = [1, 2]
        self.entry_class = ttk.Combobox(self.popup, values=class_option, width=7)
        self.entry_class.set(class_option[0])

        if self.function == "add" or self.function == "arrival":
            self.setup_add_arrival_widgets()
        elif self.function == "cancel":
            self.setup_cancel_widgets()

    def setup_add_arrival_widgets(self):
        self.label_id.place(x=20, y=20)
        self.label_arivaltime.place(x=20, y=50)
        self.label_size.place(x=20, y=80)
        self.label_ontime.place(x=20, y=110)
        self.label_class.place(x=20, y=140)

        self.entry_id.place(x=100, y=20)
        self.entry_arivaltime.place(x=100, y=50)
        self.entry_size.place(x=100, y=80)
        self.entry_ontime.place(x=100, y=110)
        self.entry_class.place(x=100, y=140)

        button_text = "ADD" if self.function == "add" else "ARRIVAL"
        add_button = tk.Button(self.popup, text=button_text, bg="green", command=self.add_arrival)
        add_button.place(x=80, y=170, width=40, height=20)

    def setup_cancel_widgets(self):
        self.label_id.place(x=50, y=50)
        self.entry_id.place(x=80, y=50)
        add_button = tk.Button(self.popup, text="CANCEL", bg="green", command=self.cancel)
        add_button.place(x=70, y=90, width=60, height=20)

    def add_arrival(self):
        id = int(self.entry_id.get())
        arrival_time = self.entry_arivaltime.get()
        size = self.entry_size.get()
        on_time = self.entry_ontime.get().lower()
        aircraft_class = int(self.entry_class.get())
        self.response = self.scheduler.add_aircraft(id, arrival_time, size, on_time, aircraft_class)
        self.popup.destroy()
        self.on_close_callback(self.response)

    def cancel(self):
        id = int(self.entry_id.get())
        self.response = self.scheduler.cancel_schedule(id)
        self.popup.destroy()
        self.on_close_callback(self.response)


class AircraftApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("400x500")
        self.root.title("AIR TRAFFIC CONTROL")
        self.root.config(bg="#E67E22")
        self.scheduler = AircraftScheduler()
        self.create_gui()

    def create_gui(self):
        main_frame = tk.Frame(self.root, bg="#CACFD2")
        main_frame.place(x=10, y=10, width=380, height=480)

        frame1 = tk.Frame(main_frame, bg="#34495E")
        frame1.place(x=0, y=0, width=380, height=50)

        frame2 = tk.Frame(main_frame, bg="#34495E")
        frame2.place(x=0, y=55, width=380, height=360)

        frame3 = tk.Frame(main_frame, bg="#34495E")
        frame3.place(x=5, y=425, width=280, height=45)

        entry = tk.Entry(frame3, bg="#34495E", font=('times new roman', 12, 'bold'), fg='white', )
        entry.place(x=0, y=0, width=280, height=45)

        message_window = tk.Listbox(frame2, font=('times new roman', 12, 'bold'), fg='white', bg='#34495E',
                                    selectmode=tk.EXTENDED)
        message_window.place(x=0, y=0, height=360, width=380)
        scrollbar = tk.Scrollbar(frame2, command=message_window.yview, width=12)
        scrollbar.place(x=368, y=0, height=360)
        message_window.config(yscrollcommand=scrollbar.set)
        response = 'Anny : Welcome to Aircraft Scheduling Station'
        message_window.insert(tk.END, response)

        anny = tk.Label(frame1, text="ANNY", font=("times new raoman", 20, "bold"), bg="#34495E", fg="white")
        anny.place(x=145, y=12)

        send_button = tk.Button(main_frame, text="SEND", command=lambda: self.insert_message(entry, message_window))
        send_button.place(x=290, y=425, width=85, height=45)

    def insert_message(self, entry, message_window):
        user_input = entry.get().lower()
        new_user_input = f"You : {user_input}\n"
        message_window.insert(tk.END, new_user_input)
        response = ''
        flag = 1
        if 'hey' in user_input or 'hello' in user_input or 'hi' in user_input:
            response = '{} ! How may I help you ?'.format(user_input)
            flag=0
        elif 'add' in user_input or 'entry' in user_input or 'schedule' in user_input:
            self.show_popup("add", message_window)
        elif 'arrive' in user_input or 'land' in user_input:
            self.show_popup("arrival", message_window)
        elif 'cancel' in user_input:
            self.show_popup("cancel", message_window)
        elif 'exit' in user_input:
            response = "Goodbye! Have a great day."
            flag = 0
        elif 'display' in user_input:
            response = self.display(self.scheduler)
            flag = 0
        else:
            response = "I'm not sure how to respond to that."
            flag = 0
        if flag == 0 :
            anny_response = f"Anny : {response}\n"
            message_window.insert(tk.END, anny_response)

    def show_popup(self, function, message_window):
        def on_close(response):
            anny_response = f"Anny : {response}\n"
            message_window.insert(tk.END, anny_response)

        PopupWindow(self.root, self.scheduler, function, on_close)

    def display(self,schedular):
        self.time_table = schedular.time_table
        if self.time_table:
            # for id,value in self.time_table.items():
            messagebox.showinfo(title="Time Table", message=self.time_table)
            return "Schedule is displayed !"
        else:
            messagebox.showerror(title="ERROR", message="No aircraft is schedule now !")
            return "Schedule is empty"

if __name__ == "__main__":
    app = AircraftApp()
    app.root.mainloop()
