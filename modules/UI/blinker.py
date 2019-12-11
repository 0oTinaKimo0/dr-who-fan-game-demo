from ..utils.drawable import Drawable
from ..utils.vector2D import Vector2
import pygame

class Blinker(Drawable):
   TIME_INTERVAL = 1
   TIME_COUNTDOWN = 10
   def __init__(self, screenSize):
      self._active = False
      # loads a fullscreen black image
      super().__init__("blinkactual.png", screenSize // 2, parallax=0)
      self._position -= Vector2(*self.getSize()) // 2
      # uses two timers to track interval and duration of the blink
      self._blinkInterval = self.TIME_INTERVAL      
      self._blinkCountdown = self.TIME_COUNTDOWN
      
   # adds a manual blink feature, resets the timers
   def handleEvent(self, event, joycon):
      if joycon:
         if event.type == pygame.JOYBUTTONDOWN and event.button == 14:         
               self._active = True
               self._blinkInterval = self.TIME_INTERVAL
               self._blinkCountdown = self.TIME_COUNTDOWN
      if not joycon:
         if event.type == pygame.KEYDOWN and event.key == pygame.K_b:         
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
      # draws a "force blink" bar at the upper right corner
      pygame.draw.rect(surface, (0,0,204,0.8), (screenSize.x-200*(self._blinkCountdown/self.TIME_COUNTDOWN), 0, 200*(self._blinkCountdown/self.TIME_COUNTDOWN), 10))
      if self._active:
         super().draw(surface)
   
   def isActive(self):
      return self._active
   
      

