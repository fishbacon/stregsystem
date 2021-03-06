from django.db import models
from django.contrib.auth import hashers
from django.core.exceptions import ValidationError
import re

from fembers import utils


# TODO these validators might belong to Member?
def validate_pin(value):
    msg = "Invalid pin"
    if re.match('\d{4}$', value) is None:
        raise ValidationError(msg)


def validate_phone_number(number):
    msg = "{} is an invalid phone number"
    if re.match('\d{1,16}$', number) is None:
        raise ValidationError(msg.format(number))


class Member(models.Model):
    username = models.CharField(max_length=64)
    name = models.CharField(max_length=64, default='')
    # gender
    # weight
    join_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    _pin = models.CharField(verbose_name="pin",
                            max_length=128,
                            blank=True,
                            null=True)
    note = models.TextField(blank=True)
    email = models.EmailField()
    _phone_number = models.CharField(verbose_name="phone number",
                                     max_length=16,
                                     blank=True,
                                     validators=[validate_phone_number])

    def phone_number_format(self):
        if len(self.phone_number) % 2:
            n = self.phone_number[1:]
            res = self.phone_number[0] + ' '
        else:
            n = self.phone_number
            res = ''
        res += ' '.join([a+b for a, b in utils.grouper(2, n)])
        return res

    @property
    def phone_number(self):
        return self._phone_number

    @phone_number.setter
    def phone_number(self, new_phone_number):
        new_phone_number = utils.remove_seperators(new_phone_number,
                                                   [' ', '-', '_', '+'])
        new_phone_number = utils.phone_letter_converter(new_phone_number)
        self._phone_number = new_phone_number

    @property
    def pin(self):
        return self._pin

    @pin.setter
    def pin(self, new_pin):
        validate_pin(new_pin)
        self._pin = hashers.make_password(new_pin)

    def check_pin(self, pin):
        return hashers.check_password(pin, self._pin)

    def change_pin(self, old_pin, new_pin):
        if self.check_pin(old_pin):
            self.pin = new_pin
            return True
        else:
            return False

    def __str__(self):
        return str.format("{s.username} #{s.number} ({s.name})", s=self)


class List(models.Model):
    name = models.CharField(max_length=64)
    members = models.ManyToManyField(Member)

    def __str__(self):
        return self.name
