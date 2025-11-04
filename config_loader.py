"""
Configuration loader for HITCON Vuls Crawler
Handles loading and managing user-configurable keybindings and settings
"""

import json
import os
from typing import Dict, Any, List

class ConfigLoader:
    """Loads and manages configuration for the TUI application"""

    DEFAULT_CONFIG_PATH = "config.json"
    USER_CONFIG_PATH = os.path.expanduser("~/.hitcon-vuls-crawler-config.json")

    def __init__(self):
        self.config: Dict[str, Any] = {}
        self.load_config()

    def load_config(self) -> None:
        """Load configuration from default and user config files"""
        # Load default config
        if os.path.exists(self.DEFAULT_CONFIG_PATH):
            with open(self.DEFAULT_CONFIG_PATH, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            self.config = self._get_default_config()

        # Override with user config if exists
        if os.path.exists(self.USER_CONFIG_PATH):
            try:
                with open(self.USER_CONFIG_PATH, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    self._merge_config(user_config)
            except Exception as e:
                print(f"Warning: Could not load user config: {e}")

    def _merge_config(self, user_config: Dict[str, Any]) -> None:
        """Merge user configuration with default configuration"""
        for key, value in user_config.items():
            if isinstance(value, dict) and key in self.config:
                self.config[key].update(value)
            else:
                self.config[key] = value

    def _get_default_config(self) -> Dict[str, Any]:
        """Return default configuration if no config file exists"""
        return {
            "keybindings": {
                "vim_mode": {
                    "down": ["j", "down"],
                    "up": ["k", "up"],
                    "page_down": ["ctrl+f", "pagedown", "d"],
                    "page_up": ["ctrl+b", "pageup", "u"],
                    "first_page": ["g,g"],
                    "last_page": ["G"],
                    "jump_to_page": ["/", "colon"],
                    "refresh": ["r"],
                    "help": ["question", "f1"],
                    "quit": ["q", "escape"]
                }
            },
            "default_mode": "vim_mode",
            "theme": {
                "primary": "cyan",
                "secondary": "magenta",
                "accent": "yellow",
                "border": "blue"
            },
            "display": {
                "items_per_page": 20,
                "show_page_numbers": True,
                "show_help_bar": True
            }
        }

    def get_keybindings(self, mode: str = None) -> Dict[str, List[str]]:
        """Get keybindings for specified mode or default mode"""
        if mode is None:
            mode = self.config.get("default_mode", "vim_mode")

        return self.config.get("keybindings", {}).get(mode, {})

    def get_theme(self) -> Dict[str, str]:
        """Get theme configuration"""
        return self.config.get("theme", {})

    def get_display_settings(self) -> Dict[str, Any]:
        """Get display settings"""
        return self.config.get("display", {})

    def save_user_config(self, config: Dict[str, Any]) -> None:
        """Save user configuration to user config file"""
        try:
            with open(self.USER_CONFIG_PATH, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving user config: {e}")

    def create_user_config_template(self) -> None:
        """Create a template user config file"""
        if not os.path.exists(self.USER_CONFIG_PATH):
            self.save_user_config(self.config)
            print(f"Created user config template at: {self.USER_CONFIG_PATH}")
