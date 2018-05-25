import sys
import operator
import LuxLex
import ply.yacc as yacc

# Get the token map
tokens = LuxLex.tokens

start = 'scene'

# scene
def p_scene(t):
    '''scene : directives worldblock
             | directives
             | worldblock'''

    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[0] = [t[1],t[2]]

# scene directives
def p_directives(t):
    '''directives : directives directive
                  | directive '''
    if len(t) > 2:
        t[0] = t[1]
        t[0].append(t[2])
    else:
        t[0] = [t[1]] 

def p_directive(t):
    '''directive : RENDERER SCONST
                 | INTEGRATOR SCONST params
                 | FILM SCONST params
                 | SAMPLER SCONST params
                 | FILTER SCONST params
                 | CAMERA SCONST params
                 | TRANSFORM matrix
                 | INCLUDE SCONST'''

    if len(t) == 3:
        if t[1] == 'Renderer' or t[1] == 'Include':
            t[0] = (t[1], eval(t[2]), None)
        else:
            t[0] = (t[1], None, t[2])
    else:
        t[0] = (t[1], eval(t[2]), t[3])

def p_worldblock(t):
    'worldblock : WORLDBEGIN objects WORLDEND'
    t[0] = t[2]

def p_objects(t):
    '''objects : objects object
               | objects ATTRIBUTEBEGIN objects ATTRIBUTEEND
               | objects TRANSFORMBEGIN objects TRANSFORMEND
               | object '''

    if len(t) == 5:
        t[0] = t[1]
        t[0].append((t[2], t[3]))
    elif len(t) == 3:
        t[0] = t[1]
        t[0].append(t[2])
    else:
        t[0] = [t[1]]

def p_object(t):
    '''object : SHAPE SCONST params
              | MAKENAMEDMATERIAL SCONST params
              | MATERIAL SCONST params
              | NAMEDMATERIAL SCONST
              | TEXTURE SCONST SCONST SCONST params
              | LIGHTSOURCE SCONST params
              | AREALIGHTSOURCE SCONST params
              | TRANSFORM matrix
              | empty'''

    if len(t) == 2:
        t[0] = t[1]
    elif len(t) == 3:
        if t[1] == 'Transform':
            t[0] = (t[1], None, t[2]) 
        else:
            t[0] = (t[1], eval(t[2]), None)
    elif len(t) == 4:
        t[0] = (t[1], eval(t[2]), t[3])
    else:
        t[0] = (t[1], eval(t[2]), eval(t[3]), eval(t[4]), t[5])

# params and values
def p_params(t):
    '''params : params param
              | param '''
    
    if len(t) > 2:
        t[0] = t[1]
        t[0].append(t[2])
    else:
        t[0] = [t[1]] 

def p_param(t):
    '''param : SCONST value
             | empty ''' 

    if len(t) > 2:
        param = t[1].split(' ')
        t[0] = (param[0].replace('"', ''), param[1].replace('"',''), t[2])

def p_value(t):
    '''value : LBRACKET ICONST RBRACKET
             | LBRACKET FCONST RBRACKET
             | LBRACKET SCONST RBRACKET
             | LBRACKET QUOTE TRUE QUOTE RBRACKET
             | LBRACKET QUOTE FALSE QUOTE RBRACKET
             | matrix
             | empty'''

    if len(t) > 4:
        t[0] = t[3]
    elif len(t) == 4:
        t[0] = eval(t[2])
    elif len(t) == 2:
        t[0] = t[1]

def p_matrix(t):
    '''matrix : LBRACKET number number number number number number number number number number number number number number number number number number number number number number number number number number number number number number number number number number number number RBRACKET
              | LBRACKET number number number number number number number number number number number number number number number number number number number number number number number number RBRACKET
              | LBRACKET number number number number number number number number number number number number number number number number RBRACKET
              | LBRACKET number number number number number number number number number number number number RBRACKET
              | LBRACKET number number number number number number number number RBRACKET
              | LBRACKET number number number number number number RBRACKET
              | LBRACKET number number number RBRACKET'''

    if len(t) == 6:
        t[0] = [t[2], t[3], t[4]]
    elif len(t) == 9:
        t[0] = [t[2], t[3], t[4], t[5], t[6], t[7]]
    elif len(t) == 11:
        t[0] = [t[2], t[3], t[4], t[5], t[6], t[7], t[8], t[9]]
    elif len(t) == 15:
        t[0] = [t[2], t[3], t[4], t[5], t[6], t[7], t[8], t[9], t[10], t[11], t[12], t[13]]
    elif len(t) == 19:
        t[0] = [t[2], t[3], t[4], t[5], t[6], t[7], t[8], t[9], t[10], t[11], t[12], t[13], t[14], t[15], t[16], t[17]]
    elif len(t) == 27:
        t[0] = [t[2], t[3], t[4], t[5], t[6], t[7], t[8], t[9], 
                t[10], t[11], t[12], t[13], t[14], t[15], t[16], t[17],
                t[18], t[19], t[20], t[21], t[22], t[23], t[24], t[25]]
    else:
        t[0] = [t[2], t[3], t[4], t[5], t[6], t[7], t[8], t[9], t[10], t[11], t[12], t[13], 
                t[14], t[15], t[16], t[17], t[18], t[19], t[20], t[21], t[22], t[23], t[24], t[25],
                t[26], t[27], t[28], t[29], t[30], t[31], t[32], t[33], t[34], t[35], t[36], t[37]]


def p_number(t):
    '''number : ICONST
              | FCONST'''
              
    t[0] = eval(t[1])

def p_empty(t):
    'empty : '

def p_error(t):
    print str(t) + "Whoa. We're hosed"

import profile

# Build the grammar
parser = yacc.yacc()

def parse(data, debug=0):
    parser.error = 0
    p = parser.parse(data, debug=debug)
    if parser.error:
        return None
    return p

# debug rules :D 
# while 1:
#     try:
#         s = raw_input('>>> ')
#     except EOFError:
#         break
#     if not s:
#         continue
#     b = parser.parse(s)
#     print 'parsed: ' + str(b)
