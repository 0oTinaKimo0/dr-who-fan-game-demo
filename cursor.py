
import pygame
from ..utils.drawable import Drawable
from ..utils.vector2D import Vector2

class Cursor(Drawable):
   
   def __init__(self, imageName, initialOffset, numRows, numCols, width, height, hPad=1, vPad=1):
      super().__init__(imageName, initialOffset)
      
      self._numRows = numRows
      self._numCols = numCols
      self._width = width
      self._height = height
      
      self.currRow = 0
      self.currCol = 0
      
      self._initialOffset = Vector2(*initialOffset)
      self._setPosition(hPad, vPad)
      
   def _setPosition(self, hPad, vPad):
      self._position.x -= self.getSize()[0] + hPad
      self._initialOffset.x -= self.getSize()[0] + hPad
   
   def reset(self):
      self.currCol = 0
      self.currRow = 0
      self._position.x = self._initialOffset.x
      self._position.y = self._initialOffset.y
      
   
   def moveDown(self):
      self.currRow += 1
      self.currRow %= self._numRows
      
   def moveUp(self):
      self.currRow -= 1
      self.currRow %= self._numRows
      
   def moveLeft(self):
      self.currCol -= 1
      self.currCol %= self._numCols
      
   def moveRight(self):
      self.currCol += 1
      self.currCol %= self._numCols
      
      
   
   def handleEvent(self, event):
      
      if event.type  == pygame.KEYDOWN:
         if event.key == pygame.K_UP:
            self.moveUp()
         elif event.key == pygame.K_DOWN:
            self.moveDown()
         elif event.key == pygame.K_LEFT:
            self.moveLeft()
         elif event.key == pygame.K_RIGHT:
            self.moveRight()
      
      self._position.x = self._initialOffset.x + self.currCol * self._width
      self._position.y = self._initialOffset.y + self.currRow * self._height
   

class HoverCursor(Cursor):
   
   def _setPosition(self, hPad, vPad):

      self._position.x -= hPad // 2
      self._initialOffset.x -= hPad // 2
      
      self._position.y -= vPad // 2
      self._initialOffset.y -= vPad // 2
   
      