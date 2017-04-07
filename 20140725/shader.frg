
varying vec2 textureCoordinate;
uniform sampler2D inputImageTexture;

uniform float aspectRatio;

int JAW_CONTOUR_COUNT = 8;
int NOSE_CONTOUR_COUNT = 3;
int CHIN_CONTOUR_COUNT = 3;
int FACE_CONTOUR_COUNT = 14;

// contour points
// 0 - 7  : jaw line
// 8 - 10 : nose
// 11 - 13 : chin

//uniform float leftContourPoints[JAW_CONTOUR_COUNT*2*5];
//uniform float rightContourPoints[JAW_CONTOUR_COUNT*2*5];
float leftContourPoints[8*2*5];
float rightContourPoints[8*2*5];

//uniform float contourMoves[JAW_CONTOUR_COUNT*2*5];
float contourMoves[8*2*5];

uniform int numberOfFaces;
//uniform int faceIndex;
int faceIndex;
uniform int isOnFaceShift;
uniform int isSymmetrical;

vec2 ZERO_V = vec2(0.0, 0.0);
float insideAlpha = 1.0;
float outsideAlpha = 0.5;


int isDraw = 1;
float radius = 0.005;

void setContours(){

    leftContourPoints[0] = 0.405;
    leftContourPoints[1] = 0.33;

    leftContourPoints[2] = 0.405;
    leftContourPoints[3] = 0.36;

    leftContourPoints[4] = 0.41;
    leftContourPoints[5] = 0.39;

    leftContourPoints[6] = 0.42;
    leftContourPoints[7] = 0.41;

    leftContourPoints[8] = 0.425;
    leftContourPoints[9] = 0.43;

    leftContourPoints[10] = 0.435;
    leftContourPoints[11] = 0.45;

    leftContourPoints[12] = 0.46;
    leftContourPoints[13] = 0.48;

    leftContourPoints[14] = 0.49;
    leftContourPoints[15] = 0.5;


    float center = 0.49;

    rightContourPoints[0] = 2.0*center - leftContourPoints[0];
    rightContourPoints[1] = leftContourPoints[1];

    rightContourPoints[2] = 2.0*center - leftContourPoints[2];
    rightContourPoints[3] = leftContourPoints[3];

    rightContourPoints[4] = 2.0*center - leftContourPoints[4];
    rightContourPoints[5] = leftContourPoints[5];

    rightContourPoints[6] = 2.0*center - leftContourPoints[6];
    rightContourPoints[7] = leftContourPoints[7];

    rightContourPoints[8] = 2.0*center - leftContourPoints[8];
    rightContourPoints[9] = leftContourPoints[9];

    rightContourPoints[10] = 2.0*center - leftContourPoints[10];
    rightContourPoints[11] = leftContourPoints[11];

    rightContourPoints[12] = 2.0*center - leftContourPoints[12];
    rightContourPoints[13] = leftContourPoints[13];

    rightContourPoints[14] = 2.0*center - leftContourPoints[14];
    rightContourPoints[15] = leftContourPoints[15];
}

void setMoves(){
    contourMoves[0]=0.0;
    contourMoves[1]=0.0;

    contourMoves[2]=0.02;
    contourMoves[3]=0.0;

    contourMoves[4]=0.03;
    contourMoves[5]=0.0;

    contourMoves[6]=0.03;
    contourMoves[7]=0.0;

    contourMoves[8]=0.02;
    contourMoves[9]=0.0;

    contourMoves[10]=0.0;
    contourMoves[11]=0.02;

    contourMoves[12]=0.0;
    contourMoves[13]=0.02;

    contourMoves[14]=0.0;
    contourMoves[15]=0.025;
}


