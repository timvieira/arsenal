normal = '\033[0m%s\033[0m'
bold = '\033[1m%s\033[0m'

black, red, green, yellow, blue, magenta, cyan, white = \
    map('\033[3%sm%%s\033[0m'.__mod__, range(8))

light_black, light_red, light_green, light_yellow, light_blue, light_magenta, light_cyan, light_white = \
    map('\033[1;3%sm%%s\033[0m'.__mod__, range(8))

bg_black, bg_red, bg_green, bg_yellow, bg_blue, bg_magenta, bg_cyan, bg_white = \
    map('\033[4%sm%%s\033[0m'.__mod__, range(8))

def test():
    for c in 'black, red, green, yellow, blue, magenta, cyan, white'.split(', '):
        print globals()[c] % c
        print globals()['light_' + c] % ('light_' + c)

    for c in 'black, red, green, yellow, blue, magenta, cyan, white'.split(', '):
        print globals()['bg_' + c] % c

if __name__ == '__main__':
    test()
