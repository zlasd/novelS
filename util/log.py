

def log_debug(msg: str):
    print(msg)


def log_info(msg: str):
    print(msg)


def log_error(msg: str, ex: Exception = None):
    print(msg)


def write(msg: str):
    with open('log.txt', 'w', encoding='utf-8', errors='ignore') as f:
        f.write(msg)
