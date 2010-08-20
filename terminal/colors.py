
black, red, green, yellow, blue, magenta, cyan, white = map('\033[3%sm%%s\033[0m'.__mod__, range(8))

def test():
    for c in 'black, red, green, yellow, blue, magenta, cyan, white'.split(', '):
        print globals()[c] % c
