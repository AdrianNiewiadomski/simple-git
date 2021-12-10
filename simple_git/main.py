import sys
from simple_git.simple_git_runner import SimplegitRunner


def main():
	exit(SimplegitRunner().run(sys.argv))
