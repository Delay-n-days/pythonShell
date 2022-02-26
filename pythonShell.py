import os
import pickle
import string


class Node(object):
    def __init__(self, name: string, isfile: bool, dirs=[], text="", isroot=False):
        self.dirs = dirs
        self.name = name
        self.isfile = isfile
        self.text = text
        self.isroot = isroot


class FindMsg(object):
    def __init__(self, findRes: bool, findMsg: str, findResNode: Node):
        self.findRes = findRes
        self.findMsg = findMsg
        self.findResNode = findResNode


class WorkMsg(object):
    def __init__(self, Node: Node):
        self.Node = Node
        self.Path = []
        self.Path.append(Node)

    def cd(self, dir_name: string):
        if (dir_name == ".."):
            find = False
            if (self.Node.isroot is True):
                return
            else:
                self.Path.pop()
                self.Node = self.Path[len(self.Path) - 1]
        else:
            findres = self.find(dir_name, False)
            if findres.findRes is True:
                self.Node = findres.findResNode
                self.Path.append(self.Node)
            else:
                print(findres.findMsg)

    def ls(self):
        if self.Node.dirs is None:
            print("")
        else:
            for i in self.Node.dirs:
                print(i.name + " ")

    def pwd(self):
        print(self.getpath())

    def mkdir(self, dir_name: string):
        findres = self.find(dir_name, False)
        if findres.findRes is False:
            newdir = Node(name=dir_name, isfile=False)
            self.Node.dirs.append(newdir)
        else:
            print("cannot create directory ‘" + dir_name + "’: File exists")

    def touch(self, file_name: string):
        newdir = Node(name=file_name, isfile=True)
        self.Node.dirs.append(newdir)

    def echo(
        self,
        str: string,
        file_name: string,
    ):
        findres = self.find(file_name, True)
        if findres.findRes is True:
            findres.findResNode.text += str
        else:
            print(findres.findMsg)

    def cat(self, file_name: string):
        findres = self.find(file_name, True)
        if findres.findRes is True:
            print(findres.findResNode.text)
        else:
            print(findres.findMsg)

    def show(self):
        print(self.getpath() + "#", end=" ")

    def getpath(self):
        if len(self.Path) > 1:
            str = 'root@ubuntu:'
        else:
            str = 'root@ubuntu:/'
        for i in self.Path:
            if (i.name != self.Path[0].name):
                str += "/" + i.name
        return str

    def find(self, find_name: string, isfile: bool) -> FindMsg:
        find = False
        FindNode = None
        findMsg = "cd: " + find_name + ": No such file or directory"
        if self.Node.dirs is None:
            find = False
        else:
            for i in self.Node.dirs:
                if i.name == find_name:
                    if (i.isfile is isfile):
                        FindNode = i
                        find = True
                        break
                    else:
                        if isfile is True:
                            findMsg = find_name + ": is a directory"
                        else:
                            findMsg = find_name + ": Not a directory"
                        find = False
                        break
        FindRes = FindMsg(findRes=find, findMsg=findMsg, findResNode=FindNode)
        return FindRes

    def save(self):
        fn = 'a.pkl'
        with open(fn, 'wb') as f:
            picklestring = pickle.dump(self, f)


root = Node(name="", isfile=True, isroot=True)
Work = None
if os.path.exists('a.pkl'):
    fn = 'a.pkl'
    with open(fn, 'rb') as f:
        Work = pickle.load(f)  # read file and build object
else:
    Work = WorkMsg(root)
root.dirs = [Node(name="root", isfile=False, dirs=[
    Node(name="work", isfile=False, text="da", dirs=[
        Node(
            name="work1",
            isfile=False,
        ),
        Node(name="a.txt", isfile=True, text="hello world"),
    ]),
    Node(name="photo", isfile=False, dirs=[Node(name="happy.jpg", isfile=True, text="(～￣▽￣)～")]),
]), Node(
    name="home",
    isfile=False,
)]

while True:
    Work.show()
    ss = input()
    arg = ss.split(" ")
    if (arg[0] == "cd"):
        Work.cd(arg[1])
    elif (arg[0] == "ls"):
        Work.ls()
    elif (arg[0] == "pwd"):
        Work.pwd()
    elif (arg[0] == "mkdir"):
        Work.mkdir(arg[1])
    elif (arg[0] == "touch"):
        Work.touch(arg[1])
    elif (arg[0] == "echo"):
        Work.echo(arg[1], arg[2])
    elif (arg[0] == "cat"):
        Work.cat(arg[1])
    elif (arg[0] == "exit"):
        Work.save()
        break
    else:
        print()
