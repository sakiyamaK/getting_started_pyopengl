# -*- coding: utf-8 -*-


# 画像の読み込み

import numpy as np
import sys
import time
from PIL import Image
import OpenGL
OpenGL.ERROR_ON_COPY = True
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from OpenGL.GL.shaders import *

DEF_V_SHADER_FILE_NAME = "shader.vtx"
DEF_F_SHADER_FILE_NAME = "shader.frg"


def compile_shader(file_path, shaderType):
    #シェーダファイルの読み込み
    source = '\n'.join(open(os.path.dirname(__file__) + "/" + file_path, 'r').readlines())

    #シェーダの種類を指定して空のシェーダオブジェクトを生成
    # GL_VERTEX_SHADER, # GL_FRAGMENT_SHADER
    shader = glCreateShader(shaderType)
    #シェーダオブジェクトとシェーダソースを結びつける
    glShaderSource(shader, source)
    #シェーダオブジェクトをコンパイル
    glCompileShader(shader)

    #シェーダオブジェクトのInfoログを取得
    log = glGetShaderInfoLog(shader)
    if log : print('Shader: ' + str(log))

    #シェーダオブジェクトについて第2引数で指定したパラメータの状態を取得
    #GL_COMPILE_STATUSならコンパイルの結果を取得
    compiled = glGetShaderiv(shader , GL_COMPILE_STATUS)
    if compiled == GL_FALSE :
        if(shaderType == GL_VERTEX_SHADER):
            print("Compile error in vertex shader.")
        else:
            print("Compile error in fragment shader.")
        exit(1)

    return shader


def build_program(vertexShader=None, fragmentShader=None):

    #シェーダプログラムオブジェクトを生成
    program = glCreateProgram()

    #バーテックスシェーダオブジェクト,フラグメントシェーダオブジェクトがあるなら関連つける
    if vertexShader:
        glAttachShader(program, vertexShader)
    if fragmentShader:
        glAttachShader(program, fragmentShader)

    #このプログラムオブジェクトが実行可能か調べる
    glValidateProgram(program)

    #関連つけられたオブジェクトたちをリンク
    glLinkProgram(program)

    #リンクも終わったのでオブジェクトを削除
    if vertexShader:
        glDeleteShader(vertexShader)
    if fragmentShader:
        glDeleteShader(fragmentShader)

    return program


def set_value_to_fragment(program, location_name, value_type, value, value_support=None):
    if value_type is "int":
        glUniform1i(glGetUniformLocation(program, location_name), value)
    elif value_type is "float":
        glUniform1f(glGetUniformLocation(program, location_name), value)


def set_value_to_vertex(program, location_name, value_type, value, value_support=None):
    if value_type is "array":
        vertex = value
        vertex_component = value_support
        loc = glGetAttribLocation(program, location_name)
        glVertexAttribPointer(loc,
                              vertex_component,
                              GL_FLOAT,
                              GL_FALSE,
                              vertex_component* 4,
                              np.array(vertex, np.float32))
        glEnableVertexAttribArray(loc)


def read_texture(texture_image, texture_number=GL_TEXTURE0):
    #テクスチャオブジェクト/もしくはその配列を生成
    texture_id = glGenTextures(1)

    #画像（この場合はテクスチャ）の型をGPUに伝える
    #第１引数がGL_UNPACK_ALIGNMENTなら１画素が何バイトか伝える
    #画像がRGBの3バイトなら第２引数に(なぜか３じゃなく)1
    #画像がRGBAの4バイトなら第２引数に4
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

    #テクスチャユニットの指定
    glActiveTexture(texture_number)

    # 第１引数のtargetに対して第２引数のテクスチャオブジェクトを結合します．
    # テクスチャオブジェクトは，テクスチャ名に対して最初にこの呼び出しが行われたときに生成されます．
    # これ以降，テクスチャに対する設定は texture に指定したテクスチャオブジェクトに対して行われます．
    glBindTexture(GL_TEXTURE_2D, texture_id)

    # 実際に画素データを転送
    if texture_image.mode == 'RGB':
        glTexImage2D( GL_TEXTURE_2D,
                      0,
                      4,
                      texture_image.size[0],
                      texture_image.size[1],
                      0,
                      GL_RGB,
                      GL_UNSIGNED_BYTE,
                      texture_image.tobytes() )
    else:
        glTexImage2D( GL_TEXTURE_2D,
                      0,
                      4,
                      texture_image.size[0],
                      texture_image.size[1],
                      0,
                      GL_RGBA,
                      GL_UNSIGNED_BYTE,
                      texture_image.tobytes() )

    #テクスチャが拡大縮小された時の設定
    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR )
    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR )
    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE )
    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE )


