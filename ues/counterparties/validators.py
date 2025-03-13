from django import forms


def validate_registration_number(value: int) -> None:
    if (len(str(value)) == 13) or (len(str(value)) == 15):
        return
    else:
        raise forms.ValidationError(
            'ОГРН состоит из 13 арабских цифр. ОГРНИП состоит из 15 арабских цифр.'
        )


def validate_tax_identification_number(value: int) -> None:
    if ((len(str(value)) == 10) or (len(str(value)) == 12)):
        return
    else:
        raise forms.ValidationError(
            'ИНН физического лица состоит из 12 арабских цифр. '
            'ИНН юридического лица состоит из 10 арабских цифр.'
        )


def validate_registration_reason_code(value: int) -> None:
    if value and (len(str(value)) != 9):
        raise forms.ValidationError(
            'КПП юридического лица состоит из 9 арабских цифр.'
        )
