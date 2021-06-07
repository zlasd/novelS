

def log_debug(msg: str, *args):
    print(msg, *args)


def log_info(msg: str, *args):
    print(msg, *args)


def log_error(msg: str, ex: Exception = None):
    print(msg)


def write(msg: str, path="log0.log"):
    with open(path, 'w', encoding='utf-8', errors='ignore') as f:
        f.write(msg)
