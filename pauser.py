
from ..utils.drawable import Drawable
from ..utils.vector2D import Vector2
from modules.player import Player
from ..utils.soundManager import *
import pygame

class Pauser(Drawable):
   def __init__(self, screenSize):
      self._active = False
      super().__init__("paused.png", screenSize // 2, parallax=0)
      # centers the image
      self._position -= Vector2(*self.getSize()) // 2   

   # toggles if the pauser is active and toggles the music
   def handleEvent(self, event, joycon):
      if not joycon:
         if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            self._active = not self._active
            if self._active:
               SoundManager.getInstance().pauseAll()
            else:
               SoundManager.getInstance().unpauseAll()
      if joycon:
         if event.type == pygame.JOYBUTTONDOWN and event.button == 15:
            self._active = not self._active
            if self._active:
               SoundManager.getInstance().pauseAll()
            else:
               SoundManager.getInstance().unpauseAll()

   
   
   def draw(self, surface):
      if self._active:
         super().draw(surface)
   
   
   def isActive(self):
      return self._active
   
      
