import sys
from manager import *


def cr(man,*args):
    p = int(args[0][0])
    print(p)
    man.create(p)

def de(man, *args):
    i = args[0]
    man.destroy(i)

def rq(man, *args):
    r,k = args[0],args[1]
    man.request(r,k)

def rl(man, *args):
    r,k = args[0],args[1]
    man.release(r,k)

def to(man):
    man.timeout()

def init():
    return Manager()


def parse_commands(file_name):
    with open(file_name, 'r') as f:
        content = f.readlines()
        content = [line.strip().split(" ") for line in content]
        return content


func_dict = {"cr": cr, "de":de, "rq": rq, "rl":rl, "to":to, "in":init}

def main():
    command_list = parse_commands(sys.argv[1])
    manager = None

    for item in command_list:
        command = item[0]
        args = item[1:]
        if command in func_dict.keys():
            if command == "in":
                manager = func_dict[command]()
                continue

            if not manager:
                print("-1")
                continue
            else:
                func_dict[command](manager) if args == [] else func_dict[command](manager,args)













if __name__ == "__main__":
    main()
