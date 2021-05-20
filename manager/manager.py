from option import Option

class TaskManager:
    def __init__(self, opt_name: str):
        super().__init__()
        self.opt = Option(opt_name)

    def run(self):
        pass