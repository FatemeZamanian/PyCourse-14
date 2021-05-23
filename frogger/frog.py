import pygame
import random
import time

pygame.init()


class Color:
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    blue = (50, 0, 200)
    grey = (100, 100, 100)
    green = (0, 255, 0)


class Game:
    width = 650
    height = 650
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Frogger')
    clock = pygame.time.Clock()
    fps = 30


def play():
    c = 0
    frogs = []
    cars = []
    woods = []
    frog = Frog()
    cars.append(BlueCar())
    while True:
        c += 1
        if Frog.count == 5:
            Game.screen.fill(Color.green)
            win_txt = Game.font.render('You win...!', True, Color.black)
            Game.screen.blit(win_txt, (Game.width / 2, Game.height / 2))
            pygame.display.update()
            time.sleep(3)
            exit()

        if Frog.live <= 0 and Frog.count <5:
            Game.screen.fill(Color.red)
            font = pygame.font.SysFont('comicsansms', 40)
            txt_lose = font.render('Game Over', True, Color.black)
            txt_score = font.render('Your score:'+str(Frog.count), True, Color.black)
            Game.screen.blit(txt_lose, (Game.width / 2, Game.height / 2 ))
            Game.screen.blit(txt_score, (Game.width / 2, Game.height / 2 +50))
            pygame.display.update()
        else:
            if frog.win()==True:
                frog=Frog()
                Frog.live -= 1
            frog.move()
            frog.rect.update(frog.x, frog.y, 45, 45)
            if c % 50 == 0:
                if random.random() < 0.8:
                    txi = random.choice(['red', 'blue', 'black'])
                    if txi == 'red':
                        cars.append(RedCar())
                    elif txi == 'blue':
                        cars.append(BlueCar())
                    elif txi == 'black':
                        cars.append(BlackCar())
            for car in cars:
                car.move()
            if c % 30 == 0:
                if random.random() < 0.7:
                    woods.append(Wood())
            for wood in woods:
                wood.move()
            Game.screen.fill((0, 0, 0))
            pygame.draw.rect(Game.screen, Color.green, [0, 600, Game.width, Game.height])
            pygame.draw.rect(Game.screen, Color.grey, [0, 350, Game.width, 250])
            pygame.draw.rect(Game.screen, Color.green, [0, 300, Game.width, 50])
            pygame.draw.rect(Game.screen, Color.blue, [0, 50, Game.width, 250])
            pygame.draw.rect(Game.screen, Color.green, [0, 0, Game.width, 50])
            for car in cars:
                car.show()
                car.rect.update(car.x, car.y, 80, 45)
            for wood in woods:
                wood.show()
                wood.rect.update(wood.x, wood.y, 50, 45)
            frog.show()

            if any(frog.accident(car.x,car.y) for car in cars):
                Frog.live -=1
                frog=Frog()

            for wood in woods:
                if frog.boat(wood.x, wood.y):
                    frog.x = wood.x + 10

            if all(frog.drown(wood.x, wood.y) for wood in woods) and 50 <= frog.y <300:
                Frog.live -= 1
                frog=Frog()

            for i in range(1,Frog.count+1):
                image = pygame.image.load('images/frog.png')
                Game.screen.blit(image, (i*100, 10))

            pygame.display.update()
            Game.clock.tick(Game.fps)


class Wood:
    speed = 1

    def __init__(self):
        self.line = random.choice(['1', '2', '3', '4', '5'])
        if self.line == '1':
            self.y = 50
            self.x = -50
        elif self.line == '2':
            self.y = 100
            self.x = Game.width + 50
        elif self.line == '3':
            self.y = 150
            self.x = -50
        elif self.line == '4':
            self.y = 200
            self.x = Game.width + 50
        elif self.line == '5':
            self.y = 250
            self.x = -50
        self.img = pygame.image.load('images/wood.png')
        self.rect = self.img.get_rect()

    def show(self):
        if self.line == '2' or self.line == '4':
            self.img = pygame.image.load('images/wood.png')
            Game.screen.blit(self.img, (self.x, self.y))
            self.rect = self.img.get_rect()
        else:
            self.img = pygame.image.load('images/woodd.png')
            Game.screen.blit(self.img, (self.x, self.y))
            self.rect = self.img.get_rect()

    def move(self):
        if self.line == '2' or self.line == '4' or self.line == '6':
            self.x -= Wood.speed
        else:
            self.x += Wood.speed


class Car:
    speed = 2

    def __init__(self):
        self.line = random.choice(['1', '2', '3', '4', '5'])
        if self.line == '1':
            self.y = 350
            self.x = -50
        elif self.line == '2':
            self.y = 400
            self.x = Game.width + 50
        elif self.line == '3':
            self.y = 450
            self.x = -50
        elif self.line == '4':
            self.y = 500
            self.x = Game.width + 50
        elif self.line == '5':
            self.y = 550
            self.x = -50

    def show(self):
        if self.line == '2' or self.line == '4' or self.line == '6':
            Game.screen.blit(self.img, (self.x, self.y))
        else:
            Game.screen.blit(pygame.transform.flip(self.img, True, False), [self.x, self.y])

    def move(self):
        if self.line == '2' or self.line == '4' or self.line == '6':
            self.x -= Car.speed
        else:
            self.x += Car.speed


class BlueCar(Car):
    def __init__(self):
        super().__init__()
        self.img = 'images/blue.png'
        self.img = pygame.image.load(self.img)
        self.rect = self.img.get_rect()


class RedCar(Car):
    def __init__(self):
        super().__init__()
        self.img = 'images/red.png'
        self.img = pygame.image.load(self.img)
        self.rect = self.img.get_rect()


class BlackCar(Car):
    def __init__(self):
        super().__init__()
        self.img = 'images/black.png'
        self.img = pygame.image.load(self.img)
        self.rect = self.img.get_rect()


class Frog:
    live = 5
    count = 0

    def __init__(self):
        self.x = Game.width / 2
        self.y = Game.height - 50
        self.w = 60
        self.image = pygame.image.load('images/frog.png')
        self.rect = self.image.get_rect()

    def show(self):
        Game.screen.blit(self.image, (self.x, self.y))

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.y -= 50
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.y += 50
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.x -= 50
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.x += 50

    def accident(self, cx, cy):
        if pygame.Rect(self.x, self.y, 45, 45).colliderect(pygame.Rect(cx, cy, 70, 30)):
            return True
        else:
            return False

    def boat(self, bx, by):
        if pygame.Rect(self.x, self.y, 45, 45).colliderect(pygame.Rect(bx, by, 45, 45)):
            return True
        else:
            return False

    def drown(self, bx, by):
        if not pygame.Rect(self.x, self.y, 50, 50).colliderect(pygame.Rect(bx, by, 50, 50)) or Game.width<self.x or self.y<0:
            return True
        else:
            return False

    def win(self):
        if self.y==50:
            Frog.count+=1
            self.y=49
            return True
        else:
            return False


if __name__ == '__main__':
    play()
