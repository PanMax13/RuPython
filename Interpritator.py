"""
Интерпритатор
"""

class Interpreter:
    """
    Интерпритатор для выполенния программ представленных в AST.
    
    Он использует паттерн Visitor для обхода AST. Каждый тип узла обрабатываетя соответствующим методом visit_имяМетода
    """

    def __init__(self):
        """
        Инициализаци интерпритатора

        Создает пустой словарь переменных, который будет заполняться в процессе 
        выполнения программы при выполнении операторов присваивания

        """

        self.variables = {}

    
    def visit(self, node):
        """
        Основноый метод для посещения узлов AST (pattern Visitor)

        Этот метод автоматически определяет, какой метод вызвать на основе переданного узла.
        """

        node_type = type(node).__name__

        method_name = f'visit_{node_type}'

        method = getattr(self, method_name, None)

        if method:
            return method(node)

        else: 
            return self.generic_visit(node)

    
    def generic_visit(self, node):
        """
        Обрабтчик для неизвестных типов узла
        """

        node_type = type(node).__name__

        raise Exception(f'Нет метода visit_{node_type} для обработки узла {node}')

    def visit_BinaryOperation(self, node):
        """
        Выполняет бинарные операции с двумя операндами
        """

        left_value = self.visit(node.left)
        right_value = self.visit(node.right)

         # Выполняем операцию в зависимости от типа оператора
        if node.op.type == 'PLUS':
            # Сложение: left + right
            result = left_value + right_value
        elif node.op.type == 'MINUS':
            # Вычитание: left - right
            result = left_value - right_value
        elif node.op.type in ('MULTIPLY', 'BY'):
            # Умножение: left * right
            # 'BY' обрабатывается как умножение (для естественного синтаксиса)
            result = left_value * right_value
        elif node.op.type == 'DIVIDE':
            # Деление: left / right
            # Может вызвать ZeroDivisionError если right_value == 0
            result = left_value / right_value
        else:
            # Неизвестный оператор
            raise Exception(f'Неизвестный бинарный оператор: {node.op.type}')

        return result

        
    def visit_Compare(self, node):
        """
        Выполняет операции сравнения
        """

        left_value = self.visit(node.left)
        right_value = self.visit(node.right)

        if node.op.type == 'EQUALS':
            result = left_value == right_value

        elif node.op.type == 'GREATER':
            result = left_value > right_value
        
        elif node.op.type == 'LESS':
            result = left_value < right_value

        else: 
            raise Exception(f'Неизвестный опертор сравнения {node.op.type}')

    
        return result


    def visit_Numbers(self, node):
        """
        Обрабатывает числовые литералы
        """
        return node.value
    
    def visit_Variable(self, node):
        """
        Инициализация переменных
        """
        variable_name = node.value

        value = self.variables.get(variable_name)

        if value is None:
            raise NameError(f"Переменная {variable_name} не определена")

        return value

    def visit_Assign(self, node):
        """ 
        Присваивание
        """

        variable_name = node.left.value

        value = self.visit(node.right)

        self.variables[variable_name] = value

        return value

    def visit_Print(self, node):
        """
        Вывод на экран
        """

        value = self.visit(node.expr)

        print(value)
        return None


    def interpret(self, ast_nodes):
        """
        Выполянет методы интерпритации программы
        """

        for node in ast_nodes:
            self.visit(node)