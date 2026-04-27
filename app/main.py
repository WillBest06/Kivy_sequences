from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivy.lang import Builder
import random


# ------------- SEQUENCE CHALLENGE CLASSES ----------------------

class SequenceChallenge:
    def __init__(self, prompt_text):
        self.prompt_text = prompt_text

    def generate_sequence(self):
        raise NotImplementedError("Subclasses need their own generate_sequence function")

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


# -------------- UI WIDGETS & SCREENS --------------------------

# We define the three screens. They inherit from Kivy's Screen class.
class StartScreen(Screen):
    pass

class GameScreen(Screen):
    pass

class VictoryScreen(Screen):
    pass

# The modular widgets that live inside the GameScreen
class HeaderWidget(BoxLayout):
    pass

class ContentWidget(BoxLayout):
    pass

class FooterWidget(BoxLayout):
    pass

class SequenceItem(BoxLayout):
    val = StringProperty("")


# -------------- MAIN APP CONTROLLER --------------------------

class MainApp(App):
    stopwatch_text = StringProperty("00:00.0")
    toggle_text = StringProperty("Start")
    status_text = StringProperty("Press Start to Begin")
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
            LetterChallenge()
        ]

    #--------------------------- STATE ROUTING --------------------------------
    
    def start_game(self):
        """Called from the Start Screen to boot up the game."""
        self.current_level = 1
        self.progress_value = 0
        self.challenge_times = []
        self.time_elapsed = 0.0
        self.stopwatch_text = "00:00.0"
        self.wrong_guesses = 0
        
        # Switch the ScreenManager to the game screen
        self.root.current = "game"
        self.load_challenge()
        
        # Automatically start the timer
        if not self.running:
            self.toggle_stopwatch()

    def reset_game(self):
        """Called from the Victory Screen to reset everything to default."""
        self.root.current = "start"
        self.time_elapsed = 0.0
        self.stopwatch_text = "00:00.0"
        self.status_text = "Press Start to Begin"
        self.progress_value = 0

    #--------------------------- STOPWATCH & INTERMISSION ----------------------

    def toggle_stopwatch(self):
        # Scenario A: We are in an intermission. The user clicked "Next Round".
        if self.in_intermission:
            self.in_intermission = False
            self.current_level += 1
            
            if self.current_level > len(self.challenges):
                self.open_victory_screen()
                return
                
            self.load_challenge()
            self.clock_event = Clock.schedule_interval(self.update_stopwatch, 0.1)
            self.toggle_text = "Pause"
            self.running = True
            return

        # Scenario B & C: Normal Start/Pause
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


    # ------------------------------ GAME LOGIC ---------------------------------

    def load_challenge(self):
        # We now access the content area through the GameScreen object
        content = self.root.get_screen("game").ids.content_area
        content.clear_widgets()

        current_challenge = self.challenges[self.current_level - 1]
        
        self.level_text = f"Level: {self.current_level} / {len(self.challenges)}"
        self.status_text = current_challenge.prompt_text
        
        sequence = current_challenge.generate_sequence()
        self.expected_sequence = sequence.copy()
        random.shuffle(sequence)

        for item in sequence:
            widget = SequenceItem(val=item)
            content.add_widget(widget)

    def check_sequence_click(self, clicked_value, widget_instance):
        if not self.running or not self.expected_sequence or self.in_intermission:
            return 

        if clicked_value != self.expected_sequence[0]:
            self.wrong_guesses += 1
            self.status_text = "Wrong order! Try again."
            return

        self.expected_sequence.pop(0)
        widget_instance.opacity = 0
        widget_instance.disabled = True
        
        # When the user FINISHES a sequence:
        if len(self.expected_sequence) == 0:
            self.challenge_times.append(self.time_elapsed)
            self.progress_value += (100 / len(self.challenges))
            
            # Reset elapsed time behind the scenes for the next level
            self.time_elapsed = 0.0 
            
            # 1. Pause the stopwatch
            if self.running:
                self.clock_event.cancel()
                self.running = False
            
            # 2. Trigger Intermission State
            self.in_intermission = True
            self.status_text = "Round Complete!\nTake a breath."
            self.toggle_text = "Next Round"
            
            # 3. Clear the board so they see the screen is empty
            self.root.get_screen("game").ids.content_area.clear_widgets()

    def open_victory_screen(self):
        # Ensure clock is stopped
        if self.running:
            self.clock_event.cancel()
            self.running = False
            
        # Switch to victory screen
        self.root.current = "victory"
        
        # Populate the victory data
        challenge_times_ui = self.root.get_screen("victory").ids.challenge_times
        challenge_times_ui.clear_widgets()
        
        for i, time in enumerate(self.challenge_times, 1):
            lbl = Label(text=f"Challenge {i} Time: {time:.2f} seconds", font_size="20sp")
            challenge_times_ui.add_widget(lbl)
        challenge_times_ui.add_widget(Label(text=f"Final score: {(sum(self.challenge_times) * 100):.0f}", font_size="20sp"))

        victory_stats_ui =  self.root.get_screen("victory").ids.victory_stats
        victory_stats_ui.clear_widgets()
        victory_stats_ui.add_widget(Label(text=f"Wrong guesses: {self.wrong_guesses}", font_size="20sp"))

    def build(self):
        # We changed the name so it doesn't double-load (like we fixed earlier!)
        return Builder.load_file("sequence_game.kv")

if __name__ == '__main__':
    MainApp().run()