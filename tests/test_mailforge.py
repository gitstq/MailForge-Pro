#!/usr/bin/env python3
"""
MailForge-Pro - Unit Tests
轻量级终端邮件营销智能引擎 - 单元测试
"""

import unittest
import json
import os
import tempfile
import csv
from pathlib import Path

# Add src to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from config import Config
from contact_manager import ContactManager
from template_engine import TemplateEngine
from stats_tracker import StatsTracker
from utils import Colors, truncate, format_number


class TestConfig(unittest.TestCase):
    """Test configuration manager."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.config = Config(config_path=os.path.join(self.temp_dir, "config.json"))

    def test_default_config(self):
        """Test default configuration values."""
        self.assertEqual(self.config.get("smtp.port"), "587")
        self.assertEqual(self.config.get("smtp.use_tls"), "true")

    def test_set_and_get(self):
        """Test setting and getting config values."""
        self.config.set("smtp.host", "smtp.gmail.com")
        self.assertEqual(self.config.get("smtp.host"), "smtp.gmail.com")

    def test_smtp_config(self):
        """Test SMTP config extraction."""
        self.config.set("smtp.host", "smtp.test.com")
        self.config.set("smtp.port", "465")
        self.config.set("smtp.username", "test@test.com")
        self.config.set("smtp.password", "secret")

        smtp = self.config.get_smtp_config()
        self.assertEqual(smtp["host"], "smtp.test.com")
        self.assertEqual(smtp["port"], 465)
        self.assertEqual(smtp["username"], "test@test.com")
        self.assertEqual(smtp["password"], "secret")
        self.assertTrue(smtp["use_tls"])

    def test_persistence(self):
        """Test config persistence across instances."""
        self.config.set("test.key", "test_value")
        config2 = Config(config_path=os.path.join(self.temp_dir, "config.json"))
        self.assertEqual(config2.get("test.key"), "test_value")


class TestContactManager(unittest.TestCase):
    """Test contact manager."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        config_path = os.path.join(self.temp_dir, "config.json")
        self.config = Config(config_path=config_path)
        self.cm = ContactManager(self.config)

    def test_email_validation(self):
        """Test email validation."""
        self.assertTrue(ContactManager.validate_email("test@example.com"))
        self.assertTrue(ContactManager.validate_email("user.name+tag@domain.co"))
        self.assertFalse(ContactManager.validate_email("invalid"))
        self.assertFalse(ContactManager.validate_email("@domain.com"))
        self.assertFalse(ContactManager.validate_email("user@"))

    def test_add_contact(self):
        """Test adding contacts."""
        result = self.cm.add_contact("test@example.com", "Test User")
        self.assertTrue(result)
        self.assertEqual(self.cm.get_contact_count(), 1)

    def test_duplicate_contact(self):
        """Test duplicate contact rejection."""
        self.cm.add_contact("test@example.com", "Test User")
        result = self.cm.add_contact("test@example.com", "Another Name")
        self.assertFalse(result)
        self.assertEqual(self.cm.get_contact_count(), 1)

    def test_remove_contact(self):
        """Test removing contacts."""
        self.cm.add_contact("test@example.com", "Test User")
        self.cm.remove_contact("test@example.com")
        self.assertEqual(self.cm.get_contact_count(), 0)

    def test_import_csv(self):
        """Test CSV import."""
        csv_file = os.path.join(self.temp_dir, "test.csv")
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["email", "name"])
            writer.writerow(["user1@example.com", "User One"])
            writer.writerow(["user2@example.com", "User Two"])

        contacts = self.cm.import_from_file(csv_file, group="test")
        self.assertEqual(len(contacts), 2)

    def test_import_json(self):
        """Test JSON import."""
        json_file = os.path.join(self.temp_dir, "test.json")
        data = [
            {"email": "user1@example.com", "name": "User One"},
            {"email": "user2@example.com", "name": "User Two"},
        ]
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f)

        contacts = self.cm.import_from_file(json_file, fmt="json")
        self.assertEqual(len(contacts), 2)

    def test_list_contacts(self):
        """Test listing contacts."""
        self.cm.add_contact("user1@example.com", "User One", group="group_a")
        self.cm.add_contact("user2@example.com", "User Two", group="group_b")
        self.cm.add_contact("user3@example.com", "User Three", group="group_a")

        all_contacts = self.cm.list_contacts()
        self.assertEqual(len(all_contacts), 3)

        group_a = self.cm.list_contacts(group="group_a")
        self.assertEqual(len(group_a), 2)

    def test_groups(self):
        """Test group listing."""
        self.cm.add_contact("user1@example.com", "User One", group="group_a")
        self.cm.add_contact("user2@example.com", "User Two", group="group_b")

        groups = self.cm.list_groups()
        self.assertEqual(groups.get("group_a"), 1)
        self.assertEqual(groups.get("group_b"), 1)

    def test_search(self):
        """Test contact search."""
        self.cm.add_contact("alice@example.com", "Alice Smith")
        self.cm.add_contact("bob@example.com", "Bob Jones")

        results = self.cm.list_contacts(search="alice")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["email"], "alice@example.com")


