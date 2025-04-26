#!/usr/bin/env python3

import json
import os
import subprocess
import gi
import sys
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio

def get_desktop_files():
            """Get all .desktop files from standard locations"""
            locations = [
                '/usr/share/applications/',
                '/usr/local/share/applications/',
                os.path.expanduser('~/.local/share/applications/')
            ]
            
            desktop_files = []
            for location in locations:
                if os.path.exists(location):
                    for file in os.listdir(location):
                        if file.endswith('.desktop') and not file.startswith('.'):
                            path = os.path.join(location, file)
                            try:
                                # Basic validation - check if file contains [Desktop Entry]
                                with open(path, 'r') as f:
                                    content = f.read()
                                    if '[Desktop Entry]' not in content:
                                        continue
                                desktop_files.append(path)
                            except:
                                continue
            
            return desktop_files
    
    # Skip hidden applications
    if app_info.get_is_hidden() or not app_info.get_show_in():
        return None
    
    name = app_info.get_name()
    icon = app_info.get_icon().to_string() if app_info.get_icon() else "application-x-executable"
    exec_cmd = app_info.get_commandline()
    
    return {
        "name": name,
        "icon": icon,
        "exec": exec_cmd,
        "desktop_file": os.path.basename(path)
    }

def get_running_apps():
    """Get list of currently running applications"""
    try:
        result = subprocess.run(
            ["hyprctl", "clients", "-j"], 
            capture_output=True, 
            text=True
        )
        clients = json.loads(result.stdout)
        
        running_apps = []
        for client in clients:
            if "class" in client and client["class"]:
                running_apps.append(client["class"].lower())
        
        return running_apps
    except Exception as e:
        print(f"Error getting running apps: {e}", file=sys.stderr)
        return []

def main():
    desktop_files = get_desktop_files()
    apps = []
    
    for file in desktop_files:
        print(f"Processing: {file}")  # Debug output
        app_data = parse_desktop_file(file)
        if app_data:
            apps.append(app_data)
    
    # Sort apps alphabetically by name
    apps.sort(key=lambda x: x["name"])
    
    # Get running apps
    running = get_running_apps()
    
    # Add running status to apps
    for app in apps:
        app_class = app["desktop_file"].split(".")[0].lower()
        app["running"] = app_class in running or app["name"].lower() in running
    
    # Output as JSON
    print(json.dumps(apps))

if __name__ == "__main__":
    main()
