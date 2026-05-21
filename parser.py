import tree_sitter_python as tspython
from tree_sitter import Language, Parser

PYTHON_LANGUAGE = Language(tspython.language())
parser = Parser(PYTHON_LANGUAGE)

code = b"""
def greet(name):
    print(f"Hello, {name}!")

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def say_hello(self):
        greet(self.name)

p = Person("Alice", 30)
p.say_hello()
"""

tree = parser.parse(code)

def traverse(node, indent=0):
    prefix = "  " * indent
    if node.child_count == 0:
        text = code[node.start_byte:node.end_byte].decode("utf-8", errors="replace")
        print(f"{prefix}{node.type}: {text}")
    else:
        print(f"{prefix}{node.type}")
        for child in node.children:
            traverse(child, indent + 1)

traverse(tree.root_node)
