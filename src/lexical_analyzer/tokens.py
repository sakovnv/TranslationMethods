from token_types import TokenTypes


class Token:
    def __init__(self, _type: TokenTypes, _value: any):
        self.type = _type
        self.value = _value

    def __str__(self):

        return 'Token({type}, {value})\n'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()
