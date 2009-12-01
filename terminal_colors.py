import os
import sys

hist = []


def actually_write():
    global hist
    sys.stdout.write("\x1b[%sm" % (";".join(hist)))

def o(msg):
    global hist
    msg = "%02i"%msg
    hist.append(msg)
    actually_write()

def undo():
    global hist
    hist.pop()
    actually_write()

def reset():
    global hist
    hist=[]
    sys.stdout.write("\x1bc\x1b[!p\x1b[?3;4l\x1b[4l\x1b>")
    default()

def default():
    o(10) # just in case someone called o(12) by mistake :P
    o(0)

def clear():
    sys.stdout.write("\x1b[H\x1b[2J")

def move(y, x):
    sys.stdout.write("\x1b[%i;%iH" % (y + 1, x + 1))

def up():
    sys.stdout.write("\x1b[A")

def down():
    sys.stdout.write("\x1b[B")

def right():
    sys.stdout.write("\x1b[C")

def left():
    sys.stdout.write("\x1b[D")

def endline():
    sys.stdout.write("\x1b[K")

def cursorinvisible():
    sys.stdout.write("\x1b[?25l")

def cursornormal():
    sys.stdout.write("\x1b[?12l\x1b[?25h")

def cursorveryvisible():
    sys.stdout.write("\x1b[?12;25h")

def deletelines(lines=1):
    sys.stdout.write("'\x1b[%iM" % lines)

def scrolldown():
    sys.stdout.write("\x1bM")

def cols():
    return int(os.popen("tput cols").read().strip())

def lines():
    return int(os.popen("tput lines").read().strip())

def savecursor():
    sys.stdout.write("\x1b7")

def restorecursor():
    sys.stdout.write("\x1b8")


colors = ('black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white')

RESET = '0'
opt_dict = {
    'bold': '1',
    'hidden': '2',
    'underscore': '4',
    'blink': '5',
    'reverse': '7',
    'conceal': '8',
}

#def bold():      o(1)
for name, key in opt_dict.iteritems():
    exec 'def {name}(): o({key})'.format(name=name, key=key)

# def black():     o(30)
for key, name in enumerate(colors):
    exec 'def {name}(): o(3{key})'.format(name=name, key=key)

# def bgred():     o(41)
for key, name in enumerate(colors):
    exec 'def bg{name}(): o(4{key})'.format(name=name, key=key)


def formatting():
    o(12)


def put(line, indent, msg):
    move(line, indent)
    sys.stdout.write(msg)

def center(line, msg):
    columns = cols()
    indent  = (columns-len(msg)) / 2
    put(line, indent, msg)
    return line, indent + len(msg)


def wrap(line, msg, rmargin=0, lmargin=0):
    line_length = (cols() - lmargin) - rmargin
    msg         = list(msg)
    curr_indent = 0
    curr_line   = line
    char        = msg.pop(0)
    while 1:
        if line_length-curr_indent<1:
            put(curr_line, lmargin + curr_indent, '\n')
            curr_line  += 1
            curr_indent = 0
            put(curr_line, lmargin, char)
        else:
            put(curr_line, lmargin + curr_indent, char)
            curr_indent +=1
            if len(msg) == 0:
                break
            char = msg.pop(0)
    return curr_line, lmargin + curr_indent


def wordwrap(line, msg, rmargin=0, lmargin=0):
    line_length = (cols() - lmargin) - rmargin
    msg = msg.split()
    curr_indent = 0
    curr_line = line
    word = msg.pop(0)
    while 1:
        if line_length < len(word):                     # word is longer than allowed line
            put(curr_line, lmargin, word[:line_length]) # wrap by letter
            word = word[line_length:]
            put(curr_line, lmargin + curr_indent, '\n')
            curr_line  += 1
            curr_indent = 0
        elif line_length - curr_indent < len(word):     # word cannot fit on remainder
            put(curr_line, lmargin + curr_indent, '\n') # of line -- wrap by word
            curr_line  += 1
            curr_indent = 0
            put(curr_line, lmargin, word)
        else:                                           # word fits on line
            put(curr_line, lmargin + curr_indent, word)
            curr_indent += len(word) + 1
            if len(msg) == 0:
                break
            word = msg.pop(0)
    return curr_line, lmargin + curr_indent

def main():
    reset()
    bgblue()
    white()
    bold()
    clear()
    reverse()
    center(5,' Windows ')
    undo()
    line, col = wordwrap(7, "Windows crashed again. I am the Blue Screen of Death. No one hears your screams.", lmargin=7, rmargin=8)
    print
    put(line + 2, 11, "*")
    line, col = wordwrap(line + 2, "Press any key to terminate the application.", lmargin=14, rmargin=8)
    put(line + 1, 11, "*")
    line, col = wordwrap(line + 1, "Press CTRL+ALT+DEL again to restart your computer. You will lose any unsaved data in all applications.", lmargin=14, rmargin=8)
    line, col = center(line+3,"Press any key to continue")
    move(line, col + 1)
    endline()
    raw_input()
    reset()

if __name__=="__main__":
    main()
