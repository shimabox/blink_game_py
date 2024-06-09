import sys
from datetime import datetime
import cv2

'''
参考
@link http://ensekitt.hatenablog.com/entry/2017/12/19/200000
@link https://note.nkmk.me/python-opencv-face-detection-haar-cascade/
@link https://note.nkmk.me/python-opencv-mosaic/
@link http://workpiles.com/2015/04/opencv-detectmultiscale-scalefactor/
'''

# フレームサイズ
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

def within_range_face_size(w: int) -> bool:
    """
    顔の大きさが適切範囲かを確認する。

    Args:
        w (int): 顔の幅

    Returns:
        bool: 顔の幅が適切な範囲内であればTrue、そうでなければFalse
    """
    if 180 <= w <= 240: # 調整いるかも
        return True
    return False

def detect_face_parts(gray_frame: cv2.Mat) -> dict[str, int]:
    """
    顔部分の情報を検出する。

    Args:
        gray_frame (cv2.Mat): グレースケールのフレーム

    Returns:
        dict[str, int]: 顔部分の座標とサイズの辞書
    """
    facerect = cascade.detectMultiScale(
        gray_frame,
        scaleFactor=1.11,
        minNeighbors=3,
        minSize=(100, 100)
    )

    if len(facerect) != 0:
        for x, y, w, h in facerect:
            # 顔の部分
            return {'x': x, 'y': y, 'w': w, 'h': h}

    return {}

def is_closed_eyes(gray_frame: cv2.Mat, face_parts: dict[str, int]) -> bool:
    """
    目を閉じているかを確認する。

    Args:
        gray_frame (cv2.Mat): グレースケールのフレーム
        face_parts (dict[str, int]): 顔部分の座標とサイズの辞書

    Returns:
        bool: 目が閉じていればTrue、開いていればFalse
    """
    # 顔の部分
    face_x = face_parts['x']
    face_y = face_parts['y']
    face_w = face_parts['w']
    face_h = face_parts['h']

    # 顔の部分から目の近傍を取る
    eyes = gray_frame[face_y: face_y + int(face_h/2), face_x: face_x + face_w]
    # cv2.imshow('face', eyes)

    min_size = (8, 8)  # 調整いるかも

    ''' 目の検出
    眼鏡をかけている場合、精度は低くなる。
    PCのスペックが良ければ、haarcascade_eye_tree_eyeglasses.xmlを使ったほうがよい。
    '''
    left_eye = left_eye_cascade.detectMultiScale(
        eyes,
        scaleFactor=1.11,
        minNeighbors=3,
        minSize=min_size
    )
    right_eye = right_eye_cascade.detectMultiScale(
        eyes,
        scaleFactor=1.11,
        minNeighbors=3,
        minSize=min_size
    )

    ''' left_eye, right_eye
    [[116  40  36  36] [34  40  40  40]] => 開いている
    [[34 40 41 41]] => 閉じている
    [] => 未検出
    '''

    # 片目だけ閉じても駄目にしたい場合(これだと結構厳しい(精度悪い？)判定になる)
    # return len(left_eye) <= 1 or len(right_eye) <= 1

    # どちらかの目が開いていればOK
    return len(left_eye) + len(right_eye) <= 2

def draw_elapsed_time(frame: cv2.Mat, start_time: int) -> None:
    """
    経過時間を描画する。

    Args:
        frame (cv2.Mat): フレーム
        start_time (int): 開始時刻のタイムスタンプ
    """
    now = int(datetime.now().timestamp())
    put_text(frame, str(now - start_time))

def put_text(frame: cv2.Mat, text: str, org: tuple[int, int] = (10, 50), fontScale: int = 3, thickness: int = 3) -> None:
    """
    フレームにテキストを描画する。

    Args:
        frame (cv2.Mat): フレーム
        text (str): 描画するテキスト
        org (tuple[int, int], optional): テキストの位置. Defaults to (10, 50).
        fontScale (int, optional): フォントのスケール. Defaults to 3.
        thickness (int, optional): フォントの太さ. Defaults to 3.
    """
    cv2.putText(
        frame,
        text,
        org,
        cv2.FONT_HERSHEY_PLAIN,
        fontScale,
        (0, 255, 0),
        thickness,
        cv2.LINE_AA
    )

#
# start
#
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print('Can not open camera')
    sys.exit()

# フレームサイズを設定
cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

# 分類器を読み込み
# https://github.com/opencv/opencv/tree/master/data/haarcascades
cascade = cv2.CascadeClassifier(
    'haarcascades/haarcascade_frontalface_alt2.xml'
)
# leftとrightは逆転する
left_eye_cascade = cv2.CascadeClassifier(
    'haarcascades/haarcascade_righteye_2splits.xml'
)
right_eye_cascade = cv2.CascadeClassifier(
    'haarcascades/haarcascade_lefteye_2splits.xml'
)

closed_eyes = False
is_started = False
start_time = 0
closed_time = 0
show_fps = False  # FPSを表示するかどうか

while True:
    # VideoCaptureから1フレーム読み込む
    ret, frame = cap.read()

    if show_fps is True:
        tick = cv2.getTickCount()

    # 処理速度を高めるために画像をグレースケールに変換したものを用意
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if not is_started:
        face_parts = detect_face_parts(gray)
        # print(face_parts)
        if len(face_parts) != 0 \
                and within_range_face_size(face_parts['w']) \
                and not is_closed_eyes(gray, face_parts):

            put_text(frame, 'Please press "s"')

            key = cv2.waitKey(100)
            if key == 115:  # s が押されたら
                is_started = True
                start_time = int(datetime.now().timestamp())

    if is_started and show_fps:
        # FPSを計算する
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - tick)
        put_text(
            frame,
            "FPS : " + str(int(fps)),
            (frame.shape[1] - 150, 40),
            2,
            2
        )

    if is_started:
        closed_eyes = is_closed_eyes(gray, face_parts)
        if closed_eyes:
            draw_elapsed_time(frame=frame, start_time=start_time)
            put_text(frame, 'End', (10, 100))
            cv2.imshow('frame', frame)  # 目が閉じられたであろう瞬間を残す
            break
        else:
            draw_elapsed_time(frame=frame, start_time=start_time)

    cv2.imshow('frame', frame)

    # キー入力を1ms待って、k が27（ESC）だったらBreakする
    k = cv2.waitKey(1)
    if k == 27:
        break

# 後処理
if closed_eyes:
    while True:
        k = cv2.waitKey(100)
        if k == 27:  # ESC が押されたらclose
            break

cap.release()
cv2.destroyAllWindows()
