import sys
import pygame
from time import sleep

from settings import Settings 
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats

class AlienInvasion:
  """管理游戏资源和⾏为的类"""
  def __init__(self):
    """初始化游戏并创建游戏资源"""
    pygame.init()
    self.clock = pygame.time.Clock() 
    self.setting = Settings()
    self.screen = pygame.display.set_mode((self.setting.screen_width,self.setting.screen_height))
    pygame.display.set_caption("Alien Invasion")
    self.stats = GameStats(self)
    self.ship = Ship(self)
    self.bullets = pygame.sprite.Group()
    self.aliens = pygame.sprite.Group()
    self._create_fleet()
    # 游戏启动后处于活动状态
    self.game_active = True
  
  def run_game(self):
    """开始游戏的主循环"""
    while True:
      self._check_events()
      if self.game_active:
        self.ship.update()
        self.bullets.update()
        self._update_bullets()
        self._update_aliens()
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
    self._check_bullet_alien_collisions()

  def _check_bullet_alien_collisions(self):
    """响应子弹和外星人的碰撞"""
    # 删除发生碰撞的子弹和外星人
    collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
    if not self.aliens:
      # 删除现有的所有子弹并创建一群新的外星人
      self.bullets.empty()
      self._create_fleet()

  def _update_aliens(self):
    """检查是否有外星人位于屏幕边缘，并更新外星舰队中所有外星人的位置"""
    self._check_fleet_edges()
    self.aliens.update()
    # 检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(self.ship, self.aliens):
      self._ship_hit()
    # 检查是否有外星人到达了屏幕的下边缘
    self._check_aliens_bottom()

  def _create_fleet(self):
    """创建一个外星人舰队"""
    # 创建一个外星人, 再不断添加，直到没有空间添加外星人为止
    # 外星人的间距为外星人的宽度
    alien = Alien(self)
    alien_width, alien_height = alien.rect.size
    current_x, current_y = alien_width, alien_height
    while current_y < (self.setting.screen_height - 3 * alien_height):
      # self._create_alien(current_x)
      # current_y += alien_height * 2
      while current_x < (self.setting.screen_width - 2 * alien_width):
        self._create_alien(current_x, current_y)
        current_x += 2 * alien_width
      current_x = alien_width
      current_y += 2 * alien_height
    
  def _create_alien(self, x_position, y_position):
    """创建一个外星人，并将其放在当前行中"""
    new_alien = Alien(self)
    new_alien.x = x_position
    new_alien.rect.x = x_position
    new_alien.rect.y = y_position
    self.aliens.add(new_alien)

  def _ship_hit(self):
    """响应飞船被外星人撞到"""
    if self.stats.ships_left > 0:
      # 将ships_left减1
      self.stats.ships_left -= 1
      # 清空外星人列表和子弹列表
      self.bullets.empty()
      self.aliens.empty()
      # 创建一个新的外星舰队, 并将飞船放到屏幕底端中央
      self._create_fleet()
      self.ship.center_ship()
      # 暂停
      sleep(0.5)
    else:
      self.game_active = False

  def _check_aliens_bottom(self):
    """检查是否有外星人到达了屏幕底端"""
    screen_rect = self.screen.get_rect()
    for alien in self.aliens.sprites():
      if alien.rect.bottom >= screen_rect.bottom:
        # 像飞船被撞到一样进行处理
        self._ship_hit()
        break

  def _check_fleet_edges(self):
    """有外星人到达边缘时采取相应的措施"""
    for alien in self.aliens.sprites():
      if alien.check_edges():
        self._change_fleet_direction()
        break

  def _change_fleet_direction(self):
    """将整群外星人下移，并改变它们的方向"""
    for alien in self.aliens.sprites():
      alien.rect.y += self.setting.fleet_drop_speed
    self.setting.fleet_direction *= -1

  def _update_screen(self):
    """更新屏幕上的图像，并切换到新屏幕"""
    # 每次循环时都重绘屏幕
    self.screen.fill(self.setting.bg_color)
    for bullet in self.bullets.sprites():
      bullet.draw_bullet()
    self.ship.blitme()
    self.aliens.draw(self.screen)
    # 让最近绘制的屏幕可见
    pygame.display.flip()

# 判断是否直接运行当前文件
if __name__ == '__main__':
  # 创建一个游戏实例病运行游戏
  ai = AlienInvasion()
  ai.run_game()
