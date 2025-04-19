import random

class EmojiSelector:
    emoji_list = [
        ':cupcake:',
        ':star-struck:',
        ':confetti_ball:',
        ':partying_face:',
        ':star2:',
        ':birthday:',
        ':balloon:',
        ':cake:',
        ':tada:',
        ':sparkles:',
        ':gift:'
    ]

    def __init__(self):
        self.index = random.randint(0, len(EmojiSelector.emoji_list) - 1)

    def get_emoji(self):
        index = self.index
        self.index = (self.index + 1) % len(EmojiSelector.emoji_list)
        return EmojiSelector.emoji_list[index]
