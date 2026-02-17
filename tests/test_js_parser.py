"""
Tests for JavaScript parser module
"""

import pytest
from miibrowser.js_parser import (
    JSParser,
    parse_javascript,
    validate_javascript,
    extract_functions,
    extract_variables,
    get_dependencies
)


class TestJSParser:
    """Test cases for JSParser class"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.parser = JSParser()
        self.sample_js = """
            function add(a, b) {
                return a + b;
            }
            
            const subtract = (x, y) => x - y;
            
            class Calculator {
                multiply(a, b) {
                    return a * b;
                }
            }
            
            let result = 0;
            const PI = 3.14;
            var name = 'test';
        """
    
    def test_parse_basic_code(self):
        """Test parsing basic JavaScript code"""
        ast = self.parser.parse(self.sample_js)
        assert ast is not None
        assert 'type' in ast
        assert ast['type'] == 'Program'
    
    def test_parse_empty_code(self):
        """Test parsing empty code"""
        ast = self.parser.parse("")
        assert ast is not None
    
    def test_parse_module(self):
        """Test parsing ES6 module"""
        code = "import foo from 'bar'; export default foo;"
        ast = self.parser.parse_module(code)
        assert ast is not None
        assert ast['type'] == 'Program'
        assert ast['sourceType'] == 'module'
    
    def test_tokenize(self):
        """Test JavaScript tokenization"""
        code = "const x = 42;"
        tokens = self.parser.tokenize(code)
        assert len(tokens) > 0
        assert tokens[0]['type'] == 'Keyword'
        assert tokens[0]['value'] == 'const'
    
    def test_extract_functions(self):
        """Test extracting function declarations"""
        functions = self.parser.extract_functions(self.sample_js)
        assert len(functions) >= 2
        func_names = [f['name'] for f in functions if f['name']]
        assert 'add' in func_names
    
    def test_extract_arrow_functions(self):
        """Test extracting arrow functions"""
        code = "const arrow = (x) => x * 2;"
        functions = self.parser.extract_functions(code)
        assert len(functions) >= 1
        assert any(f['type'] == 'ArrowFunctionExpression' for f in functions)
    
    def test_extract_async_functions(self):
        """Test extracting async functions"""
        code = "async function fetchData() { return await fetch(); }"
        functions = self.parser.extract_functions(code)
        assert len(functions) >= 1
        assert functions[0]['async'] == True
    
    def test_extract_variables(self):
        """Test extracting variable declarations"""
        variables = self.parser.extract_variables(self.sample_js)
        assert len(variables) >= 3
        var_names = [v['name'] for v in variables if v['name']]
        assert 'result' in var_names
        assert 'PI' in var_names
        assert 'name' in var_names
    
    def test_extract_const_variables(self):
        """Test extracting const variables"""
        variables = self.parser.extract_variables(self.sample_js)
        const_vars = [v for v in variables if v['kind'] == 'const']
        assert len(const_vars) > 0
    
    def test_extract_classes(self):
        """Test extracting class declarations"""
        classes = self.parser.extract_classes(self.sample_js)
        assert len(classes) >= 1
        assert classes[0]['name'] == 'Calculator'
    
    def test_extract_class_with_inheritance(self):
        """Test extracting class with inheritance"""
        code = "class Dog extends Animal { bark() {} }"
        classes = self.parser.extract_classes(code)
        assert len(classes) >= 1
        assert classes[0]['name'] == 'Dog'
        assert classes[0]['superClass'] == 'Animal'
    
    def test_extract_imports(self):
        """Test extracting import statements"""
        code = """
            import React from 'react';
            import { useState } from 'react';
            import * as Utils from './utils';
        """
        imports = self.parser.extract_imports(code)
        assert len(imports) == 3
        assert all(imp['source'] for imp in imports)
    
    def test_extract_default_import(self):
        """Test extracting default import"""
        code = "import React from 'react';"
        imports = self.parser.extract_imports(code)
        assert len(imports) == 1
        assert imports[0]['source'] == 'react'
    
    def test_extract_named_imports(self):
        """Test extracting named imports"""
        code = "import { foo, bar } from 'module';"
        imports = self.parser.extract_imports(code)
        assert len(imports) == 1
        assert len(imports[0]['specifiers']) == 2
    
    def test_extract_exports(self):
        """Test extracting export statements"""
        code = """
            export const foo = 42;
            export default function bar() {}
            export { baz };
        """
        exports = self.parser.extract_exports(code)
        assert len(exports) >= 3
    
    def test_get_all_identifiers(self):
        """Test getting all identifiers"""
        code = "const x = 1; function y() { return z; }"
        identifiers = self.parser.get_all_identifiers(code)
        assert 'x' in identifiers
        assert 'y' in identifiers
        assert 'z' in identifiers
    
    def test_analyze_complexity(self):
        """Test code complexity analysis"""
        code = """
            function test() {
                if (true) {
                    for (let i = 0; i < 10; i++) {
                        console.log(i);
                    }
                }
            }
        """
        metrics = self.parser.analyze_complexity(code)
        assert 'functions' in metrics
        assert 'loops' in metrics
        assert 'conditionals' in metrics
        assert metrics['loops'] >= 1
        assert metrics['conditionals'] >= 1
    
    def test_validate_syntax_valid(self):
        """Test validating valid JavaScript"""
        is_valid, error = self.parser.validate_syntax("const x = 42;")
        assert is_valid == True
        assert error is None
    
    def test_validate_syntax_invalid(self):
        """Test validating invalid JavaScript"""
        is_valid, error = self.parser.validate_syntax("const x = ;")
        assert is_valid == False
        assert error is not None
    
    def test_detect_module_es6(self):
        """Test detecting ES6 module"""
        code = "import foo from 'bar';"
        module_type = self.parser.detect_module_type(code)
        assert module_type == 'es6'
    
    def test_detect_module_commonjs(self):
        """Test detecting CommonJS module"""
        code = "const foo = require('bar'); module.exports = foo;"
        module_type = self.parser.detect_module_type(code)
        assert module_type == 'commonjs'
    
    def test_detect_module_none(self):
        """Test detecting no module system"""
        code = "const x = 42;"
        module_type = self.parser.detect_module_type(code)
        assert module_type == 'none'
    
    def test_extract_comments(self):
        """Test extracting comments"""
        code = """
            // Single line comment
            const x = 42;
            /* Multi-line
               comment */
            function test() {}
        """
        comments = self.parser.extract_comments(code)
        assert len(comments) >= 2
    
    def test_get_function_names(self):
        """Test getting function names"""
        functions = self.parser.get_function_names(self.sample_js)
        assert 'add' in functions
    
    def test_get_variable_names(self):
        """Test getting variable names"""
        variables = self.parser.get_variable_names(self.sample_js)
        assert 'result' in variables
        assert 'PI' in variables
    
    def test_get_class_names(self):
        """Test getting class names"""
        classes = self.parser.get_class_names(self.sample_js)
        assert 'Calculator' in classes
    
    def test_find_dependencies_es6(self):
        """Test finding ES6 dependencies"""
        code = "import foo from 'bar'; import { baz } from 'qux';"
        deps = self.parser.find_dependencies(code)
        assert len(deps['imports']) == 2
        assert 'bar' in deps['imports']
        assert 'qux' in deps['imports']
    
    def test_find_dependencies_commonjs(self):
        """Test finding CommonJS dependencies"""
        code = "const foo = require('bar'); const baz = require('qux');"
        deps = self.parser.find_dependencies(code)
        assert len(deps['requires']) == 2
        assert 'bar' in deps['requires']
        assert 'qux' in deps['requires']
    
    def test_to_json(self):
        """Test converting AST to JSON"""
        code = "const x = 42;"
        json_str = self.parser.to_json(code)
        assert json_str is not None
        assert '"type"' in json_str
        assert '"Program"' in json_str


class TestUtilityFunctions:
    """Test utility functions"""
    
    def test_parse_javascript(self):
        """Test parse_javascript utility"""
        ast = parse_javascript("const x = 42;")
        assert ast is not None
        assert ast['type'] == 'Program'
    
    def test_validate_javascript_valid(self):
        """Test validate_javascript with valid code"""
        is_valid, error = validate_javascript("const x = 42;")
        assert is_valid == True
        assert error is None
    
    def test_validate_javascript_invalid(self):
        """Test validate_javascript with invalid code"""
        is_valid, error = validate_javascript("const x = ;")
        assert is_valid == False
        assert error is not None
    
    def test_extract_functions_utility(self):
        """Test extract_functions utility"""
        code = "function foo() {} function bar() {}"
        functions = extract_functions(code)
        assert len(functions) == 2
        assert 'foo' in functions
        assert 'bar' in functions
    
    def test_extract_variables_utility(self):
        """Test extract_variables utility"""
        code = "const x = 1; let y = 2; var z = 3;"
        variables = extract_variables(code)
        assert len(variables) == 3
        assert 'x' in variables
        assert 'y' in variables
        assert 'z' in variables
    
    def test_get_dependencies_utility(self):
        """Test get_dependencies utility"""
        code = "import foo from 'bar'; const baz = require('qux');"
        deps = get_dependencies(code)
        assert 'bar' in deps['imports']
        assert 'qux' in deps['requires']


class TestAdvancedFeatures:
    """Test advanced JavaScript features"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.parser = JSParser()
    
    def test_template_literals(self):
        """Test parsing template literals"""
        code = "const msg = `Hello ${name}`;"
        ast = self.parser.parse(code)
        assert ast is not None
    
    def test_destructuring(self):
        """Test parsing destructuring"""
        code = "const { x, y } = obj; const [a, b] = arr;"
        ast = self.parser.parse(code)
        assert ast is not None
    
    def test_spread_operator(self):
        """Test parsing spread operator"""
        code = "const arr2 = [...arr1]; const obj2 = {...obj1};"
        ast = self.parser.parse(code)
        assert ast is not None
    
    def test_default_parameters(self):
        """Test parsing default parameters"""
        code = "function test(x = 0, y = 1) {}"
        functions = self.parser.extract_functions(code)
        assert len(functions) >= 1
    
    def test_rest_parameters(self):
        """Test parsing rest parameters"""
        code = "function sum(...numbers) {}"
        ast = self.parser.parse(code)
        assert ast is not None
    
    def test_generator_function(self):
        """Test parsing generator function"""
        code = "function* generator() { yield 1; }"
        functions = self.parser.extract_functions(code)
        assert len(functions) >= 1
        assert functions[0]['generator'] == True
    
    def test_class_methods(self):
        """Test parsing class methods"""
        code = """
            class Test {
                method1() {}
                static method2() {}
                async method3() {}
            }
        """
        classes = self.parser.extract_classes(code)
        assert len(classes) >= 1
    
    def test_object_shorthand(self):
        """Test parsing object shorthand"""
        code = "const obj = { x, y, method() {} };"
        ast = self.parser.parse(code)
        assert ast is not None
    
    def test_computed_property_names(self):
        """Test parsing computed property names"""
        code = "const obj = { [key]: value };"
        ast = self.parser.parse(code)
        assert ast is not None
    
    def test_optional_chaining(self):
        """Test parsing optional chaining"""
        code = "const value = obj?.prop?.nested;"
        ast = self.parser.parse(code)
        assert ast is not None
    
    def test_nullish_coalescing(self):
        """Test parsing nullish coalescing"""
        code = "const value = x ?? default;"
        ast = self.parser.parse(code)
        assert ast is not None
    
    def test_dynamic_import(self):
        """Test parsing dynamic import"""
        code = "const module = await import('./module.js');"
        ast = self.parser.parse(code)
        assert ast is not None


