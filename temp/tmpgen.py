from runtime import *


def apply ():
    __gm__ = GraphMachine()
    __gm__.add_param('func', 'f', './temp/tmpfile-pass-3.ally:2')
    __gm__.add_param('var', 'x', './temp/tmpfile-pass-3.ally:2')
    __gm__.add_arrow('f', '>', 'ap', './temp/tmpfile-pass-3.ally:3')
    __gm__.add_arrow('x', '>', 'ap', './temp/tmpfile-pass-3.ally:4')
    __gm__.add_arrow('ap', '>', 'return', './temp/tmpfile-pass-3.ally:5')
    return __gm__.run()

def fact ():
    __gm__ = GraphMachine()
    __gm__.add_param('var', 'n', './temp/tmpfile-pass-3.ally:7')
    __gm__.add_param('func', 'f', './temp/tmpfile-pass-3.ally:7')
    __gm__.add_declaration('var', 'tmp', 1, './temp/tmpfile-pass-3.ally:8')
    __gm__.add_arrow('min1', '>', 'n', './temp/tmpfile-pass-3.ally:9')
    __gm__.add_arrow('n', '>', 'min1', './temp/tmpfile-pass-3.ally:10')
    __gm__.add_arrow('n', '>', 'mul', './temp/tmpfile-pass-3.ally:11')
    __gm__.add_arrow('mul', '>', 'tmp', './temp/tmpfile-pass-3.ally:12')
    __gm__.add_arrow('tmp', '>', 'mul', './temp/tmpfile-pass-3.ally:13')
    __gm__.add_arrow('tmp', '>', 'dup', './temp/tmpfile-pass-3.ally:14')
    __gm__.add_arrow('dup', '>', 'return', './temp/tmpfile-pass-3.ally:15')
    __gm__.add_arrow('n', '>', 'gt1', './temp/tmpfile-pass-3.ally:16')
    __gm__.add_arrow('gt1', '+>', 'min1', './temp/tmpfile-pass-3.ally:17')
    __gm__.add_arrow('gt1', '->', 'dup', './temp/tmpfile-pass-3.ally:18')
    return __gm__.run()

def main ():
    __gm__ = GraphMachine()

    __gm__.add_declaration('var', 'msg', "asdf", './temp/tmpfile-pass-3.ally:21')
    __gm__.add_arrow('msg', '>', 'sys.out', './temp/tmpfile-pass-3.ally:22')
    return __gm__.run()
if __name__ == '__main__': main()