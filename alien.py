import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
  """表示单个外星人的类"""
  def __init__(self, ai_game):
    """初始化外星人并设置其起始位置"""
    super().__init__()
    self.screen = ai_game.screen
    self.setting = ai_game.setting
    self.image = pygame.image.load('images/alien.bmp')
    self.rect = self.image.get_rect()
    # 每个外星人最初都在屏幕左上角附近
    self.rect.x = self.rect.width
    self.rect.y = self.rect.height
    # 存储外星人的准确位置
    self.x = float(self.rect.x)
  
  def update(self):
    """向左或向右移动外星人"""
    self.x += (self.setting.alien_speed * self.setting.fleet_direction)
    self.rect.x = self.x

  def check_edges(self):
    """如果外星人位于屏幕边缘，就返回True"""
    screen_rect = self.screen.get_rect()
    if self.rect.right >= screen_rect.right or self.rect.left <= 0:
      return True
