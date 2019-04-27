import doctest

import model

mods_to_test = [
    model
]

if __name__ == '__main__':
    for mod in mods_to_test:
        doctest.testmod(mod, verbose=True)
