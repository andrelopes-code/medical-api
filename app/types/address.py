from pydantic_core import core_schema


class AddressCep(str):

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source,
        _handler,
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls._validate, core_schema.str_schema(max_length=9, min_length=9)
        )

    @classmethod
    def _validate(cls, cep: str, /) -> str:
        import re

        is_correct = re.match(r'\d{5}-\d{3}', cep)
        if not is_correct:
            raise ValueError('CEP must follow the pattern 88888-888')
        return cep


class AddressNumber(str):

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source,
        _handler,
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls._validate, core_schema.str_schema(max_length=10, min_length=1)
        )

    @classmethod
    def _validate(cls, number: str, /) -> str:
        import re

        if number[0] == '0':
            raise ValueError('Number cannot start with 0')

        is_correct = re.match(r'\d{1,10}', number)
        if not is_correct:
            raise ValueError('Number must be between 1 and 10 digits and only digits')
        return number


class AddressState(str):

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source,
        _handler,
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls._validate, core_schema.str_schema(max_length=2, min_length=2)
        )

    @classmethod
    def _validate(cls, state: str, /) -> str:
        is_correct = state.isalpha() and state.isascii()
        if not is_correct:
            raise ValueError('State must follow the pattern XX where X is an unaccented letter')
        return state.upper()


class AddressFormated(str):

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source,
        _handler,
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_after_validator_function(cls._validate, core_schema.str_schema(max_length=255))

    @classmethod
    def _validate(cls, value: str, /) -> str:
        normalized = value.strip()
        return normalized
