import json
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from pathlib import Path
from datetime import datetime
import configparser

ROOT = Path(__file__).resolve().parent

DEFAULT_OUTPUT_DIR = ROOT / "staging"
DEFAULT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_SETTINGS = {
    "client_id": "default_client_id",
    "export_directory": ROOT / "staging"
}

def _reloadSettings():     
    global settings
    settings = _loadSettings()

def main():
    _reloadSettings()

    def submit_form():
        if(settings["client_id"] == "default_client_id"):
            messagebox.showwarning("Client Id Not Set", "Please set a valid Client Id before submitting the form.")
            return
        
        messagebox.showinfo("Form Submitted", f"Team Id: {id_entry.get()}\nNotes: {notes_entry.get()}")

        data = [
                {
                    "team_id": id_entry.get(),
                    "notes": notes_entry.get(),
                    "status": selected_status.get()
                }
            ]
        
        file_name = f"{settings['client_id']}_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
        if Path(settings["export_directory"]) != DEFAULT_OUTPUT_DIR:
            export_file = Path(settings["export_directory"]) / file_name
        else:
            export_file = DEFAULT_OUTPUT_DIR / file_name
        with open(export_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    main_window = tk.Tk()
    screen_width = main_window.winfo_screenwidth()
    screen_height = main_window.winfo_screenheight()
    main_window.geometry("1000x600+%d+%d" % (screen_width/2-500, screen_height/2-300))
    main_window.resizable(True,True)


    mainFrame = tk.Frame(master = main_window)
    mainFrame.pack()

    id_label = tk.Label(master=mainFrame, text="Team Id:")
    id_label.grid(row=0, column=0)
    id_entry = tk.Entry(master=mainFrame)
    id_entry.grid(row=0, column=1)  

    notes_label = tk.Label(master=mainFrame, text="Notes:")
    notes_label.grid(row=1, column=0)
    notes_entry = tk.Entry(master=mainFrame)
    notes_entry.grid(row=1, column=1)

    selected_status = tk.StringVar(value="option_1")

    status_label = tk.Label(master=mainFrame, text="Status:")
    status_label.grid(row=2, column=0, sticky="nw")

    status_frame = tk.Frame(master=mainFrame)
    status_frame.grid(row=2, column=1, sticky="w")

    option_1_button = tk.Radiobutton(
        master=status_frame,
        text="Option 1",
        variable=selected_status,
        value="option_1",
        indicatoron=0,
        width=12
    )
    option_1_button.grid(row=0, column=0, padx=2, pady=2)

    option_2_button = tk.Radiobutton(
        master=status_frame,
        text="Option 2",
        variable=selected_status,
        value="option_2",
        indicatoron=0,
        width=12
    )
    option_2_button.grid(row=0, column=1, padx=2, pady=2)

    option_3_button = tk.Radiobutton(
        master=status_frame,
        text="Option 3",
        variable=selected_status,
        value="option_3",
        indicatoron=0,
        width=12
    )
    option_3_button.grid(row=0, column=2, padx=2, pady=2)

    submit_button = tk.Button(master=mainFrame, text="Submit", command=submit_form)
    submit_button.grid(row=3, column=0, columnspan=2)

    open_settings_button = tk.Button(master=mainFrame, text="Open Settings", command=lambda: openSettings(main_window))
    open_settings_button.grid(row=6, column=0, columnspan=2)

    main_window.mainloop()

def _ensureSettings():
    settings_file = ROOT / "settings.ini"
    if settings_file.exists(): return

    config = configparser.ConfigParser()
    config["SETTINGS"] = DEFAULT_SETTINGS.copy()
    with open(settings_file, "w") as f:
        config.write(f)

def _loadSettings():
    _ensureSettings()

    config = configparser.ConfigParser()
    config.read(ROOT / "settings.ini")

    if "SETTINGS" not in config:
        config["SETTINGS"] = {}

    changed = False
    for key, default_value in DEFAULT_SETTINGS.items():
        if key not in config["SETTINGS"]:
            config["SETTINGS"][key] = default_value
            changed = True
    if changed:
        with open(ROOT / "settings.ini", "w") as f:
            config.write(f)
    
    return config["SETTINGS"]

def _updateSettings(key, value):
    _ensureSettings()

    config = configparser.ConfigParser()
    config.read(ROOT / "settings.ini")

    if "SETTINGS" not in config:
        config["SETTINGS"] = {}

    config["SETTINGS"][key] = value

    with open(ROOT / "settings.ini", "w") as f:
        config.write(f)
        
    _reloadSettings()

def openSettings(window):
        settings_window = tk.Toplevel(window)

        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        settings_window.geometry("400x500+%d+%d" % (screen_width/2-200, screen_height/2-250))
        settings_window.resizable(False,False)
        # settings_window.attributes('-topmost', 1)

        settings_window.title("Settings")

        client_id_label = tk.Label(master=settings_window, text="Client Id:")
        client_id_label.grid(row=3, column=0)
        client_id_entry = tk.Entry(master=settings_window)
        client_id_entry.insert(0, settings["client_id"])
        client_id_entry.grid(row=3, column=1)

        directory_label = tk.Label(master=settings_window, text="Export Directory:")
        directory_label.grid(row=4, column=0)
        directory_entry = tk.Entry(master=settings_window)
        directory_entry.insert(0, settings["export_directory"])
        directory_entry.grid(row=4, column=1)

        def pickDirectory(entry):
            selected_directory = filedialog.askdirectory()
            if selected_directory and Path(selected_directory).exists():
                entry.delete(0, tk.END)
                entry.insert(0, selected_directory)
                _updateSettings("export_directory", selected_directory)
        
        pick_directory_button = tk.Button(master=settings_window, text="Browse", command=lambda: pickDirectory(directory_entry))
        pick_directory_button.grid(row=4, column=2)
        
        def closeWindow(): 
            _updateSettings("client_id", client_id_entry.get())
            if(Path(directory_entry.get()).exists()):
                _updateSettings("export_directory", directory_entry.get())
            else:
                messagebox.showerror("Invalid Directory", "The specified export directory does not exist. Please enter a valid directory.")
                return

            settings_window.destroy()

        settings_window.protocol("WM_DELETE_WINDOW", closeWindow)

if __name__ == '__main__': main()