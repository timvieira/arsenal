from stemmer import *
from synset import *
from dictionary import *

def LCS(u,v):
    lcs = []
    for POS in [N, V, ADJ, ADV]:
        if (u not in POS) or (v not in POS):
            continue
        for x in POS[u]:
            for y in POS[v]:
                z = lcs_by_depth(x, y)
                #z = common_hypernyms(x,y)
                if z:
                    lcs.append(z)
    return lcs

def SYN(T,H):
    if T.strip().lower() == H.strip().lower():
        return True
    for POS in [N, V, ADJ, ADV]:
        if H not in POS:
            continue
        for x in POS[H].synsets():
            if T in x:
                return True
    return False

def ANT(T,H):
    for POS in [N, V, ADJ, ADV]:
        if H not in POS:
            continue
        for x in POS[H]:
            if T in x.relation(ANTONYM):
                return True
    return False

def ISA(T,H):
    if SYN(T,H):
        return 1
    isa = -1
    for POS in [N, V, ADJ, ADV]:
        if T not in POS:
            continue
        for i, sense in enumerate(POS[T]):
            for d, x in enumerate(sense.closure(HYPERNYM)):
                d = d + 1
                if H in x:
                    if isa == -1 or d < isa:
                        isa = d
    return isa

