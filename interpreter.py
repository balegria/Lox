from expr import Visitor as ExprVisitor
from stmt import Visitor as StmtVisitor
from runtime_error import LoxRuntimeError
from tokentype import TokenType
from environment import Environment

class Interpreter(ExprVisitor, StmtVisitor):
    environment = Environment()

    def visit_LiteralExpr(self, expr):
        return expr.value

    def visit_LogicalExpr(self, expr):
        left = self._evaluate(expr.left)

        if expr.operator.type == TokenType.OR:
            if self._is_truthy(left):
                return left
        else:
            if not self._is_truthy(left):
                return left

        return self._evaluate(expr.right)

    def _evaluate(self, expr):
        return expr.accept(self)

    def execute(self, stmt):
        stmt.accept(self)

    def execute_block(self, statements, environment):
        previous_environment = self.environment
        try:
            self.environment = environment

            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous_environment

    def visit_BlockStmt(self, stmt):
        self.execute_block(stmt.statements, Environment(self.environment))
        return None

    def visit_ExpressionStmt(self, stmt):
        self._evaluate(stmt.expression)
        return None


    def visit_IfStmt(self, stmt):
        if self._is_truthy(self._evaluate(stmt.condition)):
            self.execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            self.execute(stmt.else_branch)

        return None

    def visit_PrintStmt(self, stmt):
        value = self._evaluate(stmt.expression)
        print(self._stringify(value))
        return None

    def visit_VarStmt(self, stmt):
        value = None
        if stmt.initializer is not None:
            value = self._evaluate(stmt.initializer)

        self.environment.define(stmt.name.lexeme, value)
        return None

    def visit_AssignExpr(self, expr):
        value = self._evaluate(expr.value)

        self.environment.assign(expr.name, value)
        return value

    def _is_truthy(self, right):
        if right is None:
            return False
        if isinstance(right, bool):
            return right
        return True

    def _is_equal(self, left, right):
        if left is None and right is None:
            return True
        return left == right

    def visit_BinaryExpr(self, expr):
        left = self._evaluate(expr.left)
        right = self._evaluate(expr.right)

        op_type = expr.operator.type

        if op_type == TokenType.GREATER:
            self._check_number_operands(expr.operator, left, right)
            return float(left) > float(right)
        if op_type == TokenType.GREATER_EQUAL:
            self._check_number_operands(expr.operator, left, right)
            return float(left) >= float(right)
        if op_type == TokenType.LESS:
            self._check_number_operands(expr.operator, left, right)
            return float(left) < float(right)
        if op_type == TokenType.LESS_EQUAL:
            self._check_number_operands(expr.operator, left, right)
            return float(left) <= float(right)

        if op_type == TokenType.MINUS:
            self._check_number_operands(expr.operator, left, right)
            return float(left) - float(right)
        if op_type == TokenType.PLUS:
            if isinstance(left, float) & isinstance(right, float):
                return float(left) + float(right)
            if isinstance(left, str) & isinstance(right, str):
                return str(left) + str(right)
            raise LoxRuntimeError(expr.operator, "Operands must be two numbers or two strings")
        if op_type == TokenType.SLASH:
            self._check_number_operands(expr.operator, left, right)
            return float(left) / float(right)
        if op_type == TokenType.STAR:
            self._check_number_operands(expr.operator, left, right)
            return float(left) * float(right)

        if op_type == TokenType.BANG_EQUAL:
            return not self._is_equal(left, right)
        if op_type == TokenType.EQUAL_EQUAL:
            return not self._is_equal(left, right)

        return None

    def visit_GroupingExpr(self, expr):
        return self._evaluate(expr.expression)

    def visit_UnaryExpr(self, expr):
        right = self._evaluate(expr.right)

        op_type = expr.operator.type

        if op_type == TokenType.MINUS:
            self._check_number_operand(expr.operator, right)
            return float(right) * -1
        if op_type == TokenType.BANG:
            return not self._is_truthy(right)

        return None

    def visit_VariableExpr(self, expr):
        return self.environment.get(expr.name)

    def _check_number_operands(self, operator, left, right):
        if isinstance(left, float) and isinstance(right, float):
           return

        raise LoxRuntimeError(operator, "Operands must be numbers.")

    def _check_number_operand(self, operator, operand):
        if isinstance(operand, float):
            return
        raise LoxRuntimeError(operator, "Operand must be a number")

    def _stringify(self, obj):
        if obj is None:
            return 'None'

        if isinstance(obj, float):
            str_obj = str(obj)
            if str_obj.endswith('.0'):
                str_obj = str_obj.rstrip('.0')

            return str_obj

        return str(obj)

    def interpret(self, statements):
        from main import run_time_error

        try:
            for statement in statements:
                self.execute(statement)
        except LoxRuntimeError as e:
            run_time_error(e)
