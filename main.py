import math
import random
import pygame

YELLOW = (255, 231, 42)
GREEN = (32, 161, 98)
RED = (239, 52, 155)
WHITE = (255, 255, 255)
BROWN = (150, 77, 34)

WINDOW_X_LENGTH = 900
WINDOW_Y_LENGTH = 600

GM = (450, 500)
GM_topleft = (425, 475)
GM_bottomright = (475, 525)


class Coin:
    def __init__(self, window):
        self.window = window
        self.imagePath = "./img/coin_gold_dollar.png"  # 图片的大小是45*45
        self.image = pygame.image.load(self.imagePath)
        self.font = pygame.font.SysFont('timesnewroman', 26, bold=True)
        with open("./res/lists.txt", 'r', encoding='utf-8') as file:
            context = file.readlines()
            line = random.choice(context)
        self.word = line[:-1]
        self.wordLength = len(self.word)
        self.char_widths = [self.font.size(char)[0] for char in self.word]  # 我需要每个字母都单独拿出来渲染
        text_width = sum(self.char_widths)
        self.width = max(text_width, 45)  # 计算整体宽度，也就是X轴方向上的长度
        tmp = 0
        for i in range(self.wordLength):  # 修改为每个字母在X方向上需要的偏移值
            _ = self.char_widths[i]
            self.char_widths[i] = tmp
            tmp += _
        self.charList = []
        for i in range(self.wordLength):
            char = self.font.render(self.word[i], True, WHITE, BROWN)
            self.charList.append(char)
        self.index = 0
        self.size = (self.width, 45)
        self.location = (random.randint(0, WINDOW_X_LENGTH - self.width), 0)
        self.direction = 0

    def __del__(self):
        # 垃圾回收器会自动释放该对象占用的内存空间，无需担心
        print("硬币被回收了")

    def moveCoin(self, moveX: int, moveY: int):
        x, y = self.location
        self.location = (x + moveX, y + moveY)
        self.window.blit(self.image, (x + moveX, y + moveY))
        for char, index in zip(self.charList, range(self.wordLength)):
            self.window.blit(char, (x + moveX + self.char_widths[index], y + moveY + 45))

    def moveRandom(self, frame):
        x, y = self.location
        if frame % 1000 == 0:
            self.direction = random.choice([-2, -1, 0, 1, 2])
        moveX = 0
        if frame % 20 == 0 and (0 <= x + self.direction <= WINDOW_X_LENGTH - self.width):
            moveX = self.direction
        moveY = 1
        self.moveCoin(moveX, moveY)

    def moveToMagnet(self):
        x, y = self.location
        x_distance = int((GM[0] - x) / 15)
        y_distance = int((GM[1] - y) / 15)
        self.moveCoin(x_distance, y_distance)


class GoldMagnet:
    def __init__(self, window):
        self.window = window
        # 头
        head1 = pygame.image.load("./img/head1andeyebrow.png")
        self.head1 = pygame.transform.rotozoom(head1, 0, 0.25)
        head2 = pygame.image.load("./img/head2.png")
        self.head2 = pygame.transform.rotozoom(head2, 0, 0.25)
        # 茎
        stem = pygame.image.load("./img/GoldMagnet_stem.png")
        self.stem = pygame.transform.rotozoom(stem, 0, 0.7)
        self.stemLoca = (440, 535)
        # 叶
        leaf1 = pygame.image.load("./img/GoldMagnet_leaf1.png")
        self.leaf1 = pygame.transform.rotozoom(leaf1, 0, 0.6)
        leaf2 = pygame.image.load("./img/GoldMagnet_leaf2.png")
        self.leaf2 = pygame.transform.rotozoom(leaf2, 0, 0.6)
        leaf3 = pygame.image.load("./img/GoldMagnet_leaf3.png")
        self.leaf3 = pygame.transform.rotozoom(leaf3, -20, 0.6)
        leaf4 = pygame.image.load("./img/GoldMagnet_leaf4.png")
        self.leaf4 = pygame.transform.rotozoom(leaf4, 0, 0.6)
        self.leaf1Loca = (427, 530)
        self.leaf2Loca = (430, 533)
        self.leaf3Loca = (440, 526)
        self.leaf4Loca = (450, 525)
        # 其他
        self.location = (380, 470)
        self.state = "idle"  # idle or working
        self.step = 0

    def rotating(self, image, length: int, angle: int = 0, loca: tuple = (380, 470)):
        rotatedImg = pygame.transform.rotozoom(image, angle, 1)
        angle = angle % 90
        newlen = (math.sin(math.pi * angle / 180) + math.sin(math.pi * (90 - angle) / 180)) * length
        self.window.blit(rotatedImg, (loca[0] - (newlen - length) / 2, loca[1] - (newlen - length) / 2))  # 先除后减

    def drawLeaf14AndStem(self):
        self.window.blit(self.stem, self.stemLoca)
        self.window.blit(self.leaf1, self.leaf1Loca)
        self.window.blit(self.leaf4, self.leaf4Loca)

    def drawLeaf23(self):
        self.window.blit(self.leaf2, self.leaf2Loca)
        self.window.blit(self.leaf3, self.leaf3Loca)

    def idle(self):
        x, y = self.head1.get_size()
        if self.state == "working":
            self.step += 1
            if self.step <= 20:
                self.drawLeaf14AndStem()
                self.rotating(self.head1, x, self.step - 20)
                self.drawLeaf23()
            else:
                self.step = 0
                self.state = "idle"
        else:
            self.drawLeaf14AndStem()
            self.window.blit(self.head1, self.location)
            self.drawLeaf23()

    def work(self):
        x, y = self.head1.get_size()
        if self.state == "working":
            self.drawLeaf14AndStem()
            self.rotating(self.head2, x, -20)
            self.drawLeaf23()
        else:
            self.step += 4
            if self.step <= 20:
                self.drawLeaf14AndStem()
                self.rotating(self.head1, x, self.step)
                self.drawLeaf23()
            elif 20 < self.step <= 60:
                self.drawLeaf14AndStem()
                self.rotating(self.head1, x, 40 - self.step)
                self.drawLeaf23()
            else:
                self.state = "working"
                self.step = 0


