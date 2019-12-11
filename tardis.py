import pygame
from .utils.vector2D import Vector2
import random
from .utils.drawable import Drawable
from .utils.frameManager import FrameManager
from .utils.soundManager import SoundManager

class Tardis(Drawable):
    TIME_REAPPEAR = 30
    TIME_STAY = 10
    
    def __init__(self, position):
        super().__init__("tardis.png", position)
        self._appear = False
        # two timers for reappearance and duration of stay
        self._timerReappear = self.TIME_REAPPEAR
        self._timerStay = self.TIME_STAY
        self._landingChannel = None       
    
    # if the TARDIS should appear, draw it on the screen
    def draw(self, surface):
        if self._appear:
            surface.blit(self._image, (int(self._position[0] - Drawable.WINDOW_OFFSET[0] * self._parallax),
                                    int(self._position[1] - Drawable.WINDOW_OFFSET[1] * self._parallax)))

    # updates the TARDIS and returns game state
    def update(self, ticks, state, angels, hero, surface, worldInfo):
        self._timerReappear -= ticks
        self._timerStay -= ticks
        # chooses a random spawn position that's far away enough from the player
        rangex = list(range(0,hero._tardisSpawn.left-64)) + list(range(hero._tardisSpawn.right,worldInfo[0]-64))
        rangey = list(range(0,hero._tardisSpawn.top-64)) + list(range(hero._tardisSpawn.bottom,worldInfo[1]-64))
        randPos = Vector2(random.choice(rangex),random.choice(rangey))
        # when the "stay" timer countdown is over, hides the TARDIS
        if self._timerStay <= 0:
            self._appear = False
        # 5 seconds before TARDIS spawn, play positional sound of it landing to warn the player
        if self._timerReappear <= 5:
            self._landingChannel = SoundManager.getInstance().playSound("landing.wav")
            if not self._landingChannel == None:
                SoundManager.getInstance().updateVolumePositional(self._landingChannel, hero.getPosition(), randPos, distance=300, minVolume=0.2)
        # when the "reappear" timer countdown is over, spawns the TARDIS and resets both timers
        if self._timerReappear <= 0:
            self._appear = True       
            self.setPosition(randPos)
            self._timerReappear = self.TIME_REAPPEAR
            self._timerStay = self.TIME_STAY
        # if player collides with the TARDIS, shows the "you won" screen and plays a sonic screwdriver sound
        if hero.getCollideBox().colliderect(self.getCollideBox().inflate(-40,-40)) and self._appear:
            wonChannel = SoundManager.getInstance().playSound("sonic.wav")
            state = "you won"
        # if any angel collides with the TARDIS, shows the "game over" screen and plays a sick TARDIS sound
        for a in angels._list:
            if a.getCollideBox().colliderect(self.getCollideBox()) and self._appear:
                breakingChannel = SoundManager.getInstance().playSound("breaking.wav")
                state = "game over"
        return state
        


                
        
