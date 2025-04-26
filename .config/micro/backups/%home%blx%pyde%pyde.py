import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib, Pango
import os
import subprocess
import time
import datetime
import signal

class WindowDecoration(Gtk.Box):
    def __init__(self, parent, title="Window"):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self.parent = parent
        
        # Create title bar
        self.titlebar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.titlebar.set_size_request(-1, 28)
        self.titlebar.get_style_context().add_class("titlebar")
        
        # Window title
        self.title_label = Gtk.Label(label=title)
        self.title_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.title_label.set_max_width_chars(30)
        self.titlebar.pack_start(self.title_label, True, True, 5)
        
        # Window controls
        minimize_btn = Gtk.Button(label="−")
        minimize_btn.connect("clicked", self.on_minimize_clicked)
        minimize_btn.get_style_context().add_class("window-button")
        
        maximize_btn = Gtk.Button(label="□")
        maximize_btn.connect("clicked", self.on_maximize_clicked)
        maximize_btn.get_style_context().add_class("window-button")
        
        close_btn = Gtk.Button(label="×")
        close_btn.connect("clicked", self.on_close_clicked)
        close_btn.get_style_context().add_class("window-button")
        close_btn.get_style_context().add_class("close-button")
        
        # Add buttons to title bar
        self.titlebar.pack_end(close_btn, False, False, 0)
        self.titlebar.pack_end(maximize_btn, False, False, 0)
        self.titlebar.pack_end(minimize_btn, False, False, 0)
        
        # Add title bar to window decoration
        self.pack_start(self.titlebar, False, False, 0)
        
        # Container for window content
        self.content_area = Gtk.Box()
        self.content_area.get_style_context().add_class("window-content")
        self.pack_start(self.content_area, True, True, 0)
        
        # Make the title bar draggable
        self.titlebar.set_property("can-focus", True)
        eventbox = Gtk.EventBox()
        eventbox.add(self.titlebar)
        eventbox.connect("button-press-event", self.on_titlebar_press)
        eventbox.connect("button-release-event", self.on_titlebar_release)
        eventbox.connect("motion-notify-event", self.on_titlebar_motion)
        self.remove(self.titlebar)
        self.pack_start(eventbox, False, False, 0)
        self.reorder_child(eventbox, 0)
        
        # Dragging state
        self.dragging = False
        self.drag_x = 0
        self.drag_y = 0
    
    def set_title(self, title):
        self.title_label.set_text(title)
    
    def on_minimize_clicked(self, widget):
        # Minimize functionality would depend on window manager integration
        print("Minimize clicked")
        self.parent.set_opacity(0.5)  # Simple visual effect
    
    def on_maximize_clicked(self, widget):
        # Toggle maximize state
        parent_window = self.get_toplevel()
        is_maximized = parent_window.is_maximized()
        
        if is_maximized:
            parent_window.unmaximize()
        else:
            parent_window.maximize()
    
    def on_close_clicked(self, widget):
        # Close the window
        parent_window = self.get_toplevel()
        parent_window.destroy()
    
    def on_titlebar_press(self, widget, event):
        if event.button == 1:  # Left mouse button
            self.dragging = True
            self.drag_x = event.x
            self.drag_y = event.y
            return True
        return False
    
    def on_titlebar_release(self, widget, event):
        self.dragging = False
        return False
    
    def on_titlebar_motion(self, widget, event):
        if self.dragging:
            window = self.get_toplevel()
            x, y = window.get_position()
            window.move(int(x + event.x - self.drag_x), int(y + event.y - self.drag_y))
            return True
        return False

class ManagedWindow(Gtk.Window):
            def __init__(self, title="Application Window", program=None):
                super().__init__(title=title)
                self.set_decorated(False)
                self.set_default_size(800, 600)
                self.program = program
                self.xid = None
                
                # Create window decoration
                self.decoration = WindowDecoration(self, title)
                self.add(self.decoration)
                
                # Create socket for X11 embedding
                self.socket = Gtk.Socket()
                self.decoration.content_area.pack_start(self.socket, True, True, 0)
                
                # Launch external application
                if program:
                    GLib.idle_add(self.launch_external_app)
                
                self.connect("destroy", self.on_window_closed)
                self.show_all()
            
            def launch_external_app(self):
                if self.program:
                    # Get XWindow ID for embedding
                    xid = self.socket.get_id()
                    
                    # Launch application with XEMBED
                    try:
                        subprocess.Popen(
                            [self.program, "--embed", str(xid)],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL
                        )
                    except Exception as e:
                        error_label = Gtk.Label(label=f"Error: {str(e)}")
                        self.decoration.content_area.pack_start(error_label, True, True, 0)

