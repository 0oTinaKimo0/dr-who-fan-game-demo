import pygame
from pygame import image
from .frameManager import FrameManager
from .vector2D import Vector2
import os

class Drawable(object):
   
   WINDOW_OFFSET = Vector2(0,0)
   
   
   @classmethod
   def updateWindowOffset(cls, followObject, screenSize, worldSize):
      position = followObject.getPosition()
      size = followObject.getSize()
      Drawable.WINDOW_OFFSET = [min(max(0, position[x] - screenSize[x] // 2 + size[x] // 2), worldSize[x] - screenSize[x]) for x in range(2)]
      
   @classmethod
   def adjustMousePos(cls, mousePos):
      newMousePos = list(mousePos)
      newMousePos[0] += Drawable.WINDOW_OFFSET[0]
      newMousePos[1] += Drawable.WINDOW_OFFSET[1]
      return newMousePos
   
   def adjustMenuMouse(cls, mousePos):
      ret = Vector2(*mousePos)
      
      return ret
   
      
   def __init__(self, imageName, position, offset=None, parallax=1):
      self._imageName = imageName
      if self._imageName != "":
         self._image = FrameManager.getInstance().getFrame(imageName, offset)
      else:
         self._image = pygame.Surface(200,200)
      self._worldBound = True
      self._original_image = self._image
      self._position = Vector2(*position)
      self._parallax = parallax
      
   def getPosition(self):
      return self._position

   def setPosition(self, newPosition):
      self._position = newPosition
      
   def getSize(self):
      return self._image.get_size()

   def getCollideBox(self):
      newRect =  self._position + self._image.get_rect()
      return newRect
      
   
   def draw(self, surface):
      if self._worldBound:
         surface.blit(self._image, (int(self._position[0] - Drawable.WINDOW_OFFSET[0] * self._parallax),
                                    int(self._position[1] - Drawable.WINDOW_OFFSET[1] * self._parallax)))
      else:
         surface.blit(self._image, self._position)
 
   def darken(self, percent):
      dark = pygame.Surface(self.getSize())
      dark.fill((0, 0, 0, percent*255))
      self._image.blit(dark, (0, 0))
