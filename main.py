import sys

from interpreter import Interpreter
from scanner import Scanner
from tokentype import TokenType
from parse import Parser

hasError = False
hasRuntimeError = False

def run(s):
    scanner = Scanner(s, error)
    tokens = scanner.scan_tokens()
    parser = Parser(tokens, parse_error)
    statements = parser.parse()
    if hasError:
        return
    if hasRuntimeError:
        return
    interpreter = Interpreter()
    interpreter.interpret(statements)

def error(line, message):
    global hasError
    hasError = True
    report(line, "", message)

def parse_error(token, message):
    global hasError
    hasError = True
    if token.type == TokenType.EOF:
        report(token.line, " at end", message)
    else:
        report(token.line, f" at '{token.lexeme}'", message)


def report(lineno, where, message):
    print('[line {}] Error {}: {}'.format(lineno, where, message))

def run_time_error(error):
    global hasRuntimeError
    print('[line {}]'.format(error.token.line))
    hasRuntimeError = True

def run_file(filename):
    with open(filename) as f:
        s = f.read()
    run(s)

def run_prompt():
    while True:
        inp = input('> ')
        run(inp)


if __name__ == '__main__':
    _, *args = sys.argv

    if len(args) > 1:
        print("Usage: tlox [script]")
        sys.exit(64)
    elif len(args) == 1:
        run_file(args[0])
    else:
        run_prompt()
