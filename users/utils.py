import random
import string # ascii_lowercase, ascii_uppercase


def generate_token(length=10, has_digits=True):
    token = ''.join(
        random.choice(list(string.ascii_letters + string.digits)) for i in range(length)
    )
    if has_digits and token.isalpha():
        token[random.randint(0, length)] = random.randint(0, 9)
    return token
