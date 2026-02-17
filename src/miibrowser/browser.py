"""
MiiBrowser - Chrome-style browser with tabs and DuckDuckGo search
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional, Dict, List
import threading
from miibrowser.search import DuckDuckGoSearch

try:
    from tkinterweb import HtmlFrame
    WEBVIEW_AVAILABLE = True
except ImportError:
    WEBVIEW_AVAILABLE = False
    print("Warning: tkinterweb not available. Links will open externally.")


class BrowserTab:
    """Represents a single browser tab"""
    
    def __init__(self, tab_id: int, parent_frame: tk.Frame, search_engine: DuckDuckGoSearch):
        self.tab_id = tab_id
        self.parent_frame = parent_frame
        self.search_engine = search_engine
        self.title = "New Tab"
        self.current_url = ""
        self.is_showing_web = False
        self.url_open_callback = None
        
        # Create tab content frame
        self.content_frame = tk.Frame(parent_frame, bg="#FFFFFF")
        
        # Create search results area
        self._create_search_area()
        
        # Create web viewer area
        if WEBVIEW_AVAILABLE:
            self._create_webview_area()
        
        # Show search area by default
        self.search_frame.pack(fill=tk.BOTH, expand=True)
    
    def _create_search_area(self):
        """Create search results display area"""
        self.search_frame = tk.Frame(self.content_frame, bg="#FFFFFF")
        
        # Canvas for scrolling
        self.canvas = tk.Canvas(self.search_frame, bg="#FFFFFF", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.search_frame, orient="vertical", command=self.canvas.yview)
        
        self.scrollable_frame = tk.Frame(self.canvas, bg="#FFFFFF")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Mouse wheel scrolling
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
    
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def _create_webview_area(self):
        """Create web viewer area"""
        self.webview_frame = tk.Frame(self.content_frame, bg="#FFFFFF")
        self.html_widget = HtmlFrame(self.webview_frame, messages_enabled=False)
        self.html_widget.pack(fill=tk.BOTH, expand=True)
    
    def show(self):
        """Show this tab's content"""
        self.content_frame.pack(fill=tk.BOTH, expand=True)
    
    def hide(self):
        """Hide this tab's content"""
        self.content_frame.pack_forget()
    
    def display_search_results(self, results: List[Dict], query: str):
        """Display search results in this tab"""
        self.title = f"{query[:20]}..."
        self.is_showing_web = False
        
        # Hide webview if showing
        if WEBVIEW_AVAILABLE and hasattr(self, 'webview_frame'):
            self.webview_frame.pack_forget()
        
        # Show search frame
        self.search_frame.pack(fill=tk.BOTH, expand=True)
        
        # Clear previous results
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Define color palette (Google-like colors)
        colors = [
            {"bg": "#4285F4", "fg": "#FFFFFF"},  # Google Blue
            {"bg": "#EA4335", "fg": "#FFFFFF"},  # Google Red
            {"bg": "#FBBC04", "fg": "#000000"},  # Google Yellow
            {"bg": "#34A853", "fg": "#FFFFFF"},  # Google Green
            {"bg": "#5F6368", "fg": "#FFFFFF"},  # Grey
            {"bg": "#8AB4F8", "fg": "#000000"},  # Light Blue
            {"bg": "#FDD663", "fg": "#000000"},  # Light Yellow
            {"bg": "#81C995", "fg": "#000000"},  # Light Green
        ]
        
        for idx, result in enumerate(results):
            color = colors[idx % len(colors)]
            
            # Create result frame
            result_frame = tk.Frame(
                self.scrollable_frame,
                bg=color["bg"],
                relief=tk.FLAT,
                borderwidth=0
            )
            result_frame.pack(fill=tk.X, padx=15, pady=10)
            
            # Inner padding frame
            inner_frame = tk.Frame(result_frame, bg=color["bg"])
            inner_frame.pack(fill=tk.BOTH, padx=15, pady=15)
            
            # Title
            title_label = tk.Label(
                inner_frame,
                text=result['title'],
                bg=color["bg"],
                fg=color["fg"],
                font=("Segoe UI", 16, "bold"),
                wraplength=1300,
                anchor=tk.W,
                justify=tk.LEFT
            )
            title_label.pack(fill=tk.X, pady=(0, 8))
            
            # URL (if available)
            if result['url']:
                url_label = tk.Label(
                    inner_frame,
                    text=result['url'],
                    bg=color["bg"],
                    fg="#E8F0FE" if color["fg"] == "#FFFFFF" else "#1A73E8",
                    font=("Segoe UI", 10),
                    wraplength=1300,
                    anchor=tk.W,
                    justify=tk.LEFT,
                    cursor="hand2"
                )
                url_label.pack(fill=tk.X, pady=(0, 8))
                
                # Make URL clickable
                url_label.bind("<Button-1>", lambda e, url=result['url']: self._trigger_url_open(url))
                url_label.bind("<Enter>", lambda e, lbl=url_label: lbl.config(font=("Segoe UI", 10, "underline")))
                url_label.bind("<Leave>", lambda e, lbl=url_label: lbl.config(font=("Segoe UI", 10)))
            
            # Description
            desc_label = tk.Label(
                inner_frame,
                text=result['description'][:400] + ('...' if len(result['description']) > 400 else ''),
                bg=color["bg"],
                fg=color["fg"],
                font=("Segoe UI", 11),
                wraplength=1300,
                anchor=tk.W,
                justify=tk.LEFT
            )
            desc_label.pack(fill=tk.X)
        
        # Scroll to top
        self.canvas.yview_moveto(0)
    
    def _trigger_url_open(self, url):
        """Trigger URL open callback"""
        print(f"[DEBUG] _trigger_url_open called with URL: {url}")
        print(f"[DEBUG] url_open_callback exists: {self.url_open_callback is not None}")
        
        if self.url_open_callback:
            print(f"[DEBUG] Calling url_open_callback")
            self.url_open_callback(url)
        else:
            print(f"[DEBUG] No callback, opening in external browser")
            # Fallback to external browser if callback not set
            import webbrowser
            webbrowser.open(url)
    
    def load_url(self, url: str):
        """Load URL in web viewer"""
        print(f"[DEBUG] BrowserTab.load_url called with: {url}")
        print(f"[DEBUG] WEBVIEW_AVAILABLE: {WEBVIEW_AVAILABLE}")
        print(f"[DEBUG] has webview_frame: {hasattr(self, 'webview_frame')}")
        
        if not WEBVIEW_AVAILABLE or not hasattr(self, 'webview_frame'):
            # Fallback to external browser
            print(f"[DEBUG] No webview available, opening externally")
            import webbrowser
            webbrowser.open(url)
            return False
        
        self.current_url = url
        # Extract domain for title
        domain = url.split('//')[1].split('/')[0] if '//' in url else url[:30]
        self.title = domain[:25] + "..." if len(domain) > 25 else domain
        self.is_showing_web = True
        
        # Hide search frame
        self.search_frame.pack_forget()
        
        # Show webview
        self.webview_frame.pack(fill=tk.BOTH, expand=True)
        
        try:
            print(f"[DEBUG] Loading URL in html_widget")
            self.html_widget.load_url(url)
            print(f"[DEBUG] URL loaded successfully")
            return True
        except Exception as e:
            print(f"[DEBUG] Error loading URL: {e}")
            return False
    
    def go_back(self):
        """Go back in browser history"""
        if WEBVIEW_AVAILABLE and hasattr(self, 'html_widget'):
            try:
                self.html_widget.go_back()
            except:
                pass
    
    def go_forward(self):
        """Go forward in browser history"""
        if WEBVIEW_AVAILABLE and hasattr(self, 'html_widget'):
            try:
                self.html_widget.go_forward()
            except:
                pass
    
    def reload(self):
        """Reload current page"""
        if WEBVIEW_AVAILABLE and hasattr(self, 'html_widget') and self.current_url:
            try:
                self.html_widget.load_url(self.current_url)
            except:
                pass


