import re
from enum import Enum

class TokenType(Enum):
    IDENTIFIER = 'Identifier'
    INTEGER = 'Integer'
    COMMENT = 'Comment'
    OPERATOR = 'Operator'
    STRING = 'String'
    SPACES = 'Spaces'
    PUNCTUATION = 'Punctuation'

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"{self.type} {self.value}"

class Tokenizer:
    def __init__(self):
        self.patterns = {
            TokenType.IDENTIFIER: r'[a-zA-Z][a-zA-Z_]*',
            TokenType.INTEGER: r'[0-9]+',
            TokenType.COMMENT: r'//.*',
            TokenType.OPERATOR: r'[+\-*/<>&.@/:=~|$!#%^_[\]{}`\'?]',
            TokenType.STRING: r'\"(?:\\.|[^\\"])*\"',
            TokenType.SPACES: r'\s+',
            TokenType.PUNCTUATION: r'[,;()]'
        }

    def tokenize(self, code):
        tokens = []
        while code:
            matched = False
            for type, pattern in self.patterns.items():
                match = re.match(pattern, code)
                if match:
                    value = match.group(0)
                    if type != TokenType.SPACES and type != TokenType.COMMENT:
                        tokens.append(Token(type, value))
                    code = code[len(value):]
                    matched = True
                    break
            if not matched:
                raise ValueError(f"Invalid token: {code}")
        return tokens

# Usage example
tokenizer = Tokenizer()
with open("Sample", "r") as file:
    code = file.read()

tokens = tokenizer.tokenize(code)
for token in tokens:
    print(token)
