def next_token():
    global input_string, current_position
    if current_position < len(input_string):
        token = input_string[current_position]
        current_position += 1
        return token
    else:
        return '_'

def match(token):
    global lookahead
    if lookahead == token:
        # Consume the token
        lookahead = next_token()
    else:
        print("Error: Unexpected token")

def E():
    T()
    Y()
    print("E -> TY")

def Y():
    global lookahead
    match lookahead:
        case 'or':
            match('or')
            T()
            Y()
            print("Y -> orTY")
        case 'nor':
            match('nor')
            T()
            Y()
            print("Y -> norTY")
        case 'xor':
            match('xor')
            T()
            Y()
            print("Y -> xorTY")
        case ')':
            print("Y ->")
        case '_':
            print("Y ->")
        case _:
            print("Error: Unexpected token")

def T():
    F()
    X()
    print("T -> FX")

def X():
    global lookahead
    match lookahead:
        case 'and':
            match('and')
            T()
            print("X -> andT")
        case 'nand':
            match('nand')
            T()
            print("X -> nandT")
        case 'or':
            print("X ->")
        case 'nor':
            print("X ->")
        case 'xor':
            print("X ->")
        case '_':
            print("X ->")
        case ')':
            print("X ->")
        case _:
            print("Error: Unexpected token")

def F():
    global lookahead
    match lookahead:
        case 'not':
            match('not')
            F()
            print("F -> notF")
        case '(':
            P()
            print("F -> P")
        case 'i':
            P()
            print("F -> P")
        case 'true':
            P()
            print("F -> P")
        case 'false':
            P()
            print("F -> P")
        case _:
            print("Error: Unexpected token")

def P():
    global lookahead
    match lookahead:
        case '(':
            match('(')
            E()
            match(')')
            print("P -> (E)")
        case 'i':
            match('i')
            print("P -> i")
        case 'true':
            match('true')
            print("P -> true")
        case 'false':
            match('false')
            print("P -> false")
        case _:
            print("Error: Unexpected token")

# Initialize the input string and current position
input_string = input("Enter the input string: ").split()
current_position = 0
lookahead = next_token()

# Start parsing
E()

