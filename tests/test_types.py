import pytest
from pydantic import ValidationError
from pydantic_core import SchemaValidator

from app.types.address import AddressCep, AddressFormated, AddressNumber, AddressState
from app.types.user import UserGender, UserName, UserType


@pytest.mark.parametrize(
    'gender, expected',
    [
        ('male', UserGender.male),
        ('female', UserGender.female),
        ('other', UserGender.other),
    ],
)
def test_gender(gender, expected):
    assert UserGender(gender) == expected


@pytest.mark.parametrize(
    'user_type, expected',
    [
        ('patient', UserType.patient),
        ('doctor', UserType.doctor),
        ('admin', UserType.admin),
    ],
)
def test_user_type(user_type, expected):
    assert UserType(user_type) == expected


def test_user_name():
    from uuid import uuid1

    first = uuid1().hex
    last = uuid1().hex
    name = f'{first} {last}'

    user_name = UserName(name)._validate(name)

    assert user_name == name.strip().title()
    assert user_name.first == first.title()
    assert user_name.last == last.title()

    user_name = UserName('')._validate('')


def test_valid_cep_format():

    schema = AddressCep.__get_pydantic_core_schema__(None, None)
    validator = SchemaValidator(schema)

    cep = '56789-034'
    result = validator.validate_python(cep)
    assert result == cep


def test_invalid_cep_format():

    schema = AddressCep.__get_pydantic_core_schema__(None, None)
    validator = SchemaValidator(schema)

    invalid = [
        '8888-888',
        '88888888',
        '8888888',
        '888888',
        '88888',
        '8888',
        '888',
    ]

    for cep in invalid:
        with pytest.raises(ValidationError):
            validator.validate_python(cep)


def test_valid_number_format():

    schema = AddressNumber.__get_pydantic_core_schema__(None, None)
    validator = SchemaValidator(schema)

    numbers = [
        '1',
        '12',
        '123',
        '1234',
        '12345',
        '123456',
        '1234567',
        '12345678',
        '123456789',
        '1234567890',
    ]
    for n in numbers:
        result = validator.validate_python(n)
        assert result == n


def test_invalid_number_starting_with_zero_or_more_than_10_digits():

    schema = AddressNumber.__get_pydantic_core_schema__(None, None)
    validator = SchemaValidator(schema)

    invalid = [
        '0',
        '01',
        '012',
        '0123',
        '01234',
        '012345',
        '0123456',
        '01234567',
        '012345678',
        '0123456789',
        '034953809485',
        '34053495837495837',
        '',
    ]

    for n in invalid:
        with pytest.raises(ValidationError):
            validator.validate_python(n)


def test_valid_state_format():

    schema = AddressState.__get_pydantic_core_schema__(None, None)
    validator = SchemaValidator(schema)

    states = [
        'AC',
        'al',
        'se',
        'SP',
        'TO',
    ]

    for s in states:
        result = validator.validate_python(s)
        assert result == s.upper()


def test_invalid_state_format_too_short_or_too_long_or_not_alphabetical():

    schema = AddressState.__get_pydantic_core_schema__(None, None)
    validator = SchemaValidator(schema)

    invalid = ['a', 'A!', 'ada', 'agvj', '', '#$', 'CÁ', 'Cá', 'ÇA']

    for s in invalid:
        with pytest.raises(ValidationError):
            validator.validate_python(s)


def test_valid_titled_format():

    schema = AddressFormated.__get_pydantic_core_schema__(None, None)
    validator = SchemaValidator(schema)

    titles = [
        '   starting with spaces',
        'ending with spaces   ',
        '  starting and ending with spaces   ',
    ]

    for t in titles:
        result = validator.validate_python(t)
        assert result == t.strip()
