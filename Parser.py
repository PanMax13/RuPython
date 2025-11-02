class AST:
    """
    Базовый класс для всех узлов Абстрактного Ситаксического дерева

    Наследование этого класса повзовляет объединить все узлы в систему типов, использовать полиморфизм при 
    обходе дерева, легко добавлять новые узлы и проверять, что объект является элементом AST.
    """
    pass

class BinaryOperation(AST):
    """
    Узел для представления бинарных операций

    атрибуты: 
        left: левый операнд
        right: правый операнд
        op: опреатор - + - * /
    """
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Numbers(AST):
    """
    Узел для преставления числовых литералов
    """
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Variable(AST):
    """
    Узел для представления числовых переменных.
    """
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Assign(AST):
    """
    Узел для операции присваивания. 
    """
    def __init__(self, left, right):
        self.left = left # переменная
        self.right = right # значение переменной

class Print(AST):
    # узел для вывода выражения на экран
    def __init__(self, expression):
        self.expr = expression

class Compare(AST):
    # узел для операции сравнения
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Parser:
    """
    Парер использует метод рекурсивного спуска, когда каждое выражение обрабатывается отдельным методом, 
    который вызывает другие методы согласно правилам грамматики
    """


    def __init__(self, tokens):
        # инициализация парсера. Аргументы: список токенов, полученных от парсера
        self.tokens = tokens
        self.current_token = self.tokens[0] if self.tokens else None
        self.position = 0

    def eat(self, token_type):
        """
        Смотрит текущий токен, если он соответсвует ожидаемому типу, то переходит к следующему. 
        """
        if self.current_token and self.current_token.type == token_type:
            self.position += 1
            self.current_token = self.tokens[self.position] if self.position < len(self.tokens) else None

        else: 
            raise Exception(f"Error: {token_type} is waited, {self.token_type.type} is gotten")


    def factor(self):
        """
        Обрабатывет факторы - простейшие элементы выражений.

        Фактор может быть числом, перемнной или выражением в скобках. 
        """
        # получаем текущий токен
        token = self.current_token

        # если токен - число, здаем узел Numbers(число)
        if token.type == 'NUMBER':
            self.eat("NUMBER")
            return Numbers(token)
        
        elif token.type == "IDENTIFIER": # если токен - переменная, то создаем узел переменной
            self.eat("IDENTIFIER")
            return Variable(token)
        
        elif token.type == 'LPAREN':
            self.eat('LPAREN')
            node = self.expr() # получаем значение между скобками
            self.eat('RPAREN')
            return node

        else: 
            raise Exception("Uncorrect factor")

        
    def term(self):
        """
        обрабатывем умножение и деления(термы)

        Термы имеют более высокий преоритет, чем сложение и вычитание

        Возвращает одиночный factor или BinaryOperation для цепочки операций
        """
        node = self.factor() # обрабатываем левый операнд(первый)

        while self.current_token and self.current_token.type in ("MULTIPLY", "DIVIDE"):
            token = self.current_token
            
            if token.type in ("MULTIPLY"):
                self.eat(token.type)
            elif token.type == 'DIVIDE':
                self.eat('DIVIDE')
            
            right_node = self.factor() # разбираем второй операнд
            node = BinaryOperation(left=node, operation = token, right=right_node)

        return node

    def comparison(self):
        """
        Обрабатывает операции сравнения
        """

        node = self.expr()

        while self.current_token and self.current_token.type in ('EQUALS', "GREATER", 'LESS'):
            token = self.current_token

            if token.type == 'EQUALS':
                self.eat('EQUALS')
            elif token.type == 'GREATER':
                self.eat('GREATER') 
            elif token.type == 'LESS':
                self.eat('LESS')

            right_node = self.expr()

            node = Compare(left=node, op=token, right=right_node)

        return node

    def expr(self):
        """
        Обрабатывает выражения - операции сложения и вычетания
        """

        node = self.term()
        while self.current_token and self.current_token.type in ("PLUS", "MINUS"):
            token = self.current_token

            if token.type == 'PLUS':
                self.eat('PLUS')

            elif token.type == 'MINUS':
                self.eat('MINUS')
            
            right_node = self.term()

            node = BinaryOperation(left=node, op = token, right = right_node)

        return node


    def statement(self):
        """
        Обрабатывает операторы языка
        """

        if self.current_token.type == 'PRINT':
            self.eat("PRINT")
        
            return Print(self.comparison())

        elif self.current_token.type == 'IDENTIFIER':
            left = Variable(self.current_token)
            self.eat('IDENTIFIER')
            self.eat('ASSIGN')

            right = self.comparison()

            return Assign(left, right)
        
        else:
            raise Exception(f"Некорректный оператор: {self.current_token.type}")

    
    def parse(self):
        """
        Преобразует все токены в AST-программу
        """

        nodes = []

        while self.current_token is not None:
            nodes.append(self.statement())

        return nodes