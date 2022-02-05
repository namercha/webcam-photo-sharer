from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.clipboard import Clipboard
from filesharer import FileSharer
import time
import webbrowser

Builder.load_file('frontend.kv')


class CameraScreen(Screen):

    def start(self):
        """
        Starts the camera and changes the button text.
        """
        self.ids.camera.opacity = 1
        self.ids.camera.play = True
        self.ids.camera_button.text = 'Stop Camera'
        self.ids.camera.texture = self.ids.camera._camera.texture

    def stop(self):
        """
        Stops the camera and changes the button text.
        """
        self.ids.camera.opacity = 0
        self.ids.camera.play = False
        self.ids.camera_button.text = 'Start Camera'
        self.ids.camera.texture = None

    def capture(self):
        """
        Creates a file name with the current time and captures and saves a photo
        under that file name.
        """
        current_time = time.strftime('%Y%m%d-%H%M%S')
        self.file_path = f"files/{current_time}.png"
        self.ids.camera.export_to_png(self.file_path)
        self.manager.current = 'image_screen'
        self.manager.current_screen.ids.img.source = self.file_path


class ImageScreen(Screen):

    link_message = "Create a sharable link first."

    def create_link(self):
        """
        Takes the photo that was just captured, uploads it and creates a sharable link.
        """
        filepath = App.get_running_app().root.ids.camera_screen.file_path
        filesharer = FileSharer(filepath=filepath)
        self.url = filesharer.share()
        self.ids.link.text = self.url

    def copy_link(self):
        """
        Copies the link to the clipboard.
        """
        try:
            Clipboard.copy(self.url)
        except:
            self.ids.link.text = self.link_message

    def open_link(self):
        """
        Opens the generated link in a browser.
        """
        try:
            webbrowser.open(self.url)
        except:
            self.ids.link.text = self.link_message


class RootWidget(ScreenManager):
    pass


class MainApp(App):

    def build(self):
        return RootWidget()


# Run() method is in the App class, which is inherited by MainApp class
MainApp().run()
