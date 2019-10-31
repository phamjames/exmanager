import sys
from manager import *


def cr(man):
    return man.create()

def de(man, i):
    return man.destroy(i)

def rq(man, r):
    return man.request(r)

def rl(man, r):
    return man.release(r)

def to(man):
    return man.timeout()

def init(man):
    return Manager()


def print_contents(file_name):
    with open(file_name, 'r') as f:
        contents = f.read()
    print(contents)

func_dict = {"cr": cr, "de":de, "rq": rq, "rl":rl, "to":to, "in":init}


def main():
    print_contents(sys.argv[1])











if __name__ == "__main__":
    main()
