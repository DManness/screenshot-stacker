# screenshot-stacker
A cross-platform desktop application to create stacked images.

One of the most tedious image editing tasks is combining screenshots one on top of the other. Traditionally you'd have to use a calculator to figure out how big the canvas needs to be, resize it, drag the images into place, and save the composition. Doing two or three images manually is fine, but any more and it starts to get annoying. Enter Screenshot Stacker. A simple Python3 / Qt (PySide2) application that automates simple image compositing. Stacker provides an interface to add multiple images, arrange and align them, and export the resulting composition to a number of different image formats.

## Notice

This software is in the early stages of development. While it is in a functional state, there are many improvements to the user-experience to come. Please review the usage instructions below to create a composition.

## Requirements
This script was built for Python 3.7 and tested with Python 3.9. Using a virtual environment is highly recommended 

## Building

1. Clone the repository to a location on your computer.
2. Create and activate a virtual environment. 
3. Install the required packages using `pip install -r requirements.txt`
4. Start the program by executing main.py

## Usage

1. Click `Add` to select the images for your composition.
2. Select an orientation / alignment for the images.
3. Click `Refresh` to generate a preview **You must click this button before you export your composition.**
4. Enter a path in which to export your composition.
5. Click `Refresh` one more time, then `Export`.
