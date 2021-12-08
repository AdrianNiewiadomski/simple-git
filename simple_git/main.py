import sys


def main():
	command = sys.argv[1]
	parameters = sys.argv[2:]
	print("command: ", command)
	print("parameters: ", str(parameters))


if __name__ == "__main__":
	exit(main())
