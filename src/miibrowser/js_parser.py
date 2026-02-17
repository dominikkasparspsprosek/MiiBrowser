"""
JavaScript Parser utility using esprima for full JavaScript parsing capabilities
"""

import esprima
from typing import Dict, List, Tuple, Optional, Any, Set
import json


class JSParser:
    """
    Full-featured JavaScript parser using esprima
    
    This class provides methods to parse JavaScript code, extract functions,
    variables, classes, and analyze code structure.
    """
    
    def __init__(self):
        """Initialize the JavaScript parser"""
        self.ast = None
        self.source_code = None
        self.parse_options = {
            'jsx': False,
            'range': True,
            'loc': True,
            'tolerant': True,
            'tokens': False,
            'comment': False
        }
    
    def parse(self, code: str, jsx: bool = False, tolerant: bool = True) -> Dict[str, Any]:
        """
        Parse JavaScript code and return AST
        
        Args:
            code: JavaScript code as string
            jsx: Enable JSX parsing (default: False)
            tolerant: Continue parsing after errors (default: True)
            
        Returns:
            Abstract Syntax Tree (AST) as dictionary
        """
        self.source_code = code
        options = self.parse_options.copy()
        options['jsx'] = jsx
        options['tolerant'] = tolerant
        
        try:
            self.ast = esprima.parseScript(code, options)
            return self.ast.toDict()
        except Exception as e:
            # Try parsing as module if script parsing fails
            try:
                self.ast = esprima.parseModule(code, options)
                return self.ast.toDict()
            except:
                raise ValueError(f"Failed to parse JavaScript: {str(e)}")
    
    def parse_module(self, code: str, jsx: bool = False) -> Dict[str, Any]:
        """
        Parse JavaScript as ES6 module
        
        Args:
            code: JavaScript module code
            jsx: Enable JSX parsing
            
        Returns:
            AST dictionary
        """
        self.source_code = code
        options = self.parse_options.copy()
        options['jsx'] = jsx
        
        self.ast = esprima.parseModule(code, options)
        return self.ast.toDict()
    
    def tokenize(self, code: str) -> List[Dict[str, Any]]:
        """
        Tokenize JavaScript code
        
        Args:
            code: JavaScript code as string
            
        Returns:
            List of tokens
        """
        tokens = esprima.tokenize(code, {'range': True, 'loc': True})
        return [token.toDict() for token in tokens]
    
    def extract_functions(self, code: str = None) -> List[Dict[str, Any]]:
        """
        Extract all function declarations and expressions
        
        Args:
            code: JavaScript code (uses last parsed if None)
            
        Returns:
            List of function information dictionaries
        """
        if code:
            self.parse(code)
        
        if not self.ast:
            return []
        
        functions = []
        self._traverse_ast(self.ast.toDict(), functions, 'function')
        return functions
    
    def extract_variables(self, code: str = None) -> List[Dict[str, Any]]:
        """
        Extract all variable declarations
        
        Args:
            code: JavaScript code (uses last parsed if None)
            
        Returns:
            List of variable information dictionaries
        """
        if code:
            self.parse(code)
        
        if not self.ast:
            return []
        
        variables = []
        self._traverse_ast(self.ast.toDict(), variables, 'variable')
        return variables
    
    def extract_classes(self, code: str = None) -> List[Dict[str, Any]]:
        """
        Extract all class declarations
        
        Args:
            code: JavaScript code (uses last parsed if None)
            
        Returns:
            List of class information dictionaries
        """
        if code:
            self.parse(code)
        
        if not self.ast:
            return []
        
        classes = []
        self._traverse_ast(self.ast.toDict(), classes, 'class')
        return classes
    
    def extract_imports(self, code: str = None) -> List[Dict[str, Any]]:
        """
        Extract all import statements (ES6 modules)
        
        Args:
            code: JavaScript code (uses last parsed if None)
            
        Returns:
            List of import information dictionaries
        """
        if code:
            try:
                self.parse_module(code)
            except:
                self.parse(code)
        
        if not self.ast:
            return []
        
        imports = []
        self._traverse_ast(self.ast.toDict(), imports, 'import')
        return imports
    
    def extract_exports(self, code: str = None) -> List[Dict[str, Any]]:
        """
        Extract all export statements (ES6 modules)
        
        Args:
            code: JavaScript code (uses last parsed if None)
            
        Returns:
            List of export information dictionaries
        """
        if code:
            try:
                self.parse_module(code)
            except:
                self.parse(code)
        
        if not self.ast:
            return []
        
        exports = []
        self._traverse_ast(self.ast.toDict(), exports, 'export')
        return exports
    
    def get_all_identifiers(self, code: str = None) -> Set[str]:
        """
        Get all unique identifiers used in code
        
        Args:
            code: JavaScript code (uses last parsed if None)
            
        Returns:
            Set of identifier names
        """
        if code:
            self.parse(code)
        
        if not self.ast:
            return set()
        
        identifiers = set()
        self._collect_identifiers(self.ast.toDict(), identifiers)
        return identifiers
    
    def analyze_complexity(self, code: str = None) -> Dict[str, Any]:
        """
        Analyze code complexity metrics
        
        Args:
            code: JavaScript code (uses last parsed if None)
            
        Returns:
            Dictionary with complexity metrics
        """
        if code:
            self.parse(code)
        
        if not self.ast:
            return {}
        
        ast_dict = self.ast.toDict()
        
        metrics = {
            'functions': len(self.extract_functions()),
            'variables': len(self.extract_variables()),
            'classes': len(self.extract_classes()),
            'lines': code.count('\n') + 1 if code else 0,
            'statements': self._count_statements(ast_dict),
            'loops': self._count_loops(ast_dict),
            'conditionals': self._count_conditionals(ast_dict),
            'depth': self._calculate_depth(ast_dict)
        }
        
        return metrics
    
    def validate_syntax(self, code: str) -> Tuple[bool, Optional[str]]:
        """
        Validate JavaScript syntax
        
        Args:
            code: JavaScript code to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            esprima.parseScript(code, {'tolerant': False})
            return (True, None)
        except Exception as e:
            return (False, str(e))
    
    def detect_module_type(self, code: str) -> str:
        """
        Detect module type (CommonJS, ES6, or none)
        
        Args:
            code: JavaScript code
            
        Returns:
            'commonjs', 'es6', or 'none'
        """
        has_require = 'require(' in code
        has_module_exports = 'module.exports' in code or 'exports.' in code
        has_import = 'import ' in code and ' from ' in code
        has_export = 'export ' in code
        
        if has_import or has_export:
            return 'es6'
        elif has_require or has_module_exports:
            return 'commonjs'
        else:
            return 'none'
    
    def extract_comments(self, code: str) -> List[Dict[str, Any]]:
        """
        Extract all comments from JavaScript code
        
        Args:
            code: JavaScript code
            
        Returns:
            List of comment dictionaries
        """
        try:
            result = esprima.parseScript(code, {'comment': True, 'range': True})
            return [comment.toDict() for comment in result.comments] if hasattr(result, 'comments') else []
        except:
            return []
    
    def get_function_names(self, code: str = None) -> List[str]:
        """
        Get list of all function names
        
        Args:
            code: JavaScript code (uses last parsed if None)
            
        Returns:
            List of function names
        """
        functions = self.extract_functions(code)
        names = []
        for func in functions:
            if 'name' in func and func['name']:
                names.append(func['name'])
        return names
    
    def get_variable_names(self, code: str = None) -> List[str]:
        """
        Get list of all variable names
        
        Args:
            code: JavaScript code (uses last parsed if None)
            
        Returns:
            List of variable names
        """
        variables = self.extract_variables(code)
        names = []
        for var in variables:
            if 'name' in var and var['name']:
                names.append(var['name'])
        return names
    
    def get_class_names(self, code: str = None) -> List[str]:
        """
        Get list of all class names
        
        Args:
            code: JavaScript code (uses last parsed if None)
            
        Returns:
            List of class names
        """
        classes = self.extract_classes(code)
        names = []
        for cls in classes:
            if 'name' in cls and cls['name']:
                names.append(cls['name'])
        return names
    
    def find_dependencies(self, code: str) -> Dict[str, List[str]]:
        """
        Find all dependencies (require/import statements)
        
        Args:
            code: JavaScript code
            
        Returns:
            Dictionary with 'imports' and 'requires' lists
        """
        dependencies = {
            'imports': [],
            'requires': []
        }
        
        # Extract ES6 imports
        imports = self.extract_imports(code)
        for imp in imports:
            if 'source' in imp:
                dependencies['imports'].append(imp['source'])
        
        # Extract CommonJS requires using tokens
        tokens = self.tokenize(code)
        for i, token in enumerate(tokens):
            if token.get('type') == 'Identifier' and token.get('value') == 'require':
                # Look for the next string token
                for j in range(i + 1, min(i + 5, len(tokens))):
                    if tokens[j].get('type') == 'String':
                        # Remove quotes from string value
                        value = tokens[j].get('value', '').strip('\'"')
                        if value:
                            dependencies['requires'].append(value)
                        break
        
        return dependencies
    
    def to_json(self, code: str = None, indent: int = 2) -> str:
        """
        Convert AST to JSON string
        
        Args:
            code: JavaScript code to parse (uses last parsed if None)
            indent: JSON indentation level
            
        Returns:
            JSON string representation of AST
        """
        if code:
            self.parse(code)
        
        if not self.ast:
            return "{}"
        
        return json.dumps(self.ast.toDict(), indent=indent)
    
    def _traverse_ast(self, node: Any, results: List, target_type: str):
        """Traverse AST and collect nodes of specific type"""
        if not isinstance(node, dict):
            return
        
        node_type = node.get('type', '')
        
        # Function extraction
        if target_type == 'function':
            if node_type == 'FunctionDeclaration':
                func_info = {
                    'type': 'FunctionDeclaration',
                    'name': node.get('id', {}).get('name') if node.get('id') else None,
                    'params': [p.get('name') for p in node.get('params', []) if isinstance(p, dict) and p.get('name')],
                    'async': node.get('async', False),
                    'generator': node.get('generator', False)
                }
                results.append(func_info)
            elif node_type == 'FunctionExpression':
                func_info = {
                    'type': 'FunctionExpression',
                    'name': node.get('id', {}).get('name') if node.get('id') else None,
                    'params': [p.get('name') for p in node.get('params', []) if isinstance(p, dict) and p.get('name')],
                    'async': node.get('async', False),
                    'generator': node.get('generator', False)
                }
                results.append(func_info)
            elif node_type == 'ArrowFunctionExpression':
                func_info = {
                    'type': 'ArrowFunctionExpression',
                    'name': None,
                    'params': [p.get('name') for p in node.get('params', []) if isinstance(p, dict) and p.get('name')],
                    'async': node.get('async', False)
                }
                results.append(func_info)
        
        # Variable extraction
        elif target_type == 'variable':
            if node_type == 'VariableDeclaration':
                for declarator in node.get('declarations', []):
                    if isinstance(declarator, dict):
                        var_info = {
                            'kind': node.get('kind'),
                            'name': declarator.get('id', {}).get('name') if declarator.get('id') else None
                        }
                        results.append(var_info)
        
        # Class extraction
        elif target_type == 'class':
            if node_type == 'ClassDeclaration':
                class_info = {
                    'type': 'ClassDeclaration',
                    'name': node.get('id', {}).get('name') if node.get('id') else None,
                    'superClass': node.get('superClass', {}).get('name') if node.get('superClass') else None
                }
                results.append(class_info)
            elif node_type == 'ClassExpression':
                class_info = {
                    'type': 'ClassExpression',
                    'name': node.get('id', {}).get('name') if node.get('id') else None,
                    'superClass': node.get('superClass', {}).get('name') if node.get('superClass') else None
                }
                results.append(class_info)
        
        # Import extraction
        elif target_type == 'import':
            if node_type == 'ImportDeclaration':
                import_info = {
                    'source': node.get('source', {}).get('value'),
                    'specifiers': []
                }
                for spec in node.get('specifiers', []):
                    if isinstance(spec, dict):
                        spec_type = spec.get('type')
                        if spec_type == 'ImportDefaultSpecifier':
                            import_info['specifiers'].append({
                                'type': 'default',
                                'local': spec.get('local', {}).get('name')
                            })
                        elif spec_type == 'ImportSpecifier':
                            import_info['specifiers'].append({
                                'type': 'named',
                                'imported': spec.get('imported', {}).get('name'),
                                'local': spec.get('local', {}).get('name')
                            })
                        elif spec_type == 'ImportNamespaceSpecifier':
                            import_info['specifiers'].append({
                                'type': 'namespace',
                                'local': spec.get('local', {}).get('name')
                            })
                results.append(import_info)
        
        # Export extraction
        elif target_type == 'export':
            if node_type in ['ExportDefaultDeclaration', 'ExportNamedDeclaration', 'ExportAllDeclaration']:
                export_info = {
                    'type': node_type,
                    'source': node.get('source', {}).get('value') if node.get('source') else None
                }
                results.append(export_info)
        
        # Recursively traverse child nodes
        for key, value in node.items():
            if isinstance(value, dict):
                self._traverse_ast(value, results, target_type)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        self._traverse_ast(item, results, target_type)
    
    def _collect_identifiers(self, node: Any, identifiers: Set[str]):
        """Recursively collect all identifiers"""
        if not isinstance(node, dict):
            return
        
        if node.get('type') == 'Identifier':
            name = node.get('name')
            if name:
                identifiers.add(name)
        
        for key, value in node.items():
            if isinstance(value, dict):
                self._collect_identifiers(value, identifiers)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        self._collect_identifiers(item, identifiers)
    
    def _count_statements(self, node: Any) -> int:
        """Count total statements in AST"""
        if not isinstance(node, dict):
            return 0
        
        count = 1 if 'Statement' in node.get('type', '') else 0
        
        for key, value in node.items():
            if isinstance(value, dict):
                count += self._count_statements(value)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        count += self._count_statements(item)
        
        return count
    
    def _count_loops(self, node: Any) -> int:
        """Count loop statements"""
        if not isinstance(node, dict):
            return 0
        
        node_type = node.get('type', '')
        count = 1 if node_type in ['ForStatement', 'ForInStatement', 'ForOfStatement', 'WhileStatement', 'DoWhileStatement'] else 0
        
        for key, value in node.items():
            if isinstance(value, dict):
                count += self._count_loops(value)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        count += self._count_loops(item)
        
        return count
    
    def _count_conditionals(self, node: Any) -> int:
        """Count conditional statements"""
        if not isinstance(node, dict):
            return 0
        
        node_type = node.get('type', '')
        count = 1 if node_type in ['IfStatement', 'ConditionalExpression', 'SwitchStatement'] else 0
        
        for key, value in node.items():
            if isinstance(value, dict):
                count += self._count_conditionals(value)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        count += self._count_conditionals(item)
        
        return count
    
    def _calculate_depth(self, node: Any, current_depth: int = 0) -> int:
        """Calculate maximum nesting depth"""
        if not isinstance(node, dict):
            return current_depth
        
        max_depth = current_depth
        
        for key, value in node.items():
            if isinstance(value, dict):
                depth = self._calculate_depth(value, current_depth + 1)
                max_depth = max(max_depth, depth)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        depth = self._calculate_depth(item, current_depth + 1)
                        max_depth = max(max_depth, depth)
        
        return max_depth


# Utility functions for quick JavaScript operations

def parse_javascript(code: str, jsx: bool = False) -> Dict[str, Any]:
    """
    Quick function to parse JavaScript code
    
    Args:
        code: JavaScript code as string
        jsx: Enable JSX parsing
        
    Returns:
        AST dictionary
    """
    parser = JSParser()
    return parser.parse(code, jsx=jsx)


def validate_javascript(code: str) -> Tuple[bool, Optional[str]]:
    """
    Quick function to validate JavaScript syntax
    
    Args:
        code: JavaScript code to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    parser = JSParser()
    return parser.validate_syntax(code)


