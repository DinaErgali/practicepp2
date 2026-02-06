def my_function(n):
    if isinstance(n, str):
        return "Hello, World!"
    elif isinstance(n, int):
        return 10
    elif isinstance(n, bool):
        return True
    elif isinstance(n, complex):
        return 100j
    elif isinstance(n, list):
        return [1, 2, 3]
    elif isinstance(n, tuple):
        return (1, 2, 3)
    elif isinstance(n, dict):
        return {"Name": "Alice", "Age": 25}
    else:
        return None