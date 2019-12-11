
from ..utils.drawable import Drawable
from ..utils.vector2D import Vector2
from ..utils.soundManager import SoundManager
from ..utils.frameManager import FrameManager
import pygame

pygame.font.init() 
myfont = pygame.font.SysFont('Comic Sans MS', 40)
myfontSmall = pygame.font.SysFont('Comic Sans MS', 24)

# generates the game over screen
class Losing(Drawable):
   def __init__(self, screenSize):
      self._active = False
      super().__init__("blink.png", screenSize // 2, parallax=0)      
      self._position -= Vector2(*self.getSize()) // 2  
   
   def update(self, state, action):
      if state == "game over":
         self._active = True
      else:
         self._active = False        
   # returns the game state
   def handleEvent(self, event, joycon):
      if not joycon:
         if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            return "restart"
         elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "quit"
      if joycon:
         if event.type == pygame.JOYBUTTONDOWN and event.button == 8:
            return "restart"
         elif event.type == pygame.JOYBUTTONDOWN and event.button == 13:
            return "quit"
   # renders the text onto the screen depending on if a joycon is used         
   def draw(self, surface, joycon):
      if self._active:
         super().draw(surface)
         textLine1 = myfont.render('Game Over', False, (255,255,255))
         if joycon:
            textLine2 = myfontSmall.render('Press - to restart', False, (255,255,255))
         else:
            textLine2 = myfontSmall.render('Press R to restart', False, (255,255,255))
         for i in range(0,255):
            textLine1.set_alpha(i)
         surface.blit(textLine1,(250,200))
         surface.blit(textLine2,(250,250))
   
   
   def isActive(self):
      return self._active
# generates the winning screen
class Winning(Drawable):
   def __init__(self, screenSize):
      self._active = False
      super().__init__("Congratulations.png", screenSize // 2, parallax=0)
      self._secondImage = FrameManager.getInstance().getFrame("won.png", None)
      self._position -= Vector2(*self.getSize()) // 2
      self._timer = 6

   def update(self, state, action):
      if state == "you won":
         self._active = True
      else:
         self._active = False
   # returns the game state      
   def handleEvent(self, event, joycon):
      if not joycon:
         if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            return "restart"
         elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "quit"
      if joycon:
         if event.type == pygame.JOYBUTTONDOWN and event.button == 8:
            return "restart"
         elif event.type == pygame.JOYBUTTONDOWN and event.button == 13:
            return "quit"   
   # draws a sequence of images of texts using a timer
   def draw(self, surface, ticks):
      if self._active:
         self._timer -= ticks
         super().draw(surface)
         if self._timer <= 3:
            surface.blit(self._secondImage, (int(self._position[0] * self._parallax),
                           int(self._position[1] * self._parallax)))
         if self._timer <= 1:
            textLine1 = myfontSmall.render('Thanks for playing', False, (0,0,0))
            surface.blit(textLine1,(250,400))
         if self._timer <= 0:
            textLine2 = myfontSmall.render("Don't Blink by Tina Jin", False, (0,0,0))
            surface.blit(textLine2,(240,430))                        
   
   def isActive(self):
      return self._active
   
# generates the title screen
class Title(Drawable):
   def __init__(self, screenSize):
      self._active = True
      super().__init__("titlescreen.png", screenSize // 2, parallax=0)      
      self._position -= Vector2(*self.getSize()) // 2
      self._joycon = True

   # depends whether a joycon is used based on user input
   def handleEvent(self, event):
      if event.type == pygame.MOUSEBUTTONUP:
         pos = pygame.mouse.get_pos()
         if 188<pos[0]<220 and 468<pos[1]<538:
            self._joycon = True
         if 438<pos[0]<518 and 478<pos[1]<531:
            self._joycon = False
         if 0<pos[0]<50 and 650<pos[1]<700:
            SoundManager.getInstance().stopMusic()
      if self._joycon:
         if pygame.joystick.get_count() == 0:
            self._joycon = False
         else:
            joystickL = pygame.joystick.Joystick(0)
            if not joystickL.get_init():
               joystickL.init()
            if event.type == pygame.JOYBUTTONDOWN:
               self._active = False
      else:
         if event.type == pygame.KEYDOWN:
            self._active = False         
      return self._joycon
   
   
   def draw(self, surface):
      if self._active:
         super().draw(surface)   
   
   def isActive(self):
      return self._active
   
      
