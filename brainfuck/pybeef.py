#!/usr/bin/python

import os, sys

DEBUG = bool(os.getenv('BF_DEBUG', False))
STDIN = bool(os.getenv('BF_STDIN', False))
PRINT_RANGE = 8

def parse(code, initstate=None):
    cells = [0]*256
    cursor = 0

    if initstate is not None:
        cells, cursor = initstate

    i=0
    while i<len(code):
        c = code[i]
        if c=='+':
            cells[cursor] += 1

        if c=='-':
            cells[cursor] -= 1

        if c=='>':
            cursor = ( cursor + 1 ) % 256

        if c=='<':
            cursor = ( cursor - 1 ) % 256

        if c=='.':
            sys.stdout.write(chr(cells[cursor]))

        if c==',':
            if STDIN:
                ch = sys.stdin.read(1)
                cells[cursor] = ord(ch) if ch!='' else 0
            else:
                inp = raw_input('cells[%d]=' % cursor)
                if len(inp)>1 and inp[0]=='#':
                    cells[cursor] = int(inp[1:], 0)
                else: 
                    cells[cursor] = ord(inp[0])

        if c==']':
            print 'Error during parsing'
            sys.exit(3)

        if c=='[':
            new_code = ''
            brackets = 1
            for j in range(i+1, len(code)):
                if code[j]=='[':
                    brackets+=1
                if code[j]==']':
                    brackets-=1
                if brackets==0:
                    break
                new_code += code[j]

            if brackets!=0:
                print 'Error during parsing (2)'
                sys.exit(4)
            i = j

            while cells[cursor]>0:
                cells, cursor = parse(new_code, (cells, cursor))

        if DEBUG:
            if c=='!':

                print '-'*8*PRINT_RANGE
                for n in range(0, 256, PRINT_RANGE):
                    print '\t'.join([str(e) for e in cells[n:n+PRINT_RANGE]])
                
                print '-'*8*PRINT_RANGE+'\n'

            if c=='*':
                print 'cells[%d]=%d' % (cursor, cells[cursor])

        i+=1

    return cells, cursor


def check_code(code):
    brackets = 0
    for i in range(0, len(code)):
        if code[i]==']':
            brackets-=1
        if code[i]=='[':
            brackets+=1

        if brackets<0:
            return False

    if brackets!=0:
        return False
    return True


if __name__=='__main__':
    if len(sys.argv)<2:
        print 'Usage: %s <file.bf>' % sys.argv[0]
        sys.exit(1)

    f = open(sys.argv[1], 'r')
    code = f.read()
    f.close()

    if not check_code(code):
        print 'Unbalances / misplaces brackets !'
        sys.exit(2)

    cells, cursor = parse(code)