//http://www5d.biglobe.ne.jp/~tomoya03/shtml/algorithm/Intersection.htm
//線分(直線)の交差判定
//二つの線分(直線)の端点(合計４つの点)が引数
int isIntersect(vec2 l1p1, vec2 l1p2, int isSegment1, vec2 l2p1, vec2 l2p2, int isSegment2){

    int isCross = 0;
    float t1 = 0.0;
    float t2 = 0.0;

    isCross = 1;
    if(isSegment2 == 1){
     t1 = (l1p1.x-l1p2.x)*(l2p1.y-l1p1.y) + (l1p1.y-l1p2.y)*(l1p1.x-l2p1.x);
     t2 = (l1p1.x-l1p2.x)*(l2p2.y-l1p1.y) + (l1p1.y-l1p2.y)*(l1p1.x-l2p2.x);
     isCross = (t1*t2 < 0.0) ? 1 : 0;
    }
    if(isCross == 1){
     if(isSegment1 == 1){
       t1 = (l2p1.x-l2p2.x)*(l1p1.y-l2p1.y) + (l2p1.y-l2p2.y)*(l2p1.x-l1p1.x);
       t2 = (l2p1.x-l2p2.x)*(l1p2.y-l2p1.y) + (l2p1.y-l2p2.y)*(l2p1.x-l1p2.x);
       isCross = (t1*t2 < 0.0) ? 1 : 0;
     }
    }
    return isCross;
}

//http://marupeke296.com/COL_2D_No2_PointToLine.html
//点が線分上にあるか判定
int isIntersectPointAndSegment(vec2 p , vec2 lp1, vec2 lp2){
    vec2 v1 = vec2(lp1.x - lp2.x, lp1.y - lp2.y);
    vec2 v2 = vec2(p.x - lp2.x, p.y - lp2.y);
    float len1 = length(v1);
    float len2 = length(v2);
    float dot_ = dot(v1, v2);
    int rtn = abs(dot_ - len1*len2) < 0.001 && len1 >= len2 ? 1 : 0;
    return rtn;
}

//http://imagingsolution.blog107.fc2.com/blog-entry-137.html
//直線の交点
vec2 crossPoint(vec2 l1p1, vec2 l1p2,
                vec2 l2p1, vec2 l2p2){

    float s1 = ((l2p2.x - l2p1.x) * (l1p1.y - l2p1.y) - (l2p2.y - l2p1.y) * (l1p1.x - l2p1.x))/2.0;
    float s2 = ((l2p2.x - l2p1.x) * (l2p1.y - l1p2.y) - (l2p2.y - l2p1.y) * (l2p1.x - l1p2.x))/2.0;

    float x = l1p1.x + (l1p2.x - l1p1.x) * s1 / (s1 + s2);
    float y = l1p1.y + (l1p2.y - l1p1.y) * s1 / (s1 + s2);

    return vec2(x, y);
}

//２次元平面の外積の大きさ
float cross2dLength(vec2 p1, vec2 p2){
    return abs(p1.x*p2.y - p1.y*p2.x);
}

//２直線が平行か
int isParallel(vec2 l1p1, vec2 l1p2,
            vec2 l2p1, vec2 l2p2){
    if(l1p1 == l2p2 || l2p1 == l2p2) return 0;
    float a1 = (l1p1.y - l1p2.y)/(l1p1.x - l1p2.x);
    float a2 = (l2p1.y - l2p2.y)/(l2p1.x - l2p2.x);
    return a1 == a2 ? 1 : 0;
}


//http://www.deqnotes.net/acmicpc/2d_geometry/lines
//点と直線(２点を通る直線)の距離
float distance(vec2 p, vec2 l1p1, vec2 l1p2){
    return cross2dLength(l1p2 - l1p1, p - l1p1) / length(l1p2 - l1p1);
}

