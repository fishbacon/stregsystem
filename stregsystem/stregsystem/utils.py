from itertools import zip_longest


def grouper(n, iterable, filler='x'):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=filler)


def phone_letter_converter(phone_number):
        phone_number = phone_number.lower()
        letters = "abc def ghi jkl mno pqrs tuv wxyz"

        for letters, digit in zip(letters.split(),
                                  range(2, 10)):
            for l in letters:
                phone_number = phone_number.replace(l, str(digit))
        return phone_number
