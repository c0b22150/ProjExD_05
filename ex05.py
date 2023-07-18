#cording:utf-8

import pygame as pg
import sys
import random as rd
import time

from pygame.sprite import AbstractGroup

FONT_PATH = "ex05/UDDigiKyokashoN-R.ttc"  #使用するフォント
WIDTH = 1000  #画面の横サイズ
HEIGHT = 700  #画面の縦サイズ
RECORD_PATH = "ex05/record.txt"

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

def check_bound(obj: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内か画面外かを判定し，真理値タプルを返す
    引数 obj：オブジェクト（こうかとん）SurfaceのRect
    戻り値：横方向，縦方向のはみ出し判定結果（画面内：True／画面外：False）
    """
    yoko, tate = True, True
    if obj.left < 2.5 or 797.5 < obj.right:  # 横方向のはみ出し判定
        yoko = False
    if obj.top < 0 or HEIGHT < obj.bottom:  # 縦方向のはみ出し判定
        tate = False
    return yoko, tate

def fin():
    '''
    ゲームを終了する関数
    引数 , 戻り値 : NULL
    '''
    print("終了")  #終了確認用
    pg.quit()  #pygameの終了
    sys.exit()  #メインプロセスの終了


class YOU(pg.sprite.Sprite):
    '''
    お前君についてのクラス
    '''
    delta = {  #押すキーと移動量
        pg.K_d:(+5,0),  #d_keyを押した時に右に進む
        pg.K_a:(-5,0)  #a_keyを押した時に左に進む
    }

    def __init__(self, xy: tuple[int, int]):
        """
        お前君画像Surfaceを生成する
        引数:お前君画像ファイル名の番号
        """
        super().__init__()
        img0 = pg.transform.rotozoom(pg.image.load(f"ex05/fig/omae/0.png"), 0, 2)  # 左向き
        img1 = pg.transform.flip(img0, True, False)  # 右向き
        self.imgs = {
            (-5, 0): img1,  # 右
            (+5, 0): img0,  # 左
        }
        self.dire = (+5, 0)
        self.image = self.imgs[self.dire]
        self.rect = self.image.get_rect()
        self.rect.center = xy
        self.speed = 1/2

    def update(self, key_lst: list[bool], screen: pg.Surface):
        """
        押下キーに応じてお前君を移動させる
        引数1 key_lst：押下キーの真理値リスト
        引数2 screen：画面Surface
        """
        sum_mv = [0, 0]
        for k, mv in __class__.delta.items():
            if key_lst[k]:
                self.rect.move_ip(+self.speed*mv[0], +self.speed*mv[1])
                sum_mv[0] += mv[0]
        if check_bound(self.rect) != (True, True):
            for k, mv in __class__.delta.items():
                if key_lst[k]: 
                    self.rect.move_ip(-self.speed*mv[0], -self.speed*mv[1]) 
                    sum_mv[0] -= mv[0]
        self.rect.move_ip(sum_mv)
        print(-self.speed*mv[0],-self.speed*mv[1])
        screen.blit(self.image, self.rect)

        if not (sum_mv[0] == 0 and sum_mv[1] == 0):
            self.dire = tuple(sum_mv)
            self.image = self.imgs[self.dire]
        screen.blit(self.image, self.rect)


class Patty(pg.sprite.Sprite):
    imgs = [pg.image.load(f"ex05/fig/patty/{i}.png") for i in range(0, 2)]

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = rd.choice(__class__.imgs)
        self.rect = self.image.get_rect()
        self.rect.center = rd.randint(0, WIDTH), 0
        self.vy = +3


    def update(self):
        """
        敵機を速度ベクトルself.vyに基づき移動（降下）させる
        ランダムに決めた停止位置_boundまで降下したら，_stateを停止状態に変更する
        引数 screen：画面Surface
        """
        self.rect.centery += self.vy

class Game():
    def __init__(self):
        '''
        初期化を行う関数
        引数 self:Game自身
        背景画像の読み込みとインスタンス化
        '''
        super().__init__
        self.time = Time()  #Timeクラスをインスタンス化
        self.score = Score()  #Scoreクラスをインスタンス化
        self.bg_img = pg.image.load("ex05/fig/game/bg_1.png")  #背景画像を読み込む
        self.you = YOU((700//2, HEIGHT*4/5))  #お前君の初期位置を設定

    def game(self):
        screen = pg.display.set_mode((WIDTH,HEIGHT))
        patties = pg.sprite.Group()
        cheese = pg.sprite.Group()
        tomatoes = pg.sprite.Group()
        lettuces = pg.sprite.Group()
        counter = 0
        tmr = 0  #タイマー
        clock = pg.time.Clock()  

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT: return
            if self.time.limit == 0:
                return self.score.score
            
            #パティに関する部分
            if tmr%100 == 0:  # 100フレームに1回,パティを出現させる
                patties.add(Patty())
            if pg.sprite.spritecollide(self.you, patties, True):
                self.score.score_up(5)
                self.score.update(screen)
                counter +=5
            #ここまで
            #チーズに関する部分
            if tmr%200 == 0:  # 100フレームに1回,チーズを出現させる
                cheese.add(Cheese())
            if pg.sprite.spritecollide(self.you, cheese, True):
                self.score.score_up(15)
                self.score.update(screen)
                counter +=15
            #ここまで
            #トマトに関する部分
            if tmr%150 == 50:  #100フレームに1回,トマトを出現させる
                tomatoes.add(Tomato())
            if pg.sprite.spritecollide(self.you, tomatoes, True):
                self.score.score_up(10)
                self.score.update(screen)
                counter +=10
            #ここまで
            #レタスに関する部分
            if tmr%150 == 100:  #100フレームに1回,レタスを出現させる
                lettuces.add(Lettuce())
            if pg.sprite.spritecollide(self.you, lettuces, True):
                self.score.score_up(12)
                self.score.update(screen)
                counter +=12
            #ここまで

            if tmr%50 ==0:  #50フレーム毎に実行
                self.time.limit -= 1  #制限時間を減らす
                self.time.update(screen)  #制限時間をアップデート
                self.score.update(screen)  #スコアをアップデート

            if counter >=500:  #カウンター(スコア)が500貯まったら実行
                self.time.limit += 5  #制限時間を伸ばす
                counter = 0  #カウンターリセット

            screen.fill((0,0,0))
            screen.blit(self.bg_img,[0,0])
            key_lst = pg.key.get_pressed()
            self.you.update(key_lst,screen)
            patties.update()
            patties.draw(screen)
            cheese.update()
            cheese.draw(screen)
            tomatoes.update()
            tomatoes.draw(screen)
            lettuces.update()
            lettuces.draw(screen)
            self.score.update(screen)
            self.time.update(screen)

            pg.display.update()
            tmr += 1
            clock.tick(50)


class Score_display():
    def __init__(self):
        super().__init__
        self.font = pg.font.Font(FONT_PATH, 48)  #使用するフォントの設定
        self.record_1 = "-----"  #
        self.record_2 = "-----"  #
        self.record_3 = "-----"  #
        self.record_4 = "-----"  #
        self.record_5 = "-----"  #
        self.bg_img = pg.image.load("ex05/fig/score/bg_0.png")  #背景画像を読み込む
        self.score_0 = pg.image.load("ex05/fig/score/0.png")
        self.score_1 = pg.image.load("ex05/fig/score/1.png")
        self.score_2 = pg.image.load("ex05/fig/score/2.png")
        self.record_1_img = self.font.render(f"1：　{self.record_1}", True, (0, 0, 0))
        self.record_2_img = self.font.render(f"2：　{self.record_2}", True, (0, 0, 0))
        self.record_3_img = self.font.render(f"3：　{self.record_3}", True, (0, 0, 0))
        self.record_4_img = self.font.render(f"4：　{self.record_4}", True, (0, 0, 0))
        self.record_5_img = self.font.render(f"5：　{self.record_5}", True, (0, 0, 0))
        self.rect_0 = self.score_0.get_rect()
        self.rect_1 = self.score_1.get_rect()
        self.rect_2 = self.score_2.get_rect()
        self.record_1_rect = self.record_1_img.get_rect()
        self.record_2_rect = self.record_2_img.get_rect()
        self.record_3_rect = self.record_3_img.get_rect()
        self.record_4_rect = self.record_4_img.get_rect()
        self.record_5_rect = self.record_5_img.get_rect()
        self.rect_0.center = WIDTH//2 , HEIGHT//2
        self.rect_1.center = WIDTH//2 , HEIGHT//8
        self.rect_2.center = WIDTH//11 , HEIGHT//50*47
        self.record_1_rect = WIDTH//3 , HEIGHT//8*2
        self.record_2_rect = WIDTH//3 , HEIGHT//8*3
        self.record_3_rect = WIDTH//3 , HEIGHT//8*4
        self.record_4_rect = WIDTH//3 , HEIGHT//8*5
        self.record_5_rect = WIDTH//3 , HEIGHT//8*6

    def f_read(self):
        with open(RECORD_PATH) as f:
            l_strip = [s.rstrip() for s in f.readlines()]
            memo = sorted(l_strip,reverse=True)
        self.record_1 = memo[0]
        self.record_2 = memo[1]
        self.record_3 = memo[2]
        self.record_4 = memo[3]
        self.record_5 = memo[4]
        self.record_1_img = self.font.render(f"1：　{self.record_1}", True, (0, 0, 0))
        self.record_2_img = self.font.render(f"2：　{self.record_2}", True, (0, 0, 0))
        self.record_3_img = self.font.render(f"3：　{self.record_3}", True, (0, 0, 0))
        self.record_4_img = self.font.render(f"4：　{self.record_4}", True, (0, 0, 0))
        self.record_5_img = self.font.render(f"5：　{self.record_5}", True, (0, 0, 0))

    def f_sort(self,score):
        with open(RECORD_PATH) as f:
            l_strip = [s.rstrip() for s in f.readlines()]
            memo = sorted(l_strip,reverse=True)
        if (memo[4] < str(score) and memo[4] != "-----") or (memo[4] == "-----"):
            memo[4] = str(score)
            memo = sorted(memo,reverse=True)
        with open(RECORD_PATH,"w") as f:
            for i in memo:
                f.write("%s\n"%i)

    def update(self,screen:pg.Surface):
        self.f_read()
        screen.blit(self.bg_img,[0,0])
        screen.blit(self.score_0,self.rect_0)
        screen.blit(self.score_1,self.rect_1)
        screen.blit(self.score_2,self.rect_2)
        screen.blit(self.record_1_img,self.record_1_rect)
        screen.blit(self.record_2_img,self.record_2_rect)
        screen.blit(self.record_3_img,self.record_3_rect)
        screen.blit(self.record_4_img,self.record_4_rect)
        screen.blit(self.record_5_img,self.record_5_rect)
        
    def display(self):
        screen = pg.display.set_mode((WIDTH,HEIGHT))   # 画面の大きさを設定する
        self.font = pg.font.Font(FONT_PATH, 48)  #使用するフォントの設定
        self.f_read()

        while True:
            mouseX, mouseY = pg.mouse.get_pos()  #マウスの位置を取得
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:  #閉じるボタンを押されたら終了
                    if event.key == pg.K_ESCAPE:return
                if(check_position(mouseX,mouseY,self.rect_2) == 1):
                    if event.type == pg.MOUSEBUTTONDOWN:return

            self.update(screen)
            pg.display.update()


def main():
    screen = pg.display.set_mode((WIDTH,HEIGHT))   # 画面の大きさを設定する
    pg.display.set_caption('YBG -よくある・バーガー・ゲーム-')   # 画面のタイトルを設定する
    # font = pg.font.Font(FONT_PATH, 50)  #フォントの設定
    game = Game()
    score_dis = Score_display()
    finish = Finish()  #Finishクラスのインスタンス化
    end = End()

    #ここからスタート画面
    image_state_0 = 0
    image_state_1 = 0
    image_state_2 = 0
    bg_image = pg.image.load("ex05/fig/start_display/bg_0.png")
    start_image = pg.image.load(f"ex05/fig/start_display/start_{image_state_0}.png")
    score_image = pg.image.load(f"ex05/fig/start_display/score_{image_state_1}.png")
    playrule_image = pg.image.load(f"ex05/fig/start_display/play_rule_{image_state_2}.png")
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
    #ゲーム起動時画面　ここまで

    screen.blit(bg_image,[0,0])
    screen.blit(title_image,title_image_rct)

    while True:
        pg.display.update()
        mouseX, mouseY = pg.mouse.get_pos()  #マウスの位置を取得

        for event in pg.event.get():
            if event.type == pg.QUIT:
                end.end()
                fin()            
            if event.type == pg.KEYDOWN:  # キーを押したとき
                if event.key == pg.K_ESCAPE:
                    end.end()
                    fin()
        if(image_state_0 == 1):
            if event.type == pg.MOUSEBUTTONDOWN:
                print("ゲームスタート！")
                game.__init__()
                score = game.game()
                finish.Evaluation_display(score)
                score_dis.f_sort(score)
                screen = pg.display.set_mode((WIDTH,HEIGHT))
                screen.blit(bg_image,[0,0])
                screen.blit(title_image,title_image_rct)
        if(image_state_1 == 1):
            if event.type == pg.MOUSEBUTTONDOWN:
                print("スコア！")
                score_dis.display()
                screen = pg.display.set_mode((WIDTH,HEIGHT))
                screen.blit(bg_image,[0,0])
                screen.blit(title_image,title_image_rct)
        if(image_state_2 == 1):
            if event.type == pg.MOUSEBUTTONDOWN:
                print("説明画面！")
                # rule()
                screen = pg.display.set_mode((WIDTH,HEIGHT))
                screen.blit(bg_image,[0,0])
                screen.blit(title_image,title_image_rct)

        image_state_0 = check_position(mouseX,mouseY,start_image_rct)    
        image_state_1 = check_position(mouseX,mouseY,score_image_rct)
        image_state_2 = check_position(mouseX,mouseY,playrule_image_rct)

        start_image = pg.image.load(f"ex05/fig/start_display/start_{image_state_0}.png")
        score_image = pg.image.load(f"ex05/fig/start_display/score_{image_state_1}.png")
        playrule_image = pg.image.load(f"ex05/fig/start_display/play_rule_{image_state_2}.png")

        screen.blit(start_image,start_image_rct)
        screen.blit(score_image,score_image_rct)
        screen.blit(playrule_image,playrule_image_rct)

        pg.display.update()

if __name__ == '__main__':
    pg.init()  #pygameの初期化
    main()