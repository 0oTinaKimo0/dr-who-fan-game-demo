
import pygame

from ..utils.drawable import Drawable

class PageSequence(Drawable):
   def __init__(self):
      self._pages = []
      self._currPage = 0
      self._nextPageAction = pygame.K_SPACE
      
   
   def handleEvent(self, event):
      if event.type == pygame.KEYDOWN and event.key == self._nextPageAction:
         self._currPage += 1
         
         
   
   def addPage(self, imageName):
      self._pages.append(Drawable(imageName, (0,0), parallax = 0))
   
   
   def draw(self, surface):
      if self._currPage < len(self._pages):
         self._pages[self._currPage].draw(surface)
      
      
   def isDone(self):
      return self._currPage >= len(self._pages)
   
   def reset(self):
      self._currPage = 0
   
   