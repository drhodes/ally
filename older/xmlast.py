# XML AST for pyPEG 1.3

from xml.sax.saxutils import escape
from pyPEG import Symbol

def pyAST2XML(pyAST):
    if isinstance(pyAST, unicode) or isinstance(pyAST, str):
        return escape(pyAST)
    if type(pyAST) is Symbol:
        result = u"<" + pyAST[0].replace("_", "-") + u">"
        for e in pyAST[1:]:
            result += pyAST2XML(e)
        result += u"</" + pyAST[0].replace("_", "-") + u">"
    else:
        result = u""
        for e in pyAST:
            result += pyAST2XML(e)
    return result
