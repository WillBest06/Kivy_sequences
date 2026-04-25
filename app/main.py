from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivy.lang import Builder
import random

class HeaderWidget(BoxLayout):
    pass

class ContentWidget(BoxLayout):
    pass

class FooterWidget(BoxLayout):
    pass

class RootWidget(BoxLayout):
    pass

class SequenceItem(BoxLayout):
    val = StringProperty("")

class MainApp(App):
    stopwatch_text = StringProperty("00:00.0")
    toggle_text = StringProperty("Start")
    
    status_text = StringProperty("Press Start to Begin")
    progress_value = NumericProperty(0)
    challenge_times = ListProperty()


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.time_elapsed = 0.0
        self.running = False
        self.clock_event = None
        
        self.current_level = 1
        self.correct_answer = ""

    def toggle_stopwatch(self):
        if self.running:
            if self.clock_event:
                self.clock_event.cancel()
            self.toggle_text = "Start" 
            self.running = False
        else:
            self.clock_event = Clock.schedule_interval(self.update_stopwatch, 0.1)
            self.toggle_text = "Pause"
            self.running = True
            
            if self.current_level == 1 and self.status_text == "Press Start to Begin":
                self.load_challenge()

    def update_stopwatch(self, dt):
        self.time_elapsed += dt
        minutes = int(self.time_elapsed / 60)
        seconds = int(self.time_elapsed % 60)
        tenths = int((self.time_elapsed * 10) % 10)
        self.stopwatch_text = f"{minutes:02d}:{seconds:02d}.{tenths}"

    def reset_stopwatch(self):
        if self.running:
            self.time_elapsed = 0.0

    def load_challenge(self):
        self.challenges = {
            1: self.setup_challenge_1,
            2: self.setup_challenge_2,
        }
        
        # Get the correct function based on the level, default to setup_victory
        challenge_function = self.challenges.get(self.current_level, self.setup_victory)
        challenge_function()

    def setup_challenge_1(self):
        self.status_text = "Click the numbers in ascending order!"
        content = self.root.ids.content_area
        content.clear_widgets()

        # Generate numbers, but convert them to strings immediately
        start_num = random.randint(1, 20)
        sequence = [str(i) for i in range(start_num, start_num + 5)]
        
        self.expected_sequence = sequence.copy() # e.g., ['4', '5', '6', '7', '8']
        random.shuffle(sequence)

        for item in sequence:
            # We pass the string into the widget
            widget = SequenceItem(val=item)
            content.add_widget(widget)


    def setup_challenge_2(self):
        self.status_text = "Click the letters in alphabetical order!"
        content = self.root.ids.content_area
        content.clear_widgets()

        sequence = ["h", "i", "j", "k", "l"]
        
        self.expected_sequence = sequence.copy() 
        random.shuffle(sequence)

        for item in sequence:
            widget = SequenceItem(val=item)
            content.add_widget(widget)

    def check_sequence_click(self, clicked_value, widget_instance):
        if not self.running:
            return 

        if self.expected_sequence:
            # Check if the clicked string matches the next expected string
            if clicked_value == self.expected_sequence[0]:
                
                self.expected_sequence.pop(0)
                widget_instance.opacity = 0
                widget_instance.disabled = True
                
                if len(self.expected_sequence) == 0:
                    self.current_level += 1
                    self.challenge_times.append(self.time_elapsed)
                    self.reset_stopwatch()

                    self.progress_value += (100 / len(self.challenges))
                    self.load_challenge()
            else:
                self.status_text = "Wrong order! Try again."

    def open_victory_screen(self):
        self.status_text = f"YOU WIN!\n\nFinal Time: {self.stopwatch_text}"
        self.correct_answer = ""
        if self.running:
            self.toggle_stopwatch()

    def build(self):
        return Builder.load_file("sequence_game.kv")

if __name__ == '__main__':
    MainApp().run()