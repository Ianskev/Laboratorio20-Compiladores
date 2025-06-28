import ast
import re
from functools import reduce

OPERATIONS = {
    ast.Add: lambda x, y: x + y,
    ast.Sub: lambda x, y: x - y,
    ast.Mult: lambda x, y: x * y,
    ast.Div: lambda x, y: x // y,
}

class ExpressionEvaluator:
    """Evaluates constant expressions safely using AST"""
    
    @staticmethod
    def evaluate(expression_str):
        """Try to evaluate a string expression to a constant value"""
        try:
            tree = ast.parse(expression_str.strip(), mode='eval')
            return ExpressionEvaluator._evaluate_node(tree)
        except Exception:
            return None
            
    @staticmethod
    def _evaluate_node(node):
        """Recursively evaluate an AST node"""
        if isinstance(node, ast.Expression):
            return ExpressionEvaluator._evaluate_node(node.body)
            
        if isinstance(node, ast.Num):
            return node.n
            
        if isinstance(node, ast.BinOp):
            left = ExpressionEvaluator._evaluate_node(node.left)
            right = ExpressionEvaluator._evaluate_node(node.right)
            
            op_type = type(node.op)
            if op_type in OPERATIONS:
                return OPERATIONS[op_type](left, right)
            else:
                raise TypeError(f"Unsupported operator: {op_type}")
                
        if isinstance(node, ast.UnaryOp):
            if isinstance(node.op, ast.USub):
                return -ExpressionEvaluator._evaluate_node(node.operand)
            else:
                raise TypeError(f"Unsupported unary operator: {type(node.op)}")
            
        if isinstance(node, ast.Call):
            raise ValueError(f"Function calls are not supported")
                
        raise TypeError(f"Unsupported node type: {type(node)}")

class CodeOptimizer:
    """Handles code optimization techniques"""
    
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.result_lines = []
        self.invariant_code = []
        self.hoisted_variables = set()
        self.in_main = False
        self.in_loop = False
        
    def optimize(self):
        """Main optimization function"""
        with open(self.input_file, 'r') as source:
            source_lines = source.readlines()
        
        for line in source_lines:
            self._process_line(line)
            
        with open(self.output_file, 'w') as dest:
            dest.writelines(self.result_lines)
    
    def _process_line(self, line):
        """Process a single line of code"""
        clean_line = line.strip()
        

        if clean_line.startswith("fun") and "main()" in clean_line:
            self.in_main = True
            self.result_lines.append(line)
            return
            
        if clean_line == "endfun":
            if self.in_main and self.invariant_code:
                insertion_point = 0
                for i, l in enumerate(self.result_lines):
                    if "var int" in l:
                        insertion_point = i + 1
                        
                for inv_code in self.invariant_code:
                    self.result_lines.insert(insertion_point, f"{inv_code}\n")
                    insertion_point += 1
                    
            self.in_main = False
            self.in_loop = False
            self.result_lines.append(line)
            return
            
        if "while" in clean_line and "do" in clean_line:
            self.in_loop = True
            self.result_lines.append(line)
            return
            
        if clean_line == "endwhile;":
            self.in_loop = False
            self.result_lines.append(line)
            return
        
        if self.in_loop and "=" in clean_line:
            variable, expression = self._parse_assignment(clean_line)
            if variable and expression:
                constant_value = ExpressionEvaluator.evaluate(expression)
                if constant_value is not None and variable not in self.hoisted_variables:
                    indentation = line[:len(line) - len(line.lstrip())]
                    self.invariant_code.append(f"{indentation}{variable} = {constant_value};")
                    self.hoisted_variables.add(variable)
                    return 
        optimized_line = self._fold_constants(line)
        self.result_lines.append(optimized_line)
    
    def _parse_assignment(self, line):
        """Extract variable and expression from an assignment statement"""
        if "=" not in line:
            return None, None
            
        parts = line.split("=", 1)
        var_name = parts[0].strip()
        expression = parts[1].strip().rstrip(";")
        return var_name, expression
    
    def _fold_constants(self, line):
        """Replace constant expressions with their computed values"""
        modified_line = list(line)
        
        pattern = r'([=+\-*/<>=!]+)\s*([^;()\n]+)'
        matches = re.finditer(pattern, line)
        
        for match in reversed(list(matches)):
            expr = match.group(2).strip()
            result = ExpressionEvaluator.evaluate(expr)
            if result is not None:
                start_idx = match.start(2)
                end_idx = match.end(2)
                modified_line[start_idx:end_idx] = str(result)
                
        return ''.join(modified_line)

def optimize(input_path, output_path):
    """Perform code optimization on the given file"""
    optimizer = CodeOptimizer(input_path, output_path)
    optimizer.optimize()