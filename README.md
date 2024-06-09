# blink_game_py
目をつぶったら画面キャプチャを終了するやつ(Python+OpenCV)

![IMG_4896](https://github.com/shimabox/blink_game_py/assets/2285196/cd663444-aab4-478c-9dd9-2d0988598aa6)

## これはなに

WEBカメラの映像から顔と目を検出して、目をつぶったら画面キャプチャを終了するという、ちょっとしたゲーム感覚のやつです。

## 前提条件

- Ryeがinstallされていること
  - [Installation - Rye](https://rye.astral.sh/guide/installation/ "Installation - Rye")
  - ```sh
    curl -sSf https://rye.astral.sh/get | bash
    ```
  - ```
    echo 'source "$HOME/.rye/env"' >> ~/.zshrc
    ```

※ Note: python(3系(3.8>=))が入っていれば、ryeを入れなくても以下でいけるかもしれません
```sh
sed '/-e/d' requirements.lock > requirements.txt
pip install -r requirements.txt
python src/blink_game_py/main.py
```

## 実行

### 1. clone
```sh
git clone https://github.com/shimabox/blink_game_py
cd blink_game_py
```

### 2. rye sync(依存関係の同期)

```sh
# /your/file/path/blink_game_py/
rye sync
```

### 3. 起動

```sh
rye run python src/blink_game_py/main.py
or
python src/blink_game_py/main.py
```

## 遊び方

1. 起動したら、画面`frame`にフォーカスを合わせておきます
1. 顔をカメラに向け目を`クワッ`と開けます
1. `Please press "s"` と表示されるまで顔を近づけたり遠ざけたりします
1. `s`を押します
    1. 顔認識中かつまだスタートしていない場合、少しカクつく(キー入力を待っている)のでキー入力待ちが分かるかと思います
1. 目が開いている状態の場合、1秒ずつカウントダウン表示します
1. 目が閉じられたら画面キャプチャを終了します
    1. 目が閉じられたとみなされたタイミングが最後の画面キャプチャとなります
1. `esc`を押して終了です

### 参考

- [WEBカメラの映像をPythonとOpenCVで顔認識して遊ぶ – Shimabox Blog](https://blog.shimabox.net/2018/08/29/recognize_the_face_of_webcam_image_with_python_opencv/ "WEBカメラの映像をPythonとOpenCVで顔認識して遊ぶ – Shimabox Blog")
- [PythonとOpenCVを使ったまばたき検知ゲームの(プチ)改善 – Shimabox Blog](https://blog.shimabox.net/2018/09/18/improvement_of_blink_detection_using_python_and_opencv/ "PythonとOpenCVを使ったまばたき検知ゲームの(プチ)改善 – Shimabox Blog")
