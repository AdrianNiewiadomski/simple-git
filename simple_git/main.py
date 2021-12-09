import sys
from simple_git import SimplegitRunner


def main():
	SimplegitRunner(sys.argv).run()


if __name__ == "__main__":
	exit(main())
