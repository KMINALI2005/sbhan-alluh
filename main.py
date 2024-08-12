import flet as ft
import os
from mutagen.mp3 import MP3
import random

class MusicPlayer(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.songs = []
        self.current_song_index = 0
        self.is_playing = False

    def build(self):
        self.song_list = ft.ListView(expand=1, spacing=10, padding=20)
        self.play_button = ft.IconButton(ft.icons.PLAY_ARROW, on_click=self.play_pause)
        self.next_button = ft.IconButton(ft.icons.SKIP_NEXT, on_click=self.next_song)
        self.prev_button = ft.IconButton(ft.icons.SKIP_PREVIOUS, on_click=self.prev_song)
        self.shuffle_button = ft.IconButton(ft.icons.SHUFFLE, on_click=self.shuffle_playlist)
        self.song_title = ft.Text("No song selected", size=20)
        self.progress_bar = ft.ProgressBar(width=300, value=0)

        return ft.Column(
            [
                ft.Text("Music Player", size=30, weight=ft.FontWeight.BOLD),
                ft.ElevatedButton("Add Songs", on_click=self.pick_files),
                self.song_list,
                self.song_title,
                self.progress_bar,
                ft.Row(
                    [self.prev_button, self.play_button, self.next_button, self.shuffle_button],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def pick_files(self, e):
        pick_files_dialog = ft.FilePicker(on_result=self.pick_files_result)
        self.page.overlay.append(pick_files_dialog)
        self.page.update()
        pick_files_dialog.pick_files(allow_multiple=True, file_type=ft.FilePickerFileType.AUDIO)

    def pick_files_result(self, e: ft.FilePickerResultEvent):
        if e.files:
            for f in e.files:
                self.songs.append(f.path)
                self.song_list.controls.append(ft.Text(os.path.basename(f.path)))
            self.update()

    def play_pause(self, e):
        if not self.songs:
            return

        if self.is_playing:
            self.page.audio.pause()
            self.play_button.icon = ft.icons.PLAY_ARROW
            self.is_playing = False
        else:
            if self.page.audio.src != self.songs[self.current_song_index]:
                self.page.audio.src = self.songs[self.current_song_index]
            self.page.audio.play()
            self.play_button.icon = ft.icons.PAUSE
            self.is_playing = True
            self.update_song_info()

        self.play_button.update()

    def next_song(self, e):
        if not self.songs:
            return

        self.current_song_index = (self.current_song_index + 1) % len(self.songs)
        self.play_song()

    def prev_song(self, e):
        if not self.songs:
            return

        self.current_song_index = (self.current_song_index - 1) % len(self.songs)
        self.play_song()

    def shuffle_playlist(self, e):
        if not self.songs:
            return

        random.shuffle(self.songs)
        self.current_song_index = 0
        self.update_song_list()
        self.play_song()

    def play_song(self):
        self.page.audio.src = self.songs[self.current_song_index]
        self.page.audio.play()
        self.play_button.icon = ft.icons.PAUSE
        self.is_playing = True
        self.play_button.update()
        self.update_song_info()

    def update_song_info(self):
        self.song_title.value = os.path.basename(self.songs[self.current_song_index])
        self.song_title.update()
        self.update_progress_bar()

    def update_progress_bar(self):
        def update_progress(e):
            if self.is_playing:
                current_time = self.page.audio.get_current_position()
                total_time = self.page.audio.get_duration()
                if total_time > 0:
                    self.progress_bar.value = current_time / total_time
                    self.progress_bar.update()

        self.page.audio.on_position_changed = update_progress

    def update_song_list(self):
        self.song_list.controls.clear()
        for song in self.songs:
            self.song_list.controls.append(ft.Text(os.path.basename(song)))
        self.song_list.update()

def main(page: ft.Page):
    page.title = "Android Music Player"
    page.window_width = 360  # Width suitable for most Android screens
    page.window_height = 640  # Height suitable for most Android screens
    page.window_resizable = False
    page.update()

    # Create audio object
    page.audio = ft.Audio()

    # Create and add music player to the page
    music_player = MusicPlayer()
    page.add(music_player)

ft.app(target=main)
