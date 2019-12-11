import pygame
import sys
import os
from modules.utils.vector2D import Vector2
from modules.UI.pauser import Pauser
from modules.UI.blinker import Blinker
from modules.player import Player
from modules.utils.drawable import Drawable
from modules.angel import *
from modules.tardis import Tardis
from modules.utils.soundManager import SoundManager
from modules.UI.screens import *

# initializes the pygame module
pygame.init()
# defines the screen and world dimensions
SCREEN_SIZE = Vector2(700,700)
WORLD_SIZE = Vector2(2000, 2000)
# defines a variable to control the game loop
RUNNING = True
JOYCON_ON = True
# initializes the game state
game_state = "OK"
# plays the monologue once at the start
SoundManager.getInstance().playSound("monologue.wav")


def main():
   if not pygame.get_init():
      pygame.init()

   if not RUNNING:
      pygame.quit()
      
   global game_state
   
   screen = pygame.display.set_mode(list(SCREEN_SIZE))
   
   # loads and sets the logo
   icon = pygame.image.load(os.path.join("resources", "images", "icon.png"))
   pygame.display.set_icon(icon)
   pygame.display.set_caption("Don't Blink")
   # starts the game loop
   game_loop(screen)

   
   
def game_loop(screen):
   if not pygame.get_init():
      pygame.init()
   global game_state
   global RUNNING
   global JOYCON_ON
   
   # initializes all the UI elements
   title_screen = Title(SCREEN_SIZE)
   
   background = Drawable("background.png", (0,0), None, 1)
   
   pauser = Pauser(SCREEN_SIZE)

   game_over = Losing(SCREEN_SIZE)

   you_won = Winning(SCREEN_SIZE)

   blinker = Blinker(SCREEN_SIZE)
   

   # makes a game clock for all the updates
   gameClock = pygame.time.Clock()

   # initializes all objects in game
   player = Player(Vector2(400,400), JOYCON_ON)

   tardis = Tardis(Vector2(500, 500))

   angels = AllAngels(3)

   # plays background music
   SoundManager.getInstance().playMusic("bgm.ogg",loop=-1)

   losing_screen_action = ""
   winning_screen_action = ""
   


   
   # main loop
   while RUNNING:
      # makes the game clock tick at 60 fps
      gameClock.tick(60)
      # gets ticks in seconds      
      ticks = min(0.5, gameClock.get_time() / 1000)

      # draws title screen first
      if title_screen.isActive():
         title_screen.draw(screen)
      
      else:        
         # draws everything else
         screen.fill((30,30,30))      
         background.draw(screen)
         player.draw(screen)
         angels.draw(screen)
         tardis.draw(screen)
         blinker.draw(screen, SCREEN_SIZE)
         pauser.draw(screen)
         game_over.draw(screen, JOYCON_ON)
         you_won.draw(screen, ticks)
   
      
      # flips the display to the monitor
      pygame.display.flip()

      # event handling, gets all event from the eventqueue
      for event in pygame.event.get():
         # quits game loop if the event is of type QUIT
         if event.type == pygame.QUIT:
            RUNNING = False
            break
         else:
            # determines the choice of control schemes based on user input
            if title_screen.isActive():
               JOYCON_ON = title_screen.handleEvent(event)
            losing_screen_action = game_over.handleEvent(event, JOYCON_ON)
            winning_screen_action = you_won.handleEvent(event, JOYCON_ON)
            # if the player wants to quit at either screen, quits the game loop
            if losing_screen_action == "quit" or winning_screen_action == "quit":
               game_state = "quit"
               RUNNING = False
               break
            # if the player wants to restart at either screen, restarts at title screen
            elif losing_screen_action == "restart" or winning_screen_action == "restart":
               game_state = "restart"
               main()
            pauser.handleEvent(event, JOYCON_ON)
            # if not paused, let others handle event
            if not pauser.isActive():
               player.handleEvent(event, JOYCON_ON)
               blinker.handleEvent(event, JOYCON_ON)
               
      game_over.update(game_state, losing_screen_action)
      you_won.update(game_state, winning_screen_action)
      
                     
      # lets others update if none of the screens is active     
      if not title_screen.isActive() and not you_won.isActive() and not game_over.isActive() and not pauser.isActive():
         blinker.update(ticks)
         player.rotate()
         player.update(ticks, WORLD_SIZE, JOYCON_ON)
         game_state = angels.update(WORLD_SIZE, game_state, ticks, player, tardis, blinker)
         game_state = tardis.update(ticks, game_state, angels, player, screen, WORLD_SIZE)
         Drawable.updateWindowOffset(player, SCREEN_SIZE, WORLD_SIZE)

   #if the game is not running
   pygame.quit()
   sys.exit(0)
      
      
      
if __name__ == "__main__":
   main()