class SimpleDesktopEnvironment:
    def __init__(self):
        # Main window setup
        self.window = Gtk.Window(title="Simple Desktop Environment")
        self.window.set_decorated(False)  # No window decorations
        self.window.maximize()
        self.window.fullscreen()  # Make it truly fullscreen
        self.window.connect("destroy", Gtk.main_quit)
        
        # Main layout container
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.window.add(self.main_box)
        
        # Create panel
        self.create_panel()
        
        # Create desktop area
        self.create_desktop_area()
        
        # List of managed windows
        self.managed_windows = []
        
        # Show all elements
        self.window.show_all()
        
        # Start clock update timer
        GLib.timeout_add(1000, self.update_clock)
    
    def create_panel(self):
        # Top panel
        panel = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        panel.set_size_request(-1, 30)  # Height of 30px
        panel.get_style_context().add_class("panel")
        
        # App menu button
        app_button = Gtk.Button(label="Applications")
        app_button.connect("clicked", self.on_app_menu_clicked)
        panel.pack_start(app_button, False, False, 0)
        
        # Clock in the middle
        self.clock_label = Gtk.Label()
        self.update_clock()  # Set initial time
        panel.pack_start(self.clock_label, True, True, 0)
        
        # System tray area (placeholder)
        tray_button = Gtk.Button(label="System")
        panel.pack_end(tray_button, False, False, 0)
        
        self.main_box.pack_start(panel, False, False, 0)
    
    def update_clock(self):
        # Get current time in AM/PM format
        current_time = datetime.datetime.now().strftime("%I:%M%p")
        self.clock_label.set_text(current_time)
        # Return True to keep the timer running
        return True
    
    def create_desktop_area(self):
        # Desktop area
        self.desktop = Gtk.Fixed()
        
        # Add a background
        self.desktop_eventbox = Gtk.EventBox()
        self.desktop_eventbox.add(self.desktop)
        self.desktop_eventbox.connect("button-press-event", self.on_desktop_click)
        
        self.main_box.pack_start(self.desktop_eventbox, True, True, 0)
    
    def on_app_menu_clicked(self, widget):
        # Create a simple application menu
        menu = Gtk.Menu()
        
        # Add some sample applications
        apps = [
            ("Terminal", "terminal"),
            ("File Manager", "file_manager"),
            ("Web Browser", "web_browser"),
            ("Text Editor", "text_editor"),
            ("Sample Window", "sample"),
        ]
        
        for app_name, app_cmd in apps:
            item = Gtk.MenuItem(label=app_name)
            item.connect("activate", self.launch_application, app_cmd)
            menu.append(item)
        
        # Add logout option
        separator = Gtk.SeparatorMenuItem()
        menu.append(separator)
        
        logout = Gtk.MenuItem(label="Log Out")
        logout.connect("activate", Gtk.main_quit)
        menu.append(logout)
        
        menu.show_all()
        menu.popup_at_widget(widget, Gdk.Gravity.SOUTH_WEST, Gdk.Gravity.NORTH_WEST, None)
    
    def launch_application(self, widget, app_cmd):
        # Instead of launching actual apps, we'll create our managed windows
        # In a real DE, you'd integrate with the window manager to capture real app windows
        
        app_titles = {
            "terminal": "foot",
            "file_manager": "File Manager",
            "web_browser": "Web Browser",
            "text_editor": "Text Editor",
            "sample": "Sample Window"
        }
        
        # Create a managed window for the application
        title = app_titles.get(app_cmd, "Application")
        window = ManagedWindow(title=title, program=app_cmd)
        self.managed_windows.append(window)
    
    def on_desktop_click(self, widget, event):
        # Handle right-click on desktop
        if event.button == 3:  # Right mouse button
            self.show_desktop_menu(event)
    
    def show_desktop_menu(self, event):
        menu = Gtk.Menu()
        
        # Desktop menu options
        items = [
            ("New Folder", self.not_implemented),
            ("Change Background", self.not_implemented),
            ("Display Settings", self.not_implemented),
            ("New Window", lambda w: self.launch_application(None, "sample")),
        ]
        
        for label, callback in items:
            item = Gtk.MenuItem(label=label)
            item.connect("activate", callback)
            menu.append(item)
        
        menu.show_all()
        menu.popup_at_pointer(event)
    
    def not_implemented(self, widget):
        dialog = Gtk.MessageDialog(
            transient_for=self.window,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text="Not implemented yet"
        )
        dialog.run()
        dialog.destroy()

if __name__ == "__main__":
    # Apply CSS for styling
    css_provider = Gtk.CssProvider()
    css_provider.load_from_data(b"""
        * {
            font-family: Jetbrains Mono;
            font-weight: 900;
        }
        .panel {
            background-color: #333333;
        }
        button {
            background-color: #444444;
            color: white;
            border: 1px solid #555555;
            border-radius: 10;
        }
        button:hover {
            background-color: #666666;
        }
        label {
            color: white;
        }
        .titlebar {
            background-color: #2c3e50;
            border-bottom: 1px solid #34495e;
        }
        .window-button {
            min-width: 26px;
            min-height: 26px;
            padding: 0;
            margin: 1px;
            border-radius: 3px;
            font-weight: bold;
        }
        .close-button {
            background-color: #e74c3c;
        }
        .close-button:hover {
            background-color: #c0392b;
        }
        .window-content {
            background-color: #f5f5f5;
            border: 1px solid #34495e;
            border-top: 0;
        }
    """)
    Gtk.StyleContext.add_provider_for_screen(
        Gdk.Screen.get_default(),
        css_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )
    
    # Initialize and run the desktop environment
    app = SimpleDesktopEnvironment()
    Gtk.main()
