from tkinter import *

import irsdk


fuel_level_text = ''  # Initialize
fuel_level_number_text = ''  # Initialize

laps_in_race_text = ''  # Initialize
laps_in_race_number_text = ''  # Initialize

average_text = ''  # Initialize
average_number_text = ''  # Initialize

laps_remain_text = ''  # Initialize
laps_remain_number_text = ''  # Initialize

refuel_text = ''  # Initialize
refuel_number_text = ''  # Initialize

fuel_at_end_text = ''  # Initialize
fuel_at_end_number_text = ''  # Initialize

pit_window_text = ''  # Initialize
pit_window_border = ''  # Initialize

exit_button = ''  # Initialize
exit_button_holder = ''  # Initialize

average_fuel_list = []  # Initialize
average_lap_list = []  # Initialize

running = False  # Initialize
cooldown = False  # Initialize
metric = True  # Initialize

fuel_start_of_lap = 0.00  # Initialize
start_count = -1  # Initialize
refuel = 0.0  # Initialize
laps_remain = 0.0  # Initialize


class State:
    ir_connected = False
    last_car_setup_tick = -1


def quit_app():
    sys.exit()


def reset():
    global average_fuel_list, running, cooldown, metric, fuel_start_of_lap, start_count, refuel, laps_remain, average_lap_list

    average_lap_list = []  # Initialize
    average_fuel_list = []  # Initialize

    running = False  # Initialize
    cooldown = False  # Initialize
    metric = True  # Initialize

    fuel_start_of_lap = 0.00  # Initialize
    start_count = -1  # Initialize
    refuel = 0.0  # Initialize
    laps_remain = 0.0  # Initialize


def check_iracing():
    if state.ir_connected and not (ir.is_initialized and ir.is_connected):
        state.last_car_setup_tick = False
        state.last_car_setup_tick = -1
        ir.shutdown()
    elif not state.ir_connected and ir.startup() and ir.is_initialized and ir.is_connected:
        state.ir_connected = True


def setup_canvas():
    global fuel_level_text, fuel_level_number_text, laps_in_race_text, laps_in_race_number_text, exit_button, exit_button_holder
    global average_text, average_number_text, laps_remain_text, laps_remain_number_text, pit_window_border
    global refuel_text, refuel_number_text, fuel_at_end_text, fuel_at_end_number_text, pit_window_text

    fuel_level_text = canvas.create_text(5, 5, text='Fuel Level', font=('Georgia', 8), fill='white', anchor=NW)
    fuel_level_number_text = canvas.create_text(10, 12, text='--.--', font=('Georgia', 17), fill='white', anchor=NW)

    laps_in_race_text = canvas.create_text(80, 5, text='Laps in Race', font=('Georgia', 8), fill='white', anchor=NW)
    laps_in_race_number_text = canvas.create_text(90, 12, text='--.--', font=('Georgia', 17), fill='white', anchor=NW)

    average_text = canvas.create_text(5, 50, text='Average', font=('Georgia', 8), fill='#965ed4', anchor=NW)
    average_number_text = canvas.create_text(10, 57, text='--.--', font=('Georgia', 17), fill='#965ed4', anchor=NW)

    laps_remain_text = canvas.create_text(80, 50, text='Laps Remain', font=('Georgia', 8), fill='#965ed4', anchor=NW)
    laps_remain_number_text = canvas.create_text(90, 57, text='--.--', font=('Georgia', 17), fill='#965ed4', anchor=NW)

    refuel_text = canvas.create_text(175, 50, text='Refuel', font=('Georgia', 8), fill='#965ed4', anchor=NW)
    refuel_number_text = canvas.create_text(175, 57, text='--.--', font=('Georgia', 17), fill='#965ed4', anchor=NW)

    fuel_at_end_text = canvas.create_text(240, 50, text='Fuel at End', font=('Georgia', 8), fill='#965ed4', anchor=NW)
    fuel_at_end_number_text = canvas.create_text(250, 57, text='--.--', font=('Georgia', 17), fill='#965ed4', anchor=NW)

    pit_window_text = canvas.create_text(215, 10, text='Pit', font=('Georgia', 15), fill='gray', anchor=NW)
    pit_window_border = canvas.create_rectangle(210, 12, 245, 32, outline='gray', fill='', width=2)

    exit_button = Button(app, text='X', command=quit_app, anchor=NW, relief=FLAT, background='#1e1f22', fg='red')
    exit_button_holder = canvas.create_window(290, 0, window=exit_button, anchor=NW)


