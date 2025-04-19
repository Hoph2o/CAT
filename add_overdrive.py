from reaper_python import *
import C3toolbox
import C4toolbox
import sys
import os
import traceback
sys.argv=["Main"]

import Tkinter

# Globals
global instrument_var
global length_entry
global frequency_entry
global form

def execute():
    global instrument_var, length_entry, frequency_entry, form

    try:
        instrument_name = str(instrument_var.get())
        length_val = int(length_entry.get())
        frequency_val = int(frequency_entry.get())

        C4toolbox.startup()
        C4toolbox.add_od(instrument_name, length_val, frequency_val, 0)

    except Exception as e:
        RPR_ShowConsoleMsg("Exception occurred:\n" + traceback.format_exc())

    form.destroy()

def launch():
    global instrument_var, length_entry, frequency_entry, form

    form = Tkinter.Tk()
    form.wm_title('Add overdrive')
    C3toolbox.startup()

    helpLf = Tkinter.Frame(form)
    helpLf.grid(row=0, column=1, sticky='NS', padx=5, pady=5)

    OPTIONS = ["Drums", "Guitar", "Bass", "Keys"]
    instrument_var = Tkinter.StringVar(helpLf)
    instrument_var.set(OPTIONS[0])

    instrumentOpt = apply(Tkinter.OptionMenu, (helpLf, instrument_var) + tuple(OPTIONS))
    instrumentOpt.grid(row=0, column=1, columnspan=1, sticky="WE", pady=3)

    lengthLbl = Tkinter.Label(helpLf, text="Overdrive length (in beats):")
    lengthLbl.grid(row=0, column=2, padx=5, pady=2, sticky='W')

    length_entry = Tkinter.Entry(helpLf)
    length_entry.insert(0, "4")
    length_entry.config(width=5)
    length_entry.grid(row=0, column=3, padx=5, pady=2, sticky='W')

    frequencyLbl = Tkinter.Label(helpLf, text="Overdrive frequency (in beats):")
    frequencyLbl.grid(row=0, column=4, padx=5, pady=2, sticky='W')

    frequency_entry = Tkinter.Entry(helpLf)
    frequency_entry.insert(0, "40")
    frequency_entry.config(width=5)
    frequency_entry.grid(row=0, column=5, padx=5, pady=2, sticky='W')

    allBtn = Tkinter.Button(helpLf, text="Create overdrive phrases", command=execute)
    allBtn.grid(row=0, column=6, rowspan=1, sticky="WE", padx=5, pady=2)

    logo = Tkinter.Frame(form, bg="#000")
    logo.grid(row=8, column=0, columnspan=10, sticky='WE', padx=0, pady=0)

    path = os.path.join(sys.path[0], "banner.gif")
    if os.path.exists(path):
        img = Tkinter.PhotoImage(file=path)
        imageLbl = Tkinter.Label(logo, image=img, borderwidth=0)
        imageLbl.image = img  # Keep reference
        imageLbl.grid(row=0, column=0, rowspan=2, sticky='E', padx=0, pady=0)

    form.mainloop()

if __name__ == '__main__':
    launch()
