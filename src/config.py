#!/usr/bin/env python3
"""
MailForge-Pro - Configuration Manager
轻量级终端邮件营销智能引擎 - 配置管理器

Manages SMTP settings, application preferences, and persistent configuration.
"""

import os
import json
from pathlib import Path


class Config:
    """Application configuration manager with persistent storage."""

    DEFAULT_CONFIG = {
        "smtp.host": "",
        "smtp.port": "587",
        "smtp.username": "",
        "smtp.password": "",
        "smtp.use_tls": "true",
        "smtp.use_ssl": "false",
        "smtp.timeout": "30",
        "app.data_dir": "",
        "app.contacts_dir": "",
        "app.templates_dir": "",
        "app.stats_dir": "",
        "app.default_from_name": "",
        "app.default_reply_to": "",
        "app.default_delay": "1.0",
        "app.max_retries": "3",
        "app.log_level": "INFO",
        "app.language": "en",
    }

    def __init__(self, config_path=None):
        """Initialize configuration manager."""
        if config_path is None:
            # Default config location: ~/.mailforge/config.json
            self.config_dir = Path.home() / ".mailforge"
        else:
            self.config_dir = Path(config_path).parent

        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = self.config_dir / "config.json"
        self._config = self._load()

        # Ensure data directories exist
        self._ensure_dirs()

    def _load(self):
        """Load configuration from file."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    saved = json.load(f)
                # Merge with defaults
                config = {**self.DEFAULT_CONFIG, **saved}
                return config
            except (json.JSONDecodeError, IOError):
                return dict(self.DEFAULT_CONFIG)
        return dict(self.DEFAULT_CONFIG)

    def _save(self):
        """Save configuration to file."""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=2, ensure_ascii=False)
        except IOError as e:
            raise RuntimeError(f"Failed to save config: {e}")

    def _ensure_dirs(self):
        """Ensure all required data directories exist."""
        dirs = {
            "contacts": self.get_data_dir() / "contacts",
            "templates": self.get_data_dir() / "templates",
            "stats": self.get_data_dir() / "stats",
        }
        for dir_path in dirs.values():
            dir_path.mkdir(parents=True, exist_ok=True)

    def get(self, key, default=None):
        """Get a configuration value."""
        return self._config.get(key, default or self.DEFAULT_CONFIG.get(key, ""))

    def set(self, key, value):
        """Set a configuration value and persist."""
        self._config[key] = value
        self._save()

    def get_all(self):
        """Get all configuration values."""
        return dict(self._config)

    def get_data_dir(self):
        """Get the data directory path."""
        custom = self.get("app.data_dir")
        if custom:
            return Path(custom)
        return self.config_dir / "data"

    def get_contacts_dir(self):
        """Get the contacts directory path."""
        custom = self.get("app.contacts_dir")
        if custom:
            return Path(custom)
        return self.get_data_dir() / "contacts"

    def get_templates_dir(self):
        """Get the templates directory path."""
        custom = self.get("app.templates_dir")
        if custom:
            return Path(custom)
        return self.get_data_dir() / "templates"

    def get_stats_dir(self):
        """Get the stats directory path."""
        custom = self.get("app.stats_dir")
        if custom:
            return Path(custom)
        return self.get_data_dir() / "stats"

    def get_smtp_config(self):
        """Get SMTP configuration as a dictionary."""
        return {
            "host": self.get("smtp.host"),
            "port": int(self.get("smtp.port", "587")),
            "username": self.get("smtp.username"),
            "password": self.get("smtp.password"),
            "use_tls": self.get("smtp.use_tls", "true").lower() == "true",
            "use_ssl": self.get("smtp.use_ssl", "false").lower() == "true",
            "timeout": int(self.get("smtp.timeout", "30")),
        }

    def display(self):
        """Display current configuration (with masked sensitive values)."""
        print("⚙️  MailForge-Pro Configuration")
        print("=" * 50)

        # SMTP settings
        print("\n📧 SMTP Settings:")
        smtp_keys = [k for k in self._config if k.startswith("smtp.")]
        for key in smtp_keys:
            value = self._config[key]
            if "password" in key and value:
                masked = "*" * len(value)
                print(f"   {key}: {masked}")
            elif value:
                print(f"   {key}: {value}")
            else:
                print(f"   {key}: (not set)")

        # App settings
        print("\n🔧 Application Settings:")
        app_keys = [k for k in self._config if k.startswith("app.")]
        for key in app_keys:
            value = self._config[key]
            if value:
                print(f"   {key}: {value}")
            else:
                print(f"   {key}: (default)")

        print(f"\n📁 Data Directory: {self.get_data_dir()}")
        print(f"📁 Config File: {self.config_file}")
