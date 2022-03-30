This Python script is about navigating cursor by the movement of your head.
The idea was born from a short video that had been made by Opera developers in 2009 for a April Fool's Day.

It uses only 2 libraries - OpenCV to face and eyes recognition and pyautogui to emulate the cursor movement.
The face and eyes recognition uses Haar Cascade algorithms.

At first it detect face on a single frame from the camera. After that algorithm draws a rectangle around found object.This rectangle becomes the region of interest, because eyes has to be inside it.In the next step algorithm is looking for eyes in this RoI and also put them into a rectangle.After that it checks if only 1 eye has been detected (you can just cover your eye by your hand to satisfy this condition) and if it is satisfied it causes mouse click. If the eye's x coordinate would be greater than the half of RoI width (that means only left eye was detected) then script triggers left click, in other case (if the x coordinate is smaller than half of a RoI width) it triggers right click. I would like to say that this idea is not optimal - it is quite hard to make a double click and also this detection is not as accurate as we could wish so it is possible to trigger this event unnecessary. In other case (if there is both of eyes or none of eyes detected) it allows user to move the cursor. In the showed image there are drawn some of lines to simplify this proces. If users head is at the left side of the image,script moves cursor to the left side, if it's at the bottom-right side script moves cursor in the same direction.

To exit from the script execution, user has to press the 'q' key in the frame window. 
