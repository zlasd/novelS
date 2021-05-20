import argparse

from manager import TaskManager

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--option", type=str, help="choose your option")
args = parser.parse_args()

def main():
    # new manager
    manager = TaskManager(args.option)
    # run the task
    manager.run()


if __name__ == '__main__':
    main()