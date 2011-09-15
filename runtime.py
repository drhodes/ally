# >  arrow
# >> compose
# +> if_true
# -> if_false




class GraphMachine(object):
    def __init__(self):        
        self.params = {}
        self.funcs = {}
        self.vars = {}

    def error(self, line):
        pass

    def add_param

    def add_arrow(self, src, artype, tgt, line):
        pass

    def add_declaration(self, src, artype, tgt, line):
        pass
    
    def add_compose(self, src, tgt):
        pass

    def add_cond_true(self, src, tgt):
        pass

    def add_cond_false(self, src, tgt):
        pass

    def run(self):
        print "Running!"
        pass
