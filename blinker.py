from ..utils.drawable import Drawable
from ..utils.vector2D import Vector2
import pygame

class Blinker(Drawable):
   TIME_INTERVAL = 1
   TIME_COUNTDOWN = 5
   def __init__(self, screenSize):
      self._active = False
      # 800*800 black image
      super().__init__("blinkactual.png", screenSize // 2, parallax=0)
      self._position -= Vector2(*self.getSize()) // 2
      self._blinkInterval = self.TIME_INTERVAL      
      self._blinkCountdown = self.TIME_COUNTDOWN

   def handleEvent(self, event):
      if event.type == pygame.JOYBUTTONDOWN and event.button == 14:         
            self._active = True
            self._blinkInterval = self.TIME_INTERVAL
            self._blinkCountdown = self.TIME_COUNTDOWN
            
   def update(self, ticks):
      self._blinkInterval -= ticks
      self._blinkCountdown -= ticks
      if self._blinkInterval <= 0:
         self._active = False
      if self._blinkCountdown <= 0:
         self._active = True
         self._blinkInterval = self.TIME_INTERVAL
         self._blinkCountdown = self.TIME_COUNTDOWN
   
   def draw(self, surface, screenSize):
      pygame.draw.rect(surface, (0,0,204,0.8), (screenSize.x-200*(self._blinkCountdown/self.TIME_COUNTDOWN), 0, 200*(self._blinkCountdown/self.TIME_COUNTDOWN), 10))
      if self._active:
         super().draw(surface)
   
   
   def isActive(self):
      return self._active
   
      
