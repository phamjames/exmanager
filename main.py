import sys
from manager import *

_debug = False

def cr(man,*args):
    args_list = args[0]
    p = int(args_list[0])
    return man.create(p)

def de(man, *args):
    args_list = args[0]
    i = int(args_list[0])
    found = 0
    for c in man._get_running_proc().children:

        if c.num == i:
            found = 1
    if found != 1:
        print("-1", end=' ')
    return man.destroy(i) if found == 1 else False

def rq(man, *args):
    args_list = args[0]
    r,k = int(args_list[0]), int(args_list[1])
    return man.request(r,k)

def rl(man, *args):
    args_list = args[0]
    r, k = int(args_list[0]), int(args_list[1])
    return man.release(r,k)

def to(man):
    return man.timeout()

def init():
    return Manager()


def parse_commands(file_name):
    with open(file_name, 'r') as f:
        content = f.readlines()
        content = [line.strip().split(" ") for line in content]
        return content


func_dict = {"cr": cr, "de":de, "rq": rq, "rl":rl, "to":to, "in":init}

def main():
    sys.stdout = open('output.txt', 'wt')
    command_list = parse_commands(sys.argv[1])
    manager = None
    command_num = 1
    for item in command_list:
        command = item[0]
        args = item[1:]

        if command in func_dict.keys():
            if command == "in":
                manager = func_dict[command]()
                print()
                manager.display_current_running()
                continue

            if not manager:
                continue
            else:
                if _debug:
                    print("command num {} -> {} ".format(command_num,command))

                val = func_dict[command](manager) if args == [] else func_dict[command](manager,args)
                # print()
                # print("COMMAND CALLED:" ,command,args)
                # print("h: ",[c.num for c in manager.ready_list.high])
                # print("m: ",[c.num for c in manager.ready_list.med])
                # print("l: ",[c.num for c in manager.ready_list.low])
                # print()
                # print("current proc running ",end='')
                if val == True or val == None: manager.display_current_running()
                # print("resource list of current = ", [(r.type,r.state) for r in manager._get_running_proc().resources])

                if _debug:
                    print("rl ",[x.num for x in manager.ready_list.get_all()])
                    print("pl ",[(x.num,x.priority) for x in manager._PCB_list if x != -1])
        command_num +=1










if __name__ == "__main__":
    main()
