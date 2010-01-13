import pyclbr   # parse a python module and describe its classes and methods
import pprint


misc_clbr = pyclbr.readmodule('lib.misc')
pprint.pprint(misc_clbr)

misc_clbr = pyclbr.readmodule('lib.nlp.wordnet.cache')
pprint.pprint(misc_clbr)



import inspect

def print_class_tree(tree, indent=-1):
    if isinstance(tree, list):
        for node in tree:
            print_class_tree(node, indent+1)
    else:
        print '  ' * indent, tree[0].__name__
    return

def is_class(x):
    return hasattr(x, '__bases__')

if __name__ == '__main__':

    import nltk

    X = filter(is_class, nltk.classify.__dict__.values())
    print_class_tree(inspect.getclasstree(X))


    print '------------------------------------------'
    print inspect.getcomments(nltk.classify)


    print '***************'
    print inspect.getdoc(nltk.classify).strip() == nltk.classify.__doc__.strip()

