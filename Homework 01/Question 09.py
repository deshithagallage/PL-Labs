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
    global lookahead
    T()
    print("E -> T")
    while lookahead in ['or', 'nor', 'xor']:
        match lookahead:
            case 'or':
                match('or')
                T()
                print("E -> E or T")
            case 'nor':
                match('nor')
                T()
                print("E -> E nor T")
            case 'xor':
                match('xor')
                T()
                print("E -> E xor T")
            case _:
                print("Error: Unexpected token")

def T():
    global lookahead
    F()
    print("T -> F")
    while lookahead in ['and', 'nand']:
        match lookahead:
            case 'and':
                match('and')
                F()
                print("T -> T and F")
            case 'nand':
                match('nand')
                F()
                print("T -> T nand F")
            case _:
                print("Error: Unexpected token")

def F():
    global lookahead
    match lookahead:
        case 'not':
            match('not')
            F()
            print("F -> not F")
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