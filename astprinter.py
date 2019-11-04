from expr import Visitor


class ASTPrinter(Visitor):
    def pprint(self, expr):
        # ask the expr to call our appropriate method
        # (in many langauage I'd rather use a switch on type)
        return expr.accept(self)

    def visit_BinaryExpr(self, expr):
        return f"({expr.operator.lexeme} {expr.left.accept(self)} {expr.right.accept(self)})"

    def visit_GroupingExpr(self, expr):
        return f"(group {expr.expression.accept(self)})"

    def visit_LiteralExpr(self, expr):
        if expr.value is None:
            return 'nil'
        return str(expr.value)

    def visit_UnaryExpr(self, expr):
        return f"({expr.operator.lexeme} {expr.right.accept(self)})"

