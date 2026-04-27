import random

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

class ReverseNumberChallenge(SequenceChallenge):
    def __init__(self):
        super().__init__("Click the numbers in descending order!")

    def generate_sequence(self):
        start_num = random.randint(1, 20)
        sequence = [str(i) for i in range(start_num, start_num + 5)]
        sequence.reverse()
        return sequence
        