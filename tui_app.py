"""
HITCON Vuls Crawler TUI Application
Modern text-based UI with vim keybindings support
"""

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, DataTable, Static, Input
from textual.containers import Container, Vertical, Horizontal
from textual.binding import Binding
from textual.screen import ModalScreen
from textual import on
from textual.reactive import reactive
from rich.text import Text

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
    last_key_press = 0

    def __init__(self):
        super().__init__()
        self.config = ConfigLoader()
        self.crawler = HITCONVulsCrawler()
        self.vulnerabilities: List[Vulnerability] = []
        self._setup_keybindings()

    def _setup_keybindings(self) -> None:
        """Setup keybindings from config"""
        self.keybindings = self.config.get_keybindings()

        # Create bindings list
        bindings = []

        # Map actions to methods
        action_map = {
            "down": ("move_down", "Move down"),
            "up": ("move_up", "Move up"),
            "page_down": ("next_page", "Next page"),
            "page_up": ("prev_page", "Previous page"),
            "first_page": ("first_page", "First page"),
            "last_page": ("last_page", "Last page"),
            "jump_to_page": ("jump_to_page", "Jump to page"),
            "refresh": ("refresh_page", "Refresh"),
            "help": ("show_help", "Help"),
            "quit": ("quit_app", "Quit"),
        }

        for action, (method, description) in action_map.items():
            if action in self.keybindings:
                for key in self.keybindings[action]:
                    bindings.append(Binding(key, method, description, show=False))

        self.BINDINGS = bindings

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

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """Handle row selection - could open URL in browser"""
        row_key = event.row_key
        row_data = event.data_table.get_row(row_key)
        # In the future, could open the URL in a browser here
        pass


def main():
    """Main entry point for TUI application"""
    app = HITCONVulsTUI()
    app.run()


if __name__ == "__main__":
    main()
