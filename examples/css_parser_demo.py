"""
Example usage of MiiBrowser CSS Parser

This script demonstrates the various capabilities of the CSS parser module.
"""

from miibrowser.css_parser import (
    CSSParser, 
    parse_inline_style, 
    extract_css_colors, 
    validate_css
)


def main():
    print("=" * 70)
    print("MiiBrowser CSS Parser - Example Usage")
    print("=" * 70)
    print()
    
    # Example CSS
    example_css = """
    /* Main styles */
    body {
        font-family: Arial, sans-serif;
        background-color: #f0f0f0;
        margin: 0;
        padding: 20px;
        line-height: 1.6;
    }
    
    .header {
        color: #333;
        font-size: 24px;
        font-weight: bold;
        border-bottom: 2px solid #4285f4;
    }
    
    #main-content {
        background-color: white;
        border: 1px solid #ddd;
        padding: 15px;
        border-radius: 5px;
    }
    
    .button {
        background-color: #4285f4;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 3px;
    }
    
    .button:hover {
        background-color: #357ae8;
    }
    
    @media (max-width: 768px) {
        body {
            padding: 10px;
        }
        
        .header {
            font-size: 18px;
        }
    }
    """
    
    # Initialize parser
    parser = CSSParser()
    
    # Example 1: Parse and display stylesheet structure
    print("1. PARSING STYLESHEET")
    print("-" * 70)
    rules = parser.parse_stylesheet(example_css)
    print(f"   Total rules found: {len(rules)}")
    print()
    
    # Example 2: Extract all selectors
    print("2. EXTRACTING SELECTORS")
    print("-" * 70)
    selectors = parser.extract_selectors(example_css)
    for i, selector in enumerate(selectors, 1):
        print(f"   {i}. {selector}")
    print()
    
    # Example 3: Extract all colors
    print("3. EXTRACTING COLORS")
    print("-" * 70)
    colors = parser.extract_colors(example_css)
    unique_colors = list(set(colors))
    for i, color in enumerate(unique_colors, 1):
        print(f"   {i}. {color}")
    print()
    
    # Example 4: Extract specific property
    print("4. EXTRACTING FONT-SIZE PROPERTIES")
    print("-" * 70)
    font_sizes = parser.extract_properties(example_css, "font-size")
    for selector, value in font_sizes:
        print(f"   {selector} -> {value}")
    print()
    
    # Example 5: Get all declarations organized by selector
    print("5. ALL DECLARATIONS BY SELECTOR")
    print("-" * 70)
    all_decls = parser.get_all_declarations(example_css)
    for selector, declarations in list(all_decls.items())[:3]:  # Show first 3
        print(f"   {selector}:")
        for decl in declarations[:5]:  # Show first 5 properties
            important = " !important" if decl['important'] else ""
            print(f"      • {decl['property']}: {decl['value']}{important}")
        print()
    
    # Example 6: Parse inline styles
    print("6. PARSING INLINE STYLE")
    print("-" * 70)
    inline_style = "color: red; font-size: 16px; margin: 10px 20px; font-weight: bold;"
    inline_parsed = parse_inline_style(inline_style)
    print(f"   Input: {inline_style}")
    print(f"   Parsed:")
    for prop, value in inline_parsed.items():
        print(f"      • {prop}: {value}")
    print()
    
    # Example 7: Extract media queries
    print("7. EXTRACTING MEDIA QUERIES")
    print("-" * 70)
    media_queries = parser.parse_media_queries(example_css)
    for i, mq in enumerate(media_queries, 1):
        print(f"   Media Query {i}:")
        print(f"      Condition: {mq['condition']}")
        print(f"      Rules: {', '.join(mq['rules']) if mq['rules'] else 'N/A'}")
    print()
    
    # Example 8: Minify CSS
    print("8. CSS MINIFICATION")
    print("-" * 70)
    minified = parser.minify_css(example_css)
    print(f"   Original size: {len(example_css)} characters")
    print(f"   Minified size: {len(minified)} characters")
    print(f"   Reduction: {((len(example_css) - len(minified)) / len(example_css) * 100):.1f}%")
    print(f"   Minified (first 100 chars): {minified[:100]}...")
    print()
    
    # Example 9: Prettify CSS
    print("9. CSS PRETTIFICATION")
    print("-" * 70)
    simple_css = "body{color:red;margin:0;}p{font-size:14px;}"
    prettified = parser.prettify_css(simple_css)
    print(f"   Input: {simple_css}")
    print(f"   Prettified:")
    for line in prettified.split('\n')[:10]:  # Show first 10 lines
        if line.strip():
            print(f"      {line}")
    print()
    
    # Example 10: Validate CSS
    print("10. CSS VALIDATION")
    print("-" * 70)
    
    # Valid CSS
    valid_css = "body { color: red; }"
    is_valid, error = validate_css(valid_css)
    print(f"   Testing: {valid_css}")
    print(f"   Valid: {is_valid}")
    if error:
        print(f"   Error: {error}")
    
    # Complex valid CSS
    complex_css = """
        @media (max-width: 768px) {
            .container { width: 100%; }
        }
    """
    is_valid, error = validate_css(complex_css)
    print(f"\n   Testing: Complex CSS with media query")
    print(f"   Valid: {is_valid}")
    if error:
        print(f"   Error: {error}")
    print()
    
    # Example 11: Advanced color extraction
    print("11. ADVANCED COLOR EXTRACTION")
    print("-" * 70)
    color_css = """
        .red { color: #ff0000; background: red; }
        .blue { color: rgb(0, 0, 255); }
        .green { color: rgba(0, 255, 0, 0.5); }
        .yellow { background: hsl(60, 100%, 50%); }
    """
    colors = extract_css_colors(color_css)
    print(f"   Found {len(colors)} color values:")
    for i, color in enumerate(colors, 1):
        print(f"      {i}. {color}")
    print()
    
    # Summary
    print("=" * 70)
    print("Summary: CSS Parser Features Demonstrated")
    print("=" * 70)
    print("""
    [OK] Parse complete stylesheets
    [OK] Extract CSS selectors
    [OK] Extract color values
    [OK] Extract specific properties
    [OK] Get all declarations
    [OK] Parse inline styles
    [OK] Extract media queries
    [OK] Minify CSS
    [OK] Prettify CSS
    [OK] Validate CSS syntax
    [OK] Handle complex CSS features
    """)
    print("=" * 70)


if __name__ == "__main__":
    main()
