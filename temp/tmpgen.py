from runtime import *
from ally_module import *


def add0 ():
    __gm__ = GraphMachine('add0', '      // :::: ./temp/tmpfile-pass-3.ally:2')
    __gm__.add_param('var', 'a', './temp/tmpfile-pass-3.ally:2')
    __gm__.add_declaration('var', 'b', 1, './temp/tmpfile-pass-3.ally:3')
    __gm__.add_arrow('add', '>', 'return', './temp/tmpfile-pass-3.ally:4')
    __gm__.add_arrow('a', '>', 'add', './temp/tmpfile-pass-3.ally:5')
    __gm__.add_arrow('b', '>', 'add', './temp/tmpfile-pass-3.ally:6')
    return __gm__.run()

def foo ():
    __gm__ = GraphMachine('foo', '      // :::: ./temp/tmpfile-pass-3.ally:8')
    __gm__.add_param('var', 'a', './temp/tmpfile-pass-3.ally:8')
    __gm__.add_param('var', 'b', './temp/tmpfile-pass-3.ally:8')
    __gm__.add_arrow('add', '>', 'return', './temp/tmpfile-pass-3.ally:9')
    __gm__.add_arrow('a', '>', 'add', './temp/tmpfile-pass-3.ally:10')
    __gm__.add_arrow('b', '>', 'add', './temp/tmpfile-pass-3.ally:11')
    return __gm__.run()

def main ():
    __gm__ = GraphMachine('main', '      // :::: ./temp/tmpfile-pass-3.ally:13')
    __gm__.add_param('var', 'n', './temp/tmpfile-pass-3.ally:13')
    __gm__.add_declaration('var', 'tmp', 1, './temp/tmpfile-pass-3.ally:14')
    __gm__.add_arrow('n', '>', 'mul', './temp/tmpfile-pass-3.ally:15')
    __gm__.add_arrow('mul', '>', 'tmp', './temp/tmpfile-pass-3.ally:16')
    __gm__.add_arrow('tmp', '>', 'mul', './temp/tmpfile-pass-3.ally:17')
    __gm__.add_arrow('tmp', '>', 'id', './temp/tmpfile-pass-3.ally:18')
    __gm__.add_arrow('id', '>>', 'add0', './temp/tmpfile-pass-3.ally:19')
    __gm__.add_arrow('add0', '>', 'return', './temp/tmpfile-pass-3.ally:20')
    __gm__.add_arrow('n', '>', 'min1', './temp/tmpfile-pass-3.ally:21')
    __gm__.add_arrow('min1', '>', 'n', './temp/tmpfile-pass-3.ally:22')
    __gm__.add_arrow('gt1', '+>', 'min1', './temp/tmpfile-pass-3.ally:23')
    __gm__.add_arrow('gt1', '->', 'id', './temp/tmpfile-pass-3.ally:24')
    __gm__.add_arrow('n', '>', 'gt1', './temp/tmpfile-pass-3.ally:25')
    return __gm__.run()
if __name__ == '__main__':
    am = AllyModule('math')
    am.add_trans(add0, '// :::: ./temp/tmpfile-pass-3.ally:2')
    am.add_trans(foo, '// :::: ./temp/tmpfile-pass-3.ally:8')
    am.add_trans(main, '// :::: ./temp/tmpfile-pass-3.ally:13')
    am.register_transitions()
    am.run_main()
