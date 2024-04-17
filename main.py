# Bajar ffmpeg de la pagina oficial
# Crear una carpera con los .exe en C:
# Añadir la ruta a la lista de PATHS

import ffmpeg
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from threading import Thread
from PIL import Image
import customtkinter
import subprocess

# Constants
ffmpegPath = r"C:\PATH_Programs\ffmpeg.exe"
inputPath = r"C:\Users\mamec\Documents\VS projects\VideoCompresor"
outputPath = r"C:\Users\mamec\Documents\VS projects\VideoCompresor"

#Variables
selectedInputPath = " "
selectedOutputPath = " "
selectedTNOutputPath = " "
duracion_formateada = " "

# dark | system | light
customtkinter.set_appearance_mode("dark")

# blue | green | darl-blue
customtkinter.set_default_color_theme("dark-blue")

# Thread for the compress button so the app won't freeze
def start_main():
    t = Thread(target=compress, daemon=True)
    t.start()

def start_main_TN():
    t = Thread(target=generateTN, daemon=True)
    t.start()

def sliderListener():
    print("Slider moved " + slider._command)

def generateTN():
    global selectedInputPath
    global selectedTNOutputPath
    
    #subprocess.call(['ffmpeg', '-i', selectedInputPath, '-ss', '00:00:00.000', '-vframes', '1', selectedTNOutputPath])
    #subprocess.call(['ffmpeg', '-i', selectedInputPath, '-ss', duracion_formateada, '-vframes', '1', selectedTNOutputPath])
    subprocess.call(['ffmpeg', '-i', selectedInputPath, '-vf', f"select=gte(n\\,{totalVideoFrames})", '-vframes', '1', selectedTNOutputPath])
    print("TRAZAAAA " + selectedTNOutputPath)
    display.configure(dark_image = Image.open(selectedTNOutputPath), light_image = Image.open(selectedTNOutputPath), size=(480,270))
    slider.to(int(totalVideoFrames))
    
def getAllFrames():
    for frame in range (int(totalVideoFrames(selectedInputPath))):
        if frame % 90 == 0:
            subprocess.call(['ffmpeg', '-y', '-i', selectedInputPath, '-vf', f"select=gte(n\\,{frame})", '-vframes', '1', f'tempFrames\{frame}.png'])

def setFirstFrame():
    subprocess.call(['ffmpeg', '-y', '-i', selectedInputPath, '-vf', f"select=gte(n\\,{0})", '-vframes', '1', r'temp\first.png'])

    previewFrame = Image.open(r'temp\first.png')

    display.configure(light_image = previewFrame, 
                      dark_image = previewFrame,
                      size=(320,180))
    
    slider.configure(to=(int(totalVideoFrames(selectedInputPath))))

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
    global duracion_formateada
    global selectedInputPath

    selectedInputPath = askopenfilename(initialdir = inputPath, filetypes = (("MP4 Files", "*.mp4"),("All Files", "*.*")))

    cmd = ['ffprobe', '-i', selectedInputPath, '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv=p=0']

    process = subprocess.Popen(cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            universal_newlines=True)

    duracion_str = process.stdout.readline()
    duracion_segundos = float(duracion_str)

    duracion_formateada = str(int(duracion_segundos // 3600)).zfill(2) + ':' + \
                            str(int((duracion_segundos % 3600) // 60)).zfill(2) + ':' + \
                            str(int(duracion_segundos % 60)).zfill(2)

    setFirstFrame()
    getAllFrames()

    if(selectedInputPath != ""):
        entry_input.configure(placeholder_text = selectedInputPath)

def browseOutput():
    global selectedOutputPath
    selectedOutputPath = asksaveasfilename(initialdir = outputPath, filetypes = (("MP4 Files", "*.mp4"),("All Files", "*.*")))

    if(selectedOutputPath != ""):
        entry_output.configure(placeholder_text = selectedOutputPath)

def browseOutputTN():
    global selectedTNOutputPath
    selectedTNOutputPath = asksaveasfilename(initialdir = outputPath, filetypes = (("PNG Files", "*.png"),("All Files", "*.*")))

    if(selectedOutputPath != ""):
        TN_output.configure(placeholder_text = selectedTNOutputPath)
    
    

app = customtkinter.CTk()
app.title("Video Compresor")
app.geometry("750x800")

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

firstPreviewImage = Image.open(r'resources\noVideo2.png')

display = customtkinter.CTkImage(dark_image = firstPreviewImage, 
                                 light_image = firstPreviewImage,
                                 size=(320,180))
                                 

lb_tn_text = customtkinter.CTkLabel(master=frameThumbnail, text="THUMBNAIL PREVIEW", font=("Roboto", 14, "bold"), text_color="#2596be")
lb_tn_text.grid(column=0, row=0, pady=10, padx=4) 

# Slider
slider = customtkinter.CTkSlider(master=frameThumbnail, from_=0, to=100, width=400)
slider.grid(column=0, row=1, pady=10, padx=4) 
slider.set(0)

lb_preview = customtkinter.CTkLabel(master=frameThumbnail, text="", image=display)
lb_preview.grid(column=0, row=2, pady=15, padx=40)

# -- Generate
TN_output = customtkinter.CTkEntry(master=frameThumbnail, placeholder_text="Output Path", width=400)
TN_output.grid(column=0, row=3, pady=4, padx=4) 

bt_Output = customtkinter.CTkButton(master=frameThumbnail, text="Browse", command=browseOutputTN)
bt_Output.grid(column=1, row=3, pady=4, padx=4)

buttonGenerateTN = customtkinter.CTkButton(master=frameThumbnail, text="Generate", command=start_main_TN)
buttonGenerateTN.grid(column=1, row=4, pady=4, padx=4) 

app.mainloop()


