# RipCD

VLC を使って **CD** と **指定フォルダ内の音楽ファイル**を再生できる、
ブラウザ UI の音楽プレイヤーです。

## セットアップ

```bash
python -m venv .venv
source .venv/bin/activate
pip install flask python-vlc
```

> VLC 本体も必要です（Linuxなら `vlc` パッケージ）。

## 起動

```bash
python app.py
```

ブラウザで `http://localhost:8000` を開いて操作します。

## 使い方

- **音楽フォルダ**: `./music` などを指定して「フォルダ読込」
- **CDパス**: `/media/cdrom` などを指定して「CD読込」
- 再生コントロール: `⏮ ▶ ⏸ ⏭ ⏹`

## メモ

- 読み込み対象は再帰的に探索し、以下拡張子をプレイリスト化します。  
  `.mp3 .flac .wav .aac .m4a .ogg`
- CD の既定パスは環境変数でも指定できます。

```bash
export RIPCD_CD_PATH=/mnt/cdrom
python app.py
```
