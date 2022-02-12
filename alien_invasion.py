
import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
class AlienInvasion:

    """管理游戏资源和行为的类"""
    def __init__(self):
        
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.settings=Settings()
        self.screen=pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        pygame.display.set_caption("Alien_invasion")
        self.ship=Ship(self)
        self.bullets=pygame.sprite.Group()
        self.aliens=pygame.sprite.Group()

        self._create_fleet()


    def run_game(self):
        
        """开始游戏的主循环"""
        while True:
            self._check_event()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
            self._update_screen()

    def _check_event(self):
        """响应按键和鼠标事件"""
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self,event):
        """响应按键"""
        if event.key==pygame.K_RIGHT:
            self.ship.moving_right=True
        elif event.key==pygame.K_LEFT:
            self.ship.moving_left=True
        elif event.key==pygame.K_q:
            sys.exit()
        elif event.key==pygame.K_SPACE:
            self._fire_bullet()
            
    def _check_keyup_events(self,event):
        """响应松开"""
        if event.key==pygame.K_RIGHT:
            self.ship.moving_right=False
        elif event.key==pygame.K_LEFT:
            self.ship.moving_left=False  
    
    def _fire_bullet(self):
        """创建一颗子弹并将其放入编组bullets中"""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet=Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """更新子弹的位置并删除消失的子弹"""
        #更新子弹的位置
        self.bullets.update()
        for  bullet in self.bullets.copy():
            if bullet.rect.bottom<=0:
                self.bullets.remove(bullet)
        
        self._check_bullet_alien_collisions()
    
    def _check_bullet_alien_collisions(self):
        """响应子弹和外星人的碰撞"""
        #   删除碰撞的子弹和外星人
        collisions=pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)
        if not self.aliens:
            # 删除现有子弹并新建一群外星人
            self.bullets.empty()
            self._create_fleet()

    def _update_aliens(self):
        """
        检查是否有外星人处于屏幕边缘
        更新外星人群中所有外星人的位置
        """
        self._check_fleet_edges()
        self.aliens.update()

        #检测外星人与飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            print("ship hit!!!")

    def _create_fleet(self):
        """创建外星人群"""
        #创建一个外星人并计算一行可容纳多少个外星人
        #外星人的间距为外星人宽度
        alien=Alien(self)
        alien_width,alien_height=alien.rect.size
        available_space_x=self.settings.screen_width - (2 * alien_width)
        number_aliens_x=available_space_x // (2 * alien_width)

        #计算屏幕可容纳多少行外星人
        ship_height=self.ship.rect.height
        available_space_y=(self.settings.screen_height-
                                (3 * alien_height) - ship_height)
        number_rows=available_space_y // (2 * alien_width)

        #创建外星人人群
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number,row_number)

    def _create_alien(self,alien_number,row_number):
        #创建一个外星人并将其加入当前行
        alien=Alien(self)
        alien_width,alien_height=alien.rect.size
        alien.x=alien_width + 2 * alien_width * alien_number
        alien.rect.x=alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """有外星人到达边缘时采取相应的措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    def _change_fleet_direction(self):
        """将整群外星人下移,并改变他们的方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """更换屏幕上的新的图像,并切换到新屏幕"""
        self.screen.fill(self.settings.bg_color)
        self.ship.bilitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        pygame.display.flip()                

if __name__=="__main__":
    
    """创建游戏实例并运行游戏"""
    ai=AlienInvasion()
    ai.run_game()
