
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys
import os


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glFlush()
    return


def init():
    glClearColor(0.0, 0.0, 1.0, 1.0)


def main():
    # GLUT OpenGLの初期化
    glutInit(sys.argv)
    # ディスプレイの表示モードを設定
    # mode に GLUT_RGBA を指定した場合, 色の指定をRGBで行えるようにする
    glutInitDisplayMode(GLUT_RGBA)
    # ファイル名をフォルダ名にしてwindowを生成
    window_id = glutCreateWindow(os.path.basename(__file__))
    # window再描画時に呼び出すメソッドを設定
    glutDisplayFunc(display)
    # 初期化メソッド
    init()
    # 無限ループでイベントを待つ
    glutMainLoop()


if __name__ == '__main__':
    main()
