#!/usr/bin/env python3
"""
Debug version of TUI app to test keybindings
Shows which keys are being pressed
"""

import sys
sys.path.insert(0, '.')

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static
from textual.containers import Container
from textual import events

class KeyDebugApp(App):
    """Simple app to debug keyboard input"""

    CSS = """
    #debug-output {
        height: 100%;
        padding: 2;
        border: solid green;
    }
    """

    def __init__(self):
        super().__init__()
        self.key_log = []

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Static("Press any key to see if it's being captured...\n", id="debug-output"),
            id="main"
        )
        yield Footer()

    def on_key(self, event: events.Key) -> None:
        """Capture all key presses"""
        key = event.key
        self.key_log.append(key)

        # Keep last 20 keys
        if len(self.key_log) > 20:
            self.key_log.pop(0)

        # Build output
        output = "[bold cyan]Key Press Debugger[/bold cyan]\n"
        output += "[dim]Press 'escape' to quit[/dim]\n\n"
        output += f"[bold yellow]Last key pressed:[/bold yellow] {key}\n\n"
        output += "[bold]Recent keys:[/bold]\n"
        output += " -> ".join(self.key_log[-10:])

        # Show key info
        output += f"\n\n[bold]Key details:[/bold]\n"
        output += f"  Key: {key}\n"
        output += f"  Character: {event.character if event.character else 'None'}\n"

        # Test specific keys
        output += "\n[bold]Testing specific keys:[/bold]\n"
        test_keys = ['j', 'k', 'h', 'l', 'b', 'g', 'G', 'q', '/', '?']
        for test_key in test_keys:
            status = "✅" if key == test_key else "  "
            output += f"  {status} {test_key}\n"

        self.query_one("#debug-output", Static).update(output)

        # Quit on escape
        if key == "escape":
            self.exit()

if __name__ == "__main__":
    app = KeyDebugApp()
    app.run()
