#cording:utf-8

import pygame as pg
import sys
import random as rd
import time

from pygame.sprite import AbstractGroup

FONT_PATH = "ex05/UDDigiKyokashoN-R.ttc"  #使用するフォント
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


class Finish(pg.sprite.Sprite):
    '''
    ゲーム終了時の評価画面に関するクラス
        evaluation_texts
        def __init__
        def Evaluation
        def update
        def Evaluation_display
    '''
    evaluation_texts = {  #評価画面で出力される単語辞書
            "S0": "シェフの座を譲ろう！",  #Scoreが61以上の時のセリフS0~S9
            "S1": "わしよりも優秀じゃ。",
            "S2": "どこにも行くなよ。",
            "S3": "ワシの若いころを思い出した",
            "S4": "プロフェッショナルとはお前のこと",
            "S5": "今日のお前は輝いてるよ",
            "S6": "すばらC",
            "S7": "愛してるよ。",
            "S8": "ベスト・オブ・クラーク",
            "S9": "お前はこの店の伝説だ。",
            "A0": "スーシェフになれ！",  #Scoreが41~60の時のセリフA0~A9
            "A1": "君には才能を感じる...。",
            "A2": "契約延長！",
            "A3": "時給5円上げてあげる",
            "A4": "普通に結構",
            "A5": "少しは成長してるのね。",
            "A6": "スーシェフになれ！",
            "A7": "やればできるじゃん。",
            "A8": "今日のワシはちょっと優しい",
            "A9": "お前はエリートだ！",
            "B0": "まずまずだな",  #Scoreが21~40の時のセリフB0~B9
            "B1": "これからも励みたまえ。",
            "B2": "日が暮れるまで、反復よことび。",
            "B3": "正直あきれた。",
            "B4": "こちとら遊びじゃないのよ。",
            "B5": "そうじのおばちゃんと交代。",
            "B6": "しばらく反省してこい",
            "B7": "いくつになっても半人前。",
            "B8": "少しは期待に応えておくれよ。",
            "B9": "しばらく研修行ってきて。",
            "C0": "１からやり直せ！",  #Scoreが1~20の時のセリフC0~C9
            "C1": "皿洗いからだ！",
            "C2": "面倒見切れん。",
            "C3": "お前、やる気ないでしょ？",
            "C4": "今月の給料ナシ！",
            "C5": "向こう1週間、タダ働き!",
            "C6": "お前、居眠りしてたでしょ？",
            "C7": "やぁ、うすのろくん。",
            "C8": "サボってた？",
            "C9": "じきゅう100円でいい？",
            "X0": "よゆうでクビ！",  #Scoreが0の時のセリフX0~X9
            "X1": "さっさと荷物をまとめて出ていけ！",
            "X2": "明日からこなくていいよ",
            "X3": "ミジメとはお前のこと",
            "X4": "・・・・・・。",
            "X5": "話にならん。",
            "X6": "問・題・外。",
            "X7": "何しにきたの？",
            "X8": "お前の顔など見たくもない。",
            "X9": "アドバイスのしようがない。"
        }
    
    def __init__(self):
        '''
        Finishの初期化を行う関数
        引数 self:finish自身
        画像の読み込みと画像rectの設定を行う
        '''
        self.font = pg.font.Font(FONT_PATH, 40)  #使用するフォントの設定
        self.evaluation_txt = None  #evaluation_txtを先に定義
        self.you_img = pg.image.load("ex05/fig/evaluation/you_0.png")  #お前君画像のロード
        self.chef_img = pg.image.load("ex05/fig/evaluation/chef_0.png")  #シェフ画像のロード
        self.balloon_img = pg.image.load("ex05/fig/evaluation/balloon.png")   #ふきだし画像のロード
        self.you_rct = self.you_img.get_rect()  #お前君画像のrectを取得
        self.chef_rct = self.chef_img.get_rect()  #シェフ画像のrectを取得
        self.balloon_rct = self.balloon_img.get_rect()  #ふきだし画像のrectを取得
        self.you_rct.center = WIDTH//6 , HEIGHT//50*33  #お前君画像の中心位置を設定
        self.chef_rct.center = WIDTH//6*5 , HEIGHT//50*33  #シェフ画像の中心位置を設定
        self.balloon_rct.center = WIDTH//2 , HEIGHT//4  #ふきだし画像の中心位置を設定

    def Evaluation(self,score:int):
        '''
        スコアの評価に関する関数
        引数 score : ゲームでのスコア
        スコアから評価コメントを選び、評価コメントとスコアのrectを設定する
        '''
        num = str(rd.randint(0,9))  #出力する評価コメントの番号をランダムに選ぶ
        if score == 0:
            self.evaluation_txt = self.evaluation_texts[f"X{num}"]  #スコアがX評価の時のコメントをfin_textに入れる
        elif 0 < score <=20:
            self.evaluation_txt = self.evaluation_texts[f"C{num}"]  #スコアがC評価の時のコメントをfin_textに入れる
        elif 0 < score <=40:
            self.evaluation_txt = self.evaluation_texts[f"B{num}"]  #スコアがB評価の時のコメントをfin_textに入れる
        elif 0 < score <=60:
            self.evaluation_txt = self.evaluation_texts[f"A{num}"]  #スコアがA評価の時のコメントをfin_textに入れる
        elif 100 < score:
            self.evaluation_txt = self.evaluation_texts[f"S{num}"]  #スコアがS評価の時のコメントをfin_textに入れる
        self.evaluation_img = self.font.render(f"{self.evaluation_txt}", True, (0, 0, 0))  #コメント
        self.score_text = self.font.render(f"Score: {score}", True, (0, 0, 0))  #
        self.evaluation_rct = self.evaluation_img.get_rect()  #
        self.score_rct = self.score_text.get_rect()  #
        self.evaluation_rct.center = WIDTH//2,HEIGHT//50*9  #
        self.score_rct.center = WIDTH//2,HEIGHT//10*6  #

    def update(self, screen:pg.Surface):
        screen.blit(self.balloon_img,self.balloon_rct)  #ふきだし画像を転送すtる
        screen.blit(self.evaluation_img, self.evaluation_rct)  #評価コメントを転送する
        screen.blit(self.score_text, self.score_rct)  #スコアを転送する
        screen.blit(self.you_img,self.you_rct)  #お前君画像を転送する
        screen.blit(self.chef_img,self.chef_rct)  #シェフ画像を転送する

    def Evaluation_display(self, score:int):
        screen = pg.display.set_mode((WIDTH,HEIGHT))   # 画面の大きさを設定する
        self.font = pg.font.Font(FONT_PATH, 48)  #使用するフォントの設定
        self.finish = Finish()  #インスタンス化
        self.bg_img = pg.image.load("ex05/fig/evaluation/bg_0.png")
        self.push_key = self.font.render("--Push Any Key--", True, (0, 0, 0))
        self.push_key_rct = self.push_key.get_rect()
        self.push_key_rct.center = WIDTH//2 , HEIGHT//10*8 
        screen.blit(self.bg_img,[0,0])
        self.finish.Evaluation(score)  #
        self.finish.update(screen)
        tmr = 0  #タイマー
        clock = pg.time.Clock()

        while True:
            if tmr//50 > 3:  #評価画面を開いてから4秒以降の時に実行
                for event in pg.event.get():
                    if event.type == pg.QUIT: return  #閉じるボタンが押されたら終了
                    if event.type == pg.KEYDOWN: return  #keyが押されたら終了
                if tmr//50%2 == 0:  #タイマー//50が偶数の時
                    screen.blit(self.bg_img,[0,0])
                    self.finish.update(screen)
                    screen.blit(self.push_key,self.push_key_rct)
                else:  #タイマー//50が奇数の時
                    screen.blit(self.bg_img,[0,0])
                    self.finish.update(screen)
            else:
                for event in pg.event.get():
                    if event.type == pg.QUIT: return

            pg.display.update()
            tmr += 1
            clock.tick(50)


def main():
    screen = pg.display.set_mode((WIDTH,HEIGHT))   # 画面の大きさを設定する
    pg.display.set_caption('YBG')   # 画面のタイトルを設定する
    # font = pg.font.Font(FONT_PATH, 50)  #フォントの設定
    screen.fill((255, 213, 84))  #画面を次の色で染める
    you = YOU((WIDTH//2, HEIGHT*2/3))
    patties = pg.sprite.Group()
    finish = Finish()


    tmr = 0
    clock = pg.time.Clock()

    while True:
        screen.fill((255, 213, 84))
        for event in pg.event.get():
            if event.type == pg.QUIT: return

        key_lst = pg.key.get_pressed()
        you.update(key_lst, screen)
        
        if tmr%200 == 0:  # 200フレームに1回，敵機を出現させる
            patties.add(Patty())

        patties.update()
        patties.draw(screen)

        print(tmr)
        if tmr//50 > 10:
            finish.Evaluation_display(60)
            pg.display.update
            return
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == '__main__':
    pg.init()  #pygameの初期化
    main()