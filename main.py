
import pygame
import os
from modules.utils.vector2D import Vector2
from modules.UI.pauser import Pauser
from modules.UI.blinker import Blinker
from modules.player import Player
from modules.utils.drawable import Drawable
from modules.angel import *



SCREEN_SIZE = Vector2(700,700)
WORLD_SIZE = Vector2(2000, 2000)

def main():
   
   # initialize the pygame module
   pygame.init()
   # load and set the logo
   
   pygame.display.set_caption("Don't Blink")
   
   screen = pygame.display.set_mode(list(SCREEN_SIZE))
   
   # Make a game clock for nice, smooth animations
   gameClock = pygame.time.Clock()

   if Player.JOYCON_ON:
      joystickL = pygame.joystick.Joystick(0)
      #joystickR = pygame.joystick.Joystick(1)
      if not joystickL.get_init():
         joystickL.init()
      #if not joystickLR.get_init():
         #joystickR.init()
      
   background = Drawable("background.png", (0,0), None, 1)
   
   pauser = Pauser(SCREEN_SIZE)

   blinker = Blinker(SCREEN_SIZE)
   
   player = Player(Vector2(400,400))

   angels = AllAngels(3)

   # define a variable to control the main loop
   RUNNING = True
   
   # main loop
   while RUNNING:
      
      # Let our game clock tick at 60 fps, ALWAYS
      gameClock.tick(60)
            
      # Get some time in seconds
      ticks = min(0.5, gameClock.get_time() / 1000)
      
      # Draw everything
      screen.fill((30,30,30))
      
      
      background.draw(screen)
      player.draw(screen)
      angels.draw(screen)
      blinker.draw(screen, SCREEN_SIZE)
      pauser.draw(screen)
      #background.darken(0)
   
      
      # Flip the display to the monitor
      pygame.display.flip()
      
      # event handling, gets all event from the eventqueue
      for event in pygame.event.get():
         # only do something if the event is of type QUIT or ESCAPE is pressed
         if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            # change the value to False, to exit the main loop
            RUNNING = False
         else:
            pauser.handleEvent(event)
            if not pauser.isActive():
               blinker.handleEvent(event)
               
                     
      # let others update based on the amount of time elapsed      
      if not pauser.isActive():
         blinker.update(ticks)
         player.handleEvent(event)
         player.rotate()
         player.update(ticks, WORLD_SIZE)
         angels.update(WORLD_SIZE, ticks, player, blinker)
         Drawable.updateWindowOffset(player, SCREEN_SIZE, WORLD_SIZE)
         
      
   pygame.quit()   
      
      
      
if __name__ == "__main__":
   main()
