#!/usr/bin/python

import os, sys, random, time

random.seed(time.time())

# HELPERS
class Stack:

    def __init__(self):
        self.clear()        

    def clear(self):
        self.__elts = []

    def push(self, elt):
        self.__elts.append(elt)

    def pop(self):
        return 0 if self.size()==0 else self.__elts.pop()

    def size(self):
        return len(self.__elts)

    def __str__(self):
        return '['+' '.join([str(e) for e in self.__elts])+']'


class Coord:

    def __init__(self, x, y, x_max=0, y_max=0):
        self.__x = x
        self.__y = y
        self.__xmax = x_max
        self.__ymax = y_max

    def on(self, grid):
        return grid[self.__y][self.__x]

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

    def add(self, c):
        self.__x += c.getX()
        self.__y += c.getY()
    
        if self.__xmax != 0:
            self.__x = self.__x % self.__xmax

        if self.__ymax != 0:
            self.__y = self.__y % self.__ymax

def print_grid(grid):
    
    ret = ''
    tmp = ''
    for y in range(0, len(grid)):
        char = [ord(e) for e in grid[y]]
        if max(char)==32 and min(char)==32:
            tmp += ''.join(grid[y])+'\n'
        else:
            if tmp!='':
                ret+=tmp
                tmp =''

            ret += ''.join(grid[y])
            ret += ('\n')
    sys.stdout.write(ret + '\n')

RIGHT = Coord(1,0)
LEFT = Coord(-1,0)
UP = Coord(0,-1)
DOWN = Coord(0,1)
DIRECTIONS = {'^':UP, 'v':DOWN, '>':RIGHT, '<':LEFT}
# /HELPERS

DEBUG = bool(os.getenv('BFG_DEBUG', False))

# PARSING
def parse(code):

    lines = code.replace('\r','').split('\n')
    lines_lens = [len(l) for l in lines]

    height = 25 #min(25, len(lines))
    width = 80 #min(max(lines_lens), 80)

    grid = []

    for y in range(0, height):
        grid.append([])
        for x in range(0, width):
            if y>=len(lines_lens) or x>=lines_lens[y]:
                v = ' '
            else:
                v = lines[y][x]
            
            grid[y].append(v)

    # init
    stringMode = False
    pc = Coord(0, 0, width, height)
    stack = Stack()
    direction = RIGHT

    # run
    while True:

        if DEBUG:
            print 'Stack: %s\nCoords: (%d,%d)\nGrid:' % (str(stack), pc.getX(), pc.getY())
            print_grid(grid)

        c = pc.on(grid)

        if stringMode:
            if c=='"':
                stringMode = False
            else:
                stack.push(ord(c))
        else:
            if c in ['+','-','*','/','%', '`']:
                a = stack.pop()
                b = stack.pop()
            
                if c=='+':
                    stack.push(a+b)
                    
                if c=='-':
                    stack.push(b-a)

                if c=='*':
                    stack.push(a*b)

                if c=='/':
                    stack.push(b/a)

                if c=='%':
                    stack.push(b%a)

                if c=='`':
                    stack.push(1 if b>a else 0)

            if c=='!':
                v = stack.pop()
                stack.push(1 if v==0 else 0)

            if c in DIRECTIONS.keys():
                direction = DIRECTIONS[c]

            if c=='?':
                k = DIRECTIONS.keys()
                direction = DIRECTIONS[k[random.randint(0, len(k)-1)]]

            if c=='_':
                v = stack.pop()
                direction = RIGHT if v==0 else LEFT

            if c=='|':
                v = stack.pop()
                direction = DOWN if v==0 else UP

            if c==":":
                v = stack.pop()
                stack.push(v)
                stack.push(v)

            if c=='\\':
                a = stack.pop()
                b = stack.pop()
                stack.push(a)
                stack.push(b)

            if c=='$':
                stack.pop()

            if c=='.':
                sys.stdout.write(str(stack.pop()))

            if c==',':
                sys.stdout.write(chr(stack.pop()%256))

            if c=='#':
                pc.add(direction)

            if c=='@':
                break;

            if c in ['0','1','2','3','4','5','6','7','8','9']:
                stack.push(int(c,10))

            if c=='"':
                stringMode = True

            if c=='~':
                v = sys.stdin.read(1)
                stack.push(-1 if v=='' else ord(v))

            if c=='&':
                stack.push(int(raw_input('> ')))

            if c=='g':
                y = stack.pop()
                x = stack.pop()
                if x>=width or y>=height or x<0 or y<0:
                    stack.push(0)
                else:
                    stack.push(ord(grid[y][x]))

            if c=='p':
                y = stack.pop()
                x = stack.pop()
                v = stack.pop()

                if not (x>=width or y>=height or x<0 or y<0):
                    grid[y][x] = chr(v%256)

        pc.add(direction)

# MAIN
if __name__=='__main__':

    if len(sys.argv)<2:
        print 'Usage: python %s <file.bfg>'
        sys.exit(1)

    f = open(sys.argv[1], 'r')
    code = f.read()
    f.close()

    parse(code)
