#!/usr/bin/python3
# coding: utf-8

import pygame
from pygame.locals import *
import os

"""
    Packie 1.1 - Pygame-emulation of a CX16 BASIC sprite example.

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

spritedata = (("0000001111000000",
               "0000111111110000",
               "0011111111111100",
               "0011111111111100",
               "1111111111111111",
               "1111111111111111",
               "1111111111111111",
               "1111111111111111",
               "1111111111111111",
               "1111111111111111",
               "1111111111111111",
               "1111111111111111",
               "0011111111111100",
               "0011111111111100",
               "0000111111110000",
               "0000001111000000"),

              ("0000001111000000",
               "0000001111000000",
               "0000111111110000",
               "0011111111111100",
               "0011111111111100",
               "1111111111111111",
               "1111111111110000",
               "1111111111000000",
               "1111111100000000",
               "1111111100000000",
               "1111111111000000",
               "1111111111110000",
               "1111111111111111",
               "0011111111111100",
               "0000111111110000",
               "0000001111000000"),
 
              ("0000001111000000",
               "0000111111110000",
               "0011111111111100",
               "0011111111110000",
               "1111111111110000",
               "1111111111000000",
               "1111111111000000",
               "1111111100000000",
               "1111111100000000",
               "1111111111000000",
               "1111111111000000",
               "1111111111110000",
               "0011111111110000",
               "0011111111111100",
               "0000111111110000",
               "0000001111000000"))

COLORS = {"cxblue"       : (0, 0, 170),
          "cxwhite"      : (255, 255, 255),
          "packieyellow" : (238, 238, 119),
          "transparent"  : (0, 0, 0, 0) }


class InputHandler:

    def __init__(self, hasjoystick):
        self.hasjoystick = hasjoystick
        self.joystick = {}
        if self.hasjoystick:
            self.initJoystick()
        self.initKeys()

    def initJoystick(self):
        self.js = pygame.joystick.Joystick(0)
        self.js.init()
        for i in ("left", "right", "up", "down", "firing"):
            self.joystick[i] = False

    def initKeys(self):
        self.keys_ = {}
        for i in (pygame.K_LEFT, pygame.K_RIGHT,
                  pygame.K_UP, pygame.K_DOWN, pygame.K_LCTRL,
                  pygame.K_q, pygame.K_ESCAPE):
            self.keys_[i] = False

    def processEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                for i in self.keys_:
                    if event.key == i:
                        self.keys_[i] = True
            if event.type == pygame.KEYUP:
                for i in self.keys_:
                    if event.key == i:
                        self.keys_[i] = False
            if self.hasjoystick:
                if event.type == pygame.JOYBUTTONDOWN:
                    self.joystick["firing"] = True
                if event.type == pygame.JOYBUTTONUP:
                    self.joystick["firing"] = False
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
        actions = []
        if self.keys_[pygame.K_LEFT] or self.hasjoystick and self.joystick["left"]:
            actions.append("left")
        if self.keys_[pygame.K_RIGHT] or self.hasjoystick and self.joystick["right"]:
            actions.append("right")
        if self.keys_[pygame.K_UP] or self.hasjoystick and self.joystick["up"]:
            actions.append("up")
        if self.keys_[pygame.K_DOWN] or self.hasjoystick and self.joystick["down"]:
            actions.append("down")
        if self.keys_[pygame.K_LCTRL] or self.hasjoystick and self.joystick["firing"]:
            actions.append("firing")
        if self.keys_[pygame.K_q] or self.keys_[pygame.K_ESCAPE]:
            actions.append("quit")
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
            for x in range(16):
                if data[y][x] == "1":
                    pointrect.topleft = (x * SCALEFACTOR, y * SCALEFACTOR)
                    pygame.draw.rect(surface, COLORS["packieyellow"], pointrect)
        return surface

    def getArray(self, a):
        b = []
        for i in a:
            c = []
            for u in i:
                c.append(u)
            b.append(c)
        return b

    def getStringArray(self, a):
        b = []
        for i in a:
            b.append("".join(i))
        return b

    def turnLeft(self, a):
        a = self.getArray(a)
        b = []
        for i in range(15, -1, -1):
            c = []
            for u in range(16):
                c.append(a[u][i])
            b.append(c)
        return self.getStringArray(b)

    def turnRight(self, a):
        a = self.getArray(a)
        b = []
        for i in range(16):
            c = []
            for u  in range(15, -1, -1):
                c.append(a[u][i])
            b.append(c)
        return self.getStringArray(b)

    def mirror(self, b):
        b = self.getArray(b)
        for i in b:
            i.reverse()
        return self.getStringArray(b)


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

    def moveLeft(self):
        self.direction = "left"
        self.x -= SCALEFACTOR
        self.rect.topleft = (self.x, self.y)
        self.framestate += 1
        if self.framestate > 2:
            self.nextFrame()
            self.framestate = 0

    def moveRight(self):
        self.direction = "right"
        self.x += SCALEFACTOR
        self.rect.topleft = (self.x, self.y)
        self.framestate += 1
        if self.framestate > 2:
            self.nextFrame()
            self.framestate = 0

    def moveUp(self):
        self.direction = "up"
        self.y -= SCALEFACTOR
        self.rect.topleft = (self.x, self.y)
        self.framestate += 1
        if self.framestate > 2:
            self.nextFrame()
            self.framestate = 0

    def moveDown(self):
        self.direction = "down"
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
        if "left" in actions:
            self.packie.moveLeft()
            return
        if "right" in actions:
            self.packie.moveRight()
            return
        if "up" in actions:
            self.packie.moveUp()
            return
        if "down" in actions:
            self.packie.moveDown()
            return
        if "quit" in actions:
            pygame.quit()
            return "quit"
        return 0

if __name__ == '__main__':
    Main()
