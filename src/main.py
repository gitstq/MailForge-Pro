#!/usr/bin/env python3
"""
MailForge-Pro - Main CLI Entry Point
轻量级终端邮件营销智能引擎 - 主入口
"""

import sys
import os
import argparse
import json
import csv
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from config import Config
from contact_manager import ContactManager
from template_engine import TemplateEngine
from campaign_engine import CampaignEngine
from stats_tracker import StatsTracker
from tui_dashboard import TUIDashboard
from utils import Colors, print_banner, print_success, print_error, print_warning, print_info


def main():
    parser = argparse.ArgumentParser(
        prog="mailforge",
        description="📧 MailForge-Pro - Lightweight Terminal Email Marketing Intelligent Engine",
        epilog="Example: mailforge send --campaign welcome --template welcome.html --contacts contacts.csv",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # ─── send command ───
    send_parser = subparsers.add_parser("send", help="📤 Send email campaign")
    send_parser.add_argument("--campaign", "-c", required=True, help="Campaign name")
    send_parser.add_argument("--template", "-t", required=True, help="Template file path")
    send_parser.add_argument("--contacts", "-co", required=True, help="Contacts CSV file path")
    send_parser.add_argument("--subject", "-s", default="", help="Email subject line")
    send_parser.add_argument("--from-name", "-fn", default="", help="Sender display name")
    send_parser.add_argument("--reply-to", "-rt", default="", help="Reply-to address")
    send_parser.add_argument("--delay", "-d", type=float, default=1.0, help="Delay between sends in seconds (default: 1.0)")
    send_parser.add_argument("--dry-run", action="store_true", help="Preview without sending")
    send_parser.add_argument("--limit", "-l", type=int, default=0, help="Max emails to send (0 = unlimited)")
    send_parser.add_argument("--track", action="store_true", help="Enable open/click tracking")
    send_parser.add_argument("--unsubscribe", action="store_true", help="Add unsubscribe link")

    # ─── contacts command ───
    contacts_parser = subparsers.add_parser("contacts", help="👥 Manage contacts")
    contacts_sub = contacts_parser.add_subparsers(dest="contacts_command")
    
    import_parser = contacts_sub.add_parser("import", help="Import contacts from CSV")
    import_parser.add_argument("--file", "-f", required=True, help="CSV file path")
    import_parser.add_argument("--group", "-g", default="default", help="Contact group name")
    import_parser.add_argument("--format", "-fmt", default="csv", choices=["csv", "json"], help="File format")
    
    list_parser = contacts_sub.add_parser("list", help="List all contacts")
    list_parser.add_argument("--group", "-g", default=None, help="Filter by group")
    list_parser.add_argument("--search", "-s", default=None, help="Search contacts")
    list_parser.add_argument("--format", "-fmt", default="table", choices=["table", "json", "csv"], help="Output format")
    
    remove_parser = contacts_sub.add_parser("remove", help="Remove a contact")
    remove_parser.add_argument("--email", "-e", required=True, help="Email to remove")
    
    groups_parser = contacts_sub.add_parser("groups", help="List contact groups")

    # ─── template command ───
    tmpl_parser = subparsers.add_parser("template", help="📝 Manage templates")
    tmpl_sub = tmpl_parser.add_subparsers(dest="template_command")
    
    create_parser = tmpl_sub.add_parser("create", help="Create a new template")
    create_parser.add_argument("--name", "-n", required=True, help="Template name")
    create_parser.add_argument("--subject", "-s", default="", help="Default subject line")
    create_parser.add_argument("--output", "-o", default=None, help="Output file path")
    
    list_tmpl_parser = tmpl_sub.add_parser("list", help="List all templates")
    preview_parser = tmpl_sub.add_parser("preview", help="Preview a template")
    preview_parser.add_argument("--file", "-f", required=True, help="Template file path")
    preview_parser.add_argument("--data", "-d", default=None, help="Sample data JSON for preview")

    # ─── stats command ───
    stats_parser = subparsers.add_parser("stats", help="📊 View campaign statistics")
    stats_parser.add_argument("--campaign", "-c", default=None, help="Specific campaign name")
    stats_parser.add_argument("--format", "-fmt", default="table", choices=["table", "json"], help="Output format")

    # ─── config command ───
    cfg_parser = subparsers.add_parser("config", help="⚙️ Configure SMTP settings")
    cfg_sub = cfg_parser.add_subparsers(dest="config_command")
    
    set_parser = cfg_sub.add_parser("set", help="Set configuration value")
    set_parser.add_argument("--key", "-k", required=True, help="Config key")
    set_parser.add_argument("--value", "-v", required=True, help="Config value")
    
    show_parser = cfg_sub.add_parser("show", help="Show current configuration")
    test_parser = cfg_sub.add_parser("test", help="Test SMTP connection")

    # ─── dashboard command ───
    dash_parser = subparsers.add_parser("dashboard", help="🖥️ Open TUI dashboard")
    dash_parser.add_argument("--refresh", "-r", type=int, default=5, help="Refresh interval in seconds")

    # ─── version ───
    parser.add_argument("--version", "-v", action="version", version=f"MailForge-Pro v{__import__('src').__version__}")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        print_banner()
        return

    config = Config()

    try:
        if args.command == "send":
            _handle_send(args, config)
        elif args.command == "contacts":
            _handle_contacts(args, config)
        elif args.command == "template":
            _handle_template(args, config)
        elif args.command == "stats":
            _handle_stats(args, config)
        elif args.command == "config":
            _handle_config(args, config)
        elif args.command == "dashboard":
            _handle_dashboard(args, config)
    except KeyboardInterrupt:
        print_warning("\n⚠️  Operation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print_error(f"❌ Error: {e}")
        sys.exit(1)


def _handle_send(args, config):
    """Handle the send command."""
    # Validate config
    if not config.get("smtp.host"):
        print_error("❌ SMTP host not configured. Run: mailforge config set --key smtp.host --value your.smtp.server")
        sys.exit(1)
    if not config.get("smtp.port"):
        print_error("❌ SMTP port not configured. Run: mailforge config set --key smtp.port --value 587")
        sys.exit(1)
    if not config.get("smtp.username"):
        print_error("❌ SMTP username not configured. Run: mailforge config set --key smtp.username --value your@email.com")
        sys.exit(1)
    if not config.get("smtp.password"):
        print_error("❌ SMTP password not configured. Run: mailforge config set --key smtp.password --value your_password")
        sys.exit(1)

    # Load template
    template = TemplateEngine()
    template_content = template.load(args.template)
    if template_content is None:
        print_error(f"❌ Template file not found: {args.template}")
        sys.exit(1)

    # Load contacts
    cm = ContactManager(config)
    contacts = cm.import_from_file(args.contacts)
    if not contacts:
        print_error(f"❌ No contacts found in: {args.contacts}")
        sys.exit(1)

    print_info(f"📧 Campaign: {args.campaign}")
    print_info(f"📋 Template: {args.template}")
    print_info(f"👥 Contacts: {len(contacts)}")
    print_info(f"⏱️  Delay: {args.delay}s between sends")
    if args.dry_run:
        print_warning("🔍 DRY RUN MODE - No emails will be sent")
    if args.limit > 0:
        print_info(f"🔢 Limit: {args.limit} emails max")

    # Build campaign options
    options = {
        "campaign_name": args.campaign,
        "subject": args.subject,
        "from_name": args.from_name,
        "reply_to": args.reply_to,
        "delay": args.delay,
        "dry_run": args.dry_run,
        "limit": args.limit,
        "track": args.track,
        "unsubscribe": args.unsubscribe,
    }

    # Run campaign
    engine = CampaignEngine(config, template, cm)
    results = engine.run(contacts, template_content, options)

    # Print summary
    print_success(f"\n✅ Campaign '{args.campaign}' completed!")
    print_info(f"   Sent: {results.get('sent', 0)}")
    print_info(f"   Failed: {results.get('failed', 0)}")
    print_info(f"   Skipped: {results.get('skipped', 0)}")
    if results.get('total_time'):
        print_info(f"   Time: {results['total_time']:.2f}s")


def _handle_contacts(args, config):
    """Handle the contacts command."""
    cm = ContactManager(config)

    if args.contacts_command == "import":
        contacts = cm.import_from_file(args.file, group=args.group, fmt=args.format)
        print_success(f"✅ Imported {len(contacts)} contacts into group '{args.group}'")
    elif args.contacts_command == "list":
        contacts = cm.list_contacts(group=args.group, search=args.search)
        cm.display_contacts(contacts, fmt=args.format)
    elif args.contacts_command == "remove":
        cm.remove_contact(args.email)
        print_success(f"✅ Removed contact: {args.email}")
    elif args.contacts_command == "groups":
        groups = cm.list_groups()
        if groups:
            print_info("📂 Contact Groups:")
            for group, count in groups.items():
                print_info(f"   {group}: {count} contacts")
        else:
            print_warning("⚠️  No contact groups found")
    else:
        print_error("❌ Unknown contacts command. Use: import, list, remove, groups")


def _handle_template(args, config):
    """Handle the template command."""
    template = TemplateEngine()

    if args.template_command == "create":
        output = template.create(args.name, args.subject, args.output)
        print_success(f"✅ Template created: {output}")
    elif args.template_command == "list":
        templates = template.list_templates()
        if templates:
            print_info("📝 Available Templates:")
            for t in templates:
                print_info(f"   📄 {t}")
        else:
            print_warning("⚠️  No templates found")
    elif args.template_command == "preview":
        content = template.load(args.file)
        if content is None:
            print_error(f"❌ Template not found: {args.file}")
            sys.exit(1)
        sample_data = {}
        if args.data:
            with open(args.data, 'r', encoding='utf-8') as f:
                sample_data = json.load(f)
        rendered = template.render(content, sample_data)
        print_info("📝 Template Preview:")
        print(rendered)
    else:
        print_error("❌ Unknown template command. Use: create, list, preview")


def _handle_stats(args, config):
    """Handle the stats command."""
    tracker = StatsTracker(config)
    stats = tracker.get_stats(args.campaign)

    if args.format == "json":
        print(json.dumps(stats, indent=2, ensure_ascii=False))
    else:
        tracker.display_stats(stats)


def _handle_config(args, config):
    """Handle the config command."""
    if args.config_command == "set":
        config.set(args.key, args.value)
        print_success(f"✅ Set {args.key} = {args.value}")
    elif args.config_command == "show":
        config.display()
    elif args.config_command == "test":
        engine = CampaignEngine(config, TemplateEngine(), ContactManager(config))
        result = engine.test_smtp()
        if result["success"]:
            print_success(f"✅ SMTP connection successful! Server: {result.get('server', 'unknown')}")
        else:
            print_error(f"❌ SMTP connection failed: {result.get('error', 'unknown error')}")
    else:
        print_error("❌ Unknown config command. Use: set, show, test")


def _handle_dashboard(args, config):
    """Handle the dashboard command."""
    dashboard = TUIDashboard(config, refresh_interval=args.refresh)
    dashboard.run()


if __name__ == "__main__":
    main()
