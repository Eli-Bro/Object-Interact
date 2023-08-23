import ttkbootstrap as ttk

import numpy as np
from PIL import Image, ImageTk
import GUI_Functions as gui
from GUI_Visual_Resources import *

'''
Function
'''
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
feedFrameText = ttk.Label(text='CBU Bioengineering Lab', font=('Courier', 25, 'bold', 'italic'), style='warning')
feedFrame = ttk.LabelFrame(labelwidget=feedFrameText, padding=(5, 5), style='warning')
feedFrame.grid(row=0, column=0, rowspan=3, padx=25, pady=(0, 25))

# Create the placeholder picture for the eventual live feed
feed_img, _ = setup_photo_frame('Building.jpg', feedFrame, photoDim)

## Game Info LabelFrame
gameInfoFrameText = ttk.Label(text='Game Info', font=('Courier', 18, 'bold', 'italic'), style='warning')
gameInfoFrame = ttk.LabelFrame(win, style='warning', labelwidget=gameInfoFrameText, padding=(15, 10))
gameInfoFrame.grid(row=0, column=1, padx=(0, 25), pady=(0, 5))

# Score Frame
scoreFrameText = ttk.Label(text='Score', font=('Courier', 14, 'bold'), style='warning')
scoreFrame = ttk.LabelFrame(gameInfoFrame, style='warning', labelwidget=scoreFrameText)
scoreFrame.grid(row=0, column=0, padx=10, pady=(0, 15))

# Score Output Label
scoreLabel = ttk.Label(scoreFrame, text='0', font=('Terminal', 20, 'bold'))
scoreLabel.pack(anchor=ttk.CENTER, pady=15)

# High Score Frame
highScoreFrameText = ttk.Label(text='High Score', font=('Courier', 14, 'bold'), style='warning')
highScoreFrame = ttk.LabelFrame(gameInfoFrame, style='warning', labelwidget=highScoreFrameText)
highScoreFrame.grid(row=0, column=1, padx=10, pady=(0, 15))

# High Score Output Label
highScoreLabel = ttk.Label(highScoreFrame, text='0', font=('Terminal', 20, 'bold'))
highScoreLabel.pack(anchor=ttk.CENTER, pady=15)

# Game timer
timer = ttk.Meter(gameInfoFrame,
                  bootstyle='warning',
                  interactive=False,
                  metersize=140,
                  amounttotal=30,
                  subtext='Time',
                  subtextstyle='warning')
timer.grid(row=2, column=0, columnspan=2)

## Object Label Frame
objectFrameText = ttk.Label(text='Game Controls', font=('Courier', 18, 'bold', 'italic'), style='info')
objectControlFrame = ttk.LabelFrame(win, labelwidget=objectFrameText, style='info', padding=(15, 5))
objectControlFrame.grid(row=1, column=1, padx=(0, 25))

# Circle radius preview frame
previewFrameText = ttk.Label(text='Radius', font=('Courier', 14, 'bold'), style='info')
previewFrame = ttk.LabelFrame(objectControlFrame, labelwidget=previewFrameText, style='info')
previewFrame.grid(row=0, column=0, columnspan=3)

#create the frame for circle radius preview
preview_img, raw_bg = setup_photo_frame('circle_preview.jpg', previewFrame, prevDim)
gui.resize_scale_circle(minRad, preview_img, raw_bg)

def update_radius(e):
    gui.currRadius = int(radiusScale.get())
    gui.resize_scale_circle(radiusScale.get(), preview_img, raw_bg)


# Object Radius scale
radiusScale = ttk.Scale(objectControlFrame, from_=minRad, to=maxRad, command=update_radius, length=310)
radiusScale.grid(row=1, column=0, columnspan=3, pady=5)

# Mirror Toggle
mirrorToggleMode = ttk.BooleanVar()
mirrorToggle = ttk.Checkbutton(objectControlFrame,
                               text='Mirror',
                               command=lambda: gui.toggle_mirror(mirrorToggleMode),
                               variable=mirrorToggleMode,
                               style='round-toggle')
mirrorToggle.grid(row=4, column=1, columnspan=1, pady=(0, 7))

# Time selection
selected = ttk.IntVar()
selected.set(30)
time30 = ttk.Radiobutton(objectControlFrame, text='30s', value=30, variable=selected, style='toolbutton', width=8)
time60 = ttk.Radiobutton(objectControlFrame, text='60s', value=60, variable=selected, style='toolbutton', width=8)
time90 = ttk.Radiobutton(objectControlFrame, text='90s', value=90, variable=selected, style='toolbutton', width=8)

timeBtns = {30: time30, 60: time60, 90: time90}

time30.grid(row=3, column=0)
time60.grid(row=3, column=1)
time90.grid(row=3, column=2)

# Start Object button
startObjectButton = ttk.Button(objectControlFrame,
                               text="Start",
                               command=lambda: gui.start_object(selected, timeBtns),
                               width=8, style='success')
startObjectButton.grid(row=4, column=0, sticky='e', pady=(0, 5))

resetScoreButton = ttk.Button(objectControlFrame,
                              text="Reset",
                              command=lambda: gui.reset_score(timeBtns),
                              width=8, style='danger')
resetScoreButton.grid(row=4, column=2, sticky='w', pady=(0, 5))



## Camera Controls Label Frame
cameraControlText = ttk.Label(text='Camera', font=('Courier', 18, 'bold', 'italic'), style='info')
cameraControlFrame = ttk.LabelFrame(win, labelwidget=cameraControlText, style='info')
cameraControlFrame.grid(row=2, column=1, sticky='n')

# Frame Cap Toggle
frameToggleMode = ttk.BooleanVar()
frameToggle = ttk.Checkbutton(cameraControlFrame,
                              text='Cap Frames',
                              command=lambda: gui.toggle_frame_cap(frameToggleMode),
                              variable=frameToggleMode,
                              style='round-toggle')
frameToggle.grid(row=0, column=0, columnspan=2, pady=(0, 7))

# Stop button
stopFeedButton = ttk.Button(cameraControlFrame,
                            text="Stop",
                            command=lambda: gui.stop_cam(start_object_btn=startObjectButton),
                            width=8,
                            style='danger')
stopFeedButton.grid(row=1, column=1, sticky='e', padx=(0, 10), pady=(0, 10))

# Start Camera button
startFeedButton = ttk.Button(cameraControlFrame,
                             text="Start",
                             command=lambda: gui.initiate_cam(placeholder_img=feed_img, obj_score=scoreLabel, start_object_btn=startObjectButton, timer_meter=timer, high_score=highScoreLabel),
                             width=8,
                             style='success')
startFeedButton.grid(row=1, column=0, sticky='w', padx=(10, 0), pady=(0, 10))

win.mainloop()
