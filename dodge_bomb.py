import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {  # 移動量辞書
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, 5),
    pg.K_RIGHT: (5, 0),
    pg.K_LEFT: (-5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectかばくだんRect
    戻り値：横方向、縦方向の画面内判定結果
    画面内ならTrue、画面外ならFalse
    """
    yoko, tate = True, True  # 初期値:画面内
    if (rct.left < 0) or (WIDTH < rct.right):
        yoko = False
    if (rct.top < 0) or (HEIGHT < rct.bottom):
        tate = False
    return yoko, tate  # 横方向、縦方向の画面内判定結果を返す


def gameover(screen: pg.Surface) -> None:
    """
    引数：画面
    戻り値：ゲームオーバー時の画面
    """
    go_img = pg.Surface((WIDTH, HEIGHT))  # ゲームオーバー用背景の準備
    pg.draw.rect(go_img, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
    go_img.set_alpha(180)
    go_rct = go_img.get_rect()
    go_rct.center = ((WIDTH//2, HEIGHT//2))
    go_fnt = pg.font.Font(None,80)  # ゲームオーバーの文字列の生成
    txt = go_fnt.render("Game Over", 
                        True, (255, 255, 255))
    txt_rct = txt.get_rect()
    txt_rct.center = (WIDTH//2, HEIGHT//2)
    kk_go_img = pg.image.load("fig/8.png")  # 泣いているこうかとん画像の生成
    kk_go_rct_1 = kk_go_img.get_rect()
    kk_go_rct_1.center = ((WIDTH//2-190, HEIGHT//2))
    kk_go_rct_2 = kk_go_img.get_rect()
    kk_go_rct_2.center = ((WIDTH//2+190, HEIGHT//2))

    screen.blit(go_img, go_rct)  # ゲームオーバー画面の呼び出し
    screen.blit(txt, txt_rct)
    screen.blit(kk_go_img,kk_go_rct_1)
    screen.blit(kk_go_img,kk_go_rct_2)
    pg.display.update()
    time.sleep(5)


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    引数：なし
    戻り値：サイズの異なる爆弾Surfaceを要素としたリストと加速度リスト
    """
    bb_imgs = []
    bb_accs = [a for a in range(1,11)]  # 加速度リスト
    for r in range(1,11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)  # 爆弾のサイズのリストを生成
        bb_img.set_colorkey((0,0,0))
        bb_imgs.append(bb_img)
    return bb_imgs, bb_accs


# def get_kk_img(sum_mv: tuple[int, int]) -> pg.Surface:
#     """
#     引数：こうかとんの進行方向
#     戻り値：前進するこうかとん画像
#     """
#     kk1 = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0)
#     kk2 = pg.transform.rotozoom(pg.image.load("fig/3.png"), -45, 0)
#     kk3 = pg.transform.rotozoom(pg.image.load("fig/3.png"), 90, 0)
#     kk4 = pg.transform.rotozoom(pg.image.load("fig/3.png"), 45, 0)
#     kk5 = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0)
#     kk6 = pg.transform.rotozoom(pg.image.load("fig/3.png"), -45, 0)
#     kk7 = pg.transform.rotozoom(pg.image.load("fig/3.png"), -90, 0)
#     kk8 = pg.transform.rotozoom(pg.image.load("fig/3.png"), 45, 0)
    
#     muki = {
#         (0, 0): kk1,
#         (-5, 0): kk1,
#         (-5, -5):kk2,
#         (0, -5): kk3,
#         (5, -5): kk4,
#         (5, 0): kk5,
#         (5, 5): kk6,
#         (0, 5): kk7,
#         (-5, 5): kk8,
#     }
    
#     return muki[sum_mv]
        

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20))  # 空のsurfaceを作る(爆弾用)
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0,0,0))
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)  # 横座標用の乱数
    bb_rct.centery = random.randint(0, HEIGHT)  # 縦座標用の乱数
    vx = +5
    vy = +5

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return

        if kk_rct.colliderect(bb_rct):  # こうかとんRectと爆弾Rectの衝突判定
            gameover(screen)
            return

        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]

        # kk_img = get_kk_img((0,0))  # 飛ぶ方向に従って向きを変える
        # kk_img = get_kk_img(tuple(sum_mv))

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])  # 移動をなかったことにする
        screen.blit(kk_img, kk_rct)
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 横方向にはみ出ていたら
            vx *= -1
        if not tate:  # 縦方向にはみ出ていたら
            vy *= -1
        screen.blit(bb_img, bb_rct)

        bb_imgs, bb_accs = init_bb_imgs()  # 時間経過で爆弾拡大＆加速
        avx = vx*bb_accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]
        bb_rct.move_ip(avx,vy)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
