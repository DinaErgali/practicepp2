import pygame
import os


class MusicPlayer:

    def __init__(self, music_folder):
        pygame.mixer.init()
        self.music_folder  = music_folder
        self.playlist      = self.load_songs()
        self.current       = 0       # index of current song
        self.is_playing    = False

    def load_songs(self):
        """Load all .mp3 and .wav files from the music folder."""
        songs = []
        if os.path.isdir(self.music_folder):
            for file in sorted(os.listdir(self.music_folder)):
                if file.endswith(".mp3") or file.endswith(".wav"):
                    songs.append(os.path.join(self.music_folder, file))
        return songs

    def play(self):
        """Play the current song."""
        if not self.playlist:
            return
        pygame.mixer.music.load(self.playlist[self.current])
        pygame.mixer.music.play()
        self.is_playing = True

    def stop(self):
        """Stop playback."""
        pygame.mixer.music.stop()
        self.is_playing = False

    def next_song(self):
        """Go to next song. Wraps back to first after last."""
        if not self.playlist:
            return
        self.current = (self.current + 1) % len(self.playlist)
        if self.is_playing:
            self.play()

    def prev_song(self):
        """Go to previous song. Wraps to last after first."""
        if not self.playlist:
            return
        self.current = (self.current - 1) % len(self.playlist)
        if self.is_playing:
            self.play()

    def get_song_name(self):
        """Return just the filename of the current song."""
        if not self.playlist:
            return "No songs found"
        return os.path.basename(self.playlist[self.current])

    def get_status(self):
        """Return current playback status as a string."""
        if not self.playlist:
            return "No songs"
        if self.is_playing and pygame.mixer.music.get_busy():
            return "Playing"
        return "Stopped"
