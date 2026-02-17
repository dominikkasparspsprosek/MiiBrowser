"""
CSS Enhancement Module for MiiBrowser
Provides enhanced CSS styling support for tkinterweb
"""

def get_enhanced_css():
    """
    Returns CSS that enhances tkinterweb's limited CSS support
    Focuses on: colors, backgrounds, positioning, z-index, dimensions
    """
    return """
/* ========================================
   MiiBrowser Enhanced CSS Support
   ======================================== */

/* Reset and base styles */
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #fff;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

/* ========================================
   Color and Background Support
   ======================================== */

/* Ensure inline color styles are respected */
[style*="color"] {
    color: inherit;
}

[style*="background-color"], [style*="background"] {
    background: inherit;
}

/* Common color classes */
.text-primary { color: #007bff !important; }
.text-secondary { color: #6c757d !important; }
.text-success { color: #28a745 !important; }
.text-danger { color: #dc3545 !important; }
.text-warning { color: #ffc107 !important; }
.text-info { color: #17a2b8 !important; }
.text-light { color: #f8f9fa !important; }
.text-dark { color: #343a40 !important; }
.text-white { color: #ffffff !important; }
.text-black { color: #000000 !important; }

/* Background color classes */
.bg-primary { background-color: #007bff !important; }
.bg-secondary { background-color: #6c757d !important; }
.bg-success { background-color: #28a745 !important; }
.bg-danger { background-color: #dc3545 !important; }
.bg-warning { background-color: #ffc107 !important; }
.bg-info { background-color: #17a2b8 !important; }
.bg-light { background-color: #f8f9fa !important; }
.bg-dark { background-color: #343a40 !important; }
.bg-white { background-color: #ffffff !important; }
.bg-black { background-color: #000000 !important; }

/* ========================================
   Position Support
   ======================================== */

.position-static { position: static !important; }
.position-relative { position: relative !important; }
.position-absolute { position: absolute !important; }
.position-fixed { position: fixed !important; }

/* Positioning utilities */
.top-0 { top: 0 !important; }
.bottom-0 { bottom: 0 !important; }
.left-0 { left: 0 !important; }
.right-0 { right: 0 !important; }

/* ========================================
   Z-Index Support
   ======================================== */

.z-index-0 { z-index: 0 !important; }
.z-index-1 { z-index: 1 !important; }
.z-index-2 { z-index: 2 !important; }
.z-index-3 { z-index: 3 !important; }
.z-index-10 { z-index: 10 !important; }
.z-index-100 { z-index: 100 !important; }
.z-index-1000 { z-index: 1000 !important; }

/* ========================================
   Width and Height Support
   ======================================== */

/* Width utilities */
.w-25 { width: 25% !important; }
.w-50 { width: 50% !important; }
.w-75 { width: 75% !important; }
.w-100 { width: 100% !important; }
.w-auto { width: auto !important; }

/* Height utilities */
.h-25 { height: 25% !important; }
.h-50 { height: 50% !important; }
.h-75 { height: 75% !important; }
.h-100 { height: 100% !important; }
.h-auto { height: auto !important; }

/* Min/Max width */
.mw-100 { max-width: 100% !important; }
.mh-100 { max-height: 100% !important; }

/* Viewport units simulation */
.vw-100 { width: 100vw !important; }
.vh-100 { height: 100vh !important; }

/* ========================================
   Display Utilities
   ======================================== */

.d-none { display: none !important; }
.d-block { display: block !important; }
.d-inline { display: inline !important; }
.d-inline-block { display: inline-block !important; }

/* ========================================
   Common Layout Patterns
   ======================================== */

.container {
    width: 100%;
    max-width: 1200px;
    margin-left: auto;
    margin-right: auto;
    padding-left: 15px;
    padding-right: 15px;
}

.container-fluid {
    width: 100%;
    padding-left: 15px;
    padding-right: 15px;
}

.row {
    display: block;
    margin-left: -15px;
    margin-right: -15px;
}

.col {
    display: block;
    padding-left: 15px;
    padding-right: 15px;
}

/* ========================================
   Spacing Utilities
   ======================================== */

/* Margins */
.m-0 { margin: 0 !important; }
.m-1 { margin: 0.25rem !important; }
.m-2 { margin: 0.5rem !important; }
.m-3 { margin: 1rem !important; }
.m-4 { margin: 1.5rem !important; }
.m-5 { margin: 3rem !important; }

/* Padding */
.p-0 { padding: 0 !important; }
.p-1 { padding: 0.25rem !important; }
.p-2 { padding: 0.5rem !important; }
.p-3 { padding: 1rem !important; }
.p-4 { padding: 1.5rem !important; }
.p-5 { padding: 3rem !important; }

/* ========================================
   Image Handling
   ======================================== */

img {
    max-width: 100%;
    height: auto;
    vertical-align: middle;
}

.img-fluid {
    max-width: 100%;
    height: auto;
}

/* ========================================
   Text Utilities
   ======================================== */

.text-left { text-align: left !important; }
.text-center { text-align: center !important; }
.text-right { text-align: right !important; }

.font-weight-normal { font-weight: 400 !important; }
.font-weight-bold { font-weight: 700 !important; }

/* ========================================
   Border Utilities
   ======================================== */

.border { border: 1px solid #dee2e6 !important; }
.border-0 { border: 0 !important; }
.rounded { border-radius: 0.25rem !important; }
.rounded-circle { border-radius: 50% !important; }

/* ========================================
   Opacity Support
   ======================================== */

.opacity-0 { opacity: 0 !important; }
.opacity-25 { opacity: 0.25 !important; }
.opacity-50 { opacity: 0.5 !important; }
.opacity-75 { opacity: 0.75 !important; }
.opacity-100 { opacity: 1 !important; }

/* ========================================
   Overflow Support
   ======================================== */

.overflow-auto { overflow: auto !important; }
.overflow-hidden { overflow: hidden !important; }
.overflow-visible { overflow: visible !important; }
.overflow-scroll { overflow: scroll !important; }

/* ========================================
   Common UI Components
   ======================================== */

/* Buttons */
button, .btn {
    display: inline-block;
    padding: 0.375rem 0.75rem;
    background-color: #007bff;
    color: #fff;
    border: 1px solid transparent;
    border-radius: 0.25rem;
    cursor: pointer;
}

button:hover, .btn:hover {
    background-color: #0056b3;
}

/* Links */
a {
    color: #007bff;
    text-decoration: none;
}

a:hover {
    color: #0056b3;
    text-decoration: underline;
}

/* Headers */
h1, h2, h3, h4, h5, h6 {
    margin-top: 0;
    margin-bottom: 0.5rem;
    font-weight: 500;
    line-height: 1.2;
}

h1 { font-size: 2.5rem; }
h2 { font-size: 2rem; }
h3 { font-size: 1.75rem; }
h4 { font-size: 1.5rem; }
h5 { font-size: 1.25rem; }
h6 { font-size: 1rem; }

/* Paragraphs */
p {
    margin-top: 0;
    margin-bottom: 1rem;
}

/* Lists */
ul, ol {
    margin-top: 0;
    margin-bottom: 1rem;
    padding-left: 2rem;
}

/* Tables */
table {
    border-collapse: collapse;
    width: 100%;
}

th, td {
    padding: 0.75rem;
    border: 1px solid #dee2e6;
}

th {
    background-color: #f8f9fa;
    font-weight: bold;
}

/* ========================================
   End of Enhanced CSS
   ======================================== */
"""


def get_css_injection_script(css_content):
    """
    Returns JavaScript to inject CSS into page
    """
    # Escape the CSS for JavaScript
    css_escaped = css_content.replace('\\', '\\\\').replace('\n', '\\n').replace('"', '\\"').replace("'", "\\'")
    
    return f"""
    (function() {{
        var style = document.createElement('style');
        style.type = 'text/css';
        style.innerHTML = "{css_escaped}";
        document.head.appendChild(style);
    }})();
    """
