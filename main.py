import pygame
import sys
from pygame.locals import *
from random import *

class Ball(pygame.sprite.Sprite):#球类继承自Sprite
    def __init__(self, grayball_image,greenball_image, position, speed, bg_size, target):
        pygame.sprite.Sprite.__init__(self)
        self.grayball_image = pygame.image.load(grayball_image).convert_alpha()
        self.greenball_image = pygame.image.load(greenball_image).convert_alpha()
        self.rect = self.grayball_image.get_rect()
        self.rect.left, self.rect.top = position #将小球放在指定位置
        self.side = [choice([-1, 1]), choice([-1, 1])]
        self.collide = False
        self.speed = speed
        self.target = target
        self.control = False
        self.width, self.height = bg_size[0], bg_size[1]
        self.radius = self.rect.width/2
    def check(self,motion):
        pass
    def move(self):
        if self.control:
            self.rect = self.rect.move(self.speed)
        else:
            self.rect = self.rect.move((self.side[0] * self.speed[0], self.side[1] * self.speed[1] ))
        #如果小球的右侧出了边界，那么小球左侧的位置改为右侧的边界
        if self.rect.right <= 0:
            self.rect.left = self.width
        elif self.rect.left >= self.width:
            self.rect.right = 0
        elif self.rect.bottom <= 0:
            self.rect.top = self.height
        elif self.rect.top >= self.height:
            self.rect.bottom = 0
    def check(self,motion):
        if self.target <motion <self.target + 5:
            return  True
        else:
            return False

