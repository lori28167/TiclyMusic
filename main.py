import tkinter as tk
from tkinter import messagebox
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import yt_dlp
import vlc  # For audio playback
import os

# Configura le credenziali di Spotify
client_id = '76e978f2b8b349f0bac80ecd6a5846ec'
client_secret = 'fd22fe7becdf4052968ca8a4bfe0f8d9'
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


class MusicApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TiclyMusic")
        self.root.geometry("800x600")

        self.player = None  # VLC player instance
        self.is_repeat_active = False  # Repeat flag

        # UI elements
        self.label = tk.Label(self.root, text="TiclyMusic", font=("Arial", 16))
        self.label.pack(pady=20)

        self.search_label = tk.Label(self.root, text="Metti il nome della canzone o dell'artista:")
        self.search_label.pack(pady=5)
        self.search_entry = tk.Entry(self.root, width=50)
        self.search_entry.pack(pady=5)

        self.search_button = tk.Button(self.root, text="Cerca", command=self.search_music)
        self.search_button.pack(pady=15)

        self.results_listbox = tk.Listbox(self.root, width=50, height=10)
        self.results_listbox.pack(pady=10)

        self.play_button = tk.Button(self.root, text="Ascolta", command=self.play_music)
        self.play_button.pack(pady=10)

        # Frame for pause, resume, volume and repeat buttons
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(pady=10)

        self.pause_button = tk.Button(self.control_frame, text="Pausa", command=self.pause_music, state=tk.DISABLED)
        self.pause_button.pack(side=tk.LEFT, padx=10)

        self.resume_button = tk.Button(self.control_frame, text="Riprendi", command=self.resume_music, state=tk.DISABLED)
        self.resume_button.pack(side=tk.LEFT, padx=10)

        self.repeat_button = tk.Button(self.control_frame, text="Ripeti", command=self.toggle_repeat, state=tk.DISABLED)
        self.repeat_button.pack(side=tk.LEFT, padx=10)

        # Volume slider
        self.volume_label = tk.Label(self.control_frame, text="Volume:")
        self.volume_label.pack(side=tk.LEFT, padx=10)

        self.volume_slider = tk.Scale(self.control_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=self.set_volume)
        self.volume_slider.set(50)  # Default volume 50
        self.volume_slider.pack(side=tk.LEFT, padx=10)


        self.videos = []  # List for saving video titles

    def search_music(self):
        query = self.search_entry.get().strip()
        if query:
            self.results_listbox.delete(0, tk.END)  # Clear previous search results
            self.videos = []
            self.spotify_search(query)
        else:
            messagebox.showwarning("Input Error", "Please enter a valid search term.")

    def spotify_search(self, query):
        try:
            results = sp.search(q=query, limit=5, type='track')
            if not results['tracks']['items']:
                messagebox.showinfo("No results", "No songs found.")
                return

            for idx, track in enumerate(results['tracks']['items']):
                song_name = track['name']
                artist_name = track['artists'][0]['name']
                song_full_name = f"{song_name} - {artist_name}"
                self.results_listbox.insert(tk.END, song_full_name)
                self.videos.append((song_name, artist_name))  # Save tuple (song_name, artist_name)
        except Exception as e:
            messagebox.showerror("Error", f"Spotify search error: {e}")

    def play_music(self):
        selected_index = self.results_listbox.curselection()
        if selected_index:
            song_name, artist_name = self.videos[selected_index[0]]
            self.download_and_play(song_name, artist_name)
        else:
            messagebox.showwarning("Selection Error", "Please select a song to play.")

    def download_and_play(self, song_name, artist_name):
        try:
            if self.player and self.player.is_playing():
                self.player.stop()  # Stop any song currently playing

            # Create search query by combining song and artist
            query = f"{song_name} {artist_name}"

            # YouTube audio download config
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': './downloads/%(title)s.%(ext)s',
                'noplaylist': True,
                'quiet': True,
            }

            if not os.path.exists('./downloads'):
                os.makedirs('./downloads')

            # Download the audio from YouTube
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(f"ytsearch:{query}", download=True)
                video_title = info_dict['entries'][0]['title']
                audio_file = f"./downloads/{video_title}.webm"

                # Show download complete message
                messagebox.showinfo("Download Complete", f"Downloaded: {video_title}")

                # Play the downloaded audio
                self.play_audio(audio_file)

        except Exception as e:
            messagebox.showerror("Download Error", f"An error occurred: {e}")

    def play_audio(self, audio_file):
        try:
            self.player = vlc.MediaPlayer(audio_file)
            self.player.play()

            # Set volume to current volume slider value
            self.set_volume(self.volume_slider.get())

            # Enable/Disable buttons for pause, resume, and repeat
            self.pause_button.config(state=tk.NORMAL)
            self.resume_button.config(state=tk.DISABLED)
            self.repeat_button.config(state=tk.NORMAL)

            # Set duration text
            duration = self.player.get_length() / 1000  # in seconds
            self.update_song_info(current_time=0, duration=duration)

            # Start the timeline update every second
            self.update_song_info(current_time=0, duration=duration)

            messagebox.showinfo("Now Playing", f"Playing: {os.path.basename(audio_file)}")
        except Exception as e:
            messagebox.showerror("Playback Error", f"An error occurred during playback: {e}")

    def update_song_info(self, current_time, duration):
        """ Update the current time and total duration of the song """
        # Calculate current time in minutes and seconds
        current_minutes, current_seconds = divmod(int(current_time), 60)
        total_minutes, total_seconds = divmod(int(duration), 60)

        # Update song info label with current time and duration
        self.song_info_label.config(text=f"Canzone: {current_minutes:02}:{current_seconds:02} / {total_minutes:02}:{total_seconds:02}")

        # Continuously update the song info every 1000 ms (1 second)
        if self.player and self.player.is_playing():
            self.root.after(1000, self.update_song_info, current_time=self.player.get_time() / 1000, duration=duration)

    def set_volume(self, volume):
        """ Set the VLC player volume """
        if self.player:
            self.player.audio_set_volume(int(volume))

    def pause_music(self):
        if self.player and self.player.is_playing():
            self.player.pause()
            # Toggle button states
            self.pause_button.config(state=tk.DISABLED)
            self.resume_button.config(state=tk.NORMAL)

    def resume_music(self):
        if self.player and not self.player.is_playing():
            self.player.play()
            # Toggle button states
            self.pause_button.config(state=tk.NORMAL)
            self.resume_button.config(state=tk.DISABLED)

    def toggle_repeat(self):
        """ Toggle repeat behavior """
        self.is_repeat_active = not self.is_repeat_active  # Toggle repeat
        self.repeat_button.config(text="Stop Repeat" if self.is_repeat_active else "Ripeti")


# Launch the app
if __name__ == "__main__":
    root = tk.Tk()
    app = MusicApp(root)
    root.mainloop()
