import ast
import os
from collections import defaultdict

# Mapea funciones con el formato: { 'modulo.funcion': [ 'funcion_llamada1', 'funcion_llamada2' ] }
call_graph = defaultdict(list)
function_definitions = {}

def extract_function_calls(file_path, module_name):
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            tree = ast.parse(f.read(), filename=file_path)
        except SyntaxError as e:
            print(f"Error en {file_path}: {e}")
            return

    class FunctionCallVisitor(ast.NodeVisitor):
        def __init__(self):
            self.current_func = None

        def visit_FunctionDef(self, node):
            full_name = f"{module_name}.{node.name}"
            function_definitions[full_name] = node
            self.current_func = full_name
            self.generic_visit(node)

        def visit_Call(self, node):
            if self.current_func:
                if isinstance(node.func, ast.Name):
                    call_graph[self.current_func].append(node.func.id)
                elif isinstance(node.func, ast.Attribute):
                    call_graph[self.current_func].append(node.func.attr)
            self.generic_visit(node)

    FunctionCallVisitor().visit(tree)

def scan_project(path):
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith('.py'):
                full_path = os.path.join(root, file)
                # Creamos un nombre de módulo ficticio con base en la ruta
                relative = os.path.relpath(full_path, path).replace(os.sep, ".")
                module_name = os.path.splitext(relative)[0]
                extract_function_calls(full_path, module_name)

def build_call_tree(start_func, depth=0, visited=None):
    if visited is None:
        visited = set()
    if start_func in visited:
        return  # evitar recursión infinita
    visited.add(start_func)

    indent = "  " * depth
    print(f"{indent}- {start_func}")
    for callee in call_graph.get(start_func, []):
        for full_func_name in function_definitions:
            if full_func_name.endswith(f".{callee}"):
                build_call_tree(full_func_name, depth + 1, visited)

# 🔁 USO:
# Cambia este path por la ruta raíz de tu proyecto
proyecto_path = "./mi_proyecto"  # <- ajusta esto

scan_project(proyecto_path)

# Puedes listar todas las funciones encontradas
print("\n📦 Funciones encontradas:")
for f in function_definitions:
    print(f)

# Mostrar árbol desde una función principal
print("\n🌳 Árbol de llamadas desde 'main.main' (por ejemplo):")
build_call_tree("main.main")