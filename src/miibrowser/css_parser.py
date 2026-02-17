"""
CSS Parser utility using tinycss2 for full CSS parsing capabilities
"""

import tinycss2
from typing import Dict, List, Tuple, Optional, Any


class CSSParser:
    """
    Full-featured CSS parser using tinycss2
    
    This class provides methods to parse CSS stylesheets, rules, and declarations.
    It can extract colors, fonts, dimensions, and other CSS properties.
    """
    
    def __init__(self):
        """Initialize the CSS parser"""
        self.parsed_rules = []
        self.stylesheet = None
    
    def parse_stylesheet(self, css_text: str) -> List[Any]:
        """
        Parse a complete CSS stylesheet
        
        Args:
            css_text: CSS stylesheet as a string
            
        Returns:
            List of parsed rules
        """
        self.stylesheet = tinycss2.parse_stylesheet(css_text, skip_comments=True)
        self.parsed_rules = self.stylesheet
        return self.parsed_rules
    
    def parse_declaration_list(self, css_text: str) -> List[tinycss2.ast.Declaration]:
        """
        Parse CSS declaration list (e.g., inline styles)
        
        Args:
            css_text: CSS declarations as a string (e.g., "color: red; font-size: 14px;")
            
        Returns:
            List of parsed declarations
        """
        return tinycss2.parse_declaration_list(css_text, skip_comments=True)
    
    def parse_one_declaration(self, css_text: str) -> Optional[tinycss2.ast.Declaration]:
        """
        Parse a single CSS declaration
        
        Args:
            css_text: Single CSS declaration (e.g., "color: red")
            
        Returns:
            Parsed declaration or None
        """
        return tinycss2.parse_one_declaration(css_text, skip_comments=True)
    
    def parse_rule(self, css_text: str) -> tinycss2.ast.QualifiedRule:
        """
        Parse a single CSS rule
        
        Args:
            css_text: CSS rule as a string
            
        Returns:
            Parsed rule
        """
        return tinycss2.parse_one_rule(css_text, skip_comments=True)
    
    def extract_colors(self, css_text: str) -> List[str]:
        """
        Extract all color values from CSS
        
        Args:
            css_text: CSS stylesheet or declarations
            
        Returns:
            List of color values found
        """
        colors = []
        rules = self.parse_stylesheet(css_text)
        
        for rule in rules:
            if hasattr(rule, 'content'):
                declarations = tinycss2.parse_declaration_list(rule.content)
                for decl in declarations:
                    if isinstance(decl, tinycss2.ast.Declaration):
                        if any(color_prop in decl.name.lower() for color_prop in 
                               ['color', 'background', 'border', 'fill', 'stroke']):
                            color_val = self._serialize_value(decl.value)
                            if color_val:
                                colors.append(color_val)
        
        return colors
    
    def extract_selectors(self, css_text: str) -> List[str]:
        """
        Extract all CSS selectors from a stylesheet
        
        Args:
            css_text: CSS stylesheet as a string
            
        Returns:
            List of selector strings
        """
        selectors = []
        rules = self.parse_stylesheet(css_text)
        
        for rule in rules:
            if hasattr(rule, 'prelude'):
                selector = tinycss2.serialize(rule.prelude)
                selectors.append(selector)
        
        return selectors
    
    def extract_properties(self, css_text: str, property_name: str) -> List[Tuple[str, str]]:
        """
        Extract specific CSS property values with their selectors
        
        Args:
            css_text: CSS stylesheet as a string
            property_name: Name of the property to extract (e.g., "font-size")
            
        Returns:
            List of tuples (selector, value)
        """
        results = []
        rules = self.parse_stylesheet(css_text)
        
        for rule in rules:
            if hasattr(rule, 'prelude') and hasattr(rule, 'content'):
                selector = tinycss2.serialize(rule.prelude)
                declarations = tinycss2.parse_declaration_list(rule.content)
                
                for decl in declarations:
                    if isinstance(decl, tinycss2.ast.Declaration):
                        if decl.name.lower() == property_name.lower():
                            value = self._serialize_value(decl.value)
                            results.append((selector, value))
        
        return results
    
    def get_all_declarations(self, css_text: str) -> Dict[str, List[Dict[str, str]]]:
        """
        Get all CSS declarations organized by selector
        
        Args:
            css_text: CSS stylesheet as a string
            
        Returns:
            Dictionary mapping selectors to their declarations
        """
        result = {}
        rules = self.parse_stylesheet(css_text)
        
        for rule in rules:
            if hasattr(rule, 'prelude') and hasattr(rule, 'content'):
                selector = tinycss2.serialize(rule.prelude).strip()
                declarations = tinycss2.parse_declaration_list(rule.content)
                
                decl_list = []
                for decl in declarations:
                    if isinstance(decl, tinycss2.ast.Declaration):
                        decl_list.append({
                            'property': decl.name,
                            'value': self._serialize_value(decl.value),
                            'important': decl.important
                        })
                
                if selector not in result:
                    result[selector] = []
                result[selector].extend(decl_list)
        
        return result
    
    def _serialize_value(self, tokens: List[tinycss2.ast.Node]) -> str:
        """
        Serialize CSS value tokens to string
        
        Args:
            tokens: List of CSS token nodes
            
        Returns:
            Serialized string value
        """
        return tinycss2.serialize(tokens).strip()
    
    def validate_color(self, color: str) -> bool:
        """
        Validate if a string is a valid CSS color
        
        Args:
            color: Color string to validate
            
        Returns:
            True if valid color, False otherwise
        """
        try:
            tokens = tinycss2.parse_declaration_list(f"color: {color}")
            return len(tokens) > 0
        except:
            return False
    
    def parse_media_queries(self, css_text: str) -> List[Dict[str, Any]]:
        """
        Extract and parse media queries from CSS
        
        Args:
            css_text: CSS stylesheet as a string
            
        Returns:
            List of media query dictionaries with conditions and rules
        """
        media_queries = []
        rules = self.parse_stylesheet(css_text)
        
        for rule in rules:
            if hasattr(rule, 'at_keyword') and rule.at_keyword == 'media':
                media_query = {
                    'condition': tinycss2.serialize(rule.prelude).strip(),
                    'rules': []
                }
                
                if hasattr(rule, 'content'):
                    nested_rules = tinycss2.parse_stylesheet(rule.content)
                    for nested in nested_rules:
                        if hasattr(nested, 'prelude'):
                            selector = tinycss2.serialize(nested.prelude).strip()
                            media_query['rules'].append(selector)
                
                media_queries.append(media_query)
        
        return media_queries
    
    def minify_css(self, css_text: str) -> str:
        """
        Minify CSS by removing whitespace and comments
        
        Args:
            css_text: CSS stylesheet as a string
            
        Returns:
            Minified CSS string
        """
        rules = self.parse_stylesheet(css_text)
        return tinycss2.serialize(rules)
    
    def prettify_css(self, css_text: str, indent: str = "  ") -> str:
        """
        Prettify CSS with proper indentation
        
        Args:
            css_text: CSS stylesheet as a string
            indent: Indentation string (default: two spaces)
            
        Returns:
            Prettified CSS string
        """
        rules = self.parse_stylesheet(css_text)
        result = []
        
        for rule in rules:
            if hasattr(rule, 'prelude') and hasattr(rule, 'content'):
                selector = tinycss2.serialize(rule.prelude).strip()
                result.append(f"{selector} {{")
                
                declarations = tinycss2.parse_declaration_list(rule.content)
                for decl in declarations:
                    if isinstance(decl, tinycss2.ast.Declaration):
                        value = self._serialize_value(decl.value)
                        important = " !important" if decl.important else ""
                        result.append(f"{indent}{decl.name}: {value}{important};")
                
                result.append("}\n")
            elif hasattr(rule, 'at_keyword'):
                # Handle at-rules like @media, @keyframes, etc.
                at_rule = tinycss2.serialize([rule])
                result.append(at_rule + "\n")
        
        return "\n".join(result)


