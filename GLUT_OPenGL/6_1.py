# -*- coding: utf-8 -*-

# 座標軸とビューポート

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys
import os


def display():
    # ウィンドウを塗りつぶす 0.0~1.0を指定
    # 引数には塗りつぶすバッファを指定
    # バッファの種類は下記
    # GL_COLOR_BUFFER_BIT
    # GL_DEPTH_BUFFER_BIT
    # GL_ACCUM_BUFFER_BIT
    # GL_STENCIL_BUFFER_BIT
    glClear(GL_COLOR_BUFFER_BIT)

    # glBegin()〜glEnd()の間でコマンドを指定して図形を描く
    # glBegin()の引数には描画する図形のタイプを指定
    # このタイプ次第で処理速度などが決まる
    glBegin(GL_POLYGON)

    # 図形の各頂点の座標値を設定する関数を置く
    # (-0.9, -0.9), (0.9, -0.9), (0.9, 0.9), (-0.9, 0.9)
    # の順に線を引く
    # 座標系は-1.0 ~ 1.0に正規化されている

    glColor3d(1.0, 0.0, 0.0)
    glVertex2d(-0.9, -0.9)

    glColor3d(0.0, 1.0, 0.0)
    glVertex2d(0.9, -0.9)

    glColor3d(0.0, 0.0, 1.0)
    glVertex2d(0.9, 0.9)

    glColor3d(1.0, 1.0, 0.0)
    glVertex2d(-0.9, 0.9)

    glEnd()

    # まだ実行されていない OpenGL の命令を全部実行
    # OpenGLは関数呼び出しで都度実行ではなくある程度命令が溜まったら一気に実行する仕様のため
    # ただしglFlushを呼びすぎると処理が遅くなる
    glFlush()


def init():
    # ウィンドウを塗りつぶす際の色を指定
    glClearColor(1.0, 1.0, 1.0, 1.0)


#リサイズ後のwindowのresize_wとresize_hが引数に渡される
def resize(resize_w, resize_h):
    # ビューポートを設定
    # ビューポートとは、開いたウィンドウの中で、実際に描画が行われる領域のこと
    # この場合、ウィンドウ全体をビューポートにする
    # 引数の大きさはデバイス座標なので0.0~1.0ではない
    glViewport(0, 0, resize_w, resize_h)

    # 変換行列を単位行列で初期化
    glLoadIdentity()

    #ワールド座標系を正規化デバイス座標系に平行投影(orthographicprojection: 正射影)する行列を変換行列に乗ずる
    # 引数には左から
    # 表示領域の左端(left)の位置,右端(right)の位置, 下端(bottom)の位置, 上端(top)の位置, 前方面(near)の位置, 後方面(far)の位置を指定.
    # これは, ビューポートに表示される空間の座標軸を設定.
    #  スクリーン上の表示領域をビューポートの大きさに比例させる
    # ワールド座標系の2点(-1, -1), (1, 1)を対角線とする矩形領域を200×200の大きさのウィンドウに表示した時の表示内容の大きさが常に保たれるよう設定
    w_l = -1
    w_r = 1
    w_b = -1
    w_t = 1
    glOrtho(w_l * resize_w / 200.0, w_r * resize_w / 200.0, w_b * resize_h / 200.0, w_t * resize_h / 200.0, -1.0, 1.0)



def main():
    # GLUT OpenGLの初期化
    glutInit(sys.argv)
    # ディスプレイの表示モードを設定
    # mode に GLUT_RGBA を指定した場合, 色の指定をRGBAで行えるようにする
    glutInitDisplayMode(GLUT_RGBA)
    # ファイル名をフォルダ名にしてwindowを生成
    window_id = glutCreateWindow(os.path.basename(__file__))
    # window再描画時に呼び出すメソッドを設定
    glutDisplayFunc(display)
    # ウィンドウがリサイズされたときに呼び出すメソッドを設定
    # 設定されるメソッドの引数にはリサイズ後のウィンドウの幅と高さが渡される
    glutReshapeFunc(resize)
    # (自作)初期化メソッド
    init()
    # 無限ループでイベントを待つ
    glutMainLoop()


if __name__ == '__main__':
    main()