class TypingGames:
    def __init__(self):
        # 窗口
        pygame.init()
        self.window = pygame.display.set_mode((WINDOW_X_LENGTH, WINDOW_Y_LENGTH))
        pygame.display.set_caption("TypingGame")
        background = pygame.image.load("./img/lawn_2700_1800.jpg")
        self.background = pygame.transform.rotozoom(background, 0, 1 / 3)
        self.window.blit(self.background, (0, 0))
        # 记分板  硬币  磁铁
        self.font = pygame.font.SysFont('microsoftyahei', 26, bold=True)
        self.scoreBoard = self.font.render("得分:" + '0', True, WHITE, BROWN)
        self.coin = Coin(self.window)
        self.magnet = GoldMagnet(self.window)
        # 一些标记
        self.frame = 0
        self.running = True
        self.source = 0
        pygame.display.flip()

    def __del__(self):
        print("游戏结束")
        pygame.quit()

    def run(self):
        while self.running:
            self.frame += 1
            if self.frame % 10 == 0:  # 屏幕的刷新是以这里为准的
                self.draw()

            pygame.display.update()  # update会花费很多时间，且和窗口大小有关，当delay用

            if self.coin.location[1] > WINDOW_Y_LENGTH:
                self.coin = Coin(self.window)

            if GM_topleft[0] <= self.coin.location[0] <= GM_bottomright[0] \
                    and GM_topleft[1] <= self.coin.location[1] <= GM_bottomright[1] \
                    and self.coin.index == self.coin.wordLength:
                self.source += 1
                self.coin = Coin(self.window)
                self.magnet.step = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                elif event.type == pygame.KEYDOWN:
                    if not (0x14 < event.key < 0x110000):
                        continue
                    char = chr(event.key)
                    if self.coin.index == self.coin.wordLength:
                        continue
                    targetChar = self.coin.word[self.coin.index]
                    if char == targetChar:
                        self.coin.charList[self.coin.index] = self.coin.font.render(targetChar, True, YELLOW)
                        self.coin.index += 1

    def draw(self):
        self.window.blit(self.background, (0, 0))
        # pygame.draw.rect(self.window, [255, 0, 0], [GM_topleft[0], GM_topleft[1], 50, 50], 0) # 显示吸收范围
        self.drawCoin()
        self.drawMagnet()
        self.drawSourceBoard()

    def drawCoin(self):
        if self.coin.index != self.coin.wordLength:
            self.coin.moveRandom(self.frame)
        else:
            self.coin.moveToMagnet()

    def drawMagnet(self):
        if self.coin.index != self.coin.wordLength:
            self.magnet.idle()
        else:
            self.magnet.work()

    def drawSourceBoard(self):
        self.scoreBoard = self.font.render("得分:" + str(self.source), True, WHITE, BROWN)
        self.window.blit(self.scoreBoard, (15, WINDOW_Y_LENGTH - 40))


tg = TypingGames()
tg.run()
