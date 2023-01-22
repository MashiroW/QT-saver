"""
import cairo

def draw_goat(file_path):
    # Create a new image surface
    surface = cairo.SVGSurface(file_path, 300, 300)

    # Create a cairo context
    ctx = cairo.Context(surface)

    # Draw the head
    ctx.arc(150, 150, 50, 0, 2*3.14)
    ctx.set_source_rgb(0.9, 0.9, 0.9)
    ctx.fill()
    ctx.stroke()
    
    # Draw the eyes
    ctx.arc(140, 140, 5, 0, 2*3.14)
    ctx.set_source_rgb(0, 0, 0)
    ctx.fill()
    ctx.stroke()
    ctx.arc(160, 140, 5, 0, 2*3.14)
    ctx.set_source_rgb(0, 0, 0)
    ctx.fill()
    ctx.stroke()
    
    # Draw the ears
    ctx.arc(120, 170, 10, 0, 2*3.14)
    ctx.set_source_rgb(0.9, 0.9, 0.9)
    ctx.fill()
    ctx.stroke()
    ctx.arc(180, 170, 10, 0, 2*3.14)
    ctx.set_source_rgb(0.9, 0.9, 0.9)
    ctx.fill()
    ctx.stroke()
    
    # Draw the horns
    ctx.move_to(120, 130)
    ctx.line_to(100, 110)
    ctx.set_source_rgb(0.5, 0.5, 0.5)
    ctx.stroke()
    ctx.move_to(180, 130)
    ctx.line_to(200, 110)
    ctx.set_source_rgb(0.5, 0.5, 0.5)
    ctx.stroke()
    
    # Draw the legs
    ctx.move_to(120, 200)
    ctx.line_to(120, 250)
    ctx.set_source_rgb(0.5, 0.5, 0.5)
    ctx.stroke()
    ctx.move_to(180, 200)
    ctx.line_to(180, 250)
    ctx.set_source_rgb(0.5, 0.5, 0.5)
    ctx.stroke()
    
    # Save the file
    surface.finish()
    
draw_goat("goat.svg")
"""

"""
import cv2
import numpy as np
import pyttsx3
import time

# Load the goat image
goat = cv2.imread("./chatGPT/goat.jpg")

# Create a VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter("output.avi", fourcc, 30.0, (goat.shape[1], goat.shape[0]))

# Use the pyttsx3 library to create a Text-to-Speech engine
engine = pyttsx3.init()

# Set the voice to the "Pokemon" opening theme
engine.setProperty('voice', 'com.apple.speech.synthesis.voice.BadNews')
engine.say("I wanna be the very best, like no one ever was.")
engine.runAndWait()

# Write the goat image to the video for 3 seconds
for i in range(90):
    out.write(goat)

# Release the VideoWriter object
out.release()

# Release the Text-to-Speech engine
engine.stop()
"""

"""
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0,0.0, -5)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glRotatef(1, 1, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Cube()
        pygame.display.flip()
        pygame.time.wait(10)

def Cube():
    glBegin(GL_QUADS)
    glColor3f(1,0,0)
    glVertex3f( 1, 1,-1)
    glVertex3f(-1, 1,-1)
    glVertex3f(-1, 1, 1)
    glVertex3f( 1, 1, 1)

    glColor3f(0,1,0)
    glVertex3f( 1,-1, 1)
    glVertex3f(-1,-1, 1)
    glVertex3

main()
"""