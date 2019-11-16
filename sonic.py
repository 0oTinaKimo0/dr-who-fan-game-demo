import pygame
from .utils.vector2D import Vector2
import random
from .utils.drawable import Drawable
from .utils.frameManager import FrameManager

class Sonic(Drawable):
    # initializes the player object
    def __init__(self, hero, position):     
        super().__init__("", position)
        self._image = self.drawPie(self._image)
        
        # makes the flashlight semi-transparent
        self._image.set_alpha(50)
        pygame.transform.rotate(self._image, 135)
        self._original_image = self._image
        self._rect = self._image.get_rect()
        self._direction = Vector2(0,0)
        self._velocity = hero._velocity
        

    def rotate(self):
        w = self._original_image.get_width()
        h = self._original_image.get_height()
        angle = Player.getAngle(self)
        self._image = pygame.transform.rotate(self._original_image, angle)
        self._rect = self._image.get_rect(center=(self.getX(), self.getY()))
        
    # ref: https://stackoverflow.com/questions/23246185/python-draw-pie-shapes-with-colour-filled
    def drawPie(self, surface):
        cx, cy, r = 0, 0, 200
        angle = 90
        # starts list of polygon points
        p = [(cx, cy)]
        # gets points on arc
        for n in range(0,angle):
            x = cx + int(r*math.cos(n*math.pi/180))
            y = cy + int(r*math.sin(n*math.pi/180))
            p.append((x, y))
        p.append((cx, cy))
        pie = pygame.Surface((200,200))
        pie.set_colorkey((0,0,0))
        # draws pie segment
        if len(p) > 2:
            pygame.draw.polygon(pie, (52, 113, 235), p)
        surface.blit(pie, (200,200))
        return surface
    
    def draw(self, surface):
        surface.blit(self._image, (int(self._position[0] - Drawable.WINDOW_OFFSET[0] * self._parallax),
                                    int(self._position[1] - Drawable.WINDOW_OFFSET[1] * self._parallax)))
    
    def update(self, hero, ticks):
        newPosition = Vector2(hero._center.x+ self._velocity.x * ticks  , self.getY() - self._velocity.y * ticks)
        self.setPosition(newPosition)
