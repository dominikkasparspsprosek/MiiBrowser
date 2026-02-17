"""
MiiBrowser - Chrome-style browser with tabs and DuckDuckGo search
"""

import tkinter as tk
from tkinter import ttk
import urllib.parse
from typing import Optional, Dict
from miibrowser.search import DuckDuckGoSearch
from miibrowser.css_enhancer import get_enhanced_css
from miibrowser import config

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
        self.on_navigation_callback = None
        self.history = []
        self.history_index = -1
        
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
        # Configure HtmlFrame with JavaScript and image support
        self.html_widget = HtmlFrame(
            self.webview_frame, 
            messages_enabled=False,  # Disable debug messages
        )
        self.html_widget.pack(fill=tk.BOTH, expand=True)
        self._last_checked_url = None
        self._check_pending = False
    
    def _on_url_changed(self, url):
        """Called when URL changes in webview"""
        try:
            if url and url != self.current_url and url != "about:blank":
                # Handle DuckDuckGo redirect URLs
                if 'duckduckgo.com/l/?uddg=' in url:
                    try:
                        parsed = urllib.parse.urlparse(url)
                        params = urllib.parse.parse_qs(parsed.query)
                        if 'uddg' in params:
                            actual_url = urllib.parse.unquote(params['uddg'][0])
                            self.html_widget.load_url(actual_url)
                            return
                    except Exception as e:
                        print(f"Error handling DuckDuckGo redirect: {e}")
                
                # Update history
                if self.history_index == len(self.history) - 1:
                    self.history.append(url)
                    self.history_index = len(self.history) - 1
                elif self.history_index < len(self.history) - 1:
                    self.history = self.history[:self.history_index + 1]
                    self.history.append(url)
                    self.history_index = len(self.history) - 1
                
                self.current_url = url
                self._last_checked_url = url
                # Extract domain for title
                domain = url.split('//')[1].split('/')[0] if '//' in url else url[:30]
                self.title = domain[:25] + "..." if len(domain) > 25 else domain
                
                # Trigger callback to update UI
                if self.on_navigation_callback:
                    self.on_navigation_callback(url, self.title)
        except Exception as e:
            print(f"Error in _on_url_changed: {e}")
    
    def _start_url_polling(self):
        """Start URL change detection"""
        if hasattr(self, 'html_widget') and self.is_showing_web:
            self._check_url_change_fallback()
    
    def _check_url_change_fallback(self):
        """Fallback URL check - only used if event system not available"""
        try:
            # Prevent multiple simultaneous checks
            if self._check_pending:
                return
            
            self._check_pending = True
            
            if hasattr(self, 'html_widget') and self.is_showing_web:
                new_url = None
                try:
                    new_url = self.html_widget.get_url()
                except:
                    try:
                        new_url = self.html_widget.current_url
                    except:
                        pass
                
                # Only trigger if URL actually changed and is different from last check
                if new_url and new_url != self._last_checked_url and new_url != "about:blank":
                    self._on_url_changed(new_url)
                
                # Check again after 1.5 seconds for responsive URL tracking
                if self.is_showing_web and hasattr(self, 'parent_frame'):
                    try:
                        if self.parent_frame.winfo_exists():
                            self.parent_frame.after(1500, self._delayed_check)
                    except:
                        pass
            
            self._check_pending = False
        except Exception as e:
            print(f"Error in fallback URL check: {e}")
            self._check_pending = False
    
    def _delayed_check(self):
        """Delayed check to avoid interference with rendering"""
        self._check_pending = False
        if hasattr(self, 'is_showing_web') and self.is_showing_web:
            self._check_url_change_fallback()
    
    def show(self):
        """Show this tab's content"""
        self.content_frame.pack(fill=tk.BOTH, expand=True)
    
    def hide(self):
        """Hide this tab's content"""
        self.content_frame.pack_forget()
    
    def load_url(self, url: str):
        """Load URL in web viewer with enhanced CSS support"""
        if not WEBVIEW_AVAILABLE or not hasattr(self, 'webview_frame'):
            # Fallback to external browser
            import webbrowser
            webbrowser.open(url)
            return False
        
        # Handle DuckDuckGo redirect URLs
        if 'duckduckgo.com/l/?uddg=' in url:
            try:
                parsed = urllib.parse.urlparse(url)
                params = urllib.parse.parse_qs(parsed.query)
                if 'uddg' in params:
                    url = urllib.parse.unquote(params['uddg'][0])
            except Exception as e:
                print(f"Error handling DuckDuckGo redirect: {e}")
        
        self.current_url = url
        # Add to history
        self.history.append(url)
        self.history_index = len(self.history) - 1
        
        # Extract domain for title
        domain = url.split('//')[1].split('/')[0] if '//' in url else url[:30]
        self.title = domain[:25] + "..." if len(domain) > 25 else domain
        self.is_showing_web = True
        
        # Hide search frame first
        self.search_frame.pack_forget()
        
        # Show and update webview
        self.webview_frame.pack(fill=tk.BOTH, expand=True)
        
        try:
            # Check if CSS enhancement is enabled (configured in config.py)
            if config.ENABLE_CSS_ENHANCEMENT:
                try:
                    import requests
                    from urllib.parse import urljoin
                    
                    response = requests.get(url, timeout=config.REQUEST_TIMEOUT, headers={
                        'User-Agent': config.USER_AGENT
                    })
                    
                    if response.status_code == 200:
                        html_content = response.text
                        
                        # Get the base URL for relative links (handle redirects)
                        base_url = response.url if response.url else url
                        
                        # Inject enhanced CSS and base tag into the HTML
                        enhanced_css = f"<style>{get_enhanced_css()}</style>"
                        base_tag = f'<base href="{base_url}">'
                        enhanced_head = f'{base_tag}{enhanced_css}'
                        
                        # Try to inject CSS and base tag after <head> tag or at the beginning
                        if '<head>' in html_content.lower():
                            html_content = html_content.replace('<head>', f'<head>{enhanced_head}', 1)
                        elif '<html>' in html_content.lower():
                            html_content = html_content.replace('<html>', f'<html><head>{enhanced_head}</head>', 1)
                        else:
                            html_content = f'<html><head>{enhanced_head}</head><body>{html_content}</body></html>'
                        
                        # Load the enhanced HTML
                        self.html_widget.load_html(html_content)
                    else:
                        # If fetch fails, fall back to direct URL load
                        self.html_widget.load_url(url)
                except Exception as e:
                    # If enhancement fails, fall back to direct URL load
                    if config.DEBUG_MODE:
                        print(f"CSS enhancement failed, using direct load: {e}")
                    self.html_widget.load_url(url)
            else:
                # CSS enhancement disabled - use direct URL loading (more stable)
                if config.DEBUG_MODE:
                    print(f"Loading URL directly (CSS enhancement disabled): {url}")
                self.html_widget.load_url(url)
            
            # Force frame update to ensure display
            self.webview_frame.update_idletasks()
            self.parent_frame.update_idletasks()
            
            # Start URL change detection with 3-second polling
            self._last_checked_url = url
            self._check_pending = False
            self.parent_frame.after(1500, self._check_url_change_fallback)
            
            return True
        except Exception as e:
            print(f"Error loading URL: {e}")
            return False
    
    def go_back(self):
        """Go back in browser history"""
        if WEBVIEW_AVAILABLE and hasattr(self, 'html_widget') and self.is_showing_web:
            if self.history_index > 0:
                self.history_index -= 1
                url = self.history[self.history_index]
                self.current_url = url
                try:
                    self.html_widget.load_url(url)
                    # Update title
                    domain = url.split('//')[1].split('/')[0] if '//' in url else url[:30]
                    self.title = domain[:25] + "..." if len(domain) > 25 else domain
                    if self.on_navigation_callback:
                        self.on_navigation_callback(url, self.title)
                except Exception as e:
                    print(f"Back navigation error: {e}")
    
    def go_forward(self):
        """Go forward in browser history"""
        if WEBVIEW_AVAILABLE and hasattr(self, 'html_widget') and self.is_showing_web:
            if self.history_index < len(self.history) - 1:
                self.history_index += 1
                url = self.history[self.history_index]
                self.current_url = url
                try:
                    self.html_widget.load_url(url)
                    # Update title
                    domain = url.split('//')[1].split('/')[0] if '//' in url else url[:30]
                    self.title = domain[:25] + "..." if len(domain) > 25 else domain
                    if self.on_navigation_callback:
                        self.on_navigation_callback(url, self.title)
                except Exception as e:
                    print(f"Forward navigation error: {e}")
    
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
        self.root.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
        
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
        
        # Focus on search entry
        self.root.after(100, lambda: self.search_entry.focus_set())
        
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
            text="Search",
            bg="#E8EAED",
            fg="#5F6368",
            font=("Segoe UI", 9)
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
            text="[ ]",
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
        # Window controls
        self.root.bind('<F11>', lambda e: self._toggle_fullscreen())
        self.root.bind('<Escape>', lambda e: self._exit_fullscreen())
        
        # Tab management
        self.root.bind('<Control-t>', lambda e: self._create_new_tab())
        self.root.bind('<Control-w>', lambda e: self._close_active_tab())
        self.root.bind('<Control-Tab>', lambda e: self._next_tab())
        self.root.bind('<Control-Shift-Tab>', lambda e: self._previous_tab())
        
        # Navigation
        self.root.bind('<Alt-Left>', lambda e: self._go_back())
        self.root.bind('<Alt-Right>', lambda e: self._go_forward())
        self.root.bind('<Control-r>', lambda e: self._reload_page())
        self.root.bind('<F5>', lambda e: self._reload_page())
        
        # Address bar
        self.root.bind('<Control-l>', lambda e: self._focus_address_bar())
        self.root.bind('<Control-k>', lambda e: self._focus_address_bar())
        
    def _create_new_tab(self):
        """Create a new tab"""
        tab_id = self.next_tab_id
        self.next_tab_id += 1
        
        # Create tab object
        tab = BrowserTab(tab_id, self.tab_content_area, self.search_engine)
        tab.on_navigation_callback = lambda url, title: self._on_tab_navigation(tab_id, url, title)
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
        else:
            self.search_entry.delete(0, tk.END)
        
        # Update navigation button states
        self._update_nav_buttons()
    
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
            return
        
        # Check if it's a URL
        if query.startswith(('http://', 'https://')):
            self._open_url_in_tab(query)
            return
        elif query.startswith('www.') or ('.' in query and ' ' not in query):
            self._open_url_in_tab('https://' + query)
            return
        
        # It's a search query - create DuckDuckGo URL
        encoded_query = urllib.parse.quote_plus(query)
        search_url = f"https://duckduckgo.com/?q={encoded_query}"
        
        self._open_url_in_tab(search_url)
    
    def _open_url_in_tab(self, url: str):
        """Open URL in active tab"""
        if not self.active_tab_id or not url:
            return
        
        active_tab = self.tabs[self.active_tab_id]
        
        if active_tab.load_url(url):
            # Update tab title
            self.tab_buttons[self.active_tab_id]['button'].config(text=active_tab.title)
            
            # Update URL entry
            self.search_entry.delete(0, tk.END)
            self.search_entry.insert(0, url)
            
            self._update_nav_buttons()
    
    def _on_tab_navigation(self, tab_id: int, url: str, title: str):
        """Called when a tab navigates to a new URL"""
        
        # Update tab title button
        if tab_id in self.tab_buttons:
            self.tab_buttons[tab_id]['button'].config(text=title)
        
        # If this is the active tab, update the URL bar and navigation buttons
        if tab_id == self.active_tab_id:
            self.search_entry.delete(0, tk.END)
            self.search_entry.insert(0, url)
            self._update_nav_buttons()
    
    def _go_back(self):
        """Go back in active tab"""
        if self.active_tab_id:
            self.tabs[self.active_tab_id].go_back()
            self._update_nav_buttons()
    
    def _go_forward(self):
        """Go forward in active tab"""
        if self.active_tab_id:
            self.tabs[self.active_tab_id].go_forward()
            self._update_nav_buttons()
    
    def _reload_page(self):
        """Reload page in active tab"""
        if self.active_tab_id:
            self.tabs[self.active_tab_id].reload()
    
    def _disable_nav_buttons(self):
        """Disable navigation buttons"""
        self.back_button.config(state=tk.DISABLED)
        self.forward_button.config(state=tk.DISABLED)
        self.reload_button.config(state=tk.DISABLED)
    
    def _update_nav_buttons(self):
        """Update navigation button states based on history"""
        if self.active_tab_id and self.active_tab_id in self.tabs:
            tab = self.tabs[self.active_tab_id]
            if tab.is_showing_web:
                # Enable/disable back button
                if tab.history_index > 0:
                    self.back_button.config(state=tk.NORMAL)
                else:
                    self.back_button.config(state=tk.DISABLED)
                
                # Enable/disable forward button
                if tab.history_index < len(tab.history) - 1:
                    self.forward_button.config(state=tk.NORMAL)
                else:
                    self.forward_button.config(state=tk.DISABLED)
                
                # Always enable reload when viewing web
                self.reload_button.config(state=tk.NORMAL)
            else:
                self._disable_nav_buttons()
        else:
            self._disable_nav_buttons()
    
    def _toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes('-fullscreen', self.is_fullscreen)
    
    def _exit_fullscreen(self):
        """Exit fullscreen mode"""
        if self.is_fullscreen:
            self.is_fullscreen = False
            self.root.attributes('-fullscreen', False)
    
    def _focus_address_bar(self):
        """Focus on address bar and select all text"""
        self.search_entry.focus_set()
        self.search_entry.select_range(0, tk.END)
        self.search_entry.icursor(tk.END)
    
    def run(self):
        """Start the browser application"""
        self.root.mainloop()


def main():
    """Main entry point"""
    browser = MiiBrowser()
    browser.run()


if __name__ == "__main__":
    main()
