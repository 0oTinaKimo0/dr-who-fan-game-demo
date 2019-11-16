
from ..utils.drawable import Drawable
from ..utils.vector2D import Vector2
from modules.player import Player
import pygame

class Pauser(Drawable):
   def __init__(self, screenSize):
      self._active = False
      super().__init__("paused.png", screenSize // 2, parallax=0)
      
      self._position -= Vector2(*self.getSize()) // 2
      
   
   def handleEvent(self, event):
      if not Player.JOYCON_ON:
         if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            self._active = not self._active
      if Player.JOYCON_ON:
         if event.type == pygame.JOYBUTTONDOWN and event.button == 15:
            self._active = not self._active
   
   
   def draw(self, surface):
      if self._active:
         super().draw(surface)
   
   
   def isActive(self):
      return self._active
   
      
