import string
import random

class RandomGenerator:
    @staticmethod
    def generate_char():
        lower = string.ascii_lowercase
        upper = string.ascii_uppercase
        digits = string.digits
        pool = lower + upper + digits
        return random.choice(pool)

    @staticmethod
    def generate_string(length):
        result = ''
        for i in range(length):
            result += RandomGenerator.generate_char()
        return result
