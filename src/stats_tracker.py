#!/usr/bin/env python3
"""
MailForge-Pro - Statistics Tracker
轻量级终端邮件营销智能引擎 - 统计追踪器

Tracks and aggregates campaign statistics including send rates, failure rates,
timing data, and per-campaign analytics.
"""

import json
from pathlib import Path
from datetime import datetime, timedelta


class StatsTracker:
    """Campaign statistics tracker and analyzer."""

    def __init__(self, config):
        """Initialize stats tracker."""
        self.config = config
        self.stats_dir = config.get_stats_dir()
        self.stats_dir.mkdir(parents=True, exist_ok=True)

    def get_stats(self, campaign_name=None):
        """Get campaign statistics."""
        all_stats = self._load_all_stats()

        if campaign_name:
            # Filter by campaign name
            campaign_stats = [s for s in all_stats if s.get("campaign") == campaign_name]
            if campaign_stats:
                return self._aggregate_stats(campaign_stats, campaign_name)
            return {"campaign": campaign_name, "found": False}

        # Return overview of all campaigns
        return self._build_overview(all_stats)

    def _load_all_stats(self):
        """Load all campaign stats from files."""
        stats = []
        for f in self.stats_dir.glob("*.json"):
            try:
                with open(f, 'r', encoding='utf-8') as fp:
                    data = json.load(fp)
                    data["_source_file"] = f.name
                    stats.append(data)
            except (json.JSONDecodeError, IOError):
                continue
        return sorted(stats, key=lambda x: x.get("start_time", ""), reverse=True)

    def _aggregate_stats(self, campaign_stats, campaign_name):
        """Aggregate statistics for a specific campaign."""
        total_sent = sum(s.get("sent", 0) for s in campaign_stats)
        total_failed = sum(s.get("failed", 0) for s in campaign_stats)
        total_skipped = sum(s.get("skipped", 0) for s in campaign_stats)
        total_time = sum(s.get("total_time", 0) for s in campaign_stats)

        success_rate = 0
        if total_sent + total_failed > 0:
            success_rate = (total_sent / (total_sent + total_failed)) * 100

        avg_time = 0
        if campaign_stats:
            avg_time = total_time / len(campaign_stats)

        return {
            "campaign": campaign_name,
            "runs": len(campaign_stats),
            "total_sent": total_sent,
            "total_failed": total_failed,
            "total_skipped": total_skipped,
            "success_rate": round(success_rate, 2),
            "avg_time": round(avg_time, 2),
            "total_time": round(total_time, 2),
            "last_run": campaign_stats[0].get("start_time", "") if campaign_stats else "",
            "recipients": [r for s in campaign_stats for r in s.get("recipients", [])],
        }

    def _build_overview(self, all_stats):
        """Build overview of all campaigns."""
        campaigns = {}
        for s in all_stats:
            name = s.get("campaign", "unnamed")
            if name not in campaigns:
                campaigns[name] = {
                    "campaign": name,
                    "runs": 0,
                    "total_sent": 0,
                    "total_failed": 0,
                    "total_skipped": 0,
                    "last_run": "",
                }
            campaigns[name]["runs"] += 1
            campaigns[name]["total_sent"] += s.get("sent", 0)
            campaigns[name]["total_failed"] += s.get("failed", 0)
            campaigns[name]["total_skipped"] += s.get("skipped", 0)
            if s.get("start_time", "") > campaigns[name]["last_run"]:
                campaigns[name]["last_run"] = s["start_time"]

        # Calculate success rates
        for name, data in campaigns.items():
            total = data["total_sent"] + data["total_failed"]
            data["success_rate"] = round((data["total_sent"] / total) * 100, 2) if total > 0 else 0

        return {
            "total_campaigns": len(campaigns),
            "total_runs": sum(c["runs"] for c in campaigns.values()),
            "total_emails_sent": sum(c["total_sent"] for c in campaigns.values()),
            "total_emails_failed": sum(c["total_failed"] for c in campaigns.values()),
            "campaigns": sorted(campaigns.values(), key=lambda x: x["last_run"], reverse=True),
        }

    def display_stats(self, stats):
        """Display statistics in a formatted table."""
        if "campaigns" in stats:
            # Overview mode
            print("\n📊 MailForge-Pro Campaign Statistics Overview")
            print("=" * 70)
            print(f"  Total Campaigns: {stats.get('total_campaigns', 0)}")
            print(f"  Total Runs: {stats.get('total_runs', 0)}")
            print(f"  Total Emails Sent: {stats.get('total_emails_sent', 0)}")
            print(f"  Total Emails Failed: {stats.get('total_emails_failed', 0)}")
            print()

            campaigns = stats.get("campaigns", [])
            if campaigns:
                print(f"  {'Campaign':<25} {'Runs':<8} {'Sent':<8} {'Failed':<8} {'Rate':<10} {'Last Run':<20}")
                print("  " + "-" * 79)
                for c in campaigns:
                    name = c["campaign"][:24]
                    rate = f"{c['success_rate']}%"
                    last = c.get("last_run", "")[:19]
                    print(f"  {name:<25} {c['runs']:<8} {c['total_sent']:<8} {c['total_failed']:<8} {rate:<10} {last:<20}")
        elif stats.get("found") is False:
            print(f"\n⚠️  No statistics found for campaign: {stats.get('campaign', 'unknown')}")
        else:
            # Single campaign mode
            print(f"\n📊 Campaign: {stats.get('campaign', 'unknown')}")
            print("=" * 50)
            print(f"  Runs: {stats.get('runs', 0)}")
            print(f"  Total Sent: {stats.get('total_sent', 0)}")
            print(f"  Total Failed: {stats.get('total_failed', 0)}")
            print(f"  Total Skipped: {stats.get('total_skipped', 0)}")
            print(f"  Success Rate: {stats.get('success_rate', 0)}%")
            print(f"  Avg Time: {stats.get('avg_time', 0)}s")
            print(f"  Last Run: {stats.get('last_run', 'N/A')}")

            # Show recent recipients
            recipients = stats.get("recipients", [])
            if recipients:
                failed = [r for r in recipients if r.get("status") == "failed"]
                if failed:
                    print(f"\n  ❌ Failed Recipients ({len(failed)}):")
                    for r in failed[:10]:
                        print(f"     {r.get('email', 'unknown')}: {r.get('error', 'unknown error')}")
