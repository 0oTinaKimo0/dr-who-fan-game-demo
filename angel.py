import pygame
from .utils.vector2D import Vector2
import random
import math
from .utils.drawable import Drawable
from .utils.frameManager import FrameManager
from .utils.FSM import FSM

class AllAngels:
   def __init__(self, numAngels):
      self._list = []
      self._num = numAngels
      self._timer = 60
         
   def draw(self, surface):
      for a in self._list:
         a.draw(surface)
         
         
   def update(self, worldInfo, state, ticks, hero, tardis, blink):
      # ref: https://stackoverflow.com/questions/45415347/generate-random-integer-between-two-ranges
      rangex = list(range(0,hero._safeZone.left-64)) + list(range(hero._safeZone.right,worldInfo[0]-64))
      rangey = list(range(0,hero._safeZone.top-64)) + list(range(hero._safeZone.bottom,worldInfo[1]-64))
      self.updateNum(ticks, tardis)
      while self._num > 0:
         self._list.append(Angel(ticks, (random.choice(rangex),random.choice(rangey))))
         self._num -= 1
      for a in self._list:
         a.update(Vector2(worldInfo.x,worldInfo.y), ticks, hero, tardis, blink)
         # updates the direction the angel teleports
         distanceVector = Vector2(a._image.get_width()//2 + a.getPosition().x, a._image.get_height()//2 + a.getPosition().y).__sub__(hero.getPosition())
         angle = int((180 / math.pi) * -math.atan2(distanceVector.y, distanceVector.x)-90)
         # if an angel collides with the player, the game ends
         if hero.getCollideBox().colliderect(a.getCollideBox()):
            a.freeze()
            state = "game over"
         # if an angel collides with the player's sight, freeze it
         elif (hero.getAngle()<=angle+30) and (hero.getAngle()>=angle-30) and distanceVector.magnitude() <=300 and not blink.isActive():              
            a.freeze()
         elif a.isSeen():
            a.resume()
      
   # if the angels are colliding, spawning one of them randomly
   # ref: https://stackoverflow.com/questions/24027990/how-to-exclude-an-object-from-a-list-in-python-while-looping
         for b in (obj for obj in self._list if obj != a):
            if a.getCollideBox().colliderect(b.getCollideBox()):
               randPos = Vector2(random.choice(rangex),random.choice(rangey))
               while tardis.getPosition().__sub__(randPos).magnitude() < 500:
                  randPos = Vector2(random.choice(rangex),random.choice(rangey))
               a.setPosition(randPos)

      return state
   # adds one angel per minute
   def updateNum(self, ticks, tardis):
      self._timer -= ticks
      if self._timer <= 0:
         self._num += 1
         self._timer = 60
      
         

   
class Angel(Drawable):
   # initializes a stationary angel object
   def __init__(self, ticks, position):     
      super().__init__("angeldetail.png", position)
      self._imageSeen = FrameManager.getInstance().getFrame("angelseen.png", None)
      self._image.set_alpha(120)
      self._teleUnit = Vector2(0,0)
      self._seen = False
      self._FSM = FSM()
      self._timer = 1

   # draws different images of the angel depending on if it is seen or not
   def draw(self, surface):
      if not self._seen:
         surface.blit(self._image, (int(self._position[0] - Drawable.WINDOW_OFFSET[0] * self._parallax),
                                       int(self._position[1] - Drawable.WINDOW_OFFSET[1] * self._parallax)))
      else:
         surface.blit(self._imageSeen, (int(self._position[0] - Drawable.WINDOW_OFFSET[0] * self._parallax),
                                    int(self._position[1] - Drawable.WINDOW_OFFSET[1] * self._parallax)))
      
   # updates the angel's position and checks if it has left the world bounds
   def update(self, worldInfo, ticks, hero, tardis, blink):
      
      # determines the state of the angel
      self._FSM.manageState(self._seen, tardis._appear)
      newPosition = self._position
      self.move(newPosition, ticks, hero, tardis, blink)

      # if the angel is exiting from left or right, clip it back on screen
      if newPosition.x < 0:
         newPosition.x = 0
         
      elif newPosition.x + self.getSize()[0] > worldInfo.x:
         newPosition.x = worldInfo.x - self.getSize()[0]
         
      # if the angel is exiting from top or bottom, clip it back on screen
      elif newPosition.y < 0:
         newPosition.y = 0

      elif newPosition.y + self.getSize()[1] > worldInfo.y:
         newPosition.y = worldInfo.y - self.getSize()[1]
         
      # updates the angel's position to be the new position
      self._position = newPosition

   # uses a timer to simulate the teleporting angels   
   def move(self, myPosition, ticks, hero, tardis, blink):
         self._timer -= ticks
         if self._FSM == "moving":
            distanceVector = hero.getPosition().__sub__(myPosition)
            self._teleUnit = Vector2(distanceVector.normalize().x, distanceVector.normalize().y)
         elif self._FSM == "chasing":
            distanceVector = tardis.getPosition().__sub__(myPosition)
            self._teleUnit = Vector2(distanceVector.normalize().x, distanceVector.normalize().y)
         else:
            return myPosition
         if self._timer <= 0:
            if not blink.isActive():
               myPosition[0] += self._teleUnit[0] * random.randint(60,80)
               myPosition[1] += self._teleUnit[1] * random.randint(60,80)
            else:
               myPosition[0] += self._teleUnit[0] * random.randint(100,120)
               myPosition[1] += self._teleUnit[1] * random.randint(100,120)
            self._timer = 1
         return myPosition
      
         

   def freeze(self):
      self._seen = True

   def resume(self):
      self._seen = False

   # determines if the angel is seen or not
   def isSeen(self):
      return self._seen
      
         

