import re
from enum import Enum

class TokenType(Enum):
    IDENTIFIER = 'ID'
    INTEGER = 'INT'
    COMMENT = 'Comment'
    OPERATOR = 'Operator'
    STRING = 'String'
    SPACES = 'Spaces'
    PUNCTUATION = 'Punctuation'
    RESERVED_KEYWORD = 'Reserved Keyword'

RESERVED_KEYWORDS = ['fn','where', 'let', 'aug', 'within' ,'in' ,'rec' ,'eq','gr','ge','ls','le','ne','or','@','not','&','true','false','nil','dummy','and','|']

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

class Screener:
    def __init__(self, tokens):
        self.tokens = tokens

    def merge_tokens(self):
        for i in range(len(self.tokens)):
            if i < len(self.tokens) - 1 and self.tokens[i].type == TokenType.OPERATOR:
                # Merge certain operators
                if self.tokens[i].value == '-' and self.tokens[i + 1].value == '>':
                    self.tokens[i].value = '->'
                    self.tokens.pop(i + 1)
                elif self.tokens[i].value == '>' and self.tokens[i + 1].value == '=':
                    self.tokens[i].value = '>='
                    self.tokens.pop(i + 1)
                elif self.tokens[i].value == '<' and self.tokens[i + 1].value == '=':
                    self.tokens[i].value = '<='
                    self.tokens.pop(i + 1)
                elif self.tokens[i].value == '*' and self.tokens[i + 1].value == '*':
                    self.tokens[i].value = '**'
                    self.tokens.pop(i + 1)
                # elif self.tokens[i].value == '-' and self.tokens[i + 1].type == TokenType.INTEGER:
                #     self.tokens[i + 1].value = '-' + self.tokens[i + 1].value
                #     self.tokens.pop(i)

    def screen(self):
        self.merge_tokens()
        return self.tokens


tokenizer = Tokenizer()
with open("Sample", "r") as file:
    code = file.read()

tokens = tokenizer.tokenize(code)

screener = Screener(tokens)
tokens = screener.screen()

tokenizer = Tokenizer()
with open("Sample", "r") as file:
    code = file.read()

tokens = tokenizer.tokenize(code)

screener = Screener(tokens)
tokens = screener.screen()

for token in tokens:
    print(token)
