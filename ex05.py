#cording:utf-8

#from typing import self
import pygame as pg
import sys
import random as rd

from pygame.sprite import AbstractGroup

FONT_PATH = "UDDigiKyokashoN-R.ttc"  #使用するフォント
WIDTH = 1000  #画面の横サイズ
HEIGHT = 700  #画面の縦サイズ

class YOU(pg.sprite.Sprite):

    delta = {  #押すキーと移動量
        pg.K_d:(+5,0),  
        pg.K_a:(-5,0)      
    }

    def __init__(self, xy: tuple[int, int]):
        """
        お前君画像Surfaceを生成する
        引数:お前君画像ファイル名の番号
        """
        super().__init__()
        img0 = pg.transform.rotozoom(pg.image.load(f"ex05/fig/omae/0.png"), 0, 2)  # 左向き
        img = pg.transform.flip(img0, True, False)  # 右向き
        self.imgs = {
            (+5, 0): img,  # 右
            (-5, 0): img0,  # 左
        }
        self.dire = (+5, 0)
        self.image = self.imgs[self.dire]
        self.rct = self.image.get_rect()
        self.rct.center = xy

    def update(self, key_lst: list[bool], screen: pg.Surface):
        """
        押下キーに応じてお前君を移動させる
        引数1 key_lst：押下キーの真理値リスト
        引数2 screen：画面Surface
        """
        sum_mv = [0, 0]
        for k, mv in __class__.delta.items():
            if key_lst[k]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        self.rct.move_ip(sum_mv)
        screen.blit(self.image, self.rct)


class Patty(pg.sprite.Sprite):
    imgs = [pg.image.load(f"ex05/fig/patty/{i}.png") for i in range(0, 2)]

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = rd.choice(__class__.imgs)
        self.rect = self.image.get_rect()
        self.rect.center = rd.randint(0, WIDTH), 0
        self.vy = +3
        self.bound = rd.randint(50, HEIGHT/2)  # 停止位置
        self.state = "down"  # 降下状態or停止状態
        self.interval = rd.randint(50, 300)  # 爆弾投下インターバル

    def update(self):
        """
        敵機を速度ベクトルself.vyに基づき移動（降下）させる
        ランダムに決めた停止位置_boundまで降下したら，_stateを停止状態に変更する
        引数 screen：画面Surface
        """
        self.rect.centery += self.vy


class Start_countdown:
    #開始画面の表示
    def __init__(self):
        self.moji = pg.font.SysFont("hgp創英角ポップ体",100)
        self.countdown = 3
        self.img1 = self.moji.render(f"{self.countdown}",0,(0,0,255))
        self.cx = WIDTH/2
        self.cy = HEIGHT/2

    def update(self, screen: pg.Surface):
        self.img1 = self.moji.render(f"{self.countdown}",0,(0,0,255))
        screen.blit(self.img1,(self.cx,self.cy))
        self.countdown -= 1

def main():
    screen = pg.display.set_mode((WIDTH,HEIGHT))   # 画面の大きさを設定する
    pg.display.set_caption('YBG')   # 画面のタイトルを設定する
    # font = pg.font.Font(FONT_PATH, 50)  #フォントの設定
    screen.fill((255, 213, 84))  #画面を次の色で染める
    you = YOU((WIDTH//2, HEIGHT*2/3))
    patties = pg.sprite.Group()
    countdown = Start_countdown()


    tmr = 0
    clock = pg.time.Clock()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return

        if tmr//50 < 3 and tmr%50==0:
            screen.fill((255, 213, 84))
            countdown.update(screen)

        elif tmr//50 >=3 and tmr//50 <= 34:
            screen.fill((255, 213, 84))
            key_lst = pg.key.get_pressed()
            you.update(key_lst, screen)
            
            if tmr%200 == 0:  # 200フレームに1回，敵機を出現させる
                patties.add(Patty())

            patties.update()
            patties.draw(screen)

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == '__main__':
    pg.init()  #pygameの初期化
    main()