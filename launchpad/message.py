
class Message:
    def __init__(self, data):
        self.key = data.note
        self.clicked = (data.velocity == 127)
