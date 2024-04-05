# Bajar ffmpeg de la pagina oficial
# Crear una carpera con los .exe en C:
# Añadir la ruta a la lista de PATHS

import ffmpeg
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from threading import Thread
from PIL import Image, ImageTk
import customtkinter
import subprocess

# Constants
ffmpegPath = r"C:\PATH_Programs\ffmpeg.exe"
inputPath = r"C:\Users\mamec\Documents\VS projects\VideoCompresor"
outputPath = r"C:\Users\mamec\Documents\VS projects\VideoCompresor"

#Variables
selectedInputPath = " "
selectedOutputPath = " "

# dark | system | light
customtkinter.set_appearance_mode("dark")

# blue | green | darl-blue
customtkinter.set_default_color_theme("dark-blue")

# Thread for the compress button so the app won't freeze
def start_main():
    t = Thread(target=compress, daemon=True)
    t.start()

def compress():
    global selectedInputPath
    global selectedOutputPath

    if selectedInputPath == '':
        lb_percentage.configure(text = "Input path not selected!", text_color = "red")
    
    elif selectedOutputPath == '':
        lb_percentage.configure(text = "Output path not selected!", text_color = "red")
    
    else:
        totalFrames = totalVideoFrames(selectedInputPath)

        cmd = [ffmpegPath, "-y", '-i', selectedInputPath, selectedOutputPath]
        process = subprocess.Popen(cmd,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                universal_newlines=True)

        for line in iter(process.stdout.readline, ''):
            if "frame=" in line:
                percentage = calculatePercentage(totalFrames, line[7:12].lstrip())
                bar_progress.set(percentage)
                lb_percentage.configure(text = (" Compressing... (" + str(int(percentage * 100)) + " %)"), text_color = "yellow")
    
        lb_percentage.configure(text = "Compression ended!", text_color = "green")
     
def totalVideoFrames(path):
    probe = ffmpeg.probe(path)
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)

    if video_stream:
        num_frames = int(video_stream['nb_frames'])      
        print("Total video frames:", num_frames)
        return num_frames
    else:
        print("There is no frame info.")

def calculatePercentage(totalFrames, currentFrame):
    percentage = (int(currentFrame) / int(totalFrames))
    return percentage

def browseInput():
    global selectedInputPath
    selectedInputPath = askopenfilename(initialdir = inputPath, filetypes = (("MP4 Files", "*.mp4"),("All Files", "*.*")))

    if(selectedInputPath != ""):
        entry_input.configure(placeholder_text = selectedInputPath)

def browseOutput():
    global selectedOutputPath
    selectedOutputPath = asksaveasfilename(initialdir = outputPath, filetypes = (("MP4 Files", "*.mp4"),("All Files", "*.*")))

    if(selectedOutputPath != ""):
        entry_output.configure(placeholder_text = selectedOutputPath)

def getFrame():
    subprocess.call(['ffmpeg', '-i', video_input_path, '-ss', '00:00:00.000', '-vframes', '1', img_output_path])

app = customtkinter.CTk()
app.title("Video Compresor")
app.geometry("680x700")

# Menu and sub menu
menu = tk.Menu(app)

app_menu = tk.Menu(menu, tearoff = False)
app_menu.add_command(label = "Close", command = lambda: exit())
menu.add_cascade(label = "Application", menu = app_menu)

config_menu = tk.Menu(menu, tearoff = False)
menu.add_cascade(label = "Configutarion", menu = config_menu)

help_menu = tk.Menu(menu, tearoff = False)
menu.add_cascade(label = "Help", menu = help_menu)

app.configure(menu = menu)

# Title
label = customtkinter.CTkLabel(master=app, text=" VIDEO COMPRESOR", font=("Roboto", 24, "bold"), text_color="#2596be")
label.grid(pady=20, padx=10)

# Frame Paths
framePaths = customtkinter.CTkFrame(master=app)
framePaths.grid(pady=20, padx=60)


# -- Input button
entry_input = customtkinter.CTkEntry(master=framePaths, placeholder_text="Input Path", width=400)                      
entry_input.grid(column=0, row=0, pady=5, padx=5)

bt_Input = customtkinter.CTkButton(master=framePaths, text="Browse", command=browseInput)
bt_Input.grid(column=1, row=0, pady=5, padx=5)


# -- Output button
entry_output = customtkinter.CTkEntry(master=framePaths, placeholder_text="Output Path", width=400)
entry_output.grid(column=0, row=1, pady=4, padx=4) 

bt_Output = customtkinter.CTkButton(master=framePaths, text="Browse", command=browseOutput)
bt_Output.grid(column=1, row=1, pady=4, padx=4)

# -- Progress bar
bar_progress = customtkinter.CTkProgressBar(master=framePaths, orientation="horizontal", width=400, height=20)
bar_progress.grid(column=0, row=2, pady=4, padx=4) 
bar_progress.set(0.0)

# -- Compress
buttonCompress = customtkinter.CTkButton(master=framePaths, text="Compress", command=start_main)
buttonCompress.grid(column=1, row=2, pady=4, padx=4) 

# -- Percentage label
lb_percentage = customtkinter.CTkLabel(master=framePaths, text="* Compression status *")
lb_percentage.grid(column=0, row=3, pady=4, padx=4) 


# Frame Thumbnail
frameThumbnail = customtkinter.CTkFrame(master=app)
frameThumbnail.grid(pady=20, padx=60)


display = customtkinter.CTkImage(dark_image = Image.open('preview.png'),
                                 light_image=Image.open('preview.png'),
                                 size=(400,250))
                                 

lb_tn_text = customtkinter.CTkLabel(master=frameThumbnail, text="THUMBNAIL PREVIEW", font=("Roboto", 14, "bold"), text_color="#2596be")
lb_tn_text.grid(column=0, row=0, pady=10, padx=4) 

lb_preview = customtkinter.CTkLabel(master=frameThumbnail, text="", image=display)
lb_preview.grid(column=0, row=1, pady=15, padx=40)

app.mainloop()

