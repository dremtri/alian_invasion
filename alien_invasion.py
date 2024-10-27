import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet

class AlienInvasion:
  """管理游戏资源和⾏为的类"""
  def __init__(self):
    """初始化游戏并创建游戏资源"""
    pygame.init()
    self.clock = pygame.time.Clock() 
    self.setting = Settings()
    self.screen = pygame.display.set_mode((self.setting.screen_width,self.setting.screen_height))
    pygame.display.set_caption("Alien Invasion")
    self.ship = Ship(self)
    self.bullets = pygame.sprite.Group()
  
  def run_game(self):
    """开始游戏的主循环"""
    while True:
      self._check_events()
      self.ship.update()
      self.bullets.update()
      self._update_bullets()
      self._update_screen()
      self.clock.tick(60)
  
  def _check_events(self):
    """响应按键和鼠标事件"""
    # 侦听键盘和鼠标事件
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()
      elif event.type == pygame.KEYDOWN:
        self.check_keydown_events(event)
      elif event.type == pygame.KEYUP:
          self.check_keyup_events(event)
  
  def check_keydown_events(self, event):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
      self.ship.moving_right = True
    elif event.key == pygame.K_LEFT:
      self.ship.moving_left = True
    elif event.key == pygame.K_DOWN:
      self.ship.moving_down = True
    elif event.key == pygame.K_UP:
      self.ship.moving_up = True
    elif event.key == pygame.K_q:
      sys.exit()
    elif event.key == pygame.K_SPACE:
      self._fire_bullet()

  def check_keyup_events(self, event):
    """响应松开"""
    if event.key == pygame.K_RIGHT:
      self.ship.moving_right = False
    elif event.key == pygame.K_LEFT:
      self.ship.moving_left = False
    elif event.key == pygame.K_DOWN:
      self.ship.moving_down = False
    elif event.key == pygame.K_UP:
      self.ship.moving_up = False

  def _fire_bullet(self):
    """创建一个子弹，并将其加入编组bullets中"""
    if len(self.bullets) < self.setting.bullets_allowed:
      new_bullet = Bullet(self)
      self.bullets.add(new_bullet)

  def _update_bullets(self):
    """更新子弹的位置，并删除已消失的子弹"""
    # 更新⼦弹的位置
    self.bullets.update()
    # 删除已消失的⼦弹
    for bullet in self.bullets.copy():
      if bullet.rect.bottom <= 0:
        self.bullets.remove(bullet)

  def _update_screen(self):
    """更新屏幕上的图像，并切换到新屏幕"""
    # 每次循环时都重绘屏幕
    self.screen.fill(self.setting.bg_color)
    for bullet in self.bullets.sprites():
      bullet.draw_bullet()
    self.ship.blitme()
    # 让最近绘制的屏幕可见
    pygame.display.flip()

# 判断是否直接运行当前文件
if __name__ == '__main__':
  # 创建一个游戏实例病运行游戏
  ai = AlienInvasion()
  ai.run_game()
