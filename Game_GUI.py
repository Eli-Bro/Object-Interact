import ttkbootstrap as ttk

import numpy as np
from PIL import Image, ImageTk
import GUI_Functions as gui
from GUI_Visual_Resources import *

def setup_photo_frame(photo, labelFrame, dims):
    im = Image.open(photo)
    im = im.resize(dims)
    frame = np.asarray(im)
    img = ImageTk.PhotoImage(Image.fromarray(frame))
    placeholder_img = ttk.Label(labelFrame)
    placeholder_img.grid(row=0, column=0)
    placeholder_img.configure(image=img)
    placeholder_img.image = img
    placeholder_img.update()
    return placeholder_img, frame

# Create tkinter window
win = ttk.Window(themename='superhero')
win.title("Object Interact")
style = ttk.Style()

## Live Feed Label Frame
feedFrameText = ttk.Label(text='Video Frame', font=('Courier', 25, 'bold'), style='warning')
feedFrame = ttk.LabelFrame(labelwidget=feedFrameText, padding=(25, 25), style='warning')
feedFrame.grid(row=0, column=0, rowspan=3, padx=25, pady=25)

# Create the placeholder picture for the eventual live feed
feed_img, _ = setup_photo_frame('Building.jpg', feedFrame, photoDim)

## Game Info LabelFrame
gameInfoFrame = ttk.LabelFrame(win, text='Game Info')
gameInfoFrame.grid(row=0, column=1)

# Score Title
scoreTitle = ttk.Label(gameInfoFrame, text='Score')
scoreTitle.grid(row=0, column=0)

# Score Output Label
scoreLabel = ttk.Label(gameInfoFrame, text='---')
scoreLabel.grid(row=1, column=0)

# Game timer
timer = ttk.Meter(gameInfoFrame,
                  bootstyle='warning',
                  interactive=False,
                  metersize=140,
                  amounttotal=30,
                  subtext='Time',
                  subtextstyle='warning')
timer.grid(row=2, column=0)

## Object Label Frame
objectControlFrame = ttk.LabelFrame(win, text='Game Controls')
objectControlFrame.grid(row=1, column=1)

# Circle radius preview frame
previewFrame = ttk.LabelFrame(objectControlFrame, text='Preview')
previewFrame.grid(row=0, column=0, columnspan=2)

#create the frame for circle radius preview
preview_img, raw_bg = setup_photo_frame('circle_preview.jpg', previewFrame, prevDim)
gui.resize_scale_circle(minRad, preview_img, raw_bg)

def update_radius(e):
    gui.currRadius = int(radiusScale.get())
    gui.resize_scale_circle(radiusScale.get(), preview_img, raw_bg)


# Object Radius scale
radiusScale = ttk.Scale(objectControlFrame, from_=minRad, to=maxRad, command=update_radius) #TODO: Issues with the event param, need to maybe use Game functions
radiusScale.grid(row=1, column=0, columnspan=2)

# Mirror Toggle
#TODO: Change size of toggle
mirrorToggleMode = ttk.BooleanVar()
mirrorToggle = ttk.Checkbutton(objectControlFrame,
                               text='Mirror',
                               command=lambda: gui.toggle_mirror(mirrorToggleMode),
                               variable=mirrorToggleMode,
                               style='round-toggle')
mirrorToggle.grid(row=2, column=0, columnspan=2)
print(mirrorToggle.winfo_class())
style.configure('TCheckbutton', font=100)

# Time selection
selected = ttk.IntVar()
selected.set(30)
time30 = ttk.Radiobutton(objectControlFrame, text='30s', value=30, variable=selected, style='toolbutton')
time60 = ttk.Radiobutton(objectControlFrame, text='60s', value=60, variable=selected, style='toolbutton')
time90 = ttk.Radiobutton(objectControlFrame, text='90s', value=90, variable=selected, style='toolbutton')

timeBtns = {30: time30, 60: time60, 90: time90}

time30.grid(row=3, column=0)
time60.grid(row=3, column=1)
time90.grid(row=3, column=2)

# Start Object button
startObjectButton = ttk.Button(objectControlFrame,
                               text="Start",
                               command=lambda: gui.start_object(selected, timeBtns))
startObjectButton.grid(row=4, column=0)

resetScoreButton = ttk.Button(objectControlFrame,
                              text="Reset",
                              command=lambda: gui.reset_score())
resetScoreButton.grid(row=4, column=1)



## Camera Controls Label Frame
cameraControlFrame = ttk.LabelFrame(win, text='Camera Controls')
cameraControlFrame.grid(row=2, column=1)

# Frame Cap Toggle
#TODO: Change size of toggle
frameToggleMode = ttk.BooleanVar()
frameToggle = ttk.Checkbutton(cameraControlFrame,
                              text='Cap Frames',
                              command=lambda: gui.toggle_frame_cap(frameToggleMode),
                              variable=frameToggleMode,
                              style='round-toggle')
frameToggle.grid(row=0, column=0, columnspan=2)
print(frameToggle.winfo_class())
style.configure('TCheckbutton', font=100)

# Stop button
stopFeedButton = ttk.Button(cameraControlFrame,
                            text="Stop",
                            command=lambda: gui.stop_cam(start_object_btn=startObjectButton))
stopFeedButton.grid(row=1, column=1)

# Start Camera button
startFeedButton = ttk.Button(cameraControlFrame,
                             text="Start",
                             command=lambda: gui.initiate_cam(placeholder_img=feed_img, obj_score=scoreLabel, start_object_btn=startObjectButton, timer_meter=timer))
startFeedButton.grid(row=1, column=0)

win.mainloop()
