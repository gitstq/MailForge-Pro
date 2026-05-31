#!/usr/bin/env python3
"""
MailForge-Pro - Template Engine
轻量级终端邮件营销智能引擎 - 模板引擎

Lightweight template engine with variable substitution, conditional blocks,
loop support, and built-in helper functions for email content generation.
"""

import re
import os
import json
from pathlib import Path
from datetime import datetime


class TemplateEngine:
    """Lightweight email template engine with variable substitution and helpers."""

    # Variable placeholder pattern: {{variable_name}}
    VAR_PATTERN = re.compile(r"\{\{\s*([\w.]+)\s*\}\}")

    # Conditional pattern: {%if condition%}...{%endif%}
    IF_PATTERN = re.compile(r"\{%\s*if\s+(\w+)\s*%\}(.*?)\{%\s*endif\s*%\}", re.DOTALL)

    # Loop pattern: {%for item in list%}...{%endfor%}
    FOR_PATTERN = re.compile(r"\{%\s*for\s+(\w+)\s+in\s+(\w+)\s*%\}(.*?)\{%\s*endfor\s*%\}", re.DOTALL)

    # Built-in helper functions
    HELPERS = {
        "now": lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "date": lambda: datetime.now().strftime("%Y-%m-%d"),
        "time": lambda: datetime.now().strftime("%H:%M:%S"),
        "year": lambda: str(datetime.now().year),
        "month": lambda: datetime.now().strftime("%B"),
        "day": lambda: str(datetime.now().day),
    }

    def __init__(self, templates_dir=None):
        """Initialize template engine."""
        self.templates_dir = Path(templates_dir) if templates_dir else None

    def load(self, file_path):
        """Load template content from file."""
        file_path = Path(file_path)
        if not file_path.exists():
            # Try templates directory
            if self.templates_dir:
                alt_path = self.templates_dir / file_path.name
                if alt_path.exists():
                    file_path = alt_path
                else:
                    return None
            else:
                return None

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except IOError:
            return None

    def render(self, template_content, data=None):
        """Render template with variable substitution."""
        if data is None:
            data = {}

        # Merge built-in helpers
        context = {**self.HELPERS, **data}

        # Process conditionals first
        content = self._process_conditionals(template_content, context)

        # Process loops
        content = self._process_loops(content, context)

        # Process variables
        content = self._process_variables(content, context)

        return content

    def _process_variables(self, content, context):
        """Replace {{variable}} placeholders with values."""
        def replacer(match):
            key = match.group(1)
            # Support dot notation for nested access
            value = self._get_nested_value(context, key)
            if value is not None:
                return str(value)
            return match.group(0)  # Keep original if not found

        return self.VAR_PATTERN.sub(replacer, content)

    def _process_conditionals(self, content, context):
        """Process {%if condition%}...{%endif%} blocks."""
        def replacer(match):
            condition = match.group(1)
            body = match.group(2)
            value = context.get(condition)
            if value and str(value).lower() not in ("false", "0", "", "none", "null"):
                return body
            return ""

        return self.IF_PATTERN.sub(replacer, content)

    def _process_loops(self, content, context):
        """Process {%for item in list%}...{%endfor%} blocks."""
        def replacer(match):
            item_var = match.group(1)
            list_var = match.group(2)
            body = match.group(3)
            items = context.get(list_var, [])
            if not isinstance(items, (list, tuple)):
                return ""
            result = []
            for item in items:
                if isinstance(item, dict):
                    loop_context = {**context, item_var: item, **item}
                else:
                    loop_context = {**context, item_var: item}
                result.append(self._process_variables(body, loop_context))
            return "".join(result)

        return self.FOR_PATTERN.sub(replacer, content)

    @staticmethod
    def _get_nested_value(data, key):
        """Get value from nested dict using dot notation."""
        keys = key.split(".")
        value = data
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return None
            if value is None:
                return None
        return value

    def create(self, name, subject="", output=None):
        """Create a new template file with boilerplate content."""
        if output is None:
            output = f"{name}.html"

        output = Path(output)
        content = self._generate_boilerplate(name, subject)

        with open(output, 'w', encoding='utf-8') as f:
            f.write(content)

        return str(output)

    def _generate_boilerplate(self, name, subject):
        """Generate template boilerplate content."""
        subject_text = subject or name
        return (
            "<!DOCTYPE html>\n"
            "<html>\n"
            "<head>\n"
            '    <meta charset="UTF-8">\n'
            '    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
            "    <title>" + subject_text + "</title>\n"
            "    <style>\n"
            "        body {\n"
            "            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;\n"
            "            line-height: 1.6;\n"
            "            color: #333333;\n"
            "            max-width: 600px;\n"
            "            margin: 0 auto;\n"
            "            padding: 20px;\n"
            "        }\n"
            "        .header {\n"
            "            background-color: #4A90D9;\n"
            "            color: white;\n"
            "            padding: 20px;\n"
            "            text-align: center;\n"
            "            border-radius: 8px 8px 0 0;\n"
            "        }\n"
            "        .content {\n"
            "            padding: 30px;\n"
            "            background-color: #ffffff;\n"
            "            border: 1px solid #e0e0e0;\n"
            "            border-top: none;\n"
            "        }\n"
            "        .footer {\n"
            "            padding: 20px;\n"
            "            text-align: center;\n"
            "            color: #999999;\n"
            "            font-size: 12px;\n"
            "        }\n"
            "        .button {\n"
            "            display: inline-block;\n"
            "            padding: 12px 24px;\n"
            "            background-color: #4A90D9;\n"
            "            color: white;\n"
            "            text-decoration: none;\n"
            "            border-radius: 4px;\n"
            "            font-weight: bold;\n"
            "        }\n"
            "    </style>\n"
            "</head>\n"
            "<body>\n"
            "    <div class=\"header\">\n"
            "        <h1>{{company_name}}</h1>\n"
            "    </div>\n"
            "    <div class=\"content\">\n"
            "        <h2>Hello, {{name}}!</h2>\n"
            "        <p>{{message}}</p>\n"
            "\n"
            "        {%if has_button%}\n"
            '        <p style="text-align: center;">\n'
            "            <a href=\"{{button_url}}\" class=\"button\">{{button_text}}</a>\n"
            "        </p>\n"
            "        {%endif%}\n"
            "\n"
            "        <p>Thank you for your interest!</p>\n"
            "        <p>Best regards,<br>{{sender_name}}</p>\n"
            "    </div>\n"
            "    <div class=\"footer\">\n"
            "        <p>Sent on {{date}} | {{company_name}}</p>\n"
            "        {%if unsubscribe_url%}\n"
            "        <p><a href=\"{{unsubscribe_url}}\">Unsubscribe</a></p>\n"
            "        {%endif%}\n"
            "    </div>\n"
            "</body>\n"
            "</html>\n"
        )

    def list_templates(self):
        """List available template files."""
        templates = []
        # Check current directory
        for f in Path(".").glob("*.html"):
            templates.append(f.name)
        for f in Path(".").glob("*.txt"):
            templates.append(f.name)
        # Check templates directory
        if self.templates_dir and self.templates_dir.exists():
            for f in self.templates_dir.glob("*"):
                if f.suffix in (".html", ".txt", ".mjml"):
                    templates.append(f.name)
        return sorted(set(templates))

    def validate(self, template_content):
        """Validate template syntax. Returns list of issues."""
        issues = []

        # Check for unclosed conditionals
        open_ifs = len(re.findall(r"\{%\s*if\s+\w+\s*%\}", template_content))
        close_ifs = len(re.findall(r"\{%\s*endif\s*%\}", template_content))
        if open_ifs != close_ifs:
            issues.append(f"Mismatched conditionals: {open_ifs} open, {close_ifs} close")

        # Check for unclosed loops
        open_fors = len(re.findall(r"\{%\s*for\s+\w+\s+in\s+\w+\s*%\}", template_content))
        close_fors = len(re.findall(r"\{%\s*endfor\s*%\}", template_content))
        if open_fors != close_fors:
            issues.append(f"Mismatched loops: {open_fors} open, {close_fors} close")

        # Extract and list variables used
        variables = set(self.VAR_PATTERN.findall(template_content))
        builtins = set(self.HELPERS.keys())
        user_vars = variables - builtins

        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "variables": sorted(variables),
            "user_variables": sorted(user_vars),
        }
