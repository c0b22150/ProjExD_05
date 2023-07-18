#cording:utf-8

import pygame as pg
import sys
import random as rd

from pygame.sprite import AbstractGroup

FONT_PATH = "UDDigiKyokashoN-R.ttc"  #使用するフォント
WIDTH = 1000  #画面の横サイズ
HEIGHT = 700  #画面の縦サイズ

def check_position(X,Y,rct):
    '''
    画像とカーソルが接しているか確認する関数
    引数 : mouseX ,mouseY ,hoge_image_rct
    戻り値 : 
    '''
    if (X>=rct.left) and (X<=rct.right) and (Y>=rct.top) and (Y<=rct.bottom):
        state = 1
    else:
        state = 0
    return state

<<<<<<< HEAD
=======
def check_bound(obj: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内か画面外かを判定し，真理値タプルを返す
    引数 obj：オブジェクト（こうかとん）SurfaceのRect
    戻り値：横方向，縦方向のはみ出し判定結果（画面内：True／画面外：False）
    """
    yoko, tate = True, True
    if obj.left < 0 or WIDTH < obj.right:  # 横方向のはみ出し判定
        yoko = False
    if obj.top < 0 or HEIGHT < obj.bottom:  # 縦方向のはみ出し判定
        tate = False
    return yoko, tate

>>>>>>> eba042e7e2bc049b514a019ce24e202e87f4524b
def fin():
    '''
    ゲームを終了する関数
    引数 , 戻り値 : NULL
    '''
    print("終了")  #終了確認用
    pg.quit()  #pygameの終了
    sys.exit()  #メインプロセスの終了


class YOU(pg.sprite.Sprite):
<<<<<<< HEAD

    delta = {  #押すキーと移動量
        pg.K_d:(+5,0),  
        pg.K_a:(-5,0)      
    }

=======
    '''
    お前君についてのクラス
    '''

    delta = {  #押すキーと移動量
        pg.K_d:(+5,0),  #d_keyを押した時に右に進む
        pg.K_a:(-5,0)  #a_keyを押した時に左に進む
    }


>>>>>>> eba042e7e2bc049b514a019ce24e202e87f4524b
    def __init__(self, xy: tuple[int, int]):
        """
        お前君画像Surfaceを生成する
        引数:お前君画像ファイル名の番号
        """
        super().__init__()
        img0 = pg.transform.rotozoom(pg.image.load(f"ex05/fig/omae/0.png"), 0, 2)  # 左向き
<<<<<<< HEAD
        img = pg.transform.flip(img0, True, False)  # 右向き
        self.imgs = {
            (+5, 0): img,  # 右
            (-5, 0): img0,  # 左
=======
        img1 = pg.transform.flip(img0, True, False)  # 右向き
        self.imgs = {
            (-5, 0): img1,  # 右
            (+5, 0): img0,  # 左
>>>>>>> eba042e7e2bc049b514a019ce24e202e87f4524b
        }
        self.dire = (+5, 0)
        self.image = self.imgs[self.dire]
        self.rct = self.image.get_rect()
        self.rct.center = xy
<<<<<<< HEAD
=======
        self.speed = 1/2

>>>>>>> eba042e7e2bc049b514a019ce24e202e87f4524b

    def update(self, key_lst: list[bool], screen: pg.Surface):
        """
        押下キーに応じてお前君を移動させる
        引数1 key_lst：押下キーの真理値リスト
        引数2 screen：画面Surface
        """
        sum_mv = [0, 0]
        for k, mv in __class__.delta.items():
            if key_lst[k]:
<<<<<<< HEAD
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        self.rct.move_ip(sum_mv)
        screen.blit(self.image, self.rct)

=======
                self.rct.move_ip(+self.speed*mv[0], +self.speed*mv[1])
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        if check_bound(self.rct) != (True, True):
            for k, mv in __class__.delta.items():
                if key_lst[k]:
                    self.rct.move_ip(-self.speed*mv[0], -self.speed*mv[1])
                if key_lst[pg.K_LSHIFT]:
                    self.rct.move_ip(-self.speed*2*mv[0], -self.speed*2*mv[1])    
        self.rct.move_ip(sum_mv)
        screen.blit(self.image, self.rct)

        if not (sum_mv[0] == 0 and sum_mv[1] == 0):
            self.dire = tuple(sum_mv)
            self.image = self.imgs[self.dire]
        screen.blit(self.image, self.rct)


>>>>>>> eba042e7e2bc049b514a019ce24e202e87f4524b

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


class Score:
    #スコアの表示をする
    def __init__(self):
        self.font = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 30)
        self.score = 0 #初期値
        self.img = self.font.render(f"スコア：{self.score}", 0, (0,0,255))
        self.cx = 800 #中心座標
        self.cy = 100
    
    def update(self, score: pg.Surface):
        self.img = self.font.render(f"スコア：{self.score}",0,(0,0,255))#後で見返す
        score.blit(self.img,(self.cx,self.cy))


class Time:
    #制限時間の表示をする
    def __init__(self):
        self.fonts = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 30)
        self.limit = 30
        self.imgs = self.fonts.render(f"時間：{self.limit}", 0, (0,0,255))
        self.tx = 800 #中心座標
        self.ty = 200

    def update(self, time: pg.Surface):
        self.img = self.fonts.render(f"時間：{self.limit}",0,(0,0,255))#後で見返す
        time.blit(self.img,(self.tx,self.ty))

<<<<<<< HEAD
=======
class Start():
    def __init__(self) :
        image_state_0 = 0
        image_state_1 = 0
        image_state_2 = 0
        image_state_3 = 0
        title_image = pg.image.load("ex05/fig/start_display/title.png")
        start_image = pg.image.load(f"ex05/fig/start_display/start_{image_state_0}.png")
        score_image = pg.image.load(f"ex05/fig/start_display/score_{image_state_1}.png")
        playrule_image = pg.image.load(f"ex05/fig/start_display/playrule_{image_state_2}.png")
        setting_image = pg.image.load(f"ex05/fig/start_display/setting_{image_state_3}.png")
        title_image = pg.image.load("ex05/fig/start_display/title.png")
         

>>>>>>> eba042e7e2bc049b514a019ce24e202e87f4524b
def game():
    screen = pg.display.set_mode((WIDTH,HEIGHT))   # 画面の大きさを設定する
    pg.display.set_caption('YBG')   # 画面のタイトルを設定する
    # font = pg.font.Font(FONT_PATH, 50)  #フォントの設定
    screen.fill((255, 213, 84))  #画面を次の色で染める
    you = YOU((WIDTH//2, HEIGHT*4/5))
    patties = pg.sprite.Group()
    time = Time()
    score = Score()


    tmr = 0
    clock = pg.time.Clock()

    while True:
        screen.fill((255, 213, 84))
        for event in pg.event.get():
            if event.type == pg.QUIT: return

        key_lst = pg.key.get_pressed()
        you.update(key_lst, screen)
        
<<<<<<< HEAD
=======
        
>>>>>>> eba042e7e2bc049b514a019ce24e202e87f4524b
        if tmr%200 == 0:  # 200フレームに1回，敵機を出現させる
            patties.add(Patty())

        if tmr%50 ==0:
            time.limit -= 1
            time.update(screen)

        if time.limit < 0:
            return

        patties.update()
        patties.draw(screen)
        score.update(screen)
        time.update(screen)

        pg.display.update()
        tmr += 1
        clock.tick(50)


def end(score:int):
    print()


def main():
<<<<<<< HEAD
    you = YOU((WIDTH//2, HEIGHT*4/5))
    patties = pg.sprite.Group()
=======
>>>>>>> eba042e7e2bc049b514a019ce24e202e87f4524b
    screen = pg.display.set_mode((WIDTH,HEIGHT))   # 画面の大きさを設定する
    pg.display.set_caption('YBG -よくある・バーガー・ゲーム-')   # 画面のタイトルを設定する
    # font = pg.font.Font(FONT_PATH, 50)  #フォントの設定
    screen.fill((255, 213, 84))  #画面を次の色で染める

    #ここからスタート画面
    image_statu_0 = 0
    image_statu_1 = 0
    image_statu_2 = 0
    image_state_3 = 0
    title_image = pg.image.load("ex05/fig/start_display/title.png")
    start_image = pg.image.load(f"ex05/fig/start_display/start_{image_statu_0}.png")
    score_image = pg.image.load(f"ex05/fig/start_display/score_{image_statu_1}.png")
<<<<<<< HEAD
    playrule_image = pg.image.load(f"ex05/fig/start_display/playrule_{image_statu_2}.png")
=======
    playrule_image = pg.image.load(f"ex05/fig/start_display/play_rule_{image_statu_2}.png")
>>>>>>> eba042e7e2bc049b514a019ce24e202e87f4524b
    setting_image = pg.image.load(f"ex05/fig/start_display/setting_{image_state_3}.png")
    title_image = pg.image.load("ex05/fig/start_display/title.png")

    #ゲーム起動時画面　ここから
    title_image_rct = title_image.get_rect()
    title_image_rct.center = WIDTH//2,HEIGHT//12*2
    start_image_rct = start_image.get_rect()
    start_image_rct.center = WIDTH//2,HEIGHT//12*6
    score_image_rct = score_image.get_rect()
    score_image_rct.center = WIDTH//2,HEIGHT//12*8
    playrule_image_rct = playrule_image.get_rect()
    playrule_image_rct.center = WIDTH//2,HEIGHT//12*10
    setting_image_rct = setting_image.get_rect()
    setting_image_rct.center = 50 , 40
    title_image_rct = title_image.get_rect()
    title_image_rct.center = WIDTH//2,HEIGHT//12*3
    screen.blit(title_image,title_image_rct)
    #ゲーム起動時画面　ここまで

    while True:
        pg.display.update()
        mouseX, mouseY = pg.mouse.get_pos()  #マウスの位置を取得
<<<<<<< HEAD
        
=======

>>>>>>> eba042e7e2bc049b514a019ce24e202e87f4524b
        for event in pg.event.get():
            if event.type == pg.QUIT:
                fin()            
            if event.type == pg.KEYDOWN:  # キーを押したとき
                if event.key == pg.K_ESCAPE:
                    fin()
        if(image_statu_0 == 1):
            if event.type == pg.MOUSEBUTTONDOWN:
                print("ゲームスタート！")
                game()
                end()
                screen = pg.display.set_mode((WIDTH,HEIGHT))
                screen.fill((255, 213, 84))  #画面を次の色で染める 
                screen.blit(title_image,title_image_rct)
        if(image_statu_1 == 1):
            if event.type == pg.MOUSEBUTTONDOWN:
                print("スコア！")
<<<<<<< HEAD
                score()
=======

>>>>>>> eba042e7e2bc049b514a019ce24e202e87f4524b
                screen = pg.display.set_mode((WIDTH,HEIGHT))
                screen.fill((255, 213, 84))  #画面を次の色で染める 
                screen.blit(title_image,title_image_rct)
        if(image_statu_2 == 1):
            if event.type == pg.MOUSEBUTTONDOWN:
                print("説明画面！")
<<<<<<< HEAD
                rule()
                screen = pg.display.set_mode((WIDTH,HEIGHT))
                screen.fill((255, 213, 84))  #画面を次の色で染める 
                screen.blit(title_image,title_image_rct)
        
        for patty in pg.sprite.groupcollide( patties,you, True, False):
            print("当たった")
            
=======

                screen = pg.display.set_mode((WIDTH,HEIGHT))
                screen.fill((255, 213, 84))  #画面を次の色で染める 
                screen.blit(title_image,title_image_rct)
>>>>>>> eba042e7e2bc049b514a019ce24e202e87f4524b

        image_statu_0 = check_position(mouseX,mouseY,start_image_rct)    
        image_statu_1 = check_position(mouseX,mouseY,score_image_rct)
        image_statu_2 = check_position(mouseX,mouseY,playrule_image_rct)
        image_state_3 = check_position(mouseX,mouseY,setting_image_rct)

        start_image = pg.image.load(f"ex05/fig/start_display/start_{image_statu_0}.png")
        score_image = pg.image.load(f"ex05/fig/start_display/score_{image_statu_1}.png")
<<<<<<< HEAD
        playrule_image = pg.image.load(f"ex05/fig/start_display/playrule_{image_statu_2}.png")
=======
        playrule_image = pg.image.load(f"ex05/fig/start_display/play_rule_{image_statu_2}.png")
>>>>>>> eba042e7e2bc049b514a019ce24e202e87f4524b
        setting_image = pg.image.load(f"ex05/fig/start_display/setting_{image_state_3}.png")
        screen.blit(start_image,start_image_rct)
        screen.blit(score_image,score_image_rct)
        screen.blit(playrule_image,playrule_image_rct)
        screen.blit(setting_image,setting_image_rct)

        pg.display.update()


if __name__ == '__main__':
    pg.init()  #pygameの初期化
    main()