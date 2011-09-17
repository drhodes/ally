import prelude

class Trans(object):
    def __init__(self, func, line):
        self.line = line
        self.content = None
        self.pyfunc = func
    def __repr__(self):
        return "<Trans %s>" % str(self.pyfunc)

    def __call__(self, *args):
        return self.pyfunc(args)

class AllyModule(object):
    def __init__(self, module_name):
        self.name = module_name
        self.ally_funcs = {}       

    def add_trans(self, func, line):
        self.ally_funcs[func.__name__] = Trans(func, line)

    def register_transitions(self):        
        for f in prelude.funcs:
            self.add_trans(f, "prelude")

    def run_main(self):
        pass
        
