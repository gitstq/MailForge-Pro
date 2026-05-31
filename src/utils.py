#!/usr/bin/env python3
"""
MailForge-Pro - Utility Functions
轻量级终端邮件营销智能引擎 - 工具函数集

Common utilities including colored terminal output, banner rendering,
progress display, and helper functions.
"""

import sys
import os
import time


class Colors:
    """ANSI color codes for terminal output."""

    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"

    @classmethod
    def disable(cls):
        """Disable colors (for non-TTY environments)."""
        cls.RESET = ""
        cls.BOLD = ""
        cls.DIM = ""
        cls.RED = ""
        cls.GREEN = ""
        cls.YELLOW = ""
        cls.BLUE = ""
        cls.MAGENTA = ""
        cls.CYAN = ""
        cls.WHITE = ""

    @classmethod
    def enable(cls):
        """Re-enable colors."""
        cls.RESET = "\033[0m"
        cls.BOLD = "\033[1m"
        cls.DIM = "\033[2m"
        cls.RED = "\033[91m"
        cls.GREEN = "\033[92m"
        cls.YELLOW = "\033[93m"
        cls.BLUE = "\033[94m"
        cls.MAGENTA = "\033[95m"
        cls.CYAN = "\033[96m"
        cls.WHITE = "\033[97m"


# Auto-disable colors if not a TTY
if not sys.stdout.isatty():
    Colors.disable()


def print_banner():
    """Print the MailForge-Pro ASCII banner."""
    banner = f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║  📧  {Colors.BOLD}MailForge-Pro{Colors.RESET}{Colors.CYAN}                                          ║
║      {Colors.DIM}Lightweight Terminal Email Marketing Intelligent Engine{Colors.RESET}    {Colors.CYAN}║
║                                                              ║
║  {Colors.GREEN}✨ Features:{Colors.RESET}{Colors.CYAN}                                                ║
║     📤 Email Campaign Engine with SMTP Support                 ║
║     📝 Template Engine with Variable Substitution             ║
║     👥 Contact Management with Import/Export                  ║
║     📊 Campaign Statistics & Analytics                        ║
║     🖥️  Interactive TUI Dashboard                              ║
║     🔒 Zero External Dependencies                             ║
║                                                              ║
║  {Colors.YELLOW}📖 Quick Start:{Colors.RESET}{Colors.CYAN}                                            ║
║     mailforge config set --key smtp.host --value smtp.server   ║
║     mailforge config set --key smtp.username --value you@x    ║
║     mailforge config set --key smtp.password --value ***      ║
║     mailforge send -c welcome -t tmpl.html -co contacts.csv   ║
║                                                              ║
║  {Colors.DIM}Version 1.0.0 | MIT License | github.com/gitstq{Colors.RESET}         {Colors.CYAN}║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝{Colors.RESET}
"""
    print(banner)


def print_success(msg):
    """Print a success message."""
    print(f"{Colors.GREEN}{msg}{Colors.RESET}")


def print_error(msg):
    """Print an error message."""
    print(f"{Colors.RED}{msg}{Colors.RESET}", file=sys.stderr)


def print_warning(msg):
    """Print a warning message."""
    print(f"{Colors.YELLOW}{msg}{Colors.RESET}")


def print_info(msg):
    """Print an info message."""
    print(f"{Colors.CYAN}{msg}{Colors.RESET}")


def print_bold(msg):
    """Print a bold message."""
    print(f"{Colors.BOLD}{msg}{Colors.RESET}")


def print_progress(current, total, prefix="", bar_length=40):
    """Print a progress bar."""
    if total == 0:
        return
    percent = current / total
    filled = int(bar_length * percent)
    bar = "█" * filled + "░" * (bar_length - filled)
    sys.stdout.write(f"\r{prefix} [{bar}] {current}/{total} ({percent:.1%})")
    sys.stdout.flush()
    if current == total:
        print()


def format_number(n):
    """Format a number with comma separators."""
    return f"{n:,}"


def truncate(s, length=50, suffix="..."):
    """Truncate a string to a maximum length."""
    if len(s) <= length:
        return s
    return s[:length - len(suffix)] + suffix


def file_size(path):
    """Get human-readable file size."""
    size = os.path.getsize(path)
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"
