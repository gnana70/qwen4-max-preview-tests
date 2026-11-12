import math


def _tokenize(text: str) -> list:
    tokens = []
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if ch.isspace():
            i += 1
        elif ch in "+-*/^()":
            tokens.append(ch)
            i += 1
        elif ch in "0123456789.":
            start = i
            seen_dot = False
            while i < n and text[i] in "0123456789.":
                if text[i] == ".":
                    if seen_dot:
                        raise ValueError("invalid number: more than one decimal point")
                    seen_dot = True
                i += 1
            literal = text[start:i]
            if literal == ".":
                raise ValueError("invalid number: lone decimal point")
            tokens.append(float(literal))
        else:
            raise ValueError("invalid character: " + repr(ch))
    return tokens


def evaluate(expr: str) -> float:
    """Evaluate an arithmetic expression.

    Grammar (loosest to tightest binding):
        expr  := term (('+' | '-') term)*
        term  := unary (('*' | '/') unary)*
        unary := ('+' | '-') unary | power
        power := atom ('^' unary)?          # right-associative
        atom  := NUMBER | '(' expr ')'

    Unary minus binds looser than '^', so -2^2 == -4, while 2^-2 == 0.25.
    """
    if not isinstance(expr, str):
        raise ValueError("expression must be a string")

    tokens = _tokenize(expr)
    if not tokens:
        raise ValueError("empty expression")

    pos = 0

    def peek():
        return tokens[pos] if pos < len(tokens) else None

    def advance():
        nonlocal pos
        pos += 1

    def parse_expr():
        value = parse_term()
        while peek() in ("+", "-"):
            op = peek()
            advance()
            rhs = parse_term()
            value = value + rhs if op == "+" else value - rhs
        return value

    def parse_term():
        value = parse_unary()
        while peek() in ("*", "/"):
            op = peek()
            advance()
            rhs = parse_unary()
            if op == "*":
                value = value * rhs
            else:
                if rhs == 0:
                    raise ValueError("division by zero")
                value = value / rhs
        return value

    def parse_unary():
        op = peek()
        if op == "-":
            advance()
            return -parse_unary()
        if op == "+":
            advance()
            return parse_unary()
        return parse_power()

    def parse_power():
        base = parse_atom()
        if peek() == "^":
            advance()
            exponent = parse_unary()
            return math.pow(base, exponent)
        return base

    def parse_atom():
        tok = peek()
        if isinstance(tok, float):
            advance()
            return tok
        if tok == "(":
            advance()
            value = parse_expr()
            if peek() != ")":
                raise ValueError("expected closing parenthesis")
            advance()
            return value
        raise ValueError("expected a number or '(', got " + repr(tok))

    result = parse_expr()
    if pos != len(tokens):
        raise ValueError("unexpected trailing token: " + repr(peek()))
    return result