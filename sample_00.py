
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys

name = 'sample_00'

def display():
    return

def main():
    #GLUT OpenGLの初期化
    glutInit(sys.argv)
    #name文字列でwindowを生成
    window_id = glutCreateWindow(name)
    #window再描画時に呼び出すメソッドを設定
    glutDisplayFunc(display)
    #無限ループでイベントを待つ
    glutMainLoop()

if __name__ == '__main__': main()
