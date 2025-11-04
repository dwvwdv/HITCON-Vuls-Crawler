"""
HITCON Vuls Crawler TUI Application
Modern text-based UI with vim keybindings support
"""

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, DataTable, Static, Input
from textual.containers import Container, Vertical, Horizontal
from textual.binding import Binding
from textual.screen import ModalScreen
from textual import on, events
from textual.reactive import reactive
from rich.text import Text
import webbrowser
import platform
import time

from crawler import HITCONVulsCrawler, Vulnerability
from config_loader import ConfigLoader
from typing import List, Optional


class HelpScreen(ModalScreen):
    """Modal screen showing help information"""

    BINDINGS = [
        ("escape", "dismiss", "Close"),
        ("q", "dismiss", "Close"),
    ]

    def __init__(self, keybindings: dict):
        super().__init__()
        self.keybindings = keybindings

    def compose(self) -> ComposeResult:
        """Compose the help screen"""
        help_text = self._generate_help_text()
        yield Container(
            Static(help_text, id="help-content"),
            id="help-dialog"
        )

    def _generate_help_text(self) -> str:
        """Generate help text from keybindings"""
        help_lines = [
            "[bold cyan]HITCON Vuls Crawler - Keyboard Shortcuts[/bold cyan]",
            "",
            "[bold yellow]Navigation:[/bold yellow]",
        ]

        key_descriptions = {
            "down": "Move down one item",
            "up": "Move up one item",
            "page_down": "Next page",
            "page_up": "Previous page",
            "first_page": "Jump to first page",
            "last_page": "Jump to last page",
            "jump_to_page": "Jump to specific page",
            "open_browser": "Open in browser",
            "refresh": "Refresh current page",
            "help": "Show this help",
            "quit": "Quit application"
        }

        for action, description in key_descriptions.items():
            if action in self.keybindings:
                keys = self.keybindings[action]
                key_str = ", ".join(keys[:3])  # Show first 3 keys
                help_lines.append(f"  {key_str:20} - {description}")

        help_lines.extend([
            "",
            "[bold yellow]Features:[/bold yellow]",
            "  • Vim-style navigation (configurable)",
            "  • Page caching for faster browsing",
            "  • Customizable keybindings via config.json",
            "",
            "[dim]Press ESC or q to close this help[/dim]"
        ])

        return "\n".join(help_lines)


class JumpPageScreen(ModalScreen):
    """Modal screen for jumping to a specific page"""

    BINDINGS = [
        ("escape", "dismiss", "Cancel"),
    ]

    def compose(self) -> ComposeResult:
        """Compose the jump page screen"""
        yield Container(
            Static("[bold]Jump to page:[/bold]", id="jump-label"),
            Input(placeholder="Enter page number...", id="page-input"),
            id="jump-dialog"
        )

    def on_mount(self) -> None:
        """Focus the input when screen is mounted"""
        self.query_one(Input).focus()

    @on(Input.Submitted)
    def handle_submit(self, event: Input.Submitted) -> None:
        """Handle page number submission"""
        try:
            page_num = int(event.value)
            if page_num > 0:
                self.dismiss(page_num)
            else:
                self.query_one(Input).value = ""
        except ValueError:
            self.query_one(Input).value = ""