def init_gl( vertex_shade_file, fragment_shader_file, texture_image):
    glClearColor(0.0, 0.0, 0.0, 0.0)

    texture_number = 0

    read_texture(texture_image, GL_TEXTURE0 + texture_number)

    program = build_program(
        compile_shader(vertex_shade_file, GL_VERTEX_SHADER),
        compile_shader(fragment_shader_file, GL_FRAGMENT_SHADER),
    )

    glUseProgram(program)

    # GPUに値を転送していく

    #頂点シェーダに転送
    position_vertices = [ -1.0, 1.0,  #左上
                          -1.0, -1.0,  #左下
                           1.0, -1.0,  #右下
                           1.0, 1.0,  #右上
                         ]
    set_value_to_vertex(program, "a_position", "array", position_vertices, 2)

    # texture_vertices = [ 0.0, 0.0, #左上
    #                      0.0, 1.0, #左下
    #                      1.0, 1.0, #右下
    #                      1.0, 0.0, #右上
    #                      ]
    texture_vertices = [ 0.0, 0.0, #左上
                         0.0, 1.0, #左下
                         1.0, 1.0, #右下
                         1.0, 0.0, #右上
                         ]
    set_value_to_vertex(program, "a_texCoord", "array", texture_vertices , 2)

    #フラグメントシェーダに転送

    #テクスチャユニットの番号を指定してs_textureに割り当てる 今回ならGL_TEXTURE0に画像を用意してるので0
    set_value_to_fragment(program, "inputImageTexture", "int", texture_number, None)

    set_value_to_fragment(program, "texture_width", "float", float(texture_image.size[0]), None)
    set_value_to_fragment(program, "texture_height", "float", float(texture_image.size[1]), None)



#リサイズ後のwindowのresize_wとresize_hが引数に渡される
def ReSizeGLScene(Width, Height):
    glViewport(0, 0, Width, Height)

# The main drawing function.
def DrawGLScene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glEnable(GL_TEXTURE_2D)

    global indices
    indices = [ 0, 1, 2, 0, 2, 3 ]

    # glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
    glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_SHORT, np.array(indices, np.uint16))

    glDisable(GL_TEXTURE_2D)

    glutSwapBuffers()


def keyPressed(*args):
    # If escape is pressed, kill everything.
    if args[0] == '\x1b':
        sys.exit()

def usage():
    print("usage:%s texture_file" % sys.argv[ 0 ])


def main():
    try:
        vertex_shader_file = DEF_V_SHADER_FILE_NAME
        fragment_shader_file = DEF_F_SHADER_FILE_NAME
        texture_file = sys.argv[ 1 ]
    except IndexError:
        usage()
        sys.exit( -1 )

    w_w = 640*2
    w_h = 360*2 #int(w_w * 16 / 9)
    # ディスプレイの初期位置と大きさを設定
    glutInitWindowPosition(800, 50)
    glutInitWindowSize(w_w, w_h)

    texture_image = Image.open( texture_file )
    print(texture_image.mode)
    assert texture_image.mode == 'RGBA' or texture_image.mode == 'RGB'

    glutInit(sys.argv)

    if texture_image.mode == 'RGBA':
        glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
    else:
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

    # window_width,window_height = texture_image.size
    # glutInitWindowSize( window_width, window_height )

    # the window starts at the upper left corner of the screen
    # glutInitWindowPosition(0, 0)

    glutCreateWindow( sys.argv[ 0 ] )

    glutDisplayFunc(DrawGLScene)

    # Uncomment this line to get full screen.
    #glutFullScreen()

    # When we are doing nothing, redraw the scene.
    glutIdleFunc(DrawGLScene)

    # Register the function called when our window is resized.
    glutReshapeFunc(ReSizeGLScene)

    # Register the function called when the keyboard is pressed.
    glutKeyboardFunc(keyPressed)

    # Initialize our window.
    init_gl(vertex_shader_file, fragment_shader_file, texture_image)

    # Start Event Processing Engine
    glutMainLoop()



if __name__ == '__main__':
    main()
