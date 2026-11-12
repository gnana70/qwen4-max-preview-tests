def evaluate(expr: str) -> float:
    if not isinstance(expr, str):
        raise ValueError("expression must be a string")

    text = expr
    length = len(text)
    pos = 0

    def skip_spaces():
        nonlocal pos
        while pos < length and text[pos].isspace():
            pos += 1

    def parse_number():
        nonlocal pos
        skip_spaces()
        start = pos
        seen_digit = False

        while pos < length and '0' <= text[pos] <= '9':
            pos += 1
            seen_digit = True

        if pos < length and text[pos] == '.':
            pos += 1
            while pos < length and '0' <= text[pos] <= '9':
                pos += 1
                seen_digit = True

        if not seen_digit:
            raise ValueError("invalid number")

        try:
            return float(text[start:pos])
        except OverflowError:
            return float('inf')
        except ValueError:
            raise ValueError("invalid number")

    def parse_primary():
        nonlocal pos
        skip_spaces()

        if pos >= length:
            raise ValueError("unexpected end of expression")

        if text[pos] == '(':
            pos += 1
            value = parse_expression()
            skip_spaces()

            if pos >= length or text[pos] != ')':
                raise ValueError("missing closing parenthesis")

            pos += 1
            return value

        return parse_number()

    def apply_power(base, exponent):
        try:
            result = base ** exponent
        except ZeroDivisionError:
            raise ValueError("division by zero")
        except OverflowError:
            if base < 0:
                try:
                    exp_value = float(exponent)
                except (TypeError, ValueError):
                    raise ValueError("invalid power")

                if not exp_value.is_integer():
                    raise ValueError("invalid power")

                try:
                    if int(exp_value) % 2 == 1:
                        return float('-inf')
                except Exception:
                    pass

            return float('inf')
        except (TypeError, ValueError):
            raise ValueError("invalid power")

        if isinstance(result, complex):
            raise ValueError("invalid power")

        try:
            return float(result)
        except (OverflowError, TypeError, ValueError):
            raise ValueError("invalid result")

    def parse_power():
        nonlocal pos
        base = parse_primary()
        skip_spaces()

        if pos < length and text[pos] == '^':
            pos += 1
            exponent = parse_unary()
            return apply_power(base, exponent)

        return base

    def parse_unary():
        nonlocal pos
        skip_spaces()

        sign = 1.0
        while pos < length and text[pos] == '-':
            sign = -sign
            pos += 1
            skip_spaces()

        value = parse_power()
        return -value if sign < 0 else value

    def parse_multiplicative():
        nonlocal pos
        value = parse_unary()

        while True:
            skip_spaces()

            if pos < length and text[pos] in '*/':
                op = text[pos]
                pos += 1
                right = parse_unary()

                if op == '*':
                    value = value * right
                else:
                    try:
                        value = value / right
                    except ZeroDivisionError:
                        raise ValueError("division by zero")
            else:
                break

        return value

    def parse_expression():
        nonlocal pos
        value = parse_multiplicative()

        while True:
            skip_spaces()

            if pos < length and text[pos] in '+-':
                op = text[pos]
                pos += 1
                right = parse_multiplicative()

                if op == '+':
                    value = value + right
                else:
                    value = value - right
            else:
                break

        return value

    try:
        result = parse_expression()
    except ValueError:
        raise
    except Exception as exc:
        raise ValueError("invalid expression") from exc

    skip_spaces()
    if pos != length:
        raise ValueError("unexpected trailing characters")

    try:
        return float(result)
    except Exception as exc:
        raise ValueError("invalid result") from exc