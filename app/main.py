# from os.path import dirname, join

# from kivy.app import App
# from kivy.lang import Builder
# from kivy.uix.boxlayout import BoxLayout

# KV_FILE = join(dirname(__file__), "app.kv")
# Builder.load_file(KV_FILE)


# class MainWidget(BoxLayout):
#     pass


# class MyApp(App):
#     def build(self):
#         return MainWidget()


# if __name__ == "__main__":
#     MyApp().run()

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class RootWidget(BoxLayout):
    pass

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     self.add_widget(Button(text="Start"))
        

class MainApp(App):
    def build(self):
        return RootWidget()


if __name__ == "__main__":
    MainApp().run()