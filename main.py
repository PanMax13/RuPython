from Tokenizer import Tokenizer
from Parser import Parser
from Interpritator import Interpreter


def main():
    source_code = """
    x = 10
    y = 30

    вывести x меньше y
    """

    print(source_code)
    print("Tokenization")
    
    tokenizer = Tokenizer(source_code)
    tokens = tokenizer.tokenize()
    
    for token in tokens:
        print(f"{token}")

    print("Parsing.....")

    parser = Parser(tokens)
    ast = parser.parse()

    print("AST is build")

    # interpretation

    interpreter = Interpreter()
    interpreter.interpret(ast)


if __name__ == "__main__":
    main()


