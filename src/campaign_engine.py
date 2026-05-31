#!/usr/bin/env python3
"""
MailForge-Pro - Campaign Engine
轻量级终端邮件营销智能引擎 - 邮件营销引擎

Core email sending engine with SMTP support, batch processing, rate limiting,
retry logic, open/click tracking, and unsubscribe management.
"""

import smtplib
import imaplib
import email
import time
import uuid
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formataddr, formatdate, make_msgid
from pathlib import Path
from datetime import datetime
from html import escape


class CampaignEngine:
    """Email campaign sending engine with rate limiting and tracking."""

    def __init__(self, config, template_engine, contact_manager):
        """Initialize campaign engine."""
        self.config = config
        self.template = template_engine
        self.contacts = contact_manager
        self.stats_dir = config.get_stats_dir()
        self.stats_dir.mkdir(parents=True, exist_ok=True)

    def run(self, contacts, template_content, options):
        """Run an email campaign."""
        campaign_name = options.get("campaign_name", "unnamed")
        subject = options.get("subject", "")
        from_name = options.get("from_name") or self.config.get("app.default_from_name", "")
        reply_to = options.get("reply_to") or self.config.get("app.default_reply_to", "")
        delay = options.get("delay", 1.0)
        dry_run = options.get("dry_run", False)
        limit = options.get("limit", 0)
        track = options.get("track", False)
        add_unsubscribe = options.get("unsubscribe", False)

        smtp_config = self.config.get_smtp_config()
        sender_email = smtp_config["username"]

        results = {
            "campaign": campaign_name,
            "sent": 0,
            "failed": 0,
            "skipped": 0,
            "start_time": datetime.now().isoformat(),
            "total_time": 0,
            "recipients": [],
        }

        start_time = time.time()

        # Connect to SMTP (unless dry run)
        smtp = None
        if not dry_run:
            try:
                smtp = self._connect_smtp(smtp_config)
            except Exception as e:
                results["error"] = str(e)
                results["end_time"] = datetime.now().isoformat()
                self._save_campaign_stats(campaign_name, results)
                raise

        try:
            for i, contact in enumerate(contacts):
                # Check limit
                if limit > 0 and results["sent"] >= limit:
                    results["skipped"] += len(contacts) - i
                    break

                # Skip invalid contacts
                contact_email = contact.get("email", "")
                if not contact_email or not self.contacts.validate_email(contact_email):
                    results["skipped"] += 1
                    continue

                # Prepare template data
                template_data = {
                    "email": contact_email,
                    "name": contact.get("name", contact_email.split("@")[0]),
                    "first_name": contact.get("name", "").split()[0] if contact.get("name") else contact_email.split("@")[0],
                    "company_name": from_name or "MailForge",
                    "sender_name": from_name or "MailForge",
                    "message": "",
                    **contact.get("extra", {}),
                }

                # Add tracking and unsubscribe
                if track:
                    tracking_id = str(uuid.uuid4())[:8]
                    template_data["tracking_id"] = tracking_id
                    template_data["tracking_pixel"] = f'<img src="" width="1" height="1" alt="" />'

                if add_unsubscribe:
                    template_data["unsubscribe_url"] = f"mailto:{sender_email}?subject=Unsubscribe&body={contact_email}"

                # Render template
                try:
                    rendered = self.template.render(template_content, template_data)
                except Exception as e:
                    results["failed"] += 1
                    results["recipients"].append({
                        "email": contact_email,
                        "status": "failed",
                        "error": f"Template error: {e}",
                    })
                    continue

                # Build email message
                try:
                    msg = self._build_message(
                        subject=subject or f"Message from {from_name or 'MailForge'}",
                        from_email=sender_email,
                        from_name=from_name,
                        to_email=contact_email,
                        to_name=contact.get("name", ""),
                        html_content=rendered,
                        reply_to=reply_to,
                    )
                except Exception as e:
                    results["failed"] += 1
                    results["recipients"].append({
                        "email": contact_email,
                        "status": "failed",
                        "error": f"Message build error: {e}",
                    })
                    continue

                # Send email
                if dry_run:
                    print(f"  📧 [DRY RUN] To: {contact_email} | Subject: {subject or 'N/A'}")
                    results["sent"] += 1
                    results["recipients"].append({
                        "email": contact_email,
                        "status": "dry_run",
                        "timestamp": datetime.now().isoformat(),
                    })
                else:
                    try:
                        smtp.send_message(msg)
                        results["sent"] += 1
                        results["recipients"].append({
                            "email": contact_email,
                            "status": "sent",
                            "timestamp": datetime.now().isoformat(),
                        })
                        print(f"  ✅ [{results['sent']}] Sent to: {contact_email}")
                    except Exception as e:
                        results["failed"] += 1
                        results["recipients"].append({
                            "email": contact_email,
                            "status": "failed",
                            "error": str(e),
                        })
                        print(f"  ❌ Failed to send to {contact_email}: {e}")

                # Rate limiting
                if delay > 0 and i < len(contacts) - 1:
                    time.sleep(delay)

        finally:
            if smtp:
                try:
                    smtp.quit()
                except Exception:
                    pass

        results["end_time"] = datetime.now().isoformat()
        results["total_time"] = time.time() - start_time
        self._save_campaign_stats(campaign_name, results)

        return results

    def _connect_smtp(self, smtp_config):
        """Connect to SMTP server."""
        host = smtp_config["host"]
        port = smtp_config["port"]
        use_ssl = smtp_config["use_ssl"]
        use_tls = smtp_config["use_tls"]
        timeout = smtp_config["timeout"]

        if use_ssl:
            smtp = smtplib.SMTP_SSL(host, port, timeout=timeout)
        else:
            smtp = smtplib.SMTP(host, port, timeout=timeout)

        # Enable TLS if requested
        if use_tls and not use_ssl:
            smtp.starttls()

        # Login
        smtp.login(smtp_config["username"], smtp_config["password"])

        return smtp

    def _build_message(self, subject, from_email, from_name, to_email, to_name,
                       html_content, reply_to=None, text_content=None):
        """Build a MIME email message."""
        msg = MIMEMultipart("alternative")

        # Headers
        msg["Subject"] = subject
        msg["From"] = formataddr((from_name, from_email)) if from_name else from_email
        msg["To"] = formataddr((to_name, to_email)) if to_name else to_email
        msg["Date"] = formatdate(localtime=True)
        msg["Message-ID"] = make_msgid(domain=from_email.split("@")[-1] if "@" in from_email else "localhost")

        if reply_to:
            msg["Reply-To"] = reply_to

        # Add plain text part
        if text_content is None:
            # Auto-generate plain text from HTML (basic strip)
            text_content = self._html_to_text(html_content)

        msg.attach(MIMEText(text_content, "plain", "utf-8"))

        # Add HTML part
        msg.attach(MIMEText(html_content, "html", "utf-8"))

        return msg

    @staticmethod
    def _html_to_text(html_content):
        """Basic HTML to plain text conversion."""
        import re
        # Remove style tags
        text = re.sub(r"<style[^>]*>.*?</style>", "", html_content, flags=re.DOTALL)
        # Remove script tags
        text = re.sub(r"<script[^>]*>.*?</script>", "", text, flags=re.DOTALL)
        # Replace br tags
        text = re.sub(r"<br\s*/?>", "\n", text)
        # Replace p tags
        text = re.sub(r"</p>", "\n\n", text)
        # Replace h tags
        text = re.sub(r"</h[1-6]>", "\n", text)
        # Replace li tags
        text = re.sub(r"</li>", "\n• ", text)
        # Replace a tags
        text = re.sub(r"<a[^>]*href=['\"]([^'\"]*)['\"][^>]*>(.*?)</a>", r"\2 (\1)", text)
        # Remove all remaining tags
        text = re.sub(r"<[^>]+>", "", text)
        # Decode HTML entities
        text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
        text = text.replace("&quot;", '"').replace("&#39;", "'").replace("&nbsp;", " ")
        # Clean up whitespace
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()

    def test_smtp(self):
        """Test SMTP connection."""
        smtp_config = self.config.get_smtp_config()
        try:
            smtp = self._connect_smtp(smtp_config)
            smtp.quit()
            return {"success": True, "server": smtp_config["host"]}
        except smtplib.SMTPAuthenticationError as e:
            return {"success": False, "error": f"Authentication failed: {e}"}
        except smtplib.SMTPConnectError as e:
            return {"success": False, "error": f"Connection failed: {e}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _save_campaign_stats(self, campaign_name, results):
        """Save campaign statistics to file."""
        stats_file = self.stats_dir / f"{campaign_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            with open(stats_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
        except IOError:
            pass  # Silently fail if stats can't be saved