class VulnerabilityTable(DataTable):
    """Custom DataTable for displaying vulnerabilities"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cursor_type = "row"
        self.zebra_stripes = True


class HITCONVulsTUI(App):
    """Main TUI application for HITCON Vuls Crawler"""

    CSS = """
    Screen {
        background: $surface;
    }

    #main-container {
        width: 100%;
        height: 100%;
    }

    #status-bar {
        dock: top;
        height: 3;
        background: $primary;
        color: $text;
        padding: 1;
    }

    #vuls-table {
        border: solid $primary;
    }

    #help-dialog {
        width: 80;
        height: 25;
        background: $surface;
        border: thick $primary;
        padding: 2;
    }

    #help-content {
        width: 100%;
        height: 100%;
    }

    #jump-dialog {
        width: 50;
        height: 7;
        background: $surface;
        border: thick $primary;
        padding: 1;
    }

    #jump-label {
        margin-bottom: 1;
    }

    #page-input {
        width: 100%;
    }

    .status-info {
        color: $accent;
    }
    """

    current_page = reactive(1)
    loading = reactive(False)
    vim_command_buffer = ""
    last_key_time = 0

    # Static bindings for special keys that work through Textual's binding system
    BINDINGS = [
        Binding("escape", "quit_app", "Quit", show=False),
        Binding("f1", "show_help", "Help", show=False),
    ]

    def __init__(self):
        super().__init__()
        self.config = ConfigLoader()
        self.crawler = HITCONVulsCrawler()
        self.vulnerabilities: List[Vulnerability] = []
        self.keybindings = self.config.get_keybindings()
        self.gg_pressed = False

    def compose(self) -> ComposeResult:
        """Compose the application layout"""
        yield Header(show_clock=True)
        yield Container(
            Static("", id="status-bar"),
            VulnerabilityTable(id="vuls-table"),
            id="main-container"
        )
        yield Footer()

    def on_mount(self) -> None:
        """Initialize the application"""
        table = self.query_one(VulnerabilityTable)
        table.add_columns("ID", "Title", "URL")
        table.focus()
        self.load_page(1)

    def on_key(self, event: events.Key) -> None:
        """Handle key press events for vim-style navigation"""
        key = event.key

        # Debug: Show key press in status bar (optional, can be removed)
        # Uncomment the next line to see which keys are being pressed
        # self.query_one("#status-bar", Static).update(f"[dim]Key pressed: {key}[/dim]")

        # Handle 'gg' command (go to first page)
        if key == "g":
            current_time = time.time()
            if self.gg_pressed and (current_time - self.last_key_time) < 0.5:
                # Second 'g' pressed within 0.5 seconds
                self.action_first_page()
                self.gg_pressed = False
                event.prevent_default()
                return
            else:
                # First 'g' pressed
                self.gg_pressed = True
                self.last_key_time = current_time
                event.prevent_default()
                return
        else:
            # Reset gg state if another key is pressed
            self.gg_pressed = False

        # Map single character keys to actions
        key_map = {
            # Navigation within page
            "j": self.action_move_down,
            "k": self.action_move_up,

            # Page navigation
            "h": self.action_prev_page,
            "l": self.action_next_page,

            # Actions
            "b": self.action_open_browser,
            "r": self.action_refresh_page,
            "q": self.action_quit_app,

            # Special
            "/": self.action_jump_to_page,
            "?": self.action_show_help,
            "G": self.action_last_page,  # Shift+g
        }

        if key in key_map:
            key_map[key]()
            event.prevent_default()
            event.stop()

    def update_status_bar(self) -> None:
        """Update the status bar with current page info"""
        status = self.query_one("#status-bar", Static)
        if self.loading:
            status.update("[bold yellow]Loading...[/bold yellow]")
        else:
            vul_count = len(self.vulnerabilities)
            status.update(
                f"[bold cyan]Page:[/bold cyan] {self.current_page} | "
                f"[bold cyan]Vulnerabilities:[/bold cyan] {vul_count} | "
                f"[dim]Press ? for help[/dim]"
            )

    def load_page(self, page_num: int) -> None:
        """Load vulnerabilities for a specific page"""
        if page_num < 1:
            return

        self.loading = True
        self.current_page = page_num
        self.update_status_bar()

        # Fetch vulnerabilities
        self.vulnerabilities = self.crawler.get_vulnerabilities(page_num)

        # Update table
        table = self.query_one(VulnerabilityTable)
        table.clear()

        if self.vulnerabilities:
            for idx, vul in enumerate(self.vulnerabilities, 1):
                table.add_row(
                    str(idx),
                    Text(vul.title, overflow="ellipsis"),
                    Text(vul.full_url, style="link " + vul.full_url)
                )

        self.loading = False
        self.update_status_bar()

    def action_move_down(self) -> None:
        """Move cursor down"""
        table = self.query_one(VulnerabilityTable)
        table.action_cursor_down()

    def action_move_up(self) -> None:
        """Move cursor up"""
        table = self.query_one(VulnerabilityTable)
        table.action_cursor_up()

    def action_next_page(self) -> None:
        """Go to next page"""
        self.load_page(self.current_page + 1)

    def action_prev_page(self) -> None:
        """Go to previous page"""
        if self.current_page > 1:
            self.load_page(self.current_page - 1)

    def action_first_page(self) -> None:
        """Go to first page"""
        self.load_page(1)

    def action_last_page(self) -> None:
        """Go to last page (estimate high page number)"""
        # Since we don't know the exact last page, go to a high number
        # User can navigate back if needed
        self.load_page(100)

    def action_jump_to_page(self) -> None:
        """Show jump to page dialog"""
        def handle_page_number(page_num: Optional[int]) -> None:
            if page_num is not None:
                self.load_page(page_num)

        self.push_screen(JumpPageScreen(), handle_page_number)

    def action_refresh_page(self) -> None:
        """Refresh current page"""
        # Clear cache for current page and reload
        if self.current_page in self.crawler._cache:
            del self.crawler._cache[self.current_page]
        self.load_page(self.current_page)

    def action_show_help(self) -> None:
        """Show help screen"""
        self.push_screen(HelpScreen(self.keybindings))

    def action_quit_app(self) -> None:
        """Quit the application"""
        self.exit()

    def action_open_browser(self) -> None:
        """Open the currently selected vulnerability in browser"""
        table = self.query_one(VulnerabilityTable)

        # Get the cursor position
        if table.cursor_row is None or table.cursor_row < 0:
            return

        # Get the row index (0-based)
        row_idx = table.cursor_row

        # Check if we have a vulnerability at this index
        if row_idx < len(self.vulnerabilities):
            vul = self.vulnerabilities[row_idx]
            try:
                webbrowser.open(vul.full_url)
                # Update status bar to show feedback
                status = self.query_one("#status-bar", Static)
                status.update(f"[bold green]Opening:[/bold green] {vul.full_url}")
                # Restore normal status after a moment
                self.set_timer(2.0, self.update_status_bar)
            except Exception as e:
                status = self.query_one("#status-bar", Static)
                status.update(f"[bold red]Error opening browser:[/bold red] {str(e)}")
                self.set_timer(3.0, self.update_status_bar)

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """Handle row selection - open URL in browser on enter"""
        # When user presses Enter on a row, open it in browser
        self.action_open_browser()


def main():
    """Main entry point for TUI application"""
    app = HITCONVulsTUI()
    app.run()


if __name__ == "__main__":
    main()
