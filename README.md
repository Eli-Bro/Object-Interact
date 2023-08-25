![ezgif com-gif-maker](https://github.com/Eli-Bro/Object-Interact/assets/78119596/3f69078f-3883-4093-9506-455b06f62c2b)

# Object Interaction Rehabilitation Program
- [Description](#description)
- [Set Up](#set-up)
- [How to Use](#how-to-use)

## Description
This program uses MediaPipe Human Pose Estimation paired with OpenCV to allow the user's movement to be tracked by a camera connected to the computer. The user can then play a game where circles appear around the captured video, and the user must hit the circles with either their hands or feet. The goal is to hit as many circles as possible within the time limit. Tools such as this one can be employed in rehabilitation programs to encourage daily active movement, and serves as an example of how AI tools can benefit the biomedical field.

## Set Up
The hardware required for the program is a computer and camera (either integrated in the computer like a laptop camera, or external webcam).

For the software, after downloading the project repo, install the required packages via the terminal
```python console
pip install -r requirements.txt
```

If there issues with the pip installation, such as the **access denied** message, try the following command then reset the terminal  
```python console
pip install --upgrade pip --user
```

## How to Use
To start playing the game:
1. Run the [Game_GUI.py](https://github.com/Eli-Bro/Object-Interact/blob/Fix/Game_GUI.py) file to start the front panel.
2. Start the camera under ***Camera***.
3. Select the game duration, available in **30**, **60**, or **90** seconds.
4. Select the circle size via the ```slider```.
5. Once started, a green circle will appear on the captured video. Hit it and start the game!
   - Once the game ends, a new green circle will appear.
6. For an extra challenge, turn on the ```mirror toggle``` to flip the image!

### Extra Controls
- The reset button in ***Game Controls*** allows the user to end the current game, but the start button must be clicked again to begin another game.
- The ```Cap Frame toggle``` allows for the video feed to limited at 5fps. By default, the frame rate will be unlimited.