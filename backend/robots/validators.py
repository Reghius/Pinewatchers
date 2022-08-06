from django.forms import ValidationError


def validate_krs(value):
    if len(str(value)) == 10:
        return value
    else:
        raise ValidationError('krs has to be 10 numbers')
