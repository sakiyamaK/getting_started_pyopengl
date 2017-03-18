# -*- coding: utf-8 -*-

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys
import os

def display():
    return

def main():
    #GLUT OpenGLの初期化
    glutInit(sys.argv)
    #ファイル名をフォルダ名にしてwindowを生成
    window_id = glutCreateWindow(os.path.basename(__file__))
    #window再描画時に呼び出すメソッドを設定
    glutDisplayFunc(display)
    #無限ループでイベントを待つ
    glutMainLoop()

if __name__ == '__main__': main()