class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.parser = JSParser()
    
    def test_unicode_identifiers(self):
        """Test parsing Unicode identifiers"""
        code = "const café = 'coffee';"
        ast = self.parser.parse(code)
        assert ast is not None
    
    def test_regex_literals(self):
        """Test parsing regex literals"""
        code = "const regex = /\\d+/g;"
        ast = self.parser.parse(code)
        assert ast is not None
    
    def test_nested_functions(self):
        """Test parsing nested functions"""
        code = """
            function outer() {
                function inner() {
                    return 42;
                }
                return inner;
            }
        """
        functions = self.parser.extract_functions(code)
        assert len(functions) >= 2
    
    def test_iife(self):
        """Test parsing IIFE"""
        code = "(function() { console.log('IIFE'); })();"
        ast = self.parser.parse(code)
        assert ast is not None
    
    def test_try_catch(self):
        """Test parsing try-catch"""
        code = """
            try {
                risky();
            } catch (error) {
                handle(error);
            } finally {
                cleanup();
            }
        """
        ast = self.parser.parse(code)
        assert ast is not None
    
    def test_switch_statement(self):
        """Test parsing switch statement"""
        code = """
            switch (value) {
                case 1:
                    break;
                default:
                    break;
            }
        """
        ast = self.parser.parse(code)
        assert ast is not None
    
    def test_labeled_statement(self):
        """Test parsing labeled statement"""
        code = "loop: for (let i = 0; i < 10; i++) { break loop; }"
        ast = self.parser.parse(code)
        assert ast is not None
    
    def test_new_target(self):
        """Test parsing new.target"""
        code = "function Foo() { console.log(new.target); }"
        ast = self.parser.parse(code)
        assert ast is not None
    
    def test_super_keyword(self):
        """Test parsing super keyword"""
        code = """
            class Child extends Parent {
                method() {
                    super.method();
                }
            }
        """
        ast = self.parser.parse(code)
        assert ast is not None
    
    def test_empty_statements(self):
        """Test parsing empty statements"""
        code = ";;;"
        ast = self.parser.parse(code)
        assert ast is not None


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
