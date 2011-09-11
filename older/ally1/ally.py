from functools import partial

def gen_sym_():
    global count
    count = 0
    def inner():
        global count
        count += 1
        return "_id" + str(count)
    return inner
gen_sym = gen_sym_()

def get_fields(rest, a):
    if a == ";":
        return rest
    else:
        return partial(get_fields, (rest+(["Field", a],)))

field = partial(get_fields, ())
    
#print field('x')('y')('z')(";")

def get_foo(word, arg):
    return partial(get_fields, (word, arg))
    
def get_struct(rest, arg):
    if arg == ";":
        return ("Struct", rest)
    else:
        return partial(get_struct, rest + (arg,))

struct = partial(get_foo, "Struct"+gen_sym())
print struct("Point")("x")("y")("z")(";")

struct Point x y z ;

if : eq x y then 3 else 5


#print get_fields("a")("b")(";")

'''
def struct(Name):
    return Name

print struct("Point")("x")("y")(";")
'''            








'''
struct Point x y ;

func square [ x ] [ mul x x ] ;

func dist [ x , y ] 
[ 
	let x2 = square x,
    let y2 = square y,
    return sqrt | add x2 y2
]
'''

