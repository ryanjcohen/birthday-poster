import random

class EmojiSelector:
    emoji_list = [
        ':party_meow:',
        ':confetti_ball:',
        ':party_blob:',
        ':partying_face:',
        ':party_parrot:',
        ':birthday:',
        ':balloon:',
        ':cake:',
        ':tada:',
        ':sparkles:',
        ':fast_parrot:'
    ]

    def __init__(self):
        self.index = random.randint(0, len(EmojiSelector.emoji_list) - 1)

    def get_emoji(self):
        index = self.index
        self.index = (self.index + 1) % len(EmojiSelector.emoji_list)
        return EmojiSelector.emoji_list[index]
