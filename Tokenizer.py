from Token import Token


class Tokenizer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.postion = 0
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

    
    # def tokenize(self):
    #     while self.current_char is not None:
    #         if self.current_char.isspace():
    #             self.skip_whitespaces()
    #             continue
    #
    #         # если всречается сивмол или _ - то это идентификатор переменной
    #         if self.current_char.isalpha() or self.current_char == '_':
    #             id_value = self.identifier()
    #
    #             if id_value == 'плюс':
    #                 self.tokens.append(Token('PLUS'))
    #             elif id_value = 'минус':
    #                 self.tokens.append(Token('MINUS'))
    #             elif id_value = ''
