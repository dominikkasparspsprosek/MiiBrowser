"""
MiiBrowser - Main browser window with DuckDuckGo search
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
from typing import Optional
import threading
from miibrowser.search import DuckDuckGoSearch

try:
    from tkinterweb import HtmlFrame
    WEBVIEW_AVAILABLE = True
except ImportError:
    WEBVIEW_AVAILABLE = False
    print("Warning: tkinterweb not available. Links will open externally.")


class MiiBrowser:
    """Main browser application window"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MiiBrowser - DuckDuckGo Search")
        self.root.geometry("1200x800")
        
        # Allow window resizing
        self.root.resizable(True, True)
        
        # Initialize search engine
        self.search_engine = DuckDuckGoSearch()
        self.is_fullscreen = False
        self.webview_visible = False
        self.current_url = ""
        
        # Setup UI
        self._setup_ui()
        self._setup_keybindings()
        
    def _setup_ui(self):
        """Setup the user interface"""
        # Main container
        main_frame = tk.Frame(self.root, bg="#2C2C2C")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Top bar with search
        top_frame = tk.Frame(main_frame, bg="#1E1E1E", height=60)
        top_frame.pack(fill=tk.X, padx=5, pady=5)
        top_frame.pack_propagate(False)
        
        # Search label
        search_label = tk.Label(
            top_frame, 
            text="🔍 Search:", 
            bg="#1E1E1E", 
            fg="#FFFFFF",
            font=("Arial", 12, "bold")
        )
        search_label.pack(side=tk.LEFT, padx=10)
        
        # Search entry
        self.search_entry = tk.Entry(
            top_frame,
            font=("Arial", 12),
            bg="#3C3C3C",
            fg="#FFFFFF",
            insertbackground="#FFFFFF",
            relief=tk.FLAT,
            borderwidth=2
        )
        self.search_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.search_entry.bind('<Return>', lambda e: self._perform_search())
        
        # Search button
        self.search_button = tk.Button(
            top_frame,
            text="Search",
            command=self._perform_search,
            bg="#4CAF50",
            fg="#FFFFFF",
            font=("Arial", 11, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            padx=20
        )
        self.search_button.pack(side=tk.LEFT, padx=5)
        
        # Fullscreen button
        fullscreen_button = tk.Button(
            top_frame,
            text="⛶",
            command=self._toggle_fullscreen,
            bg="#FF9800",
            fg="#FFFFFF",
            font=("Arial", 14, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            width=3
        )
        fullscreen_button.pack(side=tk.LEFT, padx=5)
        
        # Navigation bar (for web viewer)
        self.nav_frame = tk.Frame(main_frame, bg="#1E1E1E", height=40)
        self.nav_frame.pack(fill=tk.X, padx=5, pady=(0, 5))
        self.nav_frame.pack_propagate(False)
        
        # Back button
        self.back_button = tk.Button(
            self.nav_frame,
            text="◄",
            command=self._go_back,
            bg="#455A64",
            fg="#FFFFFF",
            font=("Arial", 12, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            width=3,
            state=tk.DISABLED
        )
        self.back_button.pack(side=tk.LEFT, padx=2)
        
        # Forward button
        self.forward_button = tk.Button(
            self.nav_frame,
            text="►",
            command=self._go_forward,
            bg="#455A64",
            fg="#FFFFFF",
            font=("Arial", 12, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            width=3,
            state=tk.DISABLED
        )
        self.forward_button.pack(side=tk.LEFT, padx=2)
        
        # Reload button
        self.reload_button = tk.Button(
            self.nav_frame,
            text="⟳",
            command=self._reload_page,
            bg="#455A64",
            fg="#FFFFFF",
            font=("Arial", 14, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            width=3,
            state=tk.DISABLED
        )
        self.reload_button.pack(side=tk.LEFT, padx=2)
        
        # URL bar
        self.url_entry = tk.Entry(
            self.nav_frame,
            font=("Arial", 10),
            bg="#3C3C3C",
            fg="#FFFFFF",
            insertbackground="#FFFFFF",
            relief=tk.FLAT,
            borderwidth=2
        )
        self.url_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.url_entry.bind('<Return>', lambda e: self._navigate_to_url())
        
        # Close web viewer button
        self.close_webview_button = tk.Button(
            self.nav_frame,
            text="✖",
            command=self._close_webview,
            bg="#F44336",
            fg="#FFFFFF",
            font=("Arial", 12, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            width=3
        )
        self.close_webview_button.pack(side=tk.LEFT, padx=2)
        
        # Hide navigation initially
        self.nav_frame.pack_forget()
        
        # Status bar
        status_frame = tk.Frame(main_frame, bg="#1E1E1E", height=30)
        status_frame.pack(fill=tk.X, padx=5, pady=(0, 5))
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_frame,
            text="Ready",
            bg="#1E1E1E",
            fg="#00FF00",
            font=("Arial", 9),
            anchor=tk.W
        )
        self.status_label.pack(side=tk.LEFT, padx=10, fill=tk.X)
        
        # Container for both results and web viewer
        self.content_container = tk.Frame(main_frame, bg="#2C2C2C")
        self.content_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Results container with scrollbar
        results_frame = tk.Frame(self.content_container, bg="#2C2C2C")
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Canvas for scrolling
        self.canvas = tk.Canvas(results_frame, bg="#2C2C2C", highlightthickness=0)
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.canvas.yview)
        
        self.scrollable_frame = tk.Frame(self.canvas, bg="#2C2C2C")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Mouse wheel scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Web viewer frame (hidden initially)
        self.webview_frame = None
        if WEBVIEW_AVAILABLE:
            self.webview_frame = tk.Frame(self.content_container, bg="#2C2C2C")
            self.html_widget = HtmlFrame(self.webview_frame, messages_enabled=False)
            self.html_widget.pack(fill=tk.BOTH, expand=True)
        
    def _setup_keybindings(self):
        """Setup keyboard shortcuts"""
        self.root.bind('<F11>', lambda e: self._toggle_fullscreen())
        self.root.bind('<Escape>', lambda e: self._exit_fullscreen())
        
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def _toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes('-fullscreen', self.is_fullscreen)
        
    def _exit_fullscreen(self):
        """Exit fullscreen mode"""
        if self.is_fullscreen:
            self.is_fullscreen = False
            self.root.attributes('-fullscreen', False)
    
    def _update_status(self, message: str, color: str = "#00FF00"):
        """Update status bar"""
        self.status_label.config(text=message, fg=color)
        
    def _perform_search(self):
        """Perform search in background thread"""
        query = self.search_entry.get().strip()
        
        if not query:
            self._update_status("Please enter a search query", "#FF0000")
            return
        
        # Disable search button during search
        self.search_button.config(state=tk.DISABLED, text="Searching...")
        self._update_status(f"Searching for: {query}", "#FFFF00")
        
        # Clear previous results
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Perform search in background thread
        thread = threading.Thread(target=self._search_thread, args=(query,))
        thread.daemon = True
        thread.start()
        
    def _search_thread(self, query: str):
        """Background thread for searching"""
        # Check if online
        if not self.search_engine.is_online():
            self.root.after(0, lambda: self._update_status("Offline - No internet connection", "#FF0000"))
            self.root.after(0, lambda: self.search_button.config(state=tk.NORMAL, text="Search"))
            return
        
        # Perform search
        results = self.search_engine.search(query)
        
        # Update UI in main thread
        self.root.after(0, lambda: self._display_results(results, query))
        
    def _display_results(self, results, query):
        """Display search results with formatted styling"""
        self._update_status(f"Found {len(results)} results for: {query}", "#00FF00")
        self.search_button.config(state=tk.NORMAL, text="Search")
        
        # Define color palette
        colors = [
            {"bg": "#3F51B5", "fg": "#FFFFFF"},  # Indigo
            {"bg": "#009688", "fg": "#FFFFFF"},  # Teal
            {"bg": "#673AB7", "fg": "#FFFFFF"},  # Deep Purple
            {"bg": "#FF5722", "fg": "#FFFFFF"},  # Deep Orange
            {"bg": "#2196F3", "fg": "#FFFFFF"},  # Blue
            {"bg": "#4CAF50", "fg": "#FFFFFF"},  # Green
            {"bg": "#FF9800", "fg": "#000000"},  # Orange
            {"bg": "#E91E63", "fg": "#FFFFFF"},  # Pink
        ]
        
        for idx, result in enumerate(results):
            color = colors[idx % len(colors)]
            
            # Create result frame
            result_frame = tk.Frame(
                self.scrollable_frame,
                bg=color["bg"],
                relief=tk.RAISED,
                borderwidth=2
            )
            result_frame.pack(fill=tk.X, padx=10, pady=8)
            
            # Configure minimum height
            result_frame.config(height=120)
            
            # Title
            title_label = tk.Label(
                result_frame,
                text=result['title'],
                bg=color["bg"],
                fg=color["fg"],
                font=("Arial", 14, "bold"),
                wraplength=850,
                anchor=tk.W,
                justify=tk.LEFT
            )
            title_label.pack(fill=tk.X, padx=15, pady=(10, 5))
            
            # URL (if available)
            if result['url']:
                url_label = tk.Label(
                    result_frame,
                    text=result['url'],
                    bg=color["bg"],
                    fg="#FFFF00",
                    font=("Arial", 9, "italic"),
                    wraplength=850,
                    anchor=tk.W,
                    justify=tk.LEFT,
                    cursor="hand2"
                )
                url_label.pack(fill=tk.X, padx=15, pady=(0, 5))
                
                # Make URL clickable
                url_label.bind("<Button-1>", lambda e, url=result['url']: self._open_url(url))
                url_label.bind("<Enter>", lambda e, lbl=url_label: lbl.config(font=("Arial", 9, "italic", "underline")))
                url_label.bind("<Leave>", lambda e, lbl=url_label: lbl.config(font=("Arial", 9, "italic")))
            
            # Description
            desc_label = tk.Label(
                result_frame,
                text=result['description'][:300] + ('...' if len(result['description']) > 300 else ''),
                bg=color["bg"],
                fg=color["fg"],
                font=("Arial", 10),
                wraplength=850,
                anchor=tk.W,
                justify=tk.LEFT
            )
            desc_label.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        # Scroll to top
        self.canvas.yview_moveto(0)
        
    def _open_url(self, url: str):
        """Open URL in embedded web viewer or external browser"""
        if not url:
            return
            
        if WEBVIEW_AVAILABLE and self.webview_frame:
            # Show web viewer
            self._show_webview()
            self.current_url = url
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, url)
            
            # Load URL in web viewer
            try:
                self.html_widget.load_url(url)
                self._update_status(f"Loading: {url}", "#00FFFF")
                self._enable_nav_buttons()
            except Exception as e:
                self._update_status(f"Error loading URL: {e}", "#FF0000")
        else:
            # Fallback to external browser
            import webbrowser
            webbrowser.open(url)
            self._update_status(f"Opening externally: {url}", "#FFFF00")
    
    def _show_webview(self):
        """Show web viewer and hide search results"""
        if WEBVIEW_AVAILABLE and self.webview_frame:
            # Hide results
            for widget in self.content_container.winfo_children():
                widget.pack_forget()
            
            # Show webview
            self.webview_frame.pack(fill=tk.BOTH, expand=True)
            self.nav_frame.pack(fill=tk.X, padx=5, pady=(0, 5), after=self.status_label.master)
            self.webview_visible = True
    
    def _close_webview(self):
        """Close web viewer and show search results"""
        if self.webview_frame:
            self.webview_frame.pack_forget()
        
        # Show results
        for widget in self.content_container.winfo_children():
            if widget != self.webview_frame:
                widget.pack(fill=tk.BOTH, expand=True)
        
        # Hide navigation
        self.nav_frame.pack_forget()
        self.webview_visible = False
        self._update_status("Back to search results", "#00FF00")
    
    def _navigate_to_url(self):
        """Navigate to URL in address bar"""
        url = self.url_entry.get().strip()
        if url:
            # Add http:// if no protocol specified
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            self._open_url(url)
    
    def _go_back(self):
        """Go back in web viewer history"""
        if WEBVIEW_AVAILABLE and self.html_widget:
            try:
                self.html_widget.go_back()
                self._update_status("Navigated back", "#00FF00")
            except:
                pass
    
    def _go_forward(self):
        """Go forward in web viewer history"""
        if WEBVIEW_AVAILABLE and self.html_widget:
            try:
                self.html_widget.go_forward()
                self._update_status("Navigated forward", "#00FF00")
            except:
                pass
    
    def _reload_page(self):
        """Reload current page"""
        if WEBVIEW_AVAILABLE and self.html_widget and self.current_url:
            try:
                self.html_widget.load_url(self.current_url)
                self._update_status("Page reloaded", "#00FF00")
            except:
                pass
    
    def _enable_nav_buttons(self):
        """Enable navigation buttons"""
        self.back_button.config(state=tk.NORMAL)
        self.forward_button.config(state=tk.NORMAL)
        self.reload_button.config(state=tk.NORMAL)
        
    def run(self):
        """Start the browser application"""
        self.root.mainloop()


def main():
    """Main entry point"""
    browser = MiiBrowser()
    browser.run()


if __name__ == "__main__":
    main()
