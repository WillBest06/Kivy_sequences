from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivy.lang import Builder
import random


# ------------- sequence challenge class and subclasses ----------------------

class SequenceChallenge:
    def __init__(self, prompt_text):
        self.prompt_text = prompt_text

    def generate_sequence(self):
        raise NotImplementedError("Sequence subclasses need their own generate_sequence function")

class NumberChallenge(SequenceChallenge):
    def __init__(self):
        super().__init__("Click the numbers in ascending order!")

    def generate_sequence(self):
        start_num = random.randint(1, 20)
        return [str(i) for i in range(start_num, start_num + 5)]

class LetterChallenge(SequenceChallenge):
    def __init__(self):
        super().__init__("Click the letters in alphabetical order!")

    def generate_sequence(self):
        return ["h", "i", "j", "k", "l"]


# -------------- UI widgets --------------------------

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
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.time_elapsed = 0.0
        self.running = False
        self.clock_event = None
        
        self.current_level = 1
        self.expected_sequence = []
        

        self.challenges = [
            NumberChallenge(),
            LetterChallenge()
        ]

    #--------------------------- stopwatch logic --------------------------------

    stopwatch_text = StringProperty("00:00.0")
    toggle_text = StringProperty("Start")
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

    # ------------------------------ game logic ---------------------------------

    status_text = StringProperty("Press Start to Begin")
    progress_value = NumericProperty()
    challenge_times = ListProperty()

    def load_challenge(self):
        content = self.root.ids.content_area
        content.clear_widgets()

        # checks if game has been won
        if self.current_level > len(self.challenges):
            self.open_victory_screen()
            return

        current_challenge = self.challenges[self.current_level - 1]
        
        self.status_text = current_challenge.prompt_text
        sequence = current_challenge.generate_sequence()
        
        self.expected_sequence = sequence.copy()
        random.shuffle(sequence)

        for item in sequence:
            widget = SequenceItem(val=item)
            content.add_widget(widget)

    def check_sequence_click(self, clicked_value, widget_instance):
        # returns if game is not actively running
        if not self.running or not self.expected_sequence:
            return 

        # returns if incorrect next sequence value clicked
        if clicked_value != self.expected_sequence[0]:
            self.status_text = "Wrong order! Try again."
            return

        # proceeds if correct next sequence value clicked
        self.expected_sequence.pop(0)
        widget_instance.opacity = 0
        widget_instance.disabled = True
        
        # proceeds when the user has finished the sequence
        if len(self.expected_sequence) == 0:
            self.current_level += 1
            self.progress_value += (100 / len(self.challenges))

            self.challenge_times.append(self.time_elapsed)
            self.reset_stopwatch()

            self.load_challenge()
            

    def open_victory_screen(self):
        content = self.root.ids.content_area
        content.clear_widgets()

        i = 0

        for time in self.challenge_times:
            i += 1
            label = Label(text=f"Challenge {i} time: {time:.2f}")
            content.add_widget(label)


        label = Label(text=f"YOU WIN!\n\nFinal Time: {self.stopwatch_text}")
        content.add_widget(label)
        
        if self.running:
            self.toggle_stopwatch()

    def build(self):
        return Builder.load_file("sequence_game.kv")

if __name__ == '__main__':
    MainApp().run()