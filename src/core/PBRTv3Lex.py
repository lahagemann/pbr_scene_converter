import sys
sys.path.insert(0, "../..")

import ply.lex as lex

# Reserved words
reserved = (
    'INTEGRATOR', 'TRANSFORM', 'SAMPLER', 'FILTER', 'FILM', 'CAMERA',
    'WORLDBEGIN', 'WORLDEND', 'ATTRIBUTEBEGIN', 'ATTRIBUTEEND', 'TRANSFORMBEGIN', 'TRANSFORMEND',
    'MAKENAMEDMATERIAL', 'NAMEDMATERIAL', 'MATERIAL', 'SHAPE', 'TEXTURE', 'AREALIGHTSOURCE', 'LIGHTSOURCE',
    'INTEGER', 'BOOL', 'STRING', 'FLOAT', 'RGB', 'POINT', 'NORMAL'
)

tokens = reserved + (
    # Literals (identifier, integer constant, float constant, string constant,
    # char const)
    'ID', 'ICONST', 'FCONST', 'MCONST',

    # Delimeters ( ) [ ] { } , . ; :
    'LBRACKET', 'RBRACKET', 'QUOTE'
)

# Completely ignored characters
t_ignore = ' \t\x0c'

# Newlines

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

# Delimeters
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_QUOTE = r'\"'

# Identifiers and reserved words

reserved_map = {
    'Integrator': 'INTEGRATOR', 'Transform': 'TRANSFORM', 'Sampler': 'SAMPLER', 'Filter': 'FILTER', 'Film': 'FILM', 'Camera': 'CAMERA',
    'WorldBegin': 'WORLDBEGIN', 'WorldEnd': 'WORLDEND', 'AttributeBegin': 'ATTRIBUTEBEGIN', 'AttributeEnd': 'ATTRIBUTEEND', 
    'TransformBegin': 'TRANSFORMBEGIN', 'TransformEnd': 'TRANSFORMEND',
    'MakeNamedMaterial': 'MAKENAMEDMATERIAL', 'NamedMaterial': 'NAMEDMATERIAL', 'Material': 'MATERIAL', 'Shape': 'SHAPE', 'Texture': 'TEXTURE', 
    'AreaLightSource': 'AREALIGHTSOURCE', 'LightSource': 'LIGHTSOURCE',
    'integer': 'INTEGER', 'bool': 'BOOL', 'string': 'STRING', 'float': 'FLOAT', 'rgb': 'RGB', 'point': 'POINT', 'normal': 'NORMAL'
}
for r in reserved:
    reserved_map[r.lower()] = r

def t_ID(t):
    r'[A-Za-z_][\w_]*'
    t.type = reserved_map.get(t.value, "ID")
    return t

# Integer literal
t_ICONST = r'[+|-]?\d+'

# Floating literal
t_FCONST = r'[+|-]?((\d+)(\.\d+)(e(\+|-)?(\d+))? | [+|-]?(\d+)e(\+|-)?(\d+))([lL]|[fF])?'

# Matrix literal
t_MCONST = r'\[ ([+|-]?\d+ )+ \]'

# Comments


def t_comment(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')


def t_preprocessor(t):
    r'\#(.)*?\n'
    t.lexer.lineno += 1


def t_error(t):
    print("Illegal character %s" % repr(t.value[0]))
    t.lexer.skip(1)

lexer = lex.lex()
if __name__ == "__main__":
    lex.runmain(lexer)
