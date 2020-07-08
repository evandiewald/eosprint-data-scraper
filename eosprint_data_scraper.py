import pytesseract
import pyautogui as gui
import time
from utils import parse_data
import pandas as pd
import tkinter as tk

########### USER INPUTS ############
# path to tesseract executable (windows only)
pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files\Tesseract-OCR\tesseract.exe'
# start and end indices of parameter sets of interest (see README.md)
param_start = 3
param_end = param_start + 6

##################################################################################################################
# get screen size (16:9 screens only at this point)
screen_dimensions = gui.size()

## positions: configured on a 1920x1080 display with EOSPRINT 2.5 in full-screen mode and a small taskbar at the bottom
##              of the screen (Windows). If additional tweaking is needed, use the simple get_mouse_position.py script
# exposure tab
exposure_tab_position = [1056/1920*screen_dimensions.width, 33/1080*screen_dimensions.height]
# exposure set library
exposure_set_library_position = [45/1920*screen_dimensions.width, 201/1080*screen_dimensions.height]
# exposure set starting position
exposure_set_init_position = [257/1920*screen_dimensions.width, 241/1080*screen_dimensions.height]
# process settings
process_settings_position = [45/1920*screen_dimensions.width, 297/1080*screen_dimensions.height]
# machine settings screenshot
machine_settings_region = [105/1920*screen_dimensions.width, 167/1080*screen_dimensions.height, (405-105)/1920*screen_dimensions.width, (755-167)/1080*screen_dimensions.height]
# machine settings close tab
machine_settings_dropdown = [133/1920*screen_dimensions.width, 177/1080*screen_dimensions.height]
# exposure settings screenshot (scroll down first)
exposure_settings_region = [107/1920*screen_dimensions.width, 175/1080*screen_dimensions.height, (406-107)/1920*screen_dimensions.width, (891-175)/1080*screen_dimensions.height]
# parameter set starting position
param_set_init_position = [685/1920*screen_dimensions.width, 241/1080*screen_dimensions.height]
# hatch region for screenshot
hatch_region = [877/1920*screen_dimensions.width, 316/1080*screen_dimensions.height, (1256-877)/1920*screen_dimensions.width, (933-316)/1080*screen_dimensions.height]
# upskin/downskin region for screenshot
upskin_region = [877/1920*screen_dimensions.width, 171/1080*screen_dimensions.height, (1256-877)/1920*screen_dimensions.width, (933-171)/1080*screen_dimensions.height]
# upskin_region = [890, 440, 1251-890, 762-440]


########################## PROCEDURE ############################

time.sleep(5)
# click on exposure tab
gui.moveTo(exposure_tab_position[0], exposure_tab_position[1], duration=1)
gui.click()
time.sleep(1)

# click on exposure set library
gui.moveTo(exposure_set_library_position[0], exposure_set_library_position[1])
gui.click()
time.sleep(4)

# move through parameter sets
exposure_parameters = []
k = 0
for i in range(*{'start':param_start,'stop':param_end,'step':1}.values()):
    x_pos = exposure_set_init_position[0]
    y_pos = exposure_set_init_position[1] + i*(60/1080*screen_dimensions.height)
    gui.moveTo(x_pos, y_pos)
    gui.click()
    time.sleep(1)

    param_settings = []
    for j in range(7):
        x_pos = param_set_init_position[0]
        y_pos = param_set_init_position[1] + j*(60/1080*screen_dimensions.height)
        gui.moveTo(x_pos, y_pos)
        gui.click()
        time.sleep(1)

        gui.moveTo(900/1920*screen_dimensions.width, 500/1080*screen_dimensions.height)
        gui.scroll(60)
        time.sleep(1)

        # assumes standard layout of hatch, infill, upskin, downskin, contour, contour, edge
        # upskin and downskin look slightly different
        if 1 < j < 4:
            gui.moveTo(914/1920*screen_dimensions.width, 335/1080*screen_dimensions.height)
            gui.click()
            gui.scroll(-60)

            gui.screenshot('upskin_test.png', region=upskin_region)
            data = pytesseract.image_to_string('upskin_test.png')
            param_settings.append(parse_data(data))
        else:
            gui.screenshot('hatch_test.png', region=hatch_region)
            data = pytesseract.image_to_string('hatch_test.png')
            param_settings.append(parse_data(data))
        time.sleep(1)

    exposure_parameters.append(param_settings)


# process settings
gui.moveTo(process_settings_position[0], process_settings_position[1], duration=1)
gui.click()
time.sleep(2)

gui.screenshot('process_settings.png', region=machine_settings_region)
time.sleep(1)
process_settings = parse_data(pytesseract.image_to_string('process_settings.png'))

# close dropdown and scroll down
gui.moveTo(machine_settings_dropdown[0], machine_settings_dropdown[1])
gui.click()
gui.scroll(-50)

gui.screenshot('machine_settings.png', region=exposure_settings_region)
time.sleep(1)
machine_settings = parse_data(pytesseract.image_to_string('machine_settings.png'))

process_settings = {**process_settings, **machine_settings}

###################### EXPORTING #############################

exposure_df = pd.DataFrame()
for i in range(len(exposure_parameters)):
    exposure_df = exposure_df.append(pd.DataFrame.from_dict(exposure_parameters[i]))

exposure_df.to_csv('exposure_parameters.csv')

process_settings_df = pd.DataFrame(process_settings, index=[0])
process_settings_df.to_csv('process_settings.csv')

root = tk.Tk()
root.title("EOSPRINT Scraping Complete!")
label = tk.Label(root, text="Scraping complete. You can use your computer again.")
label.pack(side="top", fill="both", expand=True, padx=20, pady=20)
button = tk.Button(root, text="OK", command=lambda: root.destroy(), width=30)
button.pack(side="bottom", fill="none", expand=True)
root.mainloop()
