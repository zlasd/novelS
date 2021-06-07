import argparse

from manager import TaskManager

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--option", type=str,
                    default="first", help="choose your option")
parser.add_argument("-b", "--bookid", type=str, help="book id in the website")
parser.add_argument("-r", "--retry", type=int, default=3,
                    help="retry nums when encount HTTP error or anti-spider mechanism")
args = parser.parse_args()


def main():
    # new manager
    manager = TaskManager(args.option, args.bookid)
    # run the task
    manager.run()


if __name__ == '__main__':
    main()
