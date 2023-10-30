#!/usr/bin/python3
# coding: utf-8

import pygame
from pygame.locals import *
import os

"""
    Packie 1.2 - Pygame-emulation of a CX16 BASIC sprite example.

    Copyright (C) 2023 Hauke Lubenow

    This program is free software: you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

SCALEFACTOR = 2

spritedata = ( (960, 4080, 16380, 16380, 65535, 65535, 65535, 65535,
                65535, 65535, 65535, 65535, 16380, 16380, 4080, 960),
               (960, 960, 4080, 16380, 16380, 65535, 65520, 65472,
                65280, 65280, 65472, 65520, 65535, 16380, 4080, 960),
               (960, 4080, 16380, 16368, 65520, 65472, 65472, 65280,
                65280, 65472, 65472, 65520, 16368, 16380, 4080, 960) )

COLORS = {"cxblue"       : (0, 0, 170),
          "cxwhite"      : (255, 255, 255),
          "packieyellow" : (238, 238, 119),
          "transparent"  : (0, 0, 0, 0) }

class InputHandler:

    def __init__(self, hasjoystick):
        self.hasjoystick = hasjoystick

        self.data = { pygame.K_LEFT   : "left", pygame.K_RIGHT : "right",
                      pygame.K_UP     : "up",   pygame.K_DOWN  : "down",
                      pygame.K_LCTRL  : "fire", pygame.K_q     : "quit",
                      pygame.K_ESCAPE : "quit" }

        self.datakeys = self.data.keys()
        self.datavalues = self.data.values()

        self.joystick = {}
        if self.hasjoystick:
            self.initJoystick()
        self.initKeys()

    def initJoystick(self):
        self.js = pygame.joystick.Joystick(0)
        self.js.init()
        for i in self.datavalues:
            if i == "quit":
                continue
            self.joystick[i] = False

    def initKeys(self):
        self.keypresses = {}
        for i in self.datakeys:
            self.keypresses[i] = False

    def processEvents(self):
        actions = {"left" : False, "right" : False, "up" : False, "down" : False,
                   "fire" : False, "quit" : False}
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                for i in self.keypresses:
                    if event.key == i:
                        self.keypresses[i] = True
            if event.type == pygame.KEYUP:
                for i in self.keypresses:
                    if event.key == i:
                        self.keypresses[i] = False
            if self.hasjoystick:
                if event.type == pygame.JOYBUTTONDOWN:
                    self.joystick["fire"] = True
                if event.type == pygame.JOYBUTTONUP:
                    self.joystick["fire"] = False
                if event.type == pygame.JOYAXISMOTION:
                    # Joystick pushed:
                    if event.axis == 0 and int(event.value) == -1:
                        self.joystick["left"] = True
                    if event.axis == 0 and int(event.value) == 1:
                        self.joystick["right"] = True
                    if event.axis == 1 and int(event.value) == -1:
                        self.joystick["up"] = True
                    if event.axis == 1 and int(event.value) == 1:
                        self.joystick["down"] = True
                    # Joystick released:
                    if event.axis == 0 and int(event.value) == 0:
                        self.joystick["left"] = False
                        self.joystick["right"] = False
                    if event.axis == 1 and int(event.value) == 0:
                        self.joystick["up"] = False
                        self.joystick["down"] = False

        # Same indentation level as "for event in pygame.event.get()":
        for i in self.datakeys:
            if self.keypresses[i]:
                actions[self.data[i]] = True
        if self.hasjoystick:
            for i in self.datavalues:
                if i == "quit":
                    continue
                if self.joystick[i]:
                    actions[i] = True
        return actions


class ImageCreator:

    def __init__(self):
        self.images = {}

        self.images["right"] = []
        for i in range(3):
            self.images["right"].append(self.getSurface(spritedata[i]))

        self.images["left"] = []
        self.images["left"].append(self.getSurface(spritedata[0]))
        self.images["left"].append(self.getSurface(self.mirror(spritedata[1])))
        self.images["left"].append(self.getSurface(self.mirror(spritedata[2])))

        self.images["up"] = []
        self.images["up"].append(self.getSurface(spritedata[0]))
        self.images["up"].append(self.getSurface(self.turnLeft(spritedata[1])))
        self.images["up"].append(self.getSurface(self.turnLeft(spritedata[2])))

        self.images["down"] = []
        self.images["down"].append(self.getSurface(spritedata[0]))
        self.images["down"].append(self.getSurface(self.turnRight(spritedata[1])))
        self.images["down"].append(self.getSurface(self.turnRight(spritedata[2])))

    def getImages(self):
        return self.images

    def getSurface(self, data):
        surface = pygame.Surface((16 * SCALEFACTOR, 16 * SCALEFACTOR))
        surface = surface.convert_alpha()
        surface.fill(COLORS["transparent"])
        pointrect = Rect((0, 0), (SCALEFACTOR, SCALEFACTOR))
        # They are sprites of 16x16 pixels:
        for y in range(16):
            b = format(data[y], '016b')
            for x in range(16):
                if b[x] == "1":
                    pointrect.topleft = (x * SCALEFACTOR, y * SCALEFACTOR)
                    pygame.draw.rect(surface, COLORS["packieyellow"], pointrect)
        return surface

    def getArraysOfSingleBinaryNumbers(self, a):
        b = []
        for i in a:
            n = format(i, '016b')
            c = []
            for u in n:
                c.append(u)
            b.append(c)
        return b

    def getArrayOfDigitalNumbers(self, a):
        b = []
        for i in a:
            b.append(int("".join(i), 2))
        return b

    def turnLeft(self, a):
        a = self.getArraysOfSingleBinaryNumbers(a)
        b = []
        for i in range(15, -1, -1):
            c = []
            for u in range(16):
                c.append(a[u][i])
            b.append(c)
        return self.getArrayOfDigitalNumbers(b)

    def turnRight(self, a):
        a = self.getArraysOfSingleBinaryNumbers(a)
        b = []
        for i in range(16):
            c = []
            for u  in range(15, -1, -1):
                c.append(a[u][i])
            b.append(c)
        return self.getArrayOfDigitalNumbers(b)

    def mirror(self, b):
        b = self.getArraysOfSingleBinaryNumbers(b)
        for i in b:
            i.reverse()
        return self.getArrayOfDigitalNumbers(b)


class Packie:

    def __init__(self):
        self.createImages()
        self.x       = 0
        self.y       = 0
        self.imagenr = 0
        self.framestate = 0
        self.framechange = 1
        self.direction = "right"

    def createImages(self):
        ic = ImageCreator()
        self.images = ic.getImages()
        self.rect   = self.images["right"][0].get_rect()

    def move(self, direction):
        self.direction = direction
        if self.direction == "left":
            self.x -= SCALEFACTOR
        if self.direction == "right":
            self.x += SCALEFACTOR
        if self.direction == "up":
            self.y -= SCALEFACTOR
        if self.direction == "down":
            self.y += SCALEFACTOR
        self.rect.topleft = (self.x, self.y)
        self.framestate += 1
        if self.framestate > 2:
            self.nextFrame()
            self.framestate = 0

    def nextFrame(self):
        self.imagenr += self.framechange
        if self.imagenr > 2:
            self.imagenr = 2
            self.framechange = -1
        if self.imagenr < 0:
            self.imagenr = 0
            self.framechange = 1

    def setPosition(self, x, y):
        self.x = x
        self.y = y
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.images[self.direction][self.imagenr], self.rect)


class Main:

    def __init__(self):

        os.environ['SDL_VIDEO_WINDOW_POS'] = "36, 16"
        self.screen = pygame.display.set_mode((1084, 480))
        pygame.display.set_caption('Packie')
        pygame.init()
        self.ih = InputHandler(True)
        self.initSprites()
        self.clock   = pygame.time.Clock()
        self.running = True

        while self.running:
            self.clock.tick(50)
            self.timer = pygame.time.get_ticks()

            self.screen.fill(COLORS["cxblue"])
            self.packie.draw(self.screen)
            if self.checkInput() == "quit":
                return
            pygame.display.flip()

    def initSprites(self):
        self.packie = Packie()
        self.packie.setPosition(500, 180)

    def checkInput(self):
        actions = self.ih.processEvents()
        for i in actions.keys():
            if i == "quit" and actions[i]:
                pygame.quit()
                return "quit"
            if i == "fire" and actions[i]:
                self.packie.fire()
                continue
            if actions[i]:
                self.packie.move(i)
                return
        return 0

if __name__ == '__main__':
    Main()
