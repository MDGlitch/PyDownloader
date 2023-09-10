import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.progressbar import ProgressBar
from kivy.core.window import Window 
from pytube import YouTube

class YouTubeDownloaderApp(App):
    def build(self):
        self.title = "YouTube Video Downloader"
        self.layout = BoxLayout(orientation="vertical", padding=10)

        Window.size = (Window.width, Window.height)

        self.url_label = Label(text="YouTube URL:")
        self.url_input = TextInput(
            hint_text="Paste your YouTube video here...",
            multiline=False,
        )

        self.download_button = Button(text="Download")
        self.download_button.bind(on_release=self.start_download)

        self.progress_bar = ProgressBar(
            max=100,
            height=30, 
            size_hint_y=None, 
        )

        self.directory_label = Label(text="Download Directory:")
        self.file_chooser = FileChooserListView(
            size_hint_y=None,
            height=1200, 
        )

        self.status_label = Label()

        self.layout.add_widget(self.url_label)
        self.layout.add_widget(self.url_input)
        self.layout.add_widget(self.download_button)
        self.layout.add_widget(self.progress_bar) 
        self.layout.add_widget(self.directory_label)
        self.layout.add_widget(self.file_chooser)
        self.layout.add_widget(self.status_label)

        return self.layout

    def start_download(self, instance):
        self.download_thread = threading.Thread(target=self.download_video)
        self.download_thread.start()
        self.url_input.text = ""

    def update_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = (bytes_downloaded / total_size) * 100
        self.progress_bar.value = percentage

    def download_video(self):
        video_url = self.url_input.text
        download_path = self.file_chooser.path

        try:
            yt = YouTube(video_url, on_progress_callback=self.update_progress)
            stream = yt.streams.get_highest_resolution()
            stream.download(output_path=download_path)
            self.status_label.text = "Download completed."
            self.progress_bar.value = 100  
        except Exception as e:
            self.status_label.text = f"Error: {str(e)}"

if __name__ == "__main__":
    YouTubeDownloaderApp().run()