//http://www.nttpc.co.jp/technology/number_algorithm.html
//矩形内の領域内外判定
int isInRegion(vec2 p,
            vec2 l1p1, vec2 l1p2, vec2 l2p1, vec2 l2p2){

    //調べる点から平行線を一方に伸ばし、各線分と交差判定して内外か調べる
    vec2 p2 = vec2(1.0, p.y);
    int crossCount = 0;
    crossCount += isIntersect(p, p2, 1, l1p1, l1p2, 1);
    crossCount += isIntersect(p, p2, 1, l1p2, l2p2, 1);
    crossCount += isIntersect(p, p2, 1, l2p2, l2p1, 1);
    crossCount += isIntersect(p, p2, 1, l2p1, l1p1, 1);

    //奇数なら内側
    int rtn = crossCount == 1 ? 1 : (crossCount == 3 ? 1 : 0);
    return rtn;
}

vec2 newPoint(vec2 nowP, vec2 move, vec2 dir){
    float moveL = length(move);
    vec2 moveDir = moveL == 0.0 ? ZERO_V : normalize(move);
    float cos_ = dir.x/length(dir);
    float sin_ = dir.y/length(dir);
    vec2 tv = vec2(moveDir.x * cos_ - moveDir.y * sin_, moveDir.x * sin_ + moveDir.y * cos_);
    return nowP + moveL * tv;
}

int isInsertCircle(vec2 p, vec2 center, float radius){
    float x = center.x - p.x;
    float y = center.y - p.y;
    return x*x + y*y < radius*radius ? 1 : 0;
}

vec2 warpPositionToUse(vec2 currentPoint,
                          vec2 contourPointMain, vec2 mainMovePoint,
                          vec2 contourPointNext,  vec2 nextMovePoint,
                          vec2 dir){

    vec2 newCoord = currentPoint;

    vec2 p11 = contourPointMain;//現在の座標
    vec2 p12 = newPoint(p11, mainMovePoint, dir);//移動後の座標

    vec2 p21 = contourPointNext;//次のcontourの現在の座標
    vec2 p22 = newPoint(p21, nextMovePoint, dir);//次のcontourの移動後の座標

    //変化がなければ終了
    if(p11 == p12 && p21 == p22){
        return newCoord;
    }

    vec2 v11 = p12 - p11;
    //修正用座標1
    vec2 p13 = outsideAlpha * v11 + p12;
    //もう一方の修正用座標1
    vec2 p14 = -insideAlpha * v11 + p11;

    vec2 v21 = p22- p21;
    //修正用座標2
    vec2 p23 = outsideAlpha * v21 + p22;
    //もう一方の修正用座標2
    vec2 p24 = -insideAlpha * v21 + p21;

    //伸ばす側か
    int isExtend = isInRegion(textureCoordinate, p12, p14, p22, p24);
    //縮める側か
    int isShrink = isInRegion(textureCoordinate, p12, p13, p22, p23);

    //どちらでもなければ終了
    if(0 == isShrink + isExtend){
     return newCoord;
    }

    vec2 crossV;
     //ベクトルの交点
     //一方しか変化させていない場合は変化させている方の傾きを交点の変わりとする
    if(v11 == ZERO_V){
        crossV = v21 + textureCoordinate ;
    }
    else if(v21 == ZERO_V){
     crossV = v11 + textureCoordinate ;
    }
    else{
        //平行の場合は傾きを交点の変わりとする
         if(1 == isParallel(p13, p14, p23, p24)){
            crossV = vec2((p13.x - p14.x), (p13.y - p14.y)) + textureCoordinate;
         }
         else{
            crossV = crossPoint(p13, p14, p23, p24);
        }
    }

    vec2 cp1 = crossPoint(textureCoordinate, crossV, p11, p21);
    vec2 cp2 = crossPoint(textureCoordinate, crossV, p12, p22);

    if(1 == isExtend){
     vec2 cp4 = crossPoint(textureCoordinate, crossV, p14, p24);
     vec2 cv1 = cp1 - cp4;
     vec2 cv2 = cp2 - cp4;
     float b1 = length(cv1);
     float b2 = length(cv2);

     newCoord = b1/b2 * (textureCoordinate-cp4) + cp4;
    }
    else{
     vec2 cp3 = crossPoint(textureCoordinate, crossV, p13, p23);
     vec2 cv1 = cp1 - cp3;
     vec2 cv2 = cp2 - cp3;
     float b1 = length(cv1);
     float b2 = length(cv2);
     newCoord = b1/b2 * (textureCoordinate-cp3) + cp3;
    }

    return newCoord;
}