def update():
    global running, cooldown, fuel_start_of_lap, metric, start_count, refuel, laps_remain

    check_iracing()

    if state.ir_connected:
        ir.freeze_var_buffer_latest()

        if ir['DisplayUnits'] == 0:
            metric = False

        if start_count == -1:
            start_count = ir['Lap']

        if ir['IsOnTrack'] == 1:
            # Defined values
            fuel_level = ir['FuelLevel']
            laps_in_race = ir['SessionLapsRemainEx']
            completed_laps = ir['RaceLaps']
            fuel_fill = ir['PitSvFuel']

            if metric is True:
                canvas.itemconfigure(fuel_level_number_text, text=str(round(fuel_level, 2)))
                if ir['Lap'] > (start_count + 2):
                    overflow = fuel_fill - refuel

                    if overflow < 0.0:
                        canvas.itemconfigure(fuel_at_end_number_text, text='0.00')
                    else:
                        canvas.itemconfigure(fuel_at_end_number_text, text=str(round(overflow, 2)))

                    if 5.0 > laps_remain > 3.0:
                        canvas.itemconfigure(pit_window_text, fill='green')
                        canvas.itemconfigure(pit_window_border, outline='green')
                    elif 3.0 > laps_remain > 1.0:
                        canvas.itemconfigure(pit_window_text, fill='yellow')
                        canvas.itemconfigure(pit_window_border, outline='yellow')
                    elif 1.0 > laps_remain >= 0.0:
                        canvas.itemconfigure(pit_window_text, fill='red')
                        canvas.itemconfigure(pit_window_border, outline='red')
                    else:
                        canvas.itemconfigure(pit_window_text, fill='gray')
                        canvas.itemconfigure(pit_window_border, outline='gray')
            else:
                canvas.itemconfigure(fuel_level_number_text, text=str(round(fuel_level / 3.785, 2)))

                if ir['Lap'] > (start_count + 2):
                    overflow = fuel_fill - refuel

                    if overflow < 0.0:
                        canvas.itemconfigure(fuel_at_end_number_text, text='0.00')
                    else:
                        canvas.itemconfigure(fuel_at_end_number_text, text=str(round(overflow / 3.785, 2)))

                    if 5.0 > laps_remain > 3.0:
                        canvas.itemconfigure(pit_window_text, fill='green')
                        canvas.itemconfigure(pit_window_border, outline='green')
                    elif 3.0 > laps_remain > 1.0:
                        canvas.itemconfigure(pit_window_text, fill='yellow')
                        canvas.itemconfigure(pit_window_border, outline='yellow')
                    elif 1.0 > laps_remain >= 0.0:
                        canvas.itemconfigure(pit_window_text, fill='red')
                        canvas.itemconfigure(pit_window_border, outline='red')
                    else:
                        canvas.itemconfigure(pit_window_text, fill='gray')
                        canvas.itemconfigure(pit_window_border, outline='gray')

            if 0.0 <= ir['LapDist'] <= 100.0 and cooldown is False and ir['Lap'] > (start_count + 1):
                if running is False:
                    running = True
                    fuel_start_of_lap = ir['FuelLevel']
                    do_cooldown()
                else:
                    running = False

                    # Estimated values
                    average_lap = calculate_average_lap(ir['LapLastLapTime'])

                    if round(laps_in_race, 2) == 32767:
                        laps_in_race = ir['SessionTimeRemain'] / average_lap

                    canvas.itemconfigure(laps_in_race_number_text, text=str(round(laps_in_race, 2)))

                    average = calculate_average(fuel_start_of_lap, ir['FuelLevel'])
                    laps_remain = calculate_laps_remain(fuel_level, average)
                    refuel = calculate_refuel(laps_in_race, completed_laps, average, fuel_level)

                    if metric is True:
                        canvas.itemconfigure(average_number_text, text=str(round(average, 2)))
                        canvas.itemconfigure(laps_remain_number_text, text=str(round(laps_remain, 2)))
                        if round(laps_in_race, 2) == 32767:
                            canvas.itemconfigure(refuel_number_text, text='--.--')
                        else:
                            canvas.itemconfigure(refuel_number_text, text=str(round(refuel, 2)))
                    else:
                        canvas.itemconfigure(average_number_text, text=str(round(average / 3.785, 2)))
                        canvas.itemconfigure(laps_remain_number_text, text=str(round(laps_remain, 2)))
                        if round(laps_in_race, 2) == 32767:
                            canvas.itemconfigure(refuel_number_text, text='--.--')
                        else:
                            canvas.itemconfigure(refuel_number_text, text=str(round(refuel / 3.785, 2)))
        else:
            reset()

    app.after(250, update)


def calculate_average_lap(last_lap):
    global average_lap_list

    average_lap_list.append(last_lap)

    average_calculated = 0.00

    for number in average_lap_list:
        average_calculated += number

    return average_calculated / len(average_lap_list)


def calculate_average(fuel_start_lap, fuel_end_lap):
    global average_fuel_list

    fuel = fuel_start_lap - fuel_end_lap

    average_fuel_list.append(fuel)

    average_calculated = 0.00

    for number in average_fuel_list:
        average_calculated += number

    return average_calculated / len(average_fuel_list)


def calculate_laps_remain(fuel_level, fuel_average):
    if fuel_average == 0:
        return 0
    else:
        return fuel_level / fuel_average


def calculate_refuel(laps_in_race, completed_laps, fuel_average, fuel_level):
    laps_left = laps_in_race - completed_laps
    fuel_needed = fuel_average * laps_left
    refuel_amount = fuel_needed - fuel_level

    if refuel_amount < 0.00:
        refuel_amount = 0.00

    return refuel_amount


def do_cooldown():
    global cooldown

    if cooldown is False:
        cooldown = True
        app.after(1000, do_cooldown)
    elif cooldown is True and ir['LapDistPct'] >= 0.5:
        cooldown = False
    else:
        app.after(1000, do_cooldown)


if __name__ == '__main__':
    ir = irsdk.IRSDK()
    state = State()

    app = Tk()

    canvas = Canvas(app, width=310, height=90, background='#1e1f22', highlightthickness=0)
    canvas.pack()

    setup_canvas()

    icon = PhotoImage(file='images/fuel.png')

    app.title('Live Fuel Application')
    app.geometry('310x90+275+985')
    app.resizable(False, False)
    app.iconphoto(False, icon)
    app.wm_attributes('-topmost', 1)
    app.attributes('-alpha', 0.925)
    app.overrideredirect(True)
    app.after(1000, update())
    app.mainloop()