# Utility functions for quick CSS operations

def parse_inline_style(style_string: str) -> Dict[str, str]:
    """
    Parse inline CSS style attribute
    
    Args:
        style_string: Inline style attribute value (e.g., "color: red; font-size: 14px;")
        
    Returns:
        Dictionary mapping property names to values
    """
    parser = CSSParser()
    declarations = parser.parse_declaration_list(style_string)
    
    result = {}
    for decl in declarations:
        if isinstance(decl, tinycss2.ast.Declaration):
            result[decl.name] = parser._serialize_value(decl.value)
    
    return result


def extract_css_colors(css_text: str) -> List[str]:
    """
    Quick function to extract all colors from CSS
    
    Args:
        css_text: CSS stylesheet or declarations
        
    Returns:
        List of color values
    """
    parser = CSSParser()
    return parser.extract_colors(css_text)


def validate_css(css_text: str) -> Tuple[bool, Optional[str]]:
    """
    Validate CSS syntax
    
    Args:
        css_text: CSS stylesheet to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        parser = CSSParser()
        parser.parse_stylesheet(css_text)
        return (True, None)
    except Exception as e:
        return (False, str(e))


# Example usage and testing
if __name__ == "__main__":
    # Example CSS
    example_css = """
    body {
        font-family: Arial, sans-serif;
        background-color: #f0f0f0;
        margin: 0;
        padding: 20px;
    }
    
    .header {
        color: #333;
        font-size: 24px;
        font-weight: bold;
    }
    
    #main-content {
        background-color: white;
        border: 1px solid #ddd;
        padding: 15px;
    }
    
    @media (max-width: 768px) {
        body {
            padding: 10px;
        }
    }
    """
    
    # Test the parser
    parser = CSSParser()
    
    print("=== Testing CSS Parser ===\n")
    
    # Parse stylesheet
    print("1. Parsing stylesheet...")
    rules = parser.parse_stylesheet(example_css)
    print(f"   Found {len(rules)} rules\n")
    
    # Extract selectors
    print("2. Extracting selectors...")
    selectors = parser.extract_selectors(example_css)
    for selector in selectors:
        print(f"   - {selector}")
    print()
    
    # Extract colors
    print("3. Extracting colors...")
    colors = parser.extract_colors(example_css)
    for color in colors:
        print(f"   - {color}")
    print()
    
    # Get all declarations
    print("4. Getting all declarations...")
    all_decls = parser.get_all_declarations(example_css)
    for selector, declarations in all_decls.items():
        print(f"   {selector}:")
        for decl in declarations:
            print(f"      {decl['property']}: {decl['value']}")
    print()
    
    # Parse inline style
    print("5. Parsing inline style...")
    inline = "color: red; font-size: 16px; margin: 10px 20px;"
    inline_parsed = parse_inline_style(inline)
    for prop, val in inline_parsed.items():
        print(f"   {prop}: {val}")
    print()
    
    # Minify CSS
    print("6. Minifying CSS...")
    minified = parser.minify_css(example_css)
    print(f"   Original length: {len(example_css)} chars")
    print(f"   Minified length: {len(minified)} chars")
    print()
    
    # Extract media queries
    print("7. Extracting media queries...")
    media = parser.parse_media_queries(example_css)
    for mq in media:
        print(f"   Condition: {mq['condition']}")
        print(f"   Rules: {', '.join(mq['rules'])}")
    print()
    
    print("=== All tests completed ===")