void main() {

    setContours();
    setMoves();

     vec2 left = vec2(leftContourPoints[0], leftContourPoints[1]);
     vec2 right = vec2(rightContourPoints[0], rightContourPoints[1]);
     vec2 dmy = left - right;
     vec2 dir = length(dmy) == 0.0 ? ZERO_V : normalize(dmy);

    faceIndex = 0;

    for(int i = 0 ; i < JAW_CONTOUR_COUNT ; i++){
        int now = i + faceIndex * FACE_CONTOUR_COUNT;
        vec2 left = vec2(leftContourPoints[2*now], leftContourPoints[2*now+1]);
        vec2 right = vec2(rightContourPoints[2*now], rightContourPoints[2*now+1]);

        vec2 moveL = vec2(contourMoves[2*now], contourMoves[2*now+1]);
        vec2 ml = newPoint(left, moveL, dir);
        vec2 moveR = vec2(-contourMoves[2*now], contourMoves[2*now+1]);
        vec2 mr = newPoint(right, moveR, dir);

        if(isInsertCircle(textureCoordinate, left, 0.005) == 1){
                gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
                return;
        }
        if(isInsertCircle(textureCoordinate, right, 0.005) == 1){
                gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
                return;
        }
        if(isInsertCircle(textureCoordinate, ml, 0.005) == 1){
            gl_FragColor = vec4(0.0, 0.0, 1.0, 1.0);
            return;
        }
        if(isInsertCircle(textureCoordinate, mr, 0.005) == 1){
            gl_FragColor = vec4(0.0, 0.0, 1.0, 1.0);
            return;
        }
    }

    vec2 newCoord = textureCoordinate;

    for(int contour = 0 ; contour < JAW_CONTOUR_COUNT-1; contour++){

         int now = contour + faceIndex * FACE_CONTOUR_COUNT;
         int next = now + 1;

         int nextContour = contour + 1;

         vec2 left = vec2(leftContourPoints[2*now], leftContourPoints[2*now+1]);
         vec2 nextLeft = vec2(leftContourPoints[2*next], leftContourPoints[2*next+1]);

         newCoord = warpPositionToUse(newCoord,
                                       left, vec2(contourMoves[2*contour], contourMoves[2*contour+1]),
                                       nextLeft, vec2(contourMoves[2*nextContour], contourMoves[2*nextContour+1]),
                                       dir);

         vec2 right = vec2(rightContourPoints[2*now], rightContourPoints[2*now+1]);
         vec2 nextRight = vec2(rightContourPoints[2*next], rightContourPoints[2*next+1]);

         newCoord = warpPositionToUse(newCoord,
                                       right, vec2(-contourMoves[2*contour], contourMoves[2*contour+1]),
                                       nextRight, vec2(-contourMoves[2*nextContour], contourMoves[2*nextContour+1]),
                                       dir);
    }

    //顎先だけ特別
    {
        int contour = JAW_CONTOUR_COUNT-1;
        int now = contour + faceIndex * FACE_CONTOUR_COUNT;
        int next = (contour-1) + faceIndex * FACE_CONTOUR_COUNT;
        int nextContour = JAW_CONTOUR_COUNT-2;

        vec2 chin = vec2(leftContourPoints[2*now], leftContourPoints[2*now+1]);
        vec2 nextChin = vec2(leftContourPoints[2*next], leftContourPoints[2*next+1]);

         newCoord = warpPositionToUse(newCoord,
                                       chin, vec2(contourMoves[2*contour], contourMoves[2*contour+1]),
                                       nextChin, vec2(contourMoves[2*nextContour], contourMoves[2*nextContour+1]),
                                       dir);
    }





    gl_FragColor = texture2D(inputImageTexture, newCoord);
}
