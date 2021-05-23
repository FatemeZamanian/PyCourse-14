import pygame
import random
import time

pygame.init()


class Color:
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    blue = (50, 0, 200)
    green = (124, 252, 0)
    crimson = (220, 20, 60)
    pink = (255, 105, 180)
    yellow = (255, 215, 0)
    teal = (0, 128, 128)


class Shape:
    images = ['images/fish.png',
              'images/fox.png',
              'images/lion.png',
              'images/monkey.png',
              'images/rabbit.png',
              'images/wolf.png',
              'images/zebra.png'
              ]

    def __init__(self):
        self.x = random.randint(0, Game.width - 80)
        self.y = random.randint(60, Game.height - 80)
        self.z = 100
        self.color = random.choice(
            [Color.white, Color.red, Color.blue, Color.green, Color.crimson, Color.pink, Color.yellow, Color.teal])
        self.img_path = random.choice(self.images)
        self.img = pygame.image.load(self.img_path)
        self.area = pygame.draw.rect(Game.screen, self.color, [self.x, self.y, self.z, self.z])

    def show(self):
        self.area = pygame.draw.rect(Game.screen, self.color, [self.x, self.y, self.z, self.z])
        Game.screen.blit(self.img, (self.x, self.y))

    def move(self):
        self.x = random.randint(0, Game.width - 80)
        self.y = random.randint(60, Game.height - 80)


class Game:
    width = 650
    height = 650
    bgColor = Color.black
    font = pygame.font.SysFont('Arial', 23)
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Guess Im new?')
    score = 0
    start = 0
    total = 0

    @staticmethod
    def play():
        Game.start = time.time()
        shapes = [Shape()]
        clock = pygame.time.Clock()
        while True:
            if len(shapes) == 63:
                Game.screen.fill(Color.green)
                win_txt = Game.font.render('You win...!', True, Color.black)
                Game.screen.blit(win_txt, (Game.width / 2, Game.height / 2))
                pygame.display.update()
                time.sleep(3)
                exit()

            if int(Game.total) == 120:
                Game.screen.fill(Color.red)
                win_txt = Game.font.render('You lose...!', True, Color.black)
                Game.screen.blit(win_txt, (Game.width / 2, Game.height / 2))
                pygame.display.update()
                time.sleep(5)
                exit()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for shape in shapes:
                        shape.move()
                        if shape.area.collidepoint(event.pos):
                            if shape == shapes[-1]:
                                while True:
                                    temp = Shape()
                                    # if not any(temp.img_path==sh.img_path and temp.color==sh.color for sh in shapes):
                                    if all(temp.img_path != sh.img_path or temp.color != sh.color for sh in shapes):
                                        shapes.append(temp)
                                        Game.score += 1
                                        break
                                else:
                                    Game.score = 0
                                    Game.play()

            Game.screen.fill(Game.bgColor)
            pygame.draw.rect(Game.screen, Color.yellow, [0, 0, Game.width, 30])
            m_score = Game.font.render('score:' + str(Game.score), True, Color.black)
            Game.screen.blit(m_score, (0, 0))
            Game.total = time.time() - Game.start
            time_txt = Game.font.render('Timer:' + str(int(Game.total)), True, Color.black)
            Game.screen.blit(time_txt, (200, 0))

            for shape in shapes:
                shape.show()

            pygame.display.update()
            clock.tick(24)


if __name__ == '__main__':
    Game.play()
