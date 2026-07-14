from Token import Token


class Tokenizer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.position = 0
        self.current_char = self.source_code[0] if self.source_code else None


        self.tokens = []

    # идем по длине кода, получаем self.current_char
    def advance(self):
        self.position += 1

        if self.position < len(self.source_code):
            self.current_char = self.source_code[self.position]

        else: 
            self.current_char = None

    # ищем пробелы в коде и в случае их нахождения сдвигаем элемент на слудующий
    def skip_whitespaces(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        while self.current_char is not None and self.current_char != '\n':
            self.advance()

    # если встречаем цифру записываем ее в result, сдвигаем элемент вправои и выводим число или 
    # float, если текущий символ . 
    def number(self):
        result = ''
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            result += self.current_char
            self.advance()

        return float(result) if '.' in result else int(result)

    # функция для создания идентификаторов переменных
    def identifier(self): 
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()

        return result

    def tokenize(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespaces()
                continue

            if self.current_char == '#':
                self.skip_comment()
                continue

            # если всречается сивмол или _ - то это идентификатор переменной
            if self.current_char.isalpha() or self.current_char == '_':
                id_value = self.identifier()

                if id_value == 'вывести':
                    self.tokens.append(Token('PRINT', 'вывести'))
                elif id_value == 'плюс':
                    self.tokens.append(Token('PLUS', '+'))
                elif id_value == 'минус':
                    self.tokens.append(Token('MINUS', '-'))
                elif id_value == 'умножить':
                    self.tokens.append(Token("MULTIPLY", '*'))
                elif id_value == 'делить':
                    self.tokens.append(Token("DIVIDE", '/'))
                
                elif id_value == 'равно':
                    self.tokens.append(Token("EQUALS", '=='))
                
                elif id_value == 'больше':
                    self.tokens.append(Token("GREATER", '>'))
                elif id_value == 'меньше':
                    self.tokens.append(Token("LESS", '<'))
                elif id_value == 'и':
                    self.tokens.append(Token('AND', '&&'))
                elif id_value == 'или':
                    self.tokens.append(Token("OR", '||'))
                elif id_value == 'не':
                    self.tokens.append(Token('NOT', '!'))
                else: 
                    self.tokens.append(Token("IDENTIFIER", id_value))
                
                continue


            # если встречаем цифру, обрабатываем число
            if self.current_char.isdigit():
                num_value = self.number()
                self.tokens.append(Token('NUMBER', num_value))
                continue

            if self.current_char == '=':
                self.tokens.append(Token('ASSIGN', '='))
                self.advance()
            elif self.current_char == '(':
                self.tokens.append(Token('LPAREN', '('))
                self.advance()
            elif self.current_char == ')':
                self.tokens.append(Token('RPAREN', ')'))
                self.advance()
            elif self.current_char == '{':
                self.tokens.append(Token('LBRACE', '{'))
                self.advance()
            elif self.current_char == '}':
                self.tokens.append(Token('RBRACE', '}'))
                self.advance()
            elif self.current_char == ',':
                self.tokens.append(Token('COMMA', ','))
                self.advance()
            else:
                raise Exception(f"Неизвестный символ: {self.current_char}")

        return self.tokens       
