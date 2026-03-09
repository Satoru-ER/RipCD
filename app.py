from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from flask import Flask, jsonify, request, send_from_directory
import vlc

AUDIO_EXTENSIONS = {".mp3", ".flac", ".wav", ".aac", ".m4a", ".ogg"}
DEFAULT_MUSIC_DIR = Path("./music")
DEFAULT_CD_DIR = Path(os.getenv("RIPCD_CD_PATH", "/media/cdrom"))


class VLCPlayer:
    def __init__(self) -> None:
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.playlist: list[Path] = []
        self.index = -1
        self.source = "folder"

    def _audio_files(self, base: Path) -> list[Path]:
        if not base.exists():
            return []
        files = [p for p in base.rglob("*") if p.suffix.lower() in AUDIO_EXTENSIONS]
        return sorted(files)

    def load_folder(self, folder: Path) -> dict[str, Any]:
        self.source = "folder"
        self.playlist = self._audio_files(folder)
        self.index = 0 if self.playlist else -1
        return self._prepare_current(autoplay=False)

    def load_cd(self, cd_root: Path) -> dict[str, Any]:
        self.source = "cd"
        self.playlist = self._audio_files(cd_root)
        self.index = 0 if self.playlist else -1
        return self._prepare_current(autoplay=False)

    def _prepare_current(self, autoplay: bool = True) -> dict[str, Any]:
        if self.index < 0 or self.index >= len(self.playlist):
            self.player.stop()
            return self.status(message="曲が見つかりませんでした。")

        path = self.playlist[self.index]
        media = self.instance.media_new(str(path))
        self.player.set_media(media)
        if autoplay:
            self.player.play()
        return self.status()

    def play(self) -> dict[str, Any]:
        if not self.playlist:
            return self.status(message="先にCDまたはフォルダを読み込んでください。")
        if self.player.get_state() == vlc.State.Paused:
            self.player.pause()
            return self.status()
        return self._prepare_current(autoplay=True)

    def pause(self) -> dict[str, Any]:
        self.player.pause()
        return self.status()

    def stop(self) -> dict[str, Any]:
        self.player.stop()
        return self.status()

    def next(self) -> dict[str, Any]:
        if not self.playlist:
            return self.status(message="プレイリストが空です。")
        self.index = (self.index + 1) % len(self.playlist)
        return self._prepare_current(autoplay=True)

    def prev(self) -> dict[str, Any]:
        if not self.playlist:
            return self.status(message="プレイリストが空です。")
        self.index = (self.index - 1) % len(self.playlist)
        return self._prepare_current(autoplay=True)

    def status(self, message: str = "") -> dict[str, Any]:
        state = str(self.player.get_state()).split(".")[-1]
        current = self.playlist[self.index].name if 0 <= self.index < len(self.playlist) else "-"
        return {
            "state": state,
            "track": current,
            "index": self.index,
            "total": len(self.playlist),
            "source": self.source,
            "message": message,
        }


app = Flask(__name__, static_folder=".")
player = VLCPlayer()


@app.get("/")
def root() -> Any:
    return send_from_directory(".", "index.html")


@app.get("/styles.css")
def styles() -> Any:
    return send_from_directory(".", "styles.css")


@app.get("/app.js")
def script() -> Any:
    return send_from_directory(".", "app.js")


@app.get("/api/status")
def status() -> Any:
    return jsonify(player.status())


@app.post("/api/load-folder")
def load_folder() -> Any:
    payload = request.get_json(silent=True) or {}
    folder = Path(payload.get("path") or DEFAULT_MUSIC_DIR)
    return jsonify(player.load_folder(folder))


@app.post("/api/load-cd")
def load_cd() -> Any:
    payload = request.get_json(silent=True) or {}
    cd_path = Path(payload.get("path") or DEFAULT_CD_DIR)
    return jsonify(player.load_cd(cd_path))


@app.post("/api/play")
def play() -> Any:
    return jsonify(player.play())


@app.post("/api/pause")
def pause() -> Any:
    return jsonify(player.pause())


@app.post("/api/stop")
def stop() -> Any:
    return jsonify(player.stop())


@app.post("/api/next")
def next_track() -> Any:
    return jsonify(player.next())


@app.post("/api/prev")
def prev_track() -> Any:
    return jsonify(player.prev())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