class MiiBrowser:
    """Main browser application with Chrome-style tabs"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MiiBrowser")
        self.root.geometry("1400x900")
        
        # Allow window resizing
        self.root.resizable(True, True)
        
        # Initialize search engine
        self.search_engine = DuckDuckGoSearch()
        self.is_fullscreen = False
        
        # Tab management
        self.tabs: Dict[int, BrowserTab] = {}
        self.tab_buttons: Dict[int, tk.Frame] = {}
        self.active_tab_id: Optional[int] = None
        self.next_tab_id = 1
        
        # Setup UI
        self._setup_ui()
        self._setup_keybindings()
        
        # Create initial tab
        self._create_new_tab()
        
        # Perform initial search automatically
        self.search_entry.insert(0, "Welcome to MiiBrowser")
        self.root.after(500, self._perform_search)  # Delay to ensure UI is ready
        
    def _setup_ui(self):
        """Setup the user interface"""
        # Main container
        main_frame = tk.Frame(self.root, bg="#F1F3F4")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Tab bar container
        tab_bar_container = tk.Frame(main_frame, bg="#DEE1E6", height=40)
        tab_bar_container.pack(fill=tk.X)
        tab_bar_container.pack_propagate(False)
        
        # Tab bar frame
        self.tab_bar = tk.Frame(tab_bar_container, bg="#DEE1E6")
        self.tab_bar.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # New tab button
        new_tab_btn = tk.Button(
            tab_bar_container,
            text="+",
            command=self._create_new_tab,
            bg="#FFFFFF",
            fg="#5F6368",
            font=("Segoe UI", 14, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            width=3,
            borderwidth=0
        )
        new_tab_btn.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Address bar frame
        address_frame = tk.Frame(main_frame, bg="#FFFFFF", height=50)
        address_frame.pack(fill=tk.X, padx=10, pady=8)
        address_frame.pack_propagate(False)
        
        # Navigation buttons frame
        nav_buttons = tk.Frame(address_frame, bg="#FFFFFF")
        nav_buttons.pack(side=tk.LEFT, padx=(5, 10))
        
        # Back button
        self.back_button = tk.Button(
            nav_buttons,
            text="◄",
            command=self._go_back,
            bg="#FFFFFF",
            fg="#5F6368",
            font=("Segoe UI", 12),
            relief=tk.FLAT,
            cursor="hand2",
            width=2,
            borderwidth=0,
            state=tk.DISABLED
        )
        self.back_button.pack(side=tk.LEFT, padx=2)
        
        # Forward button
        self.forward_button = tk.Button(
            nav_buttons,
            text="►",
            command=self._go_forward,
            bg="#FFFFFF",
            fg="#5F6368",
            font=("Segoe UI", 12),
            relief=tk.FLAT,
            cursor="hand2",
            width=2,
            borderwidth=0,
            state=tk.DISABLED
        )
        self.forward_button.pack(side=tk.LEFT, padx=2)
        
        # Reload button
        self.reload_button = tk.Button(
            nav_buttons,
            text="⟳",
            command=self._reload_page,
            bg="#FFFFFF",
            fg="#5F6368",
            font=("Segoe UI", 14),
            relief=tk.FLAT,
            cursor="hand2",
            width=2,
            borderwidth=0,
            state=tk.DISABLED
        )
        self.reload_button.pack(side=tk.LEFT, padx=2)
        
        # Search/URL entry frame with border
        entry_frame = tk.Frame(address_frame, bg="#E8EAED", relief=tk.SOLID, borderwidth=1)
        entry_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # Search icon
        search_icon = tk.Label(
            entry_frame,
            text="🔍",
            bg="#E8EAED",
            font=("Segoe UI", 12)
        )
        search_icon.pack(side=tk.LEFT, padx=(8, 5))
        
        # Search/URL entry
        self.search_entry = tk.Entry(
            entry_frame,
            font=("Segoe UI", 12),
            bg="#E8EAED",
            fg="#202124",
            insertbackground="#202124",
            relief=tk.FLAT,
            borderwidth=0
        )
        self.search_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8), pady=8)
        self.search_entry.bind('<Return>', lambda e: self._perform_search())
        self.search_entry.bind('<FocusIn>', lambda e: self._on_entry_focus(entry_frame, True))
        self.search_entry.bind('<FocusOut>', lambda e: self._on_entry_focus(entry_frame, False))
        
        # Search button
        self.search_button = tk.Button(
            address_frame,
            text="Search",
            command=self._perform_search,
            bg="#4285F4",
            fg="#FFFFFF",
            font=("Segoe UI", 11, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            borderwidth=0
        )
        self.search_button.pack(side=tk.LEFT, padx=5)
        
        # Fullscreen button
        fullscreen_button = tk.Button(
            address_frame,
            text="⛶",
            command=self._toggle_fullscreen,
            bg="#FFFFFF",
            fg="#5F6368",
            font=("Segoe UI", 14),
            relief=tk.FLAT,
            cursor="hand2",
            width=2,
            borderwidth=0
        )
        fullscreen_button.pack(side=tk.LEFT, padx=2)
        
        # Status bar
        status_frame = tk.Frame(main_frame, bg="#F1F3F4", height=25)
        status_frame.pack(fill=tk.X, padx=10, pady=(0, 5))
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_frame,
            text="Ready",
            bg="#F1F3F4",
            fg="#5F6368",
            font=("Segoe UI", 9),
            anchor=tk.W
        )
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        # Content area for tabs
        self.tab_content_area = tk.Frame(main_frame, bg="#FFFFFF")
        self.tab_content_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
    def _on_entry_focus(self, frame, focused):
        """Handle entry focus visual feedback"""
        if focused:
            frame.config(bg="#FFFFFF", relief=tk.SOLID, borderwidth=2)
            self.search_entry.config(bg="#FFFFFF")
        else:
            frame.config(bg="#E8EAED", relief=tk.SOLID, borderwidth=1)
            self.search_entry.config(bg="#E8EAED")
        
    def _setup_keybindings(self):
        """Setup keyboard shortcuts"""
        self.root.bind('<F11>', lambda e: self._toggle_fullscreen())
        self.root.bind('<Escape>', lambda e: self._exit_fullscreen())
        self.root.bind('<Control-t>', lambda e: self._create_new_tab())
        self.root.bind('<Control-w>', lambda e: self._close_active_tab())
        self.root.bind('<Control-Tab>', lambda e: self._next_tab())
    
    def _create_new_tab(self):
        """Create a new tab"""
        tab_id = self.next_tab_id
        self.next_tab_id += 1
        
        # Create tab object
        tab = BrowserTab(tab_id, self.tab_content_area, self.search_engine)
        tab.url_open_callback = self._open_url_in_tab
        self.tabs[tab_id] = tab
        
        # Create tab button
        tab_button_frame = tk.Frame(self.tab_bar, bg="#FFFFFF", relief=tk.FLAT, borderwidth=1)
        tab_button_frame.pack(side=tk.LEFT, padx=2, pady=5)
        
        # Tab title button
        tab_button = tk.Button(
            tab_button_frame,
            text="New Tab",
            command=lambda: self._switch_tab(tab_id),
            bg="#FFFFFF",
            fg="#202124",
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            cursor="hand2",
            width=20,
            anchor=tk.W,
            borderwidth=0,
            padx=10
        )
        tab_button.pack(side=tk.LEFT)
        
        # Close button
        close_button = tk.Button(
            tab_button_frame,
            text="×",
            command=lambda: self._close_tab(tab_id),
            bg="#FFFFFF",
            fg="#5F6368",
            font=("Segoe UI", 12, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            width=2,
            borderwidth=0
        )
        close_button.pack(side=tk.LEFT)
        
        self.tab_buttons[tab_id] = {
            'frame': tab_button_frame,
            'button': tab_button,
            'close': close_button
        }
        
        # Switch to new tab
        self._switch_tab(tab_id)
    
    def _switch_tab(self, tab_id: int):
        """Switch to a specific tab"""
        if tab_id not in self.tabs:
            return
        
        # Hide current tab
        if self.active_tab_id and self.active_tab_id in self.tabs:
            self.tabs[self.active_tab_id].hide()
            # Update inactive tab style
            self.tab_buttons[self.active_tab_id]['frame'].config(bg="#E8EAED")
            self.tab_buttons[self.active_tab_id]['button'].config(bg="#E8EAED")
            self.tab_buttons[self.active_tab_id]['close'].config(bg="#E8EAED")
        
        # Show new tab
        self.active_tab_id = tab_id
        self.tabs[tab_id].show()
        
        # Update active tab style
        self.tab_buttons[tab_id]['frame'].config(bg="#FFFFFF")
        self.tab_buttons[tab_id]['button'].config(bg="#FFFFFF")
        self.tab_buttons[tab_id]['close'].config(bg="#FFFFFF")
        
        # Update tab title button text
        self.tab_buttons[tab_id]['button'].config(text=self.tabs[tab_id].title)
        
        # Update URL entry if web page is showing
        if self.tabs[tab_id].is_showing_web:
            self.search_entry.delete(0, tk.END)
            self.search_entry.insert(0, self.tabs[tab_id].current_url)
            self._enable_nav_buttons()
        else:
            self.search_entry.delete(0, tk.END)
            self._disable_nav_buttons()
    
    def _close_tab(self, tab_id: int):
        """Close a specific tab"""
        if tab_id not in self.tabs:
            return
        
        # Don't close if it's the last tab
        if len(self.tabs) == 1:
            return
        
        # Hide and remove tab
        self.tabs[tab_id].hide()
        del self.tabs[tab_id]
        
        # Remove tab button
        self.tab_buttons[tab_id]['frame'].destroy()
        del self.tab_buttons[tab_id]
        
        # Switch to another tab if this was active
        if self.active_tab_id == tab_id:
            # Switch to first available tab
            next_tab_id = list(self.tabs.keys())[0]
            self._switch_tab(next_tab_id)
    
    def _close_active_tab(self):
        """Close the currently active tab"""
        if self.active_tab_id:
            self._close_tab(self.active_tab_id)
    
    def _next_tab(self):
        """Switch to next tab"""
        if not self.active_tab_id:
            return
        
        tab_ids = list(self.tabs.keys())
        current_idx = tab_ids.index(self.active_tab_id)
        next_idx = (current_idx + 1) % len(tab_ids)
        self._switch_tab(tab_ids[next_idx])
    
    def _previous_tab(self):
        """Switch to previous tab"""
        if not self.active_tab_id:
            return
        
        tab_ids = list(self.tabs.keys())
        current_idx = tab_ids.index(self.active_tab_id)
        prev_idx = (current_idx - 1) % len(tab_ids)
        self._switch_tab(tab_ids[prev_idx])
    
    def _perform_search(self):
        """Perform search in active tab"""
        if not self.active_tab_id:
            return
        
        query = self.search_entry.get().strip()
        
        if not query:
            self._update_status("Please enter a search query", "#EA4335")
            return
        
        # Check if it's a URL
        if query.startswith(('http://', 'https://')):
            # Direct URL
            self._open_url_in_tab(query)
            return
        elif '.' in query and ' ' not in query and not query.startswith('www.'):
            # Looks like a domain
            self._open_url_in_tab('https://' + query)
            return
        
        # It's a search query - create DuckDuckGo URL
        import urllib.parse
        encoded_query = urllib.parse.quote_plus(query)
        search_url = f"https://duckduckgo.com/?q={encoded_query}"
        
        self._update_status(f"Searching for: {query}", "#4285F4")
        self._open_url_in_tab(search_url)
    
    def _open_url_in_tab(self, url: str):
        """Open URL in active tab"""
        print(f"[DEBUG] _open_url_in_tab called with URL: {url}")
        print(f"[DEBUG] active_tab_id: {self.active_tab_id}")
        
        if not self.active_tab_id or not url:
            print(f"[DEBUG] Returning early - no active tab or no URL")
            return
        
        active_tab = self.tabs[self.active_tab_id]
        print(f"[DEBUG] Got active tab: {active_tab}")
        
        if active_tab.load_url(url):
            print(f"[DEBUG] URL loaded successfully in tab")
            # Update tab title
            self.tab_buttons[self.active_tab_id]['button'].config(text=active_tab.title)
            
            # Update URL entry
            self.search_entry.delete(0, tk.END)
            self.search_entry.insert(0, url)
            
            self._update_status(f"Loading: {url}", "#4285F4")
            self._enable_nav_buttons()
        else:
            print(f"[DEBUG] URL failed to load in tab, opening externally")
            self._update_status(f"Opening externally: {url}", "#FBBC04")
    
    def _go_back(self):
        """Go back in active tab"""
        if self.active_tab_id:
            self.tabs[self.active_tab_id].go_back()
            self._update_status("Navigated back", "#34A853")
    
    def _go_forward(self):
        """Go forward in active tab"""
        if self.active_tab_id:
            self.tabs[self.active_tab_id].go_forward()
            self._update_status("Navigated forward", "#34A853")
    
    def _reload_page(self):
        """Reload page in active tab"""
        if self.active_tab_id:
            self.tabs[self.active_tab_id].reload()
            self._update_status("Page reloaded", "#34A853")
    
    def _enable_nav_buttons(self):
        """Enable navigation buttons"""
        self.back_button.config(state=tk.NORMAL)
        self.forward_button.config(state=tk.NORMAL)
        self.reload_button.config(state=tk.NORMAL)
    
    def _disable_nav_buttons(self):
        """Disable navigation buttons"""
        self.back_button.config(state=tk.DISABLED)
        self.forward_button.config(state=tk.DISABLED)
        self.reload_button.config(state=tk.DISABLED)
    
    def _update_status(self, message: str, color: str = "#5F6368"):
        """Update status bar"""
        self.status_label.config(text=message, fg=color)
    
    def _toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes('-fullscreen', self.is_fullscreen)
    
    def _exit_fullscreen(self):
        """Exit fullscreen mode"""
        if self.is_fullscreen:
            self.is_fullscreen = False
            self.root.attributes('-fullscreen', False)
    
    def run(self):
        """Start the browser application"""
        self.root.mainloop()


def main():
    """Main entry point"""
    browser = MiiBrowser()
    browser.run()


if __name__ == "__main__":
    main()