class TestTemplateEngine(unittest.TestCase):
    """Test template engine."""

    def setUp(self):
        self.engine = TemplateEngine()

    def test_variable_substitution(self):
        """Test basic variable substitution."""
        template = "Hello, {{name}}! Welcome to {{company}}."
        result = self.engine.render(template, {"name": "Alice", "company": "Acme"})
        self.assertEqual(result, "Hello, Alice! Welcome to Acme.")

    def test_conditional(self):
        """Test conditional blocks."""
        template = "{%if show%}Visible{%endif%}"
        result = self.engine.render(template, {"show": True})
        self.assertEqual(result, "Visible")

        result = self.engine.render(template, {"show": False})
        self.assertEqual(result, "")

    def test_loop(self):
        """Test loop blocks."""
        template = "{%for item in items%}{{item}} {%endfor%}"
        result = self.engine.render(template, {"items": ["a", "b", "c"]})
        self.assertEqual(result, "a b c ")

    def test_built_in_helpers(self):
        """Test built-in helper functions."""
        template = "Date: {{date}}"
        result = self.engine.render(template)
        self.assertIn("Date:", result)

    def test_nested_variables(self):
        """Test nested variable access."""
        template = "{{user.name}} - {{user.email}}"
        result = self.engine.render(template, {"user": {"name": "Alice", "email": "a@b.com"}})
        self.assertEqual(result, "Alice - a@b.com")

    def test_validate(self):
        """Test template validation."""
        template = "{%if x%}hello{%endif%} {{name}}"
        result = self.engine.validate(template)
        self.assertTrue(result["valid"])
        self.assertIn("name", result["user_variables"])

    def test_mismatched_conditionals(self):
        """Test detection of mismatched conditionals."""
        template = "{%if x%}hello"
        result = self.engine.validate(template)
        self.assertFalse(result["valid"])

    def test_create_template(self):
        """Test template creation."""
        output = os.path.join(tempfile.gettempdir(), "test_template.html")
        path = self.engine.create("test", "Test Subject", output)
        self.assertTrue(os.path.exists(path))
        os.unlink(path)


class TestStatsTracker(unittest.TestCase):
    """Test statistics tracker."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        config_path = os.path.join(self.temp_dir, "config.json")
        self.config = Config(config_path=config_path)
        self.tracker = StatsTracker(self.config)

    def test_empty_stats(self):
        """Test stats with no campaigns."""
        stats = self.tracker.get_stats()
        self.assertEqual(stats["total_campaigns"], 0)

    def test_campaign_stats(self):
        """Test saving and retrieving campaign stats."""
        stats_dir = self.config.get_stats_dir()
        test_data = {
            "campaign": "test_campaign",
            "sent": 10,
            "failed": 2,
            "skipped": 1,
            "total_time": 5.5,
            "start_time": "2025-01-01T00:00:00",
            "recipients": [],
        }
        stats_file = stats_dir / "test_campaign_20250101_000000.json"
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f)

        stats = self.tracker.get_stats("test_campaign")
        self.assertEqual(stats["total_sent"], 10)
        self.assertEqual(stats["total_failed"], 2)
        self.assertEqual(stats["runs"], 1)


class TestUtils(unittest.TestCase):
    """Test utility functions."""

    def test_truncate(self):
        """Test string truncation."""
        self.assertEqual(truncate("hello", 10), "hello")
        self.assertEqual(truncate("hello world", 5), "he...")

    def test_format_number(self):
        """Test number formatting."""
        self.assertEqual(format_number(1000), "1,000")
        self.assertEqual(format_number(0), "0")

    def test_colors(self):
        """Test color codes exist."""
        self.assertTrue(hasattr(Colors, "RED"))
        self.assertTrue(hasattr(Colors, "GREEN"))
        self.assertTrue(hasattr(Colors, "BLUE"))


if __name__ == "__main__":
    unittest.main()
