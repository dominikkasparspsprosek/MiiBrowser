"""
Example usage of MiiBrowser JavaScript Parser

This script demonstrates the various capabilities of the JavaScript parser module.
"""

from miibrowser.js_parser import (
    JSParser,
    parse_javascript,
    validate_javascript,
    extract_functions,
    extract_variables,
    get_dependencies
)


def main():
    print("=" * 70)
    print("MiiBrowser JavaScript Parser - Example Usage")
    print("=" * 70)
    print()
    
    # Example JavaScript code
    example_js = """
    // ES6 Module imports
    import React, { useState, useEffect } from 'react';
    import axios from 'axios';
    
    // Class declaration with inheritance
    class Animal {
        constructor(name) {
            this.name = name;
        }
        
        speak() {
            console.log(`${this.name} makes a sound`);
        }
    }
    
    class Dog extends Animal {
        constructor(name, breed) {
            super(name);
            this.breed = breed;
        }
        
        speak() {
            console.log(`${this.name} barks!`);
        }
        
        static info() {
            return 'Dogs are loyal companions';
        }
    }
    
    // Function declarations
    function add(a, b) {
        return a + b;
    }
    
    function multiply(x, y = 1) {
        return x * y;
    }
    
    // Arrow functions
    const subtract = (a, b) => a - b;
    const greet = name => `Hello, ${name}!`;
    
    // Async function
    async function fetchUserData(userId) {
        try {
            const response = await axios.get(`/api/users/${userId}`);
            return response.data;
        } catch (error) {
            console.error('Failed to fetch user:', error);
            throw error;
        }
    }
    
    // Generator function
    function* fibonacci() {
        let [a, b] = [0, 1];
        while (true) {
            yield a;
            [a, b] = [b, a + b];
        }
    }
    
    // Variables with different scopes
    const PI = 3.14159;
    let counter = 0;
    var globalVar = 'deprecated';
    
    // Destructuring
    const { name, age } = person;
    const [first, second, ...rest] = numbers;
    
    // Object with methods
    const calculator = {
        result: 0,
        add(n) {
            this.result += n;
            return this;
        },
        multiply(n) {
            this.result *= n;
            return this;
        }
    };
    
    // Template literals
    const message = `The value of PI is approximately ${PI}`;
    
    // Conditionals and loops
    if (counter > 0) {
        for (let i = 0; i < 10; i++) {
            console.log(i);
        }
    }
    
    while (counter < 100) {
        counter++;
    }
    
    // Export statements
    export { Animal, Dog, add, multiply };
    export default fetchUserData;
    """
    
    # Initialize parser
    parser = JSParser()
    
    # Example 1: Parse JavaScript code
    print("1. PARSING JAVASCRIPT")
    print("-" * 70)
    try:
        ast = parser.parse_module(example_js)
        print(f"   ✓ Successfully parsed JavaScript code")
        print(f"   ✓ AST type: {ast['type']}")
        print(f"   ✓ Source type: {ast['sourceType']}")
        print(f"   ✓ Body statements: {len(ast['body'])}")
    except Exception as e:
        print(f"   ✗ Parse error: {e}")
    print()
    
    # Example 2: Extract functions
    print("2. EXTRACTING FUNCTIONS")
    print("-" * 70)
    functions = parser.extract_functions()
    print(f"   Found {len(functions)} functions:")
    for func in functions[:10]:  # Show first 10
        name = func['name'] or '(anonymous)'
        params = ', '.join(func['params'])
        async_str = 'async ' if func.get('async') else ''
        gen_str = '*' if func.get('generator') else ''
        print(f"   • {async_str}{gen_str}{name}({params})")
    print()
    
    # Example 3: Extract variables
    print("3. EXTRACTING VARIABLES")
    print("-" * 70)
    variables = parser.extract_variables()
    print(f"   Found {len(variables)} variables:")
    by_kind = {}
    for var in variables:
        kind = var['kind']
        name = var['name']
        if kind and name:  # Filter out None values
            if kind not in by_kind:
                by_kind[kind] = []
            by_kind[kind].append(name)
    
    for kind, names in by_kind.items():
        print(f"   {kind}: {', '.join(names[:5])}" + ('...' if len(names) > 5 else ''))
    print()
    
    # Example 4: Extract classes
    print("4. EXTRACTING CLASSES")
    print("-" * 70)
    classes = parser.extract_classes()
    print(f"   Found {len(classes)} classes:")
    for cls in classes:
        inheritance = f" extends {cls['superClass']}" if cls['superClass'] else ""
        print(f"   • {cls['name']}{inheritance}")
    print()
    
    # Example 5: Extract imports and exports
    print("5. EXTRACTING IMPORTS")
    print("-" * 70)
    imports = parser.extract_imports()
    print(f"   Found {len(imports)} import statements:")
    for imp in imports:
        spec_count = len(imp['specifiers'])
        print(f"   • from '{imp['source']}' ({spec_count} specifiers)")
    print()
    
    print("6. EXTRACTING EXPORTS")
    print("-" * 70)
    exports = parser.extract_exports()
    print(f"   Found {len(exports)} export statements:")
    for exp in exports[:5]:
        exp_type = exp['type'].replace('Declaration', '')
        source = f" from '{exp['source']}'" if exp['source'] else ""
        print(f"   • {exp_type}{source}")
    print()
    
    # Example 6: Get all identifiers
    print("7. EXTRACTING ALL IDENTIFIERS")
    print("-" * 70)
    identifiers = parser.get_all_identifiers()
    print(f"   Found {len(identifiers)} unique identifiers:")
    sample_ids = list(identifiers)[:15]
    print(f"   Sample: {', '.join(sample_ids)}")
    print()
    
    # Example 7: Analyze complexity
    print("8. ANALYZING CODE COMPLEXITY")
    print("-" * 70)
    metrics = parser.analyze_complexity(example_js)
    print("   Complexity Metrics:")
    for key, value in metrics.items():
        print(f"   • {key.capitalize()}: {value}")
    print()
    
    # Example 8: Find dependencies
    print("9. FINDING DEPENDENCIES")
    print("-" * 70)
    deps = parser.find_dependencies(example_js)
    print(f"   ES6 Imports: {len(deps['imports'])}")
    for dep in deps['imports']:
        print(f"      • {dep}")
    print(f"   CommonJS Requires: {len(deps['requires'])}")
    if deps['requires']:
        for dep in deps['requires']:
            print(f"      • {dep}")
    print()
    
    # Example 9: Detect module type
    print("10. DETECTING MODULE TYPE")
    print("-" * 70)
    module_type = parser.detect_module_type(example_js)
    print(f"   Module type: {module_type.upper()}")
    print()
    
    # Example 10: Validate JavaScript
    print("11. VALIDATING JAVASCRIPT SYNTAX")
    print("-" * 70)
    
    # Valid code
    valid_code = "const x = 42; console.log(x);"
    is_valid, error = parser.validate_syntax(valid_code)
    print(f"   Valid code: {valid_code}")
    print(f"   Result: {'✓ Valid' if is_valid else '✗ Invalid'}")
    
    # Invalid code
    invalid_code = "const x = ;"
    is_valid, error = parser.validate_syntax(invalid_code)
    print(f"\n   Invalid code: {invalid_code}")
    print(f"   Result: {'✓ Valid' if is_valid else '✗ Invalid'}")
    if error:
        print(f"   Error: {error[:50]}...")
    print()
    
    # Example 11: Tokenization
    print("12. TOKENIZING JAVASCRIPT")
    print("-" * 70)
    simple_code = "const add = (a, b) => a + b;"
    tokens = parser.tokenize(simple_code)
    print(f"   Code: {simple_code}")
    print(f"   Tokens ({len(tokens)}):")
    for token in tokens[:10]:
        print(f"      • {token['type']}: '{token['value']}'")
    print()
    
    # Example 12: Extract comments
    print("13. EXTRACTING COMMENTS")
    print("-" * 70)
    code_with_comments = """
        // This is a single-line comment
        const x = 42;
        
        /* This is a
           multi-line comment */
        function test() {}
    """
    comments = parser.extract_comments(code_with_comments)
    print(f"   Found {len(comments)} comments:")
    for comment in comments:
        value_preview = comment['value'][:40].replace('\n', ' ')
        print(f"      • {comment['type']}: {value_preview}...")
    print()
    
    # Example 13: Utility functions
    print("14. USING UTILITY FUNCTIONS")
    print("-" * 70)
    
    quick_code = """
        function foo() { return 42; }
        function bar(x, y) { return x + y; }
        const baz = () => 'hello';
        let x = 1, y = 2;
    """
    
    # Quick function extraction
    func_names = extract_functions(quick_code)
    print(f"   Function names: {', '.join(func_names)}")
    
    # Quick variable extraction
    var_names = extract_variables(quick_code)
    print(f"   Variable names: {', '.join(var_names)}")
    
    # Quick validation
    is_valid, _ = validate_javascript(quick_code)
    print(f"   Syntax valid: {is_valid}")
    print()
    
    # Summary
    print("=" * 70)
    print("Summary: JavaScript Parser Features Demonstrated")
    print("=" * 70)
    print("""
    ✓ Parse complete JavaScript programs
    ✓ Parse ES6 modules
    ✓ Extract all functions (regular, arrow, async, generators)
    ✓ Extract all variables (const, let, var)
    ✓ Extract all classes and inheritance
    ✓ Extract import/export statements
    ✓ Get all identifiers
    ✓ Analyze code complexity
    ✓ Find dependencies (imports & requires)
    ✓ Detect module type (ES6, CommonJS, none)
    ✓ Validate JavaScript syntax
    ✓ Tokenize JavaScript code
    ✓ Extract comments
    ✓ Support modern JavaScript features (ES6+)
    """)
    print("=" * 70)


if __name__ == "__main__":
    main()
