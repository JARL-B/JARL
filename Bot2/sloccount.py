import os

def sloccount_py(root='.'):
    files = []
    for r, d, f in os.walk(root):
        for name in f:
            files.append('{}/{}'.format(r, name))

    sloc = 0
    for fn in files:
        if fn.endswith('py'):
            with open(fn, 'r') as f:
                for line in f:
                    if line.strip():
                        sloc += 1

    return sloc