# def collide_check(item,target):
#     col_balls = []
#     for each in target:
#         distance = math.sqrt(\
#             math.pow((item.rect.center[0] - each.rect.center[0]),2)\
#             + math.pow((item.rect.center[1] - each.rect.center[1]),2))
#         if distance <= (item.rect.width + each.rect.width)/2:
#             col_balls.append(each)
#     return col_balls
class Glass(pygame.sprite.Sprite):
    def __init__(self, glass_image,mouse_image, bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.glass_image = pygame.image.load(glass_image).convert_alpha()
        self.glass_rect = self.glass_image.get_rect()
        self.glass_rect.left, self.glass_rect.top = \
                             (bg_size[0] - self.glass_rect.width)//2,\
                              bg_size[1] - self.glass_rect.height
        self.mouse_image = pygame.image.load(mouse_image).convert_alpha()
        self.mouse_rect = self.mouse_image.get_rect()
        self.mouse_rect.left, self.mouse_rect.top = \
        self.glass_rect.left, self.glass_rect.top
        #初始化鼠标的位置于左上角
        pygame.mouse.set_pos([self.glass_rect.left, self.glass_rect.top])
        #鼠标不可见
        pygame.mouse.set_visible(True)

def main():
    pygame.init()

    greenball_iamge = "green_ball.png"
    gray_image = "gray_ball.png"
    glass_image = "glass_image.png"
    mouse_image = "hand.png"
    bg_image = "background.png"
    running = True
    #添加魔性音乐
    pygame.mixer.music.load("bg_music.ogg")
    pygame.mixer.music.play()

    #添加音效
    loser_sound = pygame.mixer.Sound("loser.wav")
    laugh_sound = pygame.mixer.Sound("laugh.wav")
    winner_sound = pygame.mixer.Sound("winner.wav")
    hole_sound = pygame.mixer.Sound("hole.wav")

    #音乐播放完时游戏结束
    GAMEOVER = USEREVENT
    pygame.mixer.music.set_endevent(GAMEOVER)

    bg_size = width, height = 1024, 681#根据背景图片指定游戏界面尺寸
    screen = pygame.display.set_mode(bg_size)
    pygame.display.set_caption("Play the ball - First Demo")
    background = pygame.image.load(bg_image).convert_alpha()

    hole = [(117, 118, 199, 201),\
            (225, 227, 390, 392),\
            (503, 505, 320, 322),\
            (698, 700, 192, 194),\
            (906, 908, 419, 421)]

    balls = []#用来存放小球对象的列表
    group = pygame.sprite.Group()

    #创建五个小球
    BALL_NUM = 5
    for i in range(BALL_NUM):
        #位置随机，速度随机
        position = randint(0, width-100,), randint(0, height-100)
        speed = [randint(1, 5), randint(1, 5)]
        ball = Ball(gray_image, greenball_iamge, position, speed, bg_size, 5*(i+1))
        # while collide_check(ball,balls):
        #     ball.rect.left, ball.rect.top = randint(0, width - 100), \
        #     randint(0, height - 100)

        while pygame.sprite.spritecollide(ball,group,False,pygame.sprite.collide_circle):
            ball.rect.left, ball.rect.top = randint(0, width - 100), \
            randint(0, height - 100)
        balls.append(ball)
        group.add(ball)
    area = Glass(glass_image,mouse_image, bg_size)

    motion = 0
    MYTIMER = USEREVENT + 1
    pygame.time.set_timer(MYTIMER,1000)
    pygame.key.set_repeat(100,100)


    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == GAMEOVER:
                loser_sound.play()
                pygame.time.delay(2000)
                laugh_sound.play()
                running = False
            elif event.type == MYTIMER:
                if motion:
                    for each in group:
                        if each.check(motion):
                            each.speed = [0, 0]
                            each.control = True
                    motion = 0
            elif event.type == MOUSEMOTION:
                motion += 1
            elif event.type == KEYDOWN:
                if event.key == K_w:
                    for each in group:
                        if each.control:
                            each.speed[1] -= 1
                if event.key == K_s:
                    for each in group:
                        if each.control:
                            each.speed[1] += 1
                if event.key == K_a:
                    for each in group:
                        if each.control:
                            each.speed[0] -= 1
                if event.key == K_d:
                    for each in group:
                        if each.control:
                            each.speed[0] += 1
                if event.key == K_SPACE:
                    for each in group:
                        if each.control:
                            for i in hole:
                                if i[0] <= each.rect.left <= i[1] and\
                                    i[2] <= each.rect.top <=i[3]:
                                    #播放音效
                                    hole_sound.play()
                                    each.speed = [0, 0]
                                    group.remove(each)
                                    temp = balls.pop(balls.index(each))
                                    balls.insert(0, temp)
                                    hole.remove(i)
                            if not hole:
                                pygame.mixer.music.stop()
                                winner_sound.play()
                                pygame.time.delay(3000)
                                msg = pygame.image.load("win.png").convert_alpha()
                                msg_pos = (width -msg.get_width())//2,(height-msg.get_height())//2
                                msg.append((msg, msg_pos))
                                laugh_sound.play()



        screen.blit(background, (0, 0))
        screen.blit(area.glass_image, area.glass_rect)
        # 获取鼠标的当前位置，并设置代替光标的图片
        area.mouse_rect.left, area.mouse_rect.top = pygame.mouse.get_pos()
        #限制鼠标只能在玻璃内摩擦摩擦
        if area.mouse_rect.left < area.glass_rect.left:
            area.mouse_rect.left = area.glass_rect.left
        if area.mouse_rect.left > area.glass_rect.right - area.mouse_rect.width:
            area.mouse_rect.left = area.glass_rect.right - area.mouse_rect.width
        if area.mouse_rect.top < area.glass_rect.top:
            area.mouse_rect.top = area.glass_rect.top
        if area.mouse_rect.top >area.glass_rect.bottom - area.mouse_rect.height:
            area.mouse_rect.top = area.glass_rect.bottom - area.mouse_rect.height
        screen.blit(area.mouse_image, area.mouse_rect)


        for each in balls:
            each.move()
            if each.collide:
                each.speed = [randint(1, 10), randint(1, 10)]
                each.collide = False
            if each.control:
                screen.blit(each.greenball_image, each.rect)
            else:
                screen.blit(each.grayball_image, each.rect)

        # for i in range(BALL_NUM):
        #     item = balls.pop(i)
        #     if collide_check(item,balls):
        #         item.speed[0] = -item.speed[0]
        #         item.speed[1] = -item.speed[1]
        #     balls.insert(i,item)
        for each in group:
            group.remove(each)
            if pygame.sprite.spritecollide(each, group, False, pygame.sprite.collide_circle):
                each.side[0] = -each.side[0]
                each.side[1] = -each.side[1]
                each.collide = True
                if each.control:
                    each.side[0] = -1
                    each.side[1] = -1
                    each.control = False

            group.add(each)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()

