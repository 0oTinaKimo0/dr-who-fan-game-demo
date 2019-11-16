
from .cursor import *
from ..utils.drawable import Drawable
from ..utils.vector2D import Vector2

import pygame
import os

class BaseMenu(Drawable):
   _MENU_FOLDER = os.path.join("resources", "menus")
   
   def __init__(self, position, fileName):
      super().__init__("", position)
      
      self._hPad = 4
      self._vPad = 4
      
      if not pygame.font.get_init():
         pygame.font.init()
         
      self._fontColor = pygame.Color("WHITE")
      self._fontSize = 8
      self._font = pygame.font.Font(os.path.join("resources", "fonts", "PressStart2P.ttf"), self._fontSize)
      
      self._loadOptionList(fileName)
      
   
   def _loadOptionList(self, fileName):
      textFile = open(os.path.join(BaseMenu._MENU_FOLDER, fileName))
      
      self._list = [[y for y in x.split(",")] for x in textFile.read().split("\n")]
      self._renderList()
      
      textFile.close()
      
   def _renderList(self):
      self._renderedList = [[self._font.render(x, False, self._fontColor) for x in y] for y in self._list]

      self._width = self._renderedList[0][0].get_width() + self._hPad
      self._height = self._renderedList[0][0].get_height() + self._vPad
      
   def reset(self):
      pass
      
   def draw(self, surface):
      for i in range(len(self._renderedList)):
         for j in range(len(self._renderedList[i])):
            surface.blit(self._renderedList[i][j], (self._position.x + self._width * j,
                                                    self._position.y + self._height * i))
      #pygame.draw.circle(surface, (0,0,0), list(self._position),  2)
            
   def handleEvent(self, event):
      
      if self._selectionHappened(event):
         row, col = self._getSelection(event)
         return self._list[row][col]
   
   
   def _selectionHappened(self, event):
      return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
   
   def _getSelection(self, event=None):
      selection = Drawable.adjustMenuMouse(Vector2(*event.pos))
      selection -= self._position
      selection.x //= self._width
      selection.y //= self._height
      return int(selection.y), int(selection.x)
      
   

class CursorMenu(BaseMenu):
   _MENU_FOLDER = os.path.join("resources", "menus")
   
   def __init__(self, position, fileName, cursorType=Cursor, cursorImageName="arrow.png"):
      
      self._cursorType = cursorType
      self._cursorImageName = cursorImageName
      
      super().__init__(position, fileName)
      
   
   def _renderList(self):
      super()._renderList()
      
      self._cursor = self._cursorType(self._cursorImageName,
                                      self._position,
                                      len(self._list), len(self._list[0]),
                                      self._width, self._height,
                                      self._hPad, self._vPad)
      
   def reset(self):
      self._cursor.reset()
      
      
   def draw(self, surface):
      super().draw(surface)
      
      self._cursor.draw(surface)
   
   def handleEvent(self, event):
      
      selectResult = super().handleEvent(event)
      if selectResult != None:
         return selectResult
   
      self._cursor.handleEvent(event)
   
   def _selectionHappened(self, event):
      return event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN
   
   def _getSelection(self, event=None):
      return self._cursor.currRow, self._cursor.currCol
         

class HoverCursorMenu(CursorMenu):
   def __init__(self, position, fileName, cursorImageName="hover.png"):
      super().__init__(position, fileName, HoverCursor, cursorImageName)
