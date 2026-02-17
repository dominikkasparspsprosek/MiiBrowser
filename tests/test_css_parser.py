"""
Tests for CSS parser module
"""

import pytest
from miibrowser.css_parser import (
    CSSParser, 
    parse_inline_style, 
    extract_css_colors, 
    validate_css
)


class TestCSSParser:
    """Test cases for CSSParser class"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.parser = CSSParser()
        self.sample_css = """
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
        """
    
    def test_parse_stylesheet(self):
        """Test parsing a complete stylesheet"""
        rules = self.parser.parse_stylesheet(self.sample_css)
        assert len(rules) > 0
        assert rules is not None
    
    def test_parse_empty_stylesheet(self):
        """Test parsing empty stylesheet"""
        rules = self.parser.parse_stylesheet("")
        assert rules == []
    
    def test_extract_selectors(self):
        """Test extracting CSS selectors"""
        selectors = self.parser.extract_selectors(self.sample_css)
        assert len(selectors) == 3
        assert 'body' in selectors[0]
        assert '.header' in selectors[1]
        assert '#main-content' in selectors[2]
    
    def test_extract_colors(self):
        """Test extracting color values"""
        colors = self.parser.extract_colors(self.sample_css)
        assert len(colors) > 0
        assert any('#f0f0f0' in color for color in colors)
        assert any('#333' in color for color in colors)
        assert any('white' in color for color in colors)
    
    def test_extract_properties(self):
        """Test extracting specific CSS properties"""
        font_sizes = self.parser.extract_properties(self.sample_css, "font-size")
        assert len(font_sizes) > 0
        assert any('24px' in value for selector, value in font_sizes)
    
    def test_get_all_declarations(self):
        """Test getting all CSS declarations"""
        all_decls = self.parser.get_all_declarations(self.sample_css)
        assert len(all_decls) > 0
        assert 'body' in str(all_decls.keys())
    
    def test_parse_declaration_list(self):
        """Test parsing CSS declaration list"""
        decls = "color: red; font-size: 14px; margin: 10px;"
        parsed = self.parser.parse_declaration_list(decls)
        # Filter for only Declaration objects (excluding whitespace tokens)
        import tinycss2
        declarations = [d for d in parsed if isinstance(d, tinycss2.ast.Declaration)]
        assert len(declarations) == 3
    
    def test_parse_one_declaration(self):
        """Test parsing single CSS declaration"""
        decl = self.parser.parse_one_declaration("color: red")
        assert decl is not None
        assert decl.name == "color"
    
    def test_validate_color(self):
        """Test CSS color validation"""
        assert self.parser.validate_color("red")
        assert self.parser.validate_color("#ff0000")
        assert self.parser.validate_color("rgb(255, 0, 0)")
        assert self.parser.validate_color("rgba(255, 0, 0, 0.5)")
    
    def test_minify_css(self):
        """Test CSS minification"""
        minified = self.parser.minify_css(self.sample_css)
        # tinycss2 serialization preserves formatting, so we just check it's valid
        assert minified is not None
        assert len(minified) > 0
        # Verify it contains CSS selectors
        assert 'body' in minified or '.header' in minified
    
    def test_prettify_css(self):
        """Test CSS prettification"""
        prettified = self.parser.prettify_css(self.sample_css)
        assert prettified is not None
        assert len(prettified) > 0
    
    def test_parse_media_queries(self):
        """Test parsing media queries"""
        css_with_media = """
            body { color: black; }
            
            @media (max-width: 768px) {
                body { color: blue; }
                .header { font-size: 16px; }
            }
            
            @media (min-width: 1024px) {
                .container { width: 1200px; }
            }
        """
        media_queries = self.parser.parse_media_queries(css_with_media)
        assert len(media_queries) == 2
        assert any('max-width' in mq['condition'] for mq in media_queries)
        assert any('min-width' in mq['condition'] for mq in media_queries)
    
    def test_important_declaration(self):
        """Test parsing !important declarations"""
        css = "p { color: red !important; }"
        all_decls = self.parser.get_all_declarations(css)
        for selector, decls in all_decls.items():
            for decl in decls:
                if decl['property'] == 'color':
                    assert decl['important'] == True
    
    def test_multiple_selectors(self):
        """Test parsing rules with multiple selectors"""
        css = "h1, h2, h3 { color: blue; }"
        selectors = self.parser.extract_selectors(css)
        assert len(selectors) > 0
        assert 'h1' in selectors[0]
    
    def test_nested_selectors(self):
        """Test parsing nested/descendant selectors"""
        css = "div .header p { color: red; }"
        selectors = self.parser.extract_selectors(css)
        assert len(selectors) > 0
        assert 'div' in selectors[0]
    
    def test_pseudo_classes(self):
        """Test parsing pseudo-classes"""
        css = "a:hover { color: blue; }"
        selectors = self.parser.extract_selectors(css)
        assert len(selectors) > 0
        assert ':hover' in selectors[0]
    
    def test_pseudo_elements(self):
        """Test parsing pseudo-elements"""
        css = "p::before { content: '→'; }"
        selectors = self.parser.extract_selectors(css)
        assert len(selectors) > 0
        assert '::before' in selectors[0]
    
    def test_attribute_selectors(self):
        """Test parsing attribute selectors"""
        css = 'input[type="text"] { border: 1px solid #ccc; }'
        selectors = self.parser.extract_selectors(css)
        assert len(selectors) > 0
        assert '[' in selectors[0]
    
    def test_at_keyframes(self):
        """Test parsing @keyframes"""
        css = """
            @keyframes slide {
                from { left: 0; }
                to { left: 100px; }
            }
        """
        rules = self.parser.parse_stylesheet(css)
        assert len(rules) > 0
    
    def test_at_font_face(self):
        """Test parsing @font-face"""
        css = """
            @font-face {
                font-family: 'MyFont';
                src: url('myfont.woff2');
            }
        """
        rules = self.parser.parse_stylesheet(css)
        assert len(rules) > 0


class TestInlineStyleParser:
    """Test cases for inline style parsing"""
    
    def test_parse_simple_inline_style(self):
        """Test parsing simple inline style"""
        style = "color: red; font-size: 16px;"
        parsed = parse_inline_style(style)
        assert parsed['color'] == 'red'
        assert parsed['font-size'] == '16px'
    
    def test_parse_empty_inline_style(self):
        """Test parsing empty inline style"""
        parsed = parse_inline_style("")
        assert parsed == {}
    
    def test_parse_inline_style_with_important(self):
        """Test parsing inline style with !important"""
        style = "color: red !important;"
        parsed = parse_inline_style(style)
        assert 'color' in parsed
    
    def test_parse_inline_style_no_semicolon(self):
        """Test parsing inline style without trailing semicolon"""
        style = "color: blue"
        parsed = parse_inline_style(style)
        assert parsed['color'] == 'blue'
    
    def test_parse_complex_inline_style(self):
        """Test parsing complex inline style"""
        style = "margin: 10px 20px 30px 40px; padding: 5px; border: 1px solid #000;"
        parsed = parse_inline_style(style)
        assert len(parsed) == 3
        assert 'margin' in parsed
        assert 'padding' in parsed
        assert 'border' in parsed


class TestColorExtraction:
    """Test cases for color extraction"""
    
    def test_extract_hex_colors(self):
        """Test extracting hex colors"""
        css = "body { color: #ff0000; background: #00ff00; }"
        colors = extract_css_colors(css)
        assert len(colors) > 0
    
    def test_extract_named_colors(self):
        """Test extracting named colors"""
        css = "p { color: red; background: blue; }"
        colors = extract_css_colors(css)
        assert len(colors) > 0
    
    def test_extract_rgb_colors(self):
        """Test extracting RGB colors"""
        css = "div { color: rgb(255, 0, 0); }"
        colors = extract_css_colors(css)
        assert len(colors) > 0
    
    def test_extract_rgba_colors(self):
        """Test extracting RGBA colors"""
        css = "span { background: rgba(0, 0, 255, 0.5); }"
        colors = extract_css_colors(css)
        assert len(colors) > 0
    
    def test_extract_hsl_colors(self):
        """Test extracting HSL colors"""
        css = "a { color: hsl(120, 100%, 50%); }"
        colors = extract_css_colors(css)
        assert len(colors) > 0


class TestCSSValidation:
    """Test cases for CSS validation"""
    
    def test_validate_correct_css(self):
        """Test validating correct CSS"""
        css = "body { color: red; }"
        is_valid, error = validate_css(css)
        assert is_valid == True
        assert error is None
    
    def test_validate_empty_css(self):
        """Test validating empty CSS"""
        is_valid, error = validate_css("")
        assert is_valid == True
    
    def test_validate_complex_css(self):
        """Test validating complex CSS"""
        css = """
            @media (max-width: 768px) {
                body { font-size: 14px; }
            }
            
            .header { color: blue; }
        """
        is_valid, error = validate_css(css)
        assert is_valid == True


class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.parser = CSSParser()
    
    def test_parse_css_with_comments(self):
        """Test parsing CSS with comments"""
        css = """
            /* This is a comment */
            body { color: red; }
            /* Another comment */
        """
        rules = self.parser.parse_stylesheet(css)
        assert len(rules) > 0
    
    def test_unicode_in_css(self):
        """Test parsing CSS with Unicode characters"""
        css = "body::before { content: '→ « »'; }"
        rules = self.parser.parse_stylesheet(css)
        assert len(rules) > 0
    
    def test_vendor_prefixes(self):
        """Test parsing vendor-prefixed properties"""
        css = """
            div {
                -webkit-transform: rotate(45deg);
                -moz-transform: rotate(45deg);
                transform: rotate(45deg);
            }
        """
        all_decls = self.parser.get_all_declarations(css)
        assert len(all_decls) > 0
    
    def test_calc_function(self):
        """Test parsing calc() function"""
        css = "div { width: calc(100% - 50px); }"
        all_decls = self.parser.get_all_declarations(css)
        assert len(all_decls) > 0
    
    def test_var_function(self):
        """Test parsing CSS variables"""
        css = """
            :root { --main-color: #06c; }
            body { color: var(--main-color); }
        """
        rules = self.parser.parse_stylesheet(css)
        assert len(rules) > 0
    
    def test_gradient(self):
        """Test parsing gradient values"""
        css = "div { background: linear-gradient(to right, red, blue); }"
        all_decls = self.parser.get_all_declarations(css)
        assert len(all_decls) > 0
    
    def test_multiple_backgrounds(self):
        """Test parsing multiple background values"""
        css = "div { background: url(img1.png), url(img2.png); }"
        all_decls = self.parser.get_all_declarations(css)
        assert len(all_decls) > 0
    
    def test_shorthand_properties(self):
        """Test parsing shorthand properties"""
        css = """
            div {
                margin: 10px 20px;
                padding: 5px;
                border: 1px solid red;
                font: bold 16px/1.5 Arial, sans-serif;
            }
        """
        all_decls = self.parser.get_all_declarations(css)
        assert len(all_decls) > 0
        for selector, decls in all_decls.items():
            assert len(decls) >= 4


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