def extract_functions(code: str) -> List[str]:
    """
    Quick function to extract function names
    
    Args:
        code: JavaScript code
        
    Returns:
        List of function names
    """
    parser = JSParser()
    return parser.get_function_names(code)


def extract_variables(code: str) -> List[str]:
    """
    Quick function to extract variable names
    
    Args:
        code: JavaScript code
        
    Returns:
        List of variable names
    """
    parser = JSParser()
    return parser.get_variable_names(code)


def get_dependencies(code: str) -> Dict[str, List[str]]:
    """
    Quick function to find all dependencies
    
    Args:
        code: JavaScript code
        
    Returns:
        Dictionary with imports and requires
    """
    parser = JSParser()
    return parser.find_dependencies(code)


# Example usage and testing
if __name__ == "__main__":
    # Example JavaScript
    example_js = """
    // Import statements
    import React from 'react';
    import { useState, useEffect } from 'react';
    
    // Class declaration
    class Calculator {
        constructor() {
            this.result = 0;
        }
        
        add(x, y) {
            return x + y;
        }
    }
    
    // Function declaration
    function greet(name) {
        console.log('Hello, ' + name);
    }
    
    // Arrow function
    const multiply = (a, b) => a * b;
    
    // Variables
    const PI = 3.14159;
    let counter = 0;
    var oldStyle = 'deprecated';
    
    // Async function
    async function fetchData(url) {
        const response = await fetch(url);
        return response.json();
    }
    
    // Export
    export { Calculator, greet, multiply };
    export default fetchData;
    """
    
    # Test the parser
    parser = JSParser()
    
    print("=" * 70)
    print("MiiBrowser JavaScript Parser - Example Usage")
    print("=" * 70)
    print()
    
    # Parse code
    print("1. Parsing JavaScript...")
    try:
        ast = parser.parse_module(example_js)
        print(f"   ✓ Successfully parsed {len(example_js)} characters")
    except Exception as e:
        print(f"   ✗ Parse error: {e}")
    print()
    
    # Extract functions
    print("2. Extracting functions...")
    functions = parser.extract_functions()
    for func in functions:
        print(f"   - {func['type']}: {func['name'] or '(anonymous)'} ({', '.join(func['params'])})")
    print()
    
    # Extract variables
    print("3. Extracting variables...")
    variables = parser.extract_variables()
    for var in variables[:5]:  # Show first 5
        print(f"   - {var['kind']}: {var['name']}")
    print()
    
    # Extract classes
    print("4. Extracting classes...")
    classes = parser.extract_classes()
    for cls in classes:
        superclass = f" extends {cls['superClass']}" if cls['superClass'] else ""
        print(f"   - {cls['name']}{superclass}")
    print()
    
    # Extract imports/exports
    print("5. Extracting imports...")
    imports = parser.extract_imports()
    for imp in imports:
        print(f"   - from '{imp['source']}'")
    print()
    
    print("6. Extracting exports...")
    exports = parser.extract_exports()
    print(f"   - Found {len(exports)} export statements")
    print()
    
    # Analyze complexity
    print("7. Analyzing complexity...")
    metrics = parser.analyze_complexity()
    for key, value in metrics.items():
        print(f"   - {key}: {value}")
    print()
    
    # Find dependencies
    print("8. Finding dependencies...")
    deps = parser.find_dependencies(example_js)
    print(f"   - ES6 imports: {len(deps['imports'])}")
    print(f"   - CommonJS requires: {len(deps['requires'])}")
    print()
    
    print("=" * 70)
    print("All tests completed successfully!")
    print("=" * 70)
