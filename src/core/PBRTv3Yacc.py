import sys
import PBRTv3Lex
import ply.yacc as yacc

# Get the token map
tokens = PBRTv3Lex.tokens

# RULES HERE

# scene directives
def p_integrator(t):
    'integrator : INTEGRATOR QUOTE ID QUOTE params'
    pass


# params and values
def p_params(t):
    '''params : empty
              | params param '''
    pass

def p_param(t):
    '''param : QUOTE INTEGER ID QUOTE value
             | QUOTE BOOL ID QUOTE value
             | QUOTE STRING ID QUOTE value 
             | QUOTE FLOAT ID QUOTE value
             | QUOTE RGB ID QUOTE value
             | QUOTE POINT ID QUOTE value
             | QUOTE NORMAL ID QUOTE value''' 
    pass

def p_value(t):
    '''value : empty'''

def p_empty(t):
    'empty : '
    pass

def p_error(t):
    print("Whoa. We're hosed")

import profile
# Build the grammar

parser = yacc.yacc()
#yacc.yacc(method='LALR',write_tables=False,debug=False)

#profile.run("yacc.yacc(method='LALR')")

def parse(data, debug=0):
    parser.error = 0
    p = parser.parse(data, debug=debug)
    if parser.error:
        return None
    return p

parse("Integrator \"path\" \"integer maxdepth\"")
