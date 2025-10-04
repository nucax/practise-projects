# https://pastebin.com/zApmxvxX
import re

def tokenize(code):
    tokens = re.findall(r'[A-Za-z_]\w*|[0-9]+|=|\+|print', code)
    return tokens

def parse(tokens):
    ast = []
    i = 0
    while i < len(tokens):
        if tokens[i] == 'print':
            ast.append(('print', tokens[i+1]))
            i += 2
        elif tokens[i+1] == '=':
            var = tokens[i]
            value = tokens[i+2]
            if i+3 < len(tokens) and tokens[i+3] == '+':
                right = tokens[i+4]
                ast.append(('add', var, value, right))
                i += 5
            else:
                ast.append(('assign', var, value))
                i += 3
        else:
            i += 1
    return ast

def generate(ast):
    asm = []
    for node in ast:
        if node[0] == 'assign':
            asm.append(f"LOAD {node[2]}")
            asm.append(f"STORE {node[1]}")
        elif node[0] == 'add':
            asm.append(f"LOAD {node[2]}")
            asm.append(f"ADD {node[3]}")
            asm.append(f"STORE {node[1]}")
        elif node[0] == 'print':
            asm.append(f"PRINT {node[1]}")
    return "\n".join(asm)

# Example use
code = """
x = 5
y = x + 3
print y
"""

tokens = tokenize(code)
ast = parse(tokens)
assembly = generate(ast)

print("Tokens:", tokens)
print("\nAssembly:\n" + assembly)
