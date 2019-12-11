from .utils.drawable import Drawable
from .utils.animated import Animated
from .utils.vector2D import Vector2
from .utils.frameManager import FrameManager
import pygame
import math

VELOCITY = 160
class Player(Animated):
   def __init__(self, position, joycon):
      super().__init__("doctor.png", position)
      self._velocity = Vector2(0,0)
      self._direction = Vector2(0,0)
      self._center = Vector2(0,0)
      # defines the player's collidebox to be smaller than the actual image
      self._collideBox = pygame.Rect((0,0),(10,10))
      # lets angels and TARDIS spawn far away enough from the player
      self._safeZone = pygame.Rect((0,0),(200,200))
      self._tardisSpawn = pygame.Rect((0,0),(800,800))
      self._movement = { "up" : False,
                         "left" : False,
                         "down" : False,
                         "right" : False,
                         pygame.K_w: False,
                         pygame.K_a: False,
                         pygame.K_s: False,
                         pygame.K_d: False
                        }
         
   # handles movement depending on if the joycon is activated or not
   def handleEvent(self, event, joycon):         
      if joycon:
         if event.type == pygame.JOYHATMOTION:
            if event.hat == 0:
               if event.value[0] == 1:
                  self._movement["down"] = True                              
               elif event.value[0] == -1:
                  self._movement["up"] = True
               else:
                  self._movement["up"] = False
                  self._movement["down"] = False
               if event.value[1] == 1:
                  self._movement["right"] = True
               elif event.value[1] == -1:
                  self._movement["left"] = True
               else:
                  self._movement["right"] = False
                  self._movement["left"] = False

      else:
         if event.type in [pygame.KEYDOWN, pygame.KEYUP]:
            if event.key in self._movement.keys():
               self._movement[event.key] = (event.type == pygame.KEYDOWN)
                             
   # gets and sets the angle the player is looking at
   def getAngle(self):
      mouse_x, mouse_y = Drawable.adjustMousePos(pygame.mouse.get_pos())
      rel_x, rel_y = mouse_x - self._center[0], mouse_y - self._center[1]
      angle = int((180 / math.pi) * -math.atan2(rel_y, rel_x) - 90)
      return angle
   
   def setAngle(self):
      angle = self.getAngle()
      self._direction = Vector2(math.cos(angle), math.sin(angle))
      self._direction.scale(100)

   # ref: https://gamedev.stackexchange.com/questions/132163/how-can-i-make-the-player-look-to-the-mouse-direction-pygame-2d
   # rotates the player's image about its center
   def rotate(self):
      angle = self.getAngle()
      self._image = pygame.transform.rotate(self._original_image, angle)
      self._rect = self._image.get_rect(center=(self.getPosition().x, self.getPosition().y))
      
   def update(self, ticks, worldInfo, joycon):
      angle = self.getAngle()
      self.setAngle()

      if not joycon:
         if self._movement[pygame.K_w]:
            self._velocity[1] = -VELOCITY
         elif self._movement[pygame.K_s]:
            self._velocity[1] = VELOCITY
         else:
            self._velocity[1] = 0
         if self._movement[pygame.K_a]:
            self._velocity[0] = -VELOCITY
         elif self._movement[pygame.K_d]:
            self._velocity[0] = VELOCITY
         else:
            self._velocity[0] = 0
         
      if joycon:
         if self._movement["up"]:
            self._velocity[1] = -VELOCITY
         elif self._movement["down"]:
            self._velocity[1] = VELOCITY
         else:
            self._velocity.y = 0
         if self._movement["left"]:
            self._velocity[0] = -VELOCITY
         elif self._movement["right"]:
            self._velocity[0] = VELOCITY      
         else:
            self._velocity.x = 0
            
              
      distanceVector = self._velocity * ticks
      newPosition = self.getPosition() + distanceVector
      
      for dim in range(len(self.getSize())):
         if newPosition[dim] + self.getSize()[dim] > worldInfo[dim] or  newPosition[dim] < 0:
            self._velocity[dim] = -self._velocity[dim]
            
            distanceVector = self._velocity * ticks
            newPosition = self.getPosition() + distanceVector         
      
      self.setPosition(newPosition)
      self._center = Vector2(self._original_image.get_rect().centerx + self.getPosition().x, self._original_image.get_rect().centery + self.getPosition().y)
      self._collideBox.center = (self._center.x, self._center.y)
      self._safeZone.center = (self._center.x, self._center.y)
      self._tardisSpawn.center = (self._center.x, self._center.y)


   def isBlinking(self):
      return self._blink
      

   
      
