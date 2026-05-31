#!/usr/bin/env python3
"""
MailForge-Pro - TUI Dashboard
轻量级终端邮件营销智能引擎 - TUI交互式仪表盘

Interactive terminal dashboard for monitoring campaigns, contacts, and system status.
Uses only Python standard library (curses-like manual rendering).
"""

import os
import sys
import time
import json
from pathlib import Path
from datetime import datetime


class TUIDashboard:
    """Interactive TUI dashboard for MailForge-Pro."""

    def __init__(self, config, refresh_interval=5):
        """Initialize TUI dashboard."""
        self.config = config
        self.refresh_interval = refresh_interval
        self.running = False

    def run(self):
        """Run the TUI dashboard."""
        self.running = True
        print("\n🖥️  MailForge-Pro TUI Dashboard")
        print("   Press Ctrl+C to exit\n")

        try:
            while self.running:
                self._render()
                time.sleep(self.refresh_interval)
        except KeyboardInterrupt:
            self.running = False
            print("\n\n👋 Dashboard closed.")

    def _render(self):
        """Render the dashboard."""
        # Clear screen (ANSI escape)
        print("\033[2J\033[H", end="")

        # Header
        self._print_header()

        # Stats section
        self._print_stats()

        # Recent campaigns
        self._print_recent_campaigns()

        # Contacts summary
        self._print_contacts_summary()

        # System info
        self._print_system_info()

        # Footer
        self._print_footer()

    def _print_header(self):
        """Print dashboard header."""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"╔══════════════════════════════════════════════════════════════╗")
        print(f"║  📧 MailForge-Pro Dashboard                    🕐 {now:<14}║")
        print(f"╠══════════════════════════════════════════════════════════════╣")

    def _print_stats(self):
        """Print statistics overview."""
        stats_dir = self.config.get_stats_dir()
        total_sent = 0
        total_failed = 0
        total_campaigns = 0

        if stats_dir.exists():
            for f in stats_dir.glob("*.json"):
                try:
                    with open(f, 'r', encoding='utf-8') as fp:
                        data = json.load(fp)
                        total_sent += data.get("sent", 0)
                        total_failed += data.get("failed", 0)
                        total_campaigns += 1
                except (json.JSONDecodeError, IOError):
                    continue

        success_rate = 0
        if total_sent + total_failed > 0:
            success_rate = (total_sent / (total_sent + total_failed)) * 100

        # Status bar
        if success_rate >= 95:
            status = "🟢 Excellent"
        elif success_rate >= 80:
            status = "🟡 Good"
        elif success_rate >= 50:
            status = "🟠 Fair"
        elif total_campaigns == 0:
            status = "⚪ No Data"
        else:
            status = "🔴 Poor"

        print(f"║                                                              ║")
        print(f"║  📊 Statistics                                                ║")
        print(f"║  ─────────────────────────────────────────────────────────── ║")
        print(f"║  Campaigns: {total_campaigns:<6}  Sent: {total_sent:<6}  Failed: {total_failed:<6}  {status:<14}║")
        print(f"║  Success Rate: {success_rate:.1f}%                                          ║")

    def _print_recent_campaigns(self):
        """Print recent campaigns."""
        stats_dir = self.config.get_stats_dir()
        print(f"║                                                              ║")
        print(f"║  📋 Recent Campaigns                                         ║")
        print(f"║  ─────────────────────────────────────────────────────────── ║")

        if not stats_dir.exists():
            print(f"║  No campaigns found.                                        ║")
            return

        files = sorted(stats_dir.glob("*.json"), reverse=True)[:5]
        if not files:
            print(f"║  No campaigns found.                                        ║")
            return

        for f in files:
            try:
                with open(f, 'r', encoding='utf-8') as fp:
                    data = json.load(fp)
                name = data.get("campaign", "unknown")[:20]
                sent = data.get("sent", 0)
                failed = data.get("failed", 0)
                t = data.get("total_time", 0)
                print(f"║  📤 {name:<20} Sent:{sent:<5} Fail:{failed:<5} Time:{t:.1f}s       ║")
            except (json.JSONDecodeError, IOError):
                continue

    def _print_contacts_summary(self):
        """Print contacts summary."""
        contacts_file = self.config.get_contacts_dir() / "contacts.json"
        total_contacts = 0
        groups = 0

        if contacts_file.exists():
            try:
                with open(contacts_file, 'r', encoding='utf-8') as fp:
                    data = json.load(fp)
                total_contacts = len(data.get("contacts", []))
                groups = len(data.get("groups", {}))
            except (json.JSONDecodeError, IOError):
                pass

        print(f"║                                                              ║")
        print(f"║  👥 Contacts: {total_contacts:<6}  Groups: {groups:<6}                            ║")

    def _print_system_info(self):
        """Print system information."""
        smtp_host = self.config.get("smtp.host") or "Not configured"
        smtp_port = self.config.get("smtp.port") or "587"
        data_dir = str(self.config.get_data_dir())

        print(f"║                                                              ║")
        print(f"║  ⚙️  SMTP: {smtp_host}:{smtp_port:<40}║")
        print(f"║  📁 Data: {data_dir[:45]:<47}║")

    def _print_footer(self):
        """Print dashboard footer."""
        print(f"╠══════════════════════════════════════════════════════════════╣")
        print(f"║  Refresh: {self.refresh_interval}s  |  Press Ctrl+C to exit                    ║")
        print(f"╚══════════════════════════════════════════════════════════════╝")
