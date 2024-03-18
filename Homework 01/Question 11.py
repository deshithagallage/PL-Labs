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
    while lookahead == 'or':
        match('or')
        T()
        print("BT(or, 2)")
    while lookahead == 'nor':
        match('nor')
        T()
        print("BT(nor, 2)")
    while lookahead == 'xor':
        match('xor')
        T()
        print("BT(xor, 2)")

def T():
    global lookahead
    F()
    while lookahead == 'and':
        match('and')
        T()
        print("BT(and, 2)")
    while lookahead == 'nand':
        match('nand')
        T()
        print("BT(nand, 2)")

def F():
    global lookahead
    match lookahead:
        case 'not':
            match('not')
            F()
            print("BT(not, 1)")
        case '(':
            P()
        case 'i':
            P()
        case 'true':
            P()
        case 'false':
            P()

def P():
    global lookahead
    match lookahead:
        case '(':
            match('(')
            E()
            match(')')
        case 'i':
            match('i')
            print("BT(i, 0)")
        case 'true':
            match('true')
            print("BT(true, 0)")
        case 'false':
            match('false')
            print("BT(false, 0)")


# Initialize the input string and current position
input_string = input("Enter the input string: ").split()
current_position = 0
lookahead = next_token()

# Start parsing
E()