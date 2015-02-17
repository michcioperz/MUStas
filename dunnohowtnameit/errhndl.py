import random

ALMIGHTY_ERRORS = [
    "It is pitch black. You are likely to be eaten by a grue.",
    "Hello, friend. I see you.",
]

def plea_for_advice():
    return " ".join([random.choice(ALMIGHTY_ERRORS),"By which I mean:\n"])
