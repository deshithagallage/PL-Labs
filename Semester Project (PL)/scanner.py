import re

def tokenize(code):
    patterns = {
        'Identifier': r'[a-zA-Z][a-zA-Z_]*',
        'Integer': r'[0-9]+',
        'Comment': r'//.*',
        'Operator': r'[+\-*/<>&.@/:=~|$!#%^_[\]{}`\'?]',
        'String': r'\"(?:\\.|[^\\"])*\"',
        'Spaces': r'\s+',
        'Punctuation': r'[,;()]'
    }

    tokens = []
    while code:
        matched = False
        for token_type, pattern in patterns.items():
            match = re.match(pattern, code)
            if match:
                value = match.group(0)
                if token_type != 'Spaces' and token_type != 'Comment':
                    tokens.append((token_type, value))
                code = code[len(value):]
                matched = True
                break
        if not matched:
            raise ValueError(f"Invalid token: {code}")
    return tokens

with open("Sample", "r") as file:
    code = file.read()

tokens = tokenize(code)
for token in tokens:
    print(token)
