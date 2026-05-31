#!/usr/bin/env python3
"""
MailForge-Pro - Contact Manager
轻量级终端邮件营销智能引擎 - 联系人管理器

Manages contact lists with import/export, grouping, search, and validation.
Supports CSV and JSON formats with deduplication and email validation.
"""

import os
import re
import json
import csv
from pathlib import Path
from datetime import datetime


class ContactManager:
    """Contact list manager with import, export, grouping, and search."""

    EMAIL_REGEX = re.compile(
        r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$"
    )

    def __init__(self, config):
        """Initialize contact manager."""
        self.config = config
        self.contacts_dir = config.get_contacts_dir()
        self.contacts_dir.mkdir(parents=True, exist_ok=True)
        self._contacts_file = self.contacts_dir / "contacts.json"
        self._contacts = self._load()

    def _load(self):
        """Load contacts from storage."""
        if self._contacts_file.exists():
            try:
                with open(self._contacts_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {"contacts": [], "groups": {}}
        return {"contacts": [], "groups": {}}

    def _save(self):
        """Save contacts to storage."""
        try:
            with open(self._contacts_file, 'w', encoding='utf-8') as f:
                json.dump(self._contacts, f, indent=2, ensure_ascii=False)
        except IOError as e:
            raise RuntimeError(f"Failed to save contacts: {e}")

    @staticmethod
    def validate_email(email):
        """Validate email format."""
        return bool(ContactManager.EMAIL_REGEX.match(email.strip()))

    def add_contact(self, email, name="", group="default", extra=None):
        """Add a single contact. Returns True if added, False if duplicate."""
        email = email.strip().lower()
        if not self.validate_email(email):
            raise ValueError(f"Invalid email address: {email}")

        # Check for duplicates
        for c in self._contacts["contacts"]:
            if c["email"] == email:
                return False

        contact = {
            "email": email,
            "name": name.strip(),
            "group": group,
            "added_at": datetime.now().isoformat(),
            "extra": extra or {},
        }
        self._contacts["contacts"].append(contact)

        # Update group count
        if group not in self._contacts["groups"]:
            self._contacts["groups"][group] = 0
        self._contacts["groups"][group] += 1

        self._save()
        return True

    def remove_contact(self, email):
        """Remove a contact by email."""
        email = email.strip().lower()
        original_count = len(self._contacts["contacts"])
        self._contacts["contacts"] = [
            c for c in self._contacts["contacts"] if c["email"] != email
        ]
        if len(self._contacts["contacts"]) < original_count:
            self._rebuild_groups()
            self._save()

    def _rebuild_groups(self):
        """Rebuild group counts from contact list."""
        groups = {}
        for c in self._contacts["contacts"]:
            g = c.get("group", "default")
            groups[g] = groups.get(g, 0) + 1
        self._contacts["groups"] = groups

    def import_from_file(self, file_path, group="default", fmt=None):
        """Import contacts from a CSV or JSON file."""
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if fmt is None:
            fmt = file_path.suffix.lstrip(".").lower()

        contacts = []
        if fmt == "csv":
            contacts = self._import_csv(file_path, group)
        elif fmt == "json":
            contacts = self._import_json(file_path, group)
        else:
            raise ValueError(f"Unsupported format: {fmt}. Use 'csv' or 'json'.")

        # Add contacts
        added = 0
        skipped = 0
        for contact in contacts:
            try:
                if self.add_contact(
                    email=contact.get("email", ""),
                    name=contact.get("name", ""),
                    group=group,
                    extra=contact.get("extra", {}),
                ):
                    added += 1
                else:
                    skipped += 1
            except ValueError:
                skipped += 1

        return contacts

    def _import_csv(self, file_path, group):
        """Import contacts from CSV file."""
        contacts = []
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                email = row.get("email", row.get("Email", row.get("EMAIL", "")))
                name = row.get("name", row.get("Name", row.get("NAME", "")))
                if email:
                    extra = {k: v for k, v in row.items() if k.lower() not in ("email", "name")}
                    contacts.append({"email": email, "name": name, "extra": extra})
        return contacts

    def _import_json(self, file_path, group):
        """Import contacts from JSON file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        elif isinstance(data, dict) and "contacts" in data:
            return data["contacts"]
        return []

    def list_contacts(self, group=None, search=None):
        """List contacts with optional group filter and search."""
        contacts = self._contacts["contacts"]
        if group:
            contacts = [c for c in contacts if c.get("group") == group]
        if search:
            search_lower = search.lower()
            contacts = [
                c for c in contacts
                if search_lower in c.get("email", "").lower()
                or search_lower in c.get("name", "").lower()
            ]
        return contacts

    def list_groups(self):
        """List all contact groups with counts."""
        return dict(self._contacts.get("groups", {}))

    def get_contact_count(self, group=None):
        """Get total contact count, optionally filtered by group."""
        if group:
            return self._contacts["groups"].get(group, 0)
        return len(self._contacts["contacts"])

    def export_contacts(self, output_path, fmt="csv", group=None):
        """Export contacts to file."""
        contacts = self.list_contacts(group=group)
        output_path = Path(output_path)

        if fmt == "csv":
            with open(output_path, 'w', encoding='utf-8', newline='') as f:
                if contacts:
                    fieldnames = ["email", "name", "group", "added_at"]
                    # Add any extra fields
                    for c in contacts:
                        for key in c.get("extra", {}):
                            if key not in fieldnames:
                                fieldnames.append(key)
                    writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
                    writer.writeheader()
                    for c in contacts:
                        row = {**c, **c.get("extra", {})}
                        writer.writerow(row)
        elif fmt == "json":
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(contacts, f, indent=2, ensure_ascii=False)

    def display_contacts(self, contacts, fmt="table"):
        """Display contacts in specified format."""
        if not contacts:
            print("⚠️  No contacts found.")
            return

        if fmt == "json":
            print(json.dumps(contacts, indent=2, ensure_ascii=False))
        elif fmt == "csv":
            writer = csv.writer(sys.stdout)
            writer.writerow(["Email", "Name", "Group", "Added"])
            for c in contacts:
                writer.writerow([
                    c.get("email", ""),
                    c.get("name", ""),
                    c.get("group", ""),
                    c.get("added_at", ""),
                ])
        else:
            # Table format
            print(f"\n👥 Contacts ({len(contacts)} total)")
            print("-" * 80)
            print(f"  {'Email':<35} {'Name':<20} {'Group':<15}")
            print("-" * 80)
            for c in contacts[:50]:  # Limit display
                email = c.get("email", "")[:34]
                name = c.get("name", "")[:19]
                group = c.get("group", "")[:14]
                print(f"  {email:<35} {name:<20} {group:<15}")
            if len(contacts) > 50:
                print(f"  ... and {len(contacts) - 50} more contacts")
            print("-" * 80)


# Need sys for display_contacts
import sys
