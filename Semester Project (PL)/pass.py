import lex
from lex import Screener


class ASTNode:
    def __init__(self, type):
        self.type = type
        self.value = None
        self.sourceLineNumber = -1
        self.child = None
        self.sibling = None
        self.indentation = 0

    # print the tree
    def printTree(self):
        print(self.type)

        if self.child:
            print(" child of " + str(self.type) + " is ", end=" ")
            self.child.printTree()

        if self.sibling:
            print(" sibling of " + str(self.type) + " is " , end=" ")
            self.sibling.printTree()

    # output to the file
    def printTreeToFile(self, file):

        for _ in range(self.indentation):
            file.write(".")
        
        file.write(str(self.type) + "\n")

        if self.child:
            self.child.indentation = self.indentation + 1
            self.child.printTreeToFile(file)

        if self.sibling:
            self.sibling.indentation = self.indentation
            self.sibling.printTreeToFile(file)


class TreeNode:
    def __init__(self, data):
        self.data = data
        self.children = []
        self.parent = None

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    # pre-order traversal of n araay tree
    def printTree(self):
        print(self.data)
        if self.children:
            for child in self.children:
                child.printTree()


class ASTParsser:
    def __int__(self, tokens):
        self.tokens = tokens
        self.currentToken = None
        self.index = 0

    def read(self):
        global stack
        if self.currentToken.type in [lex.TokenType.IDENTIFIER, lex.TokenType.INTEGER, lex.TokenType.STRING]:

            terminalNode = ASTNode( "<"+str(self.currentToken.type.value)+":"+  str(self.currentToken.value)+">")
            stack.append(terminalNode)

        if self.currentToken.value in  ['true', 'false', 'nil', 'dummy']:
            stack.append(ASTNode(self.currentToken.value))

        print("reading : " + str(self.currentToken.value))
        self.index += 1

        if (self.index < len(self.tokens)):
            self.currentToken = self.tokens[self.index]

    def buildTree(self, token, ariness):
        global stack

        print("stack content before ")
        for node in stack:
            print(node.type)

        print("building tree")

        node = ASTNode(token)
        node.value = None
        node.sourceLineNumber = -1
        node.child = None
        node.sibling = None

        while ariness > 0:
            child = stack[-1]
            stack.pop()

            if node.child is not None:
                child.sibling = node.child
            node.child = child

            node.sourceLineNumber = child.sourceLineNumber
            ariness -= 1

        node.printTree()

        stack.append(node)  # Assuming push() is a function that pushes a node onto a stack

        print("stack content after")
        for node in stack:
            print(node.type)

    # Expressions
    def procE(self):
        print('procE')

        match self.currentToken.value:
            case 'let':
                self.read()

                self.procD()

                if self.currentToken.value != 'in':
                    print("Error: in is expected")
                    return
                self.read()

                self.procE()

                print('E -> let D in E')
                self.buildTree('let', 2)

            case 'fn':
                self.read()

                n = 0
                while self.currentToken.type == lex.TokenType.IDENTIFIER or self.currentToken.value == '(':
                    self.procVb()
                    n += 1
                if n == 0:
                    print("E: at least one 'Vb' expected\n")
                    return

                if self.currentToken.value != '.':
                    print("Error: . is expected")
                    return
                self.read()

                self.procE()

                print('E -> fn Vb . E')
                self.buildTree("lambda", n+1)

        # Check this after 
        self.procEw()
        print('E->Ew')

    def procEw(self):
        print('procEw')

        self.procT()
        print('Ew->T')

        if self.currentToken.value == 'where':
            self.read()

            self.procDr()

            print('Ew->T where Dr')
            self.buildTree("where", 2)

    # Tuple Expressions
    def procT(self):
        print('procT')

        self.procTa()

        n = 0
        while self.currentToken.value == ',':
            self.read()
            self.procTa()
            n += 1
            print('T->Ta , Ta')

        if n > 0:
            self.buildTree('tau', n+1)
        else:
            print('T->Ta')

    def procTa(self):
        print('procTa')

        self.procTc()
        print('Ta->Tc')

        while self.currentToken.value == 'aug':
            self.read()

            self.procTc()
            print('Ta->Tc aug Tc')

            self.buildTree("aug", 2)

    def procTc(self):
        print('procTc')

        self.procB()
        print('Tc->B')

        if self.currentToken.value == '->':
            self.read()

            self.procTc()

            if self.currentToken.value != '|':
                print("Error: | is expected")
                return
            self.read()

            self.procTc()

            print('Tc->B -> Tc | Tc')
            self.buildTree("->", 3)

    # Boolean Expressions
    def procB(self):
        print('procB')

        self.procBt()
        print('B->Bt')

        while self.currentToken.value == 'or':
            self.read()

            self.procBt()

            print('B->B or Bt')
            self.buildTree("or", 2)

    def procBt(self):
        print('procBt')

        self.procBs()
        print('Bt->Bs')

        while self.currentToken.value == '&':
            self.read()

            self.procBs()

            print('Bt->Bt & Bs')
            self.buildTree("&", 2)

    def procBs(self):
        print('procBs')

        if self.currentToken.value == 'not':
            self.read()

            self.procBp()

            print('Bs->not Bp')
            self.buildTree("not", 1)

        else:
            self.procBp()
            print('Bs->Bp')

    def procBp(self):
        print('procBp')

        self.procA()
        print('Bp->A')
        print(self.currentToken.value+"######")

        # Bp -> A ( 'gr' | '>') A
        match self.currentToken.value:
            case '>':
                self.read()
                self.procA()
                print('Bp->A gr A')
                self.buildTree("gr", 2)
            case 'gr':
                self.read()
                self.procA()
                print('Bp->A gr A')
                self.buildTree("gr", 2)

            case 'ge':
                self.read()
                self.procA()
                print('Bp->A ge A')
                self.buildTree("ge", 2)

            case '>=':
                self.read()
                self.procA()
                print('Bp->A ge A')
                self.buildTree("ge", 2)

            case '<':
                self.read()
                self.procA()
                print('Bp->A ls A')
                self.buildTree("ls", 2)

            case 'ls':
                self.read()
                self.procA()
                print('Bp->A ls A')
                self.buildTree("ls", 2)

            case '<=':
                self.read()
                self.procA()
                print('Bp->A le A')
                self.buildTree("le", 2)

            case 'le':
                self.read()
                self.procA()
                print('Bp->A le A')
                self.buildTree("le", 2)

            case 'eq':
                self.read()
                self.procA()
                print('Bp->A eq A')
                self.buildTree("eq", 2)

            case 'ne':
                self.read()
                self.procA()
                print('Bp->A ne A')
                self.buildTree("ne", 2)

            case _:
                return

    # Arithmetic Expressions
    def procA(self):
        print('procA')

        if self.currentToken.value == '+':
            self.read()
            self.procAt()
            print('A->+ At')
            self.buildTree("+", 1)

        elif self.currentToken.value == '-':
            self.read()
            self.procAt()
            print('A->- At')
            self.buildTree("neg", 1)

        else:
            self.procAt()
            print('A->At')

        plus = '+'
        while self.currentToken.value == '+' or self.currentToken.value == '-':
            if self.currentToken.value=='-':
                plus='-'
            self.read()

            self.procAt()

            print('A->A + / -At')
            print(self.currentToken.value)
            self.buildTree(plus, 2)


    def procAt(self):
        print('procAt')

        self.procAf()
        print('At->Af')
        while self.currentToken.value == '*' or self.currentToken.value == '/':
            self.read()
            self.procAf()
            print('At->Af * Af')
            print("current token value " + self.currentToken.value)
            self.buildTree(self.currentToken.value, 2)

    def procAf(self):
        print('procAf')

        self.procAp()
        print('Af->Ap')
        while self.currentToken.value == '**':
            self.read()
            self.procAf()
            print('Af->Ap ** Af')
            self.buildTree("**", 2)

    def procAp(self):
        print('procAp')

        self.procR()
        print('Ap->R')
        while self.currentToken.value == '@':
            self.read()
            self.procR()
            print('Ap->R @ R')
            self.buildTree("@", 2)

    def procR(self):
        print('procR')

        self.procRn()
        print('R->Rn')

        while (self.currentToken.type in [lex.TokenType.IDENTIFIER, lex.TokenType.INTEGER,
                                           lex.TokenType.STRING] or self.currentToken.value in ['true', 'false', 'nil', 'dummy', "("]):
            self.procRn()
            print('R->R Rn')

            self.buildTree("gamma", 2)

    def procRn(self):
        print("procRn")

        if self.currentToken.type in [lex.TokenType.IDENTIFIER, lex.TokenType.INTEGER,
                                       lex.TokenType.STRING]:

            print('Rn->' + str(self.currentToken.value))

            self.read()

        elif self.currentToken.value in ['true', 'false', 'nil', 'dummy']:
            print('Rn->' + self.currentToken.value)
            self.read()
            print("self.currentToken.value" , self.currentToken.value)
           
        elif self.currentToken.value == '(':
            self.read()
            self.procE()
            if self.currentToken.value != ')':
                print("Error: ) is expected")
                return
            self.read()
            print('Rn->( E )')

    def procD(self):
        print('procD')

        self.procDa()
        print('D->Da')
        while self.currentToken.value == 'within':
            self.read()
            self.procD()
            print('D->Da within D')
            self.buildTree("within", 2)

    def procDa(self):
        print('procDa')

        self.procDr()
        print('Da->Dr')
        n = 0
        while self.currentToken.value == 'and':
            n += 1
            self.read()
            self.procDa()
            print('Da->and Dr')
        
        if n > 0:
            self.buildTree("and", n + 1)

    def procDr(self):
        print('procDr')

        if self.currentToken.value == 'rec':
            self.read()
            self.procDb()
            print('Dr->rec Db')
            self.buildTree("rec", 1)

        self.procDb()
        print('Dr->Db')

    def procDb(self):
        print('procDb')

        if self.currentToken.value == '(':
            self.read()
            self.procD()
            if self.currentToken.value != ')':
                print("Error: ) is expected")
                return
            self.read()
            print('Db->( D )')
            self.buildTree("()", 1)

        elif self.currentToken.type == lex.TokenType.IDENTIFIER:
            self.read()

            if self.currentToken.type == lex.TokenType.PUNCTUATION and self.currentToken.value == ',':
                self.read()
                self.procVb()

                if self.currentToken.value != '=':
                    print("Error: = is expected")
                    return
                self.buildTree(",", 2)

                self.read()
                self.procE()
                self.buildTree("=", 2)
            else :
                if self.currentToken.value == '=':
                    self.read()
                    self.procE()
                    print('Db->id = E')
                    self.buildTree("=", 2)

                else :
                    n = 0
                    while self.currentToken.type == lex.TokenType.IDENTIFIER or self.currentToken.value == '(':
                        self.procVb()
                        n += 1

                    if n == 0:
                        print("Error: ID or ( is expected")
                        return

                    if self.currentToken.value != '=':
                        print("Error: = is expected")
                        return
                    self.read()

                    self.procE()
                    print('Db->identifier Vb+ = E')
                    self.buildTree("function_form", n + 2)

    def procVb(self):
        print('procVb')
        if self.currentToken.type == lex.TokenType.IDENTIFIER:
            self.read()
            print('Vb->id')

        elif self.currentToken.value == '(':
            self.read()

            if self.currentToken.type == ')':
                print('Vb->( )')
                self.buildTree("()", 0)
                self.read()

            else:
                self.procVL()
                print('Vb->( Vl )')

                if self.currentToken.value != ')':
                    print("Error: ) is expected")
                    return
                
            self.read()

        else:
            print("Error: ID or ( is expected")
            return

    def procVL(self):
        print("procVL")

        if self.currentToken.type != lex.TokenType.IDENTIFIER:
            print("562 VL: Identifier expected")  # Replace with appropriate error handling
        else:
            print('VL->' + self.currentToken.value)

            self.read()
            trees_to_pop = 0
            while self.currentToken.value == ',':
                # Vl -> '<IDENTIFIER>' list ',' => ','?;
                self.read()
                if self.currentToken.type != lex.TokenType.IDENTIFIER:
                    print(" 572 VL: Identifier expected")  # Replace with appropriate error handling
                self.read()
                print('VL->id , ?')

                trees_to_pop += 1

            print('498')
            if trees_to_pop > 0:
                self.buildTree(',', trees_to_pop +1)  # +1 for the first identifier


with open('Sample') as file:
    program = file.read()
    # print(program)

stack = []
tokens = []
# tokenize input
tokenizer = lex.Tokenizer()
tokens = tokenizer.tokenize(program)

for token in tokens:
    print(token.type, token.value)
    if token.value in lex.RESERVED_KEYWORDS:
        token.type = lex.TokenType.RESERVED_KEYWORD

screener = Screener(tokens)
tokens = screener.screen()
# parse input
print(" after screening ")
# for token in tokens:
#     print(token.type, token.value)
parser = ASTParsser()
parser.tokens = tokens
parser.currentToken = tokens[0]
parser.index = 0

parser.procE()
print(len(stack))
root = stack[0]
root.printTree()
with open("output", "w") as file:
    root.indentation = 0
    root.printTreeToFile(file)