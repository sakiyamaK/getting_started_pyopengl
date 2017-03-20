# -*- coding: utf-8 -*-


# シェーダーの読み込み

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from OpenGL.GL.ARB.shader_objects import *
from OpenGL.GL.ARB.vertex_shader import *
from OpenGL.GL.ARB.fragment_shader import *


DEF_V_SHADER_FILE_NAME = "shader.vtx"
DEF_F_SHADER_FILE_NAME = "shader.frg"

buffer = 0
gl2Program = 0

# 頂点バッファオブジェクトに４頂点分のメモリ領域を確保する
position = [0.9, 0.9, -0.9, 0.9, -0.9, -0.9, 0.9, -0.9]
position_component = 2


def read_shader_source(shader, file):
    print("glShaderSourceARB:", bool(glShaderSourceARB))
    source = '\n'.join(open(os.path.dirname(__file__) + "/" + file, 'r').readlines())
    glShaderSourceARB( shader, source)
    glCompileShaderARB(shader)
    return shader


def display():
    # ウィンドウを塗りつぶす 0.0~1.0を指定
    # 引数には塗りつぶすバッファを指定
    # バッファの種類は下記
    # GL_COLOR_BUFFER_BIT
    # GL_DEPTH_BUFFER_BIT
    # GL_ACCUM_BUFFER_BIT
    # GL_STENCIL_BUFFER_BIT
    glClear(GL_COLOR_BUFFER_BIT)

    #シェーダプログラムを用意
    glUseProgram(gl2Program)

    #indexが0のattribute変数の頂点バッファオブジェクトへの対応を有効にする
    glEnableVertexAttribArray(0)

    #頂点バッファオブジェクトとしてbufferを指定する
    glBindBuffer(GL_ARRAY_BUFFER, buffer)

    # 頂点バッファオブジェクトの場所と書式を指定する
    glVertexAttribPointer(0, position_component, GL_FLOAT, GL_FALSE, 0, None)

    #図形を描く
    glDrawArrays(GL_LINE_LOOP, 0, int(len(position) / position_component))

    # 頂点バッファオブジェクトを解放する
    glBindBuffer(GL_ARRAY_BUFFER, 0)

    #indexが0のattribute変数の頂点バッファオブジェクトへの対応を無効にする
    glDisableVertexAttribArray(0)

    # まだ実行されていない OpenGL の命令を全部実行
    # OpenGLは関数呼び出しで都度実行ではなくある程度命令が溜まったら一気に実行する仕様のため
    # ただしglFlushを呼びすぎると処理が遅くなる
    glFlush()


def init():
    # ウィンドウを塗りつぶす際の色を指定
    glClearColor(1.0, 1.0, 1.0, 1.0)

    #頂点シェーダ,フラグメントシェーダの用意
    vert_shader = glCreateShader(GL_VERTEX_SHADER)
    frag_shader = glCreateShader(GL_FRAGMENT_SHADER)

    # シェーダのソースプログラムの読み込み
    vert_shader = read_shader_source(vert_shader, DEF_V_SHADER_FILE_NAME)
    frag_shader = read_shader_source(frag_shader, DEF_F_SHADER_FILE_NAME)

    # バーテックスシェーダのソースプログラムのコンパイル
    glCompileShader(vert_shader)
    compiled = glGetShaderiv(vert_shader, GL_COMPILE_STATUS)
    log = glGetShaderInfoLog(vert_shader)
    if log : print('Vertex Shader: ' + str(log))
    if compiled == GL_FALSE :
        print("Compile error in vertex shader.")
        exit(1)

    # フラグメントシェーダのソースプログラムのコンパイル
    glCompileShader(frag_shader)
    compiled = glGetShaderiv(frag_shader, GL_COMPILE_STATUS)
    log = glGetShaderInfoLog(frag_shader)
    if log : print('Vertex Shader: ' + str(log))
    if compiled == GL_FALSE :
        print("Compile error in fragment shader.")
        exit(1)

    # プログラムオブジェクトの作成
    global gl2Program
    gl2Program = glCreateProgram()

    # シェーダオブジェクトのシェーダプログラムへの登録
    glAttachShader(gl2Program, vert_shader)
    glAttachShader(gl2Program, frag_shader)

    # シェーダオブジェクトの削除
    glDeleteShader(vert_shader)
    glDeleteShader(frag_shader)

    # attribute変数 positionのindexを0に指定する
    glBindAttribLocation(gl2Program, 0, "position")

    # シェーダプログラムのリンク
    glLinkProgram(gl2Program)
    linked = glGetProgramiv(gl2Program, GL_LINK_STATUS)
    log = glGetProgramInfoLog(gl2Program)
    if log : print('Vertex Shader: ' + str(log))
    if linked == GL_FALSE :
        print("Link error.\n")
        exit(1)


    #バッファオブジェクトを作成します.
    #引数に作成するバッファオブジェクトの数を指定します.
    # 作成されたバッファオブジェクトの名前(番号)が戻り値に指定した配列にn個入ります.
    # 頂点バッファオブジェクトを１つ作る
    global buffer
    buffer = glGenBuffers(1)

    glBindBuffer(GL_ARRAY_BUFFER, buffer)

    size_of_float = 4 #float型の大きさ
    glBufferData(
        GL_ARRAY_BUFFER,
        len(position) * size_of_float,# byte size
        (GLfloat * len(position))(*position),# 謎のctypes
        GL_STATIC_DRAW)

    # 頂点バッファオブジェクトを解放する
    glBindBuffer(GL_ARRAY_BUFFER, 0)


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
    w_w = 640
    w_h = int(w_w * 16 / 9)
    #ディスプレイの初期位置と大きさを設定
    glutInitWindowPosition(800, 50)
    glutInitWindowSize(w_w, w_h)
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
    # glutReshapeFunc(resize)
    # (自作)初期化メソッド
    init()
    # 無限ループでイベントを待つ
    glutMainLoop()


if __name__ == '__main__':
    main()
