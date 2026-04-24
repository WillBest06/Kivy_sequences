from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.uix.label import Label

class RootWidget(BoxLayout):
    pass

class HeaderWidget(BoxLayout):
    elapsed = 0.0
    running = False
    event = None

    def start_stopwatch(self):
        if self.running:
            return

        self.running = True
        self.event = Clock.schedule_interval(self.update_stopwatch, 0)

    def update_stopwatch(self, dt):
        self.elapsed += dt
        self.ids.stopwatch_label.text = f"{self.elapsed:.2f}"

    def pause_stopwatch(self):
        if self.event:
            self.event.cancel()
            self.event = None

        self.running = False

class ContentWidget(BoxLayout):
    pass

    # def challenge_1():
    #     nums = [1, 2, 3, 4, 5]
    #     pass

    # def challenge_2():
    #     letters = ["h", "i", "j", "k", "l"]
    #     pass

    # def challenge_3():
    #     pass

    # def challenge_4():
    #     pass

class FooterWidget(BoxLayout):
    pass

class MainApp(App):
    pass

if __name__ == "__main__":
    MainApp().run()