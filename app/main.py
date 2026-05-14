from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivy.lang import Builder
import random
from sequence_challenges import *

# -------------- UI Widgets/screens --------------------------

class StartScreen(Screen):
    pass

class GameScreen(Screen):
    pass

class VictoryScreen(Screen):
    pass

class HeaderWidget(BoxLayout):
    pass

class ContentWidget(BoxLayout):
    pass

class FooterWidget(BoxLayout):
    pass

class SequenceItem(BoxLayout):
    val = StringProperty("")


# -------------- app controller --------------------------

class MainApp(App):
    stopwatch_text = StringProperty("00:00.0")
    toggle_text = StringProperty("Start")
    status_text = StringProperty()
    level_text = StringProperty("Level: 1")
    progress_value = NumericProperty(0)
    challenge_times = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.time_elapsed = 0.0
        self.running = False
        self.clock_event = None
        self.in_intermission = False
        
        self.current_level = 1
        self.expected_sequence = []
        
        self.challenges = [
            NumberChallenge(),
            LetterChallenge(),
            ReverseNumberChallenge(),
            NegativeNumberChallenge()
        ]

    #--------------------------- game state stuff  --------------------------------
    
    def start_game(self):
        self.current_level = 1
        self.progress_value = 0
        self.challenge_times = []
        self.time_elapsed = 0.0
        self.stopwatch_text = "00:00.0"
        self.wrong_guesses = 0
        
        self.root.current = "game"
        self.load_challenge()
        
        if not self.running:
            self.toggle_stopwatch()

    def reset_game(self):
        self.root.current = "start"
        self.time_elapsed = 0.0
        self.stopwatch_text = "00:00.0"
        self.progress_value = 0

    def start_next_round(self):
        self.in_intermission = False
        self.current_level += 1
        self.time_elapsed = 0.0 

        # checks if the game is won 
        if self.current_level > len(self.challenges):
            self.open_victory_screen()
            return
            
        self.load_challenge()
        
        # turns the stopwatch back on
        self.toggle_stopwatch()

    def handle_footer_button(self):
        if self.in_intermission:
            self.start_next_round()
        else:
            self.toggle_stopwatch()

    #--------------------------- stopwatch stuff ----------------------

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

    def update_stopwatch(self, dt):
        self.time_elapsed += dt
        minutes = int(self.time_elapsed / 60)
        seconds = int(self.time_elapsed % 60)
        tenths = int((self.time_elapsed * 10) % 10)
        self.stopwatch_text = f"{minutes:02d}:{seconds:02d}.{tenths}"

    # ------------------------------ game logic stuff ---------------------------------

    def load_challenge(self):
        # references the container for all of the sequence items
        content = self.root.get_screen("game").ids.content_area.ids.sequence_row
        content.clear_widgets()

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

        self.level_text = f"Level: {self.current_level}"

    def check_answer(self, clicked_value, widget_instance):
        # ignores unexpected clicks
        if not self.running or not self.expected_sequence or self.in_intermission:
            return 

        # handles wrong guesses
        if clicked_value != self.expected_sequence[0]:
            self.wrong_guesses += 1
            self.status_text = f"{clicked_value} was incorrect! Try again."
            return

        # handles right guesses
        self.expected_sequence.pop(0)
        widget_instance.opacity = 0
        widget_instance.disabled = True
        self.status_text = f"{clicked_value} was correct!"
        
        # check if sequence is completed
        if len(self.expected_sequence) == 0:
            self.challenge_times.append(self.time_elapsed)
            self.progress_value += (100 / len(self.challenges))
            
            # pauses the stopwatch
            if self.running:
                self.toggle_stopwatch()
            
            # pauses between rounds
            self.in_intermission = True
            self.status_text = "Round Complete!\nTake a breath."
            self.toggle_text = "Next Round"
            
            # removes old widgets in prep for new ones
            self.root.get_screen("game").ids.content_area.ids.sequence_row.clear_widgets()

    def open_victory_screen(self):
        if self.running:
            self.toggle_stopwatch()
            
        self.root.current = "victory"
        
        challenge_times_ui = self.root.get_screen("victory").ids.challenge_times
        challenge_times_ui.clear_widgets()
        
        for i, time in enumerate(self.challenge_times, 1):
            lbl = Label(text=f"Challenge {i} Time: {time:.2f} seconds", font_size="20sp", color=(0,0,0,1))
            challenge_times_ui.add_widget(lbl)
            
        challenge_times_ui.add_widget(Label(text=f"Final score: {(sum(self.challenge_times) * 100):.0f}", font_size="20sp", color=(0,0,0,1)))

        victory_stats_ui = self.root.get_screen("victory").ids.victory_stats
        victory_stats_ui.clear_widgets()
        victory_stats_ui.add_widget(Label(text=f"Wrong guesses: {self.wrong_guesses}", font_size="20sp", color=(0,0,0,1)))

    def build(self):
        return Builder.load_file("sequence_game.kv")

if __name__ == '__main__':
    MainApp().run()