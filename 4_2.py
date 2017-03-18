# -*- coding: utf-8 -*-

# ウィンドウを塗りつぶす

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

    # まだ実行されていない OpenGL の命令を全部実行
    # OpenGLは関数呼び出しで都度実行ではなくある程度命令が溜まったら一気に実行する仕様のため
    # ただしglFlushを呼びすぎると処理が遅くなる
    glFlush()
    return


def init():
    # ウィンドウを塗りつぶす際の色を指定
    # glutInitDisplayModeでRGBAを指定しているので、この場合は青色
    glClearColor(0.0, 0.0, 1.0, 1.0)


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
    # (自作)初期化メソッド
    init()
    # 無限ループでイベントを待つ
    glutMainLoop()


if __name__ == '__main__':
    main()
