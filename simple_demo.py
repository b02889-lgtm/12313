def greet(name):
    return f"Hello, {name}!"


def add(a, b):
    return a + b


def multiply(a, b):
    return a * b


def summarize_numbers(a, b):
    return {
        "a": a,
        "b": b,
        "sum": add(a, b),
        "product": multiply(a, b),
    }


def main():
    message = greet("Copilot")
    result = summarize_numbers(3, 5)

    print(message)
    print(f"{result['a']} + {result['b']} = {result['sum']}")
    print(f"{result['a']} * {result['b']} = {result['product']}")


if __name__ == "__main__":
    main()
