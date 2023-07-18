#cording:utf-8

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
        img0 = pg.transform.rotozoom(pg.image.load(f"ex05/ex05/fig/omae/0.png"), 0, 2)  # 左向き
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
    imgs = [pg.image.load(f"ex05/ex05/fig/patty/{i}.png") for i in range(0, 2)]

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

    """
    皿に積まれる具材を表すクラス
    """
    #colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

    def __init__(self,you:YOU,gus:Patty ):
        """
        引数1 you：YOU
        引数2 gus：落ちてくる具材の民
        """
        super().__init__()
        self.image = pg.Surface(())
        pg.draw.circle(self.image, color, (rad, rad), rad)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()

        # 具材の高さをリストに
        self.Surface.get_width()  
    

        self.rect.centerx = emy.rect.centerx
        self.rect.centery = emy.rect.centery+emy.rect.height/2
        self.speed = 6

    def update(self):
        """
        具材の民とYOUの座標を連結される
        """
        self.rect.move_ip(+self.speed*self.vx, +self.speed*self.vy)
        if check_bound(self.rect) != (True, True):
            self.kill()


def main():
    screen = pg.display.set_mode((WIDTH,HEIGHT))   # 画面の大きさを設定する
    pg.display.set_caption('YBG')   # 画面のタイトルを設定する
    # font = pg.font.Font(FONT_PATH, 50)  #フォントの設定
    screen.fill((255, 213, 84))  #画面を次の色で染める
    you = YOU((WIDTH//2, HEIGHT*2/3))
    patties = pg.sprite.Group()


    tmr = 0
    clock = pg.time.Clock()

    while True:
        screen.fill((255, 213, 84))
        for event in pg.event.get():
            if event.type == pg.QUIT: return

        key_lst = pg.key.get_pressed()
        you.update(key_lst, screen)
        
        #人にあったたら物を積む
        #groupcollideが当たった時の判定をしてくれる
        #pattyとyouを消して新しいyou（pattyを持っている）に変換
        for patty in pg.sprite.groupcollide(you, patties, True,True).keys():
            you.change_img(YOU(you[patty], screen))  # pattyを持ったyouに変換
            score.score_up(10)  # 10点アップ（特定の点数）
            
        
            
        
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