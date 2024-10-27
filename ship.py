import pygame

class Ship:
  """管理飞船的类"""
  def __init__(self, ai_game):
    """初始化⻜船并设置其初始位置"""
    self.screen = ai_game.screen
    self.setting = ai_game.setting
    self.screen_rect = ai_game.screen.get_rect()
    # 加载⻜船图像并获取其外接矩形
    self.image = pygame.image.load('images/ship.bmp')
    self.rect = self.image.get_rect()
    # 对于每艘新⻜船，都将其放在屏幕底部中央
    self.rect.midbottom = self.screen_rect.midbottom

    # 在飞船的 x 中存储一个浮点数
    self.x = float(self.rect.x)
    self.y = float(self.rect.y)
    # 移动标志 (飞船一开始不移动)
    self.moving_right = False
    self.moving_left = False
    self.moving_down = False
    self.moving_up = False

  def update(self):
    """根据移动标志调整飞船的位置"""
    # 更新飞船的属性 x 的值，而不是其外接矩形的属性 x 的值
    if self.moving_right and self.rect.right < self.screen_rect.right:
      self.x += self.setting.ship_speed
    if self.moving_left and self.rect.left > 0:
      self.x -= self.setting.ship_speed
    if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
      self.y += self.setting.ship_speed
    if self.moving_up and self.rect.top > 0:
      self.y -= self.setting.ship_speed
    # 根据 self.x 更新 rect 对象
    self.rect.x = self.x
    self.rect.y = self.y

  def blitme(self):
    """在指定位置绘制⻜船"""
    self.screen.blit(self.image, self.rect)