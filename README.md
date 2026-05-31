<div align="center">

# 📧 MailForge-Pro

**Lightweight Terminal Email Marketing Intelligent Engine**

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero-success.svg)](pyproject.toml)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()

[简体中文](#简体中文) | [繁體中文](#繁體中文) | [English](#english)

</div>

---

<a id="english"></a>

## 🎉 About

**MailForge-Pro** is a lightweight, zero-dependency terminal email marketing intelligent engine built with Python. It provides a complete CLI toolkit for managing email campaigns — from contact management and template rendering to batch sending with rate limiting, real-time analytics, and an interactive TUI dashboard.

### 💡 Why MailForge-Pro?

- **Zero External Dependencies** — Built entirely with Python standard library, no pip install needed
- **Privacy-First** — All data stored locally, no cloud services required
- **Developer-Friendly** — Clean CLI interface with intuitive commands
- **Self-Hosted** — Full control over your email infrastructure

### 🌟 Inspiration

Inspired by the growing demand for self-hosted email marketing solutions (like BillionMail trending on GitHub), MailForge-Pro brings email campaign capabilities directly to your terminal with zero setup overhead.

---

## ✨ Core Features

| Feature | Description |
|---------|-------------|
| 📤 **Campaign Engine** | Full SMTP support with TLS/SSL, batch sending, rate limiting, and retry logic |
| 📝 **Template Engine** | Variable substitution (`{{name}}`), conditionals (`{%if%}`), loops (`{%for%}`), built-in helpers |
| 👥 **Contact Manager** | CSV/JSON import, grouping, search, deduplication, email validation |
| 📊 **Statistics Tracker** | Per-campaign analytics with success rates, timing data, and failure tracking |
| 🖥️ **TUI Dashboard** | Real-time interactive terminal dashboard for monitoring campaigns |
| 🔒 **Zero Dependencies** | Pure Python standard library — no external packages required |
| 🌍 **Cross-Platform** | Works on Windows, macOS, and Linux |
| 📋 **Dry Run Mode** | Preview campaigns without actually sending emails |
| 🎯 **Personalization** | Per-recipient template rendering with custom variables |
| 🚫 **Unsubscribe Support** | Built-in unsubscribe link generation |
| ⏱️ **Rate Limiting** | Configurable delay between sends to avoid spam filters |
| 📦 **Batch Processing** | Send to thousands of contacts with progress tracking |

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** installed
- An SMTP server (Gmail, SendGrid, Mailgun, or any SMTP service)

### Installation

```bash
# Clone the repository
git clone https://github.com/gitstq/MailForge-Pro.git
cd MailForge-Pro

# Run directly (no installation needed!)
python -m src.main --help
```

### Configure SMTP

```bash
# Set your SMTP server
mailforge config set --key smtp.host --value smtp.gmail.com
mailforge config set --key smtp.port --value 587
mailforge config set --key smtp.username --value your@email.com
mailforge config set --key smtp.password --value your_app_password

# Test connection
mailforge config test
```

### Send Your First Campaign

```bash
# Import contacts
mailforge contacts import --file contacts.csv --group subscribers

# Create a template
mailforge template create --name welcome --subject "Welcome!"

# Send campaign (dry run first!)
mailforge send -c welcome -t welcome.html -co contacts.csv --dry-run

# Send for real
mailforge send -c welcome -t welcome.html -co contacts.csv --subject "Welcome to MailForge!" --delay 2.0
```

---

## 📖 Detailed Usage Guide

### 📤 Sending Campaigns

```bash
# Basic send
mailforge send -c campaign_name -t template.html -co contacts.csv

# With all options
mailforge send \
  -c newsletter \
  -t templates/newsletter.html \
  -co contacts.csv \
  --subject "Monthly Newsletter" \
  --from-name "My Company" \
  --reply-to reply@company.com \
  --delay 1.5 \
  --limit 100 \
  --track \
  --unsubscribe
```

### 👥 Contact Management

```bash
# Import from CSV
mailforge contacts import --file subscribers.csv --group newsletter

# Import from JSON
mailforge contacts import --file data.json --format json --group vip

# List all contacts
mailforge contacts list

# Filter by group
mailforge contacts list --group newsletter

# Search contacts
mailforge contacts list --search "gmail"

# Remove a contact
mailforge contacts remove --email unwanted@example.com

# List groups
mailforge contacts groups
```

### 📝 Template Management

```bash
# Create a new template
mailforge template create --name promo --subject "Special Offer" --output promo.html

# List available templates
mailforge template list

# Preview a template with sample data
mailforge template preview --file welcome.html --data sample.json
```

### 📊 Campaign Statistics

```bash
# View all campaign stats
mailforge stats

# View specific campaign
mailforge stats --campaign welcome

# Export as JSON
mailforge stats --format json
```

### ⚙️ Configuration

```bash
# Set a config value
mailforge config set --key smtp.host --value smtp.gmail.com

# Show all config
mailforge config show

# Test SMTP connection
mailforge config test
```

### 🖥️ TUI Dashboard

```bash
# Open interactive dashboard (auto-refresh every 5s)
mailforge dashboard

# Custom refresh interval
mailforge dashboard --refresh 10
```

### 📝 Template Syntax

MailForge-Pro templates support:

```html
<!-- Variable substitution -->
Hello, {{name}}! Your email is {{email}}.

<!-- Nested variables -->
Company: {{user.company.name}}

<!-- Conditional blocks -->
{%if premium%}
  <p>Thanks for being a premium member!</p>
{%endif%}

<!-- Loop blocks -->
{%for item in items%}
  <p>{{item.name}} - {{item.price}}</p>
{%endfor%}

<!-- Built-in helpers -->
Date: {{date}} | Time: {{time}} | Year: {{year}}
```

---

## 💡 Design Philosophy & Roadmap

### Design Principles

1. **Zero Dependencies** — Everything runs on Python standard library
2. **Privacy First** — No data leaves your machine
3. **Simplicity** — Clean CLI, no complex setup
4. **Extensibility** — Modular architecture for easy extension

### Roadmap

- [ ] Web UI dashboard
- [ ] IMAP bounce/failure tracking
- [ ] A/B testing support
- [ ] Scheduled campaign sending
- [ ] Email validation API integration
- [ ] Plugin system for custom processors

---

## 📦 Installation & Deployment

### Direct Run (Recommended)

```bash
git clone https://github.com/gitstq/MailForge-Pro.git
cd MailForge-Pro
python -m src.main [command]
```

### Install as Package

```bash
git clone https://github.com/gitstq/MailForge-Pro.git
cd MailForge-Pro
pip install .

# Now use directly
mailforge [command]
```

### Compatible Environments

| Platform | Python 3.8 | Python 3.9 | Python 3.10 | Python 3.11 | Python 3.12 |
|----------|:----------:|:----------:|:-----------:|:-----------:|:-----------:|
| Windows  | ✅ | ✅ | ✅ | ✅ | ✅ |
| macOS    | ✅ | ✅ | ✅ | ✅ | ✅ |
| Linux    | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Made with ❤️ by [gitstq](https://github.com/gitstq)**

⭐ If you find this project helpful, please give it a star!

</div>

---

<a id="简体中文"></a>

# 📧 MailForge-Pro（简体中文）

**轻量级终端邮件营销智能引擎**

## 🎉 项目介绍

**MailForge-Pro** 是一个基于 Python 构建的轻量级、零依赖终端邮件营销智能引擎。它提供了一套完整的 CLI 工具集，用于管理邮件营销活动——从联系人管理和模板渲染，到带速率限制的批量发送、实时分析，以及交互式 TUI 仪表盘。

### 💡 为什么选择 MailForge-Pro？

- **零外部依赖** — 完全基于 Python 标准库构建，无需 pip install
- **隐私优先** — 所有数据本地存储，无需云服务
- **开发者友好** — 清晰的 CLI 界面，直观的命令设计
- **完全自托管** — 完全掌控你的邮件基础设施

### 🌟 灵感来源

受到自托管邮件营销解决方案日益增长的需求启发（如 GitHub 上热门的 BillionMail），MailForge-Pro 将邮件营销能力直接带到你的终端，零配置开销。

---

## ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 📤 **营销引擎** | 完整 SMTP 支持（TLS/SSL）、批量发送、速率限制、重试机制 |
| 📝 **模板引擎** | 变量替换（`{{name}}`）、条件判断（`{%if%}`）、循环（`{%for%}`）、内置助手函数 |
| 👥 **联系人管理** | CSV/JSON 导入、分组、搜索、去重、邮箱验证 |
| 📊 **统计追踪** | 按活动分析，含成功率、时间数据、失败追踪 |
| 🖥️ **TUI 仪表盘** | 实时交互式终端仪表盘，监控营销活动 |
| 🔒 **零依赖** | 纯 Python 标准库 — 无需任何外部包 |
| 🌍 **跨平台** | 支持 Windows、macOS 和 Linux |
| 📋 **试运行模式** | 预览活动而不实际发送邮件 |
| 🎯 **个性化** | 按收件人渲染模板，支持自定义变量 |
| 🚫 **退订支持** | 内置退订链接生成 |
| ⏱️ **速率限制** | 可配置发送间隔，避免触发垃圾邮件过滤器 |
| 📦 **批量处理** | 向数千联系人发送，带进度追踪 |

---

## 🚀 快速开始

### 环境要求

- **Python 3.8+**
- SMTP 服务器（Gmail、SendGrid、Mailgun 或任何 SMTP 服务）

### 安装

```bash
# 克隆仓库
git clone https://github.com/gitstq/MailForge-Pro.git
cd MailForge-Pro

# 直接运行（无需安装！）
python -m src.main --help
```

### 配置 SMTP

```bash
# 设置 SMTP 服务器
mailforge config set --key smtp.host --value smtp.gmail.com
mailforge config set --key smtp.port --value 587
mailforge config set --key smtp.username --value your@email.com
mailforge config set --key smtp.password --value your_app_password

# 测试连接
mailforge config test
```

### 发送你的第一个营销活动

```bash
# 导入联系人
mailforge contacts import --file contacts.csv --group subscribers

# 创建模板
mailforge template create --name welcome --subject "欢迎！"

# 试运行
mailforge send -c welcome -t welcome.html -co contacts.csv --dry-run

# 正式发送
mailforge send -c welcome -t welcome.html -co contacts.csv --subject "欢迎加入 MailForge！" --delay 2.0
```

---

## 📖 详细使用指南

### 📤 发送营销活动

```bash
# 基本发送
mailforge send -c campaign_name -t template.html -co contacts.csv

# 完整选项
mailforge send \
  -c newsletter \
  -t templates/newsletter.html \
  -co contacts.csv \
  --subject "月度通讯" \
  --from-name "我的公司" \
  --reply-to reply@company.com \
  --delay 1.5 \
  --limit 100 \
  --track \
  --unsubscribe
```

### 👥 联系人管理

```bash
# 从 CSV 导入
mailforge contacts import --file subscribers.csv --group newsletter

# 从 JSON 导入
mailforge contacts import --file data.json --format json --group vip

# 列出所有联系人
mailforge contacts list

# 按分组筛选
mailforge contacts list --group newsletter

# 搜索联系人
mailforge contacts list --search "gmail"

# 移除联系人
mailforge contacts remove --email unwanted@example.com

# 列出分组
mailforge contacts groups
```

### 📝 模板管理

```bash
# 创建新模板
mailforge template create --name promo --subject "特别优惠" --output promo.html

# 列出可用模板
mailforge template list

# 预览模板
mailforge template preview --file welcome.html --data sample.json
```

### 📊 活动统计

```bash
# 查看所有活动统计
mailforge stats

# 查看特定活动
mailforge stats --campaign welcome

# 导出为 JSON
mailforge stats --format json
```

### 📝 模板语法

```html
<!-- 变量替换 -->
你好，{{name}}！你的邮箱是 {{email}}。

<!-- 条件判断 -->
{%if premium%}
  <p>感谢你成为高级会员！</p>
{%endif%}

<!-- 循环 -->
{%for item in items%}
  <p>{{item.name}} - {{item.price}}</p>
{%endfor%}

<!-- 内置助手函数 -->
日期：{{date}} | 时间：{{time}} | 年份：{{year}}
```

---

## 💡 设计思路与迭代规划

### 设计理念

1. **零依赖** — 一切基于 Python 标准库运行
2. **隐私优先** — 数据不离开你的机器
3. **简洁至上** — 清晰的 CLI，无需复杂配置
4. **可扩展** — 模块化架构，易于扩展

### 后续规划

- [ ] Web UI 仪表盘
- [ ] IMAP 退信/失败追踪
- [ ] A/B 测试支持
- [ ] 定时发送
- [ ] 邮箱验证 API 集成
- [ ] 插件系统

---

## 📦 打包与部署

```bash
# 直接运行（推荐）
git clone https://github.com/gitstq/MailForge-Pro.git
cd MailForge-Pro
python -m src.main [command]

# 安装为包
pip install .
mailforge [command]
```

---

## 🤝 贡献指南

欢迎贡献！请阅读 [贡献指南](CONTRIBUTING.md) 了解详情。

---

## 📄 开源协议

本项目基于 MIT 协议开源 - 详见 [LICENSE](LICENSE) 文件。

---

<div align="center">

**由 [gitstq](https://github.com/gitstq) 用 ❤️ 打造**

⭐ 如果这个项目对你有帮助，请给个 Star！

</div>

---

<a id="繁體中文"></a>

# 📧 MailForge-Pro（繁體中文）

**輕量級終端郵件營銷智慧引擎**

## 🎉 專案介紹

**MailForge-Pro** 是一個基於 Python 構建的輕量級、零依賴終端郵件營銷智慧引擎。它提供了一套完整的 CLI 工具集，用於管理郵件營銷活動——從聯絡人管理和模板渲染，到帶速率限制的批次發送、即時分析，以及互動式 TUI 儀表盤。

### 💡 為什麼選擇 MailForge-Pro？

- **零外部依賴** — 完全基於 Python 標準庫構建，無需 pip install
- **隱私優先** — 所有資料本地存儲，無需雲端服務
- **開發者友善** — 清晰的 CLI 介面，直觀的命令設計
- **完全自託管** — 完全掌控你的郵件基礎設施

### 🌟 靈感來源

受到自託管郵件營銷解決方案日益增長的需求啟發（如 GitHub 上熱門的 BillionMail），MailForge-Pro 將郵件營銷能力直接帶到你的終端，零配置開銷。

---

## ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 📤 **營銷引擎** | 完整 SMTP 支援（TLS/SSL）、批次發送、速率限制、重試機制 |
| 📝 **模板引擎** | 變數替換（`{{name}}`）、條件判斷（`{%if%}`）、迴圈（`{%for%}`）、內建助手函數 |
| 👥 **聯絡人管理** | CSV/JSON 匯入、分組、搜尋、去重、郵箱驗證 |
| 📊 **統計追蹤** | 按活動分析，含成功率、時間資料、失敗追蹤 |
| 🖥️ **TUI 儀表盤** | 即時互動式終端儀表盤，監控營銷活動 |
| 🔒 **零依賴** | 純 Python 標準庫 — 無需任何外部套件 |
| 🌍 **跨平台** | 支援 Windows、macOS 和 Linux |
| 📋 **試運行模式** | 預覽活動而不實際發送郵件 |
| 🎯 **個人化** | 按收件人渲染模板，支援自訂變數 |
| 🚫 **退訂支援** | 內建退訂連結生成 |
| ⏱️ **速率限制** | 可配置發送間隔，避免觸發垃圾郵件過濾器 |
| 📦 **批次處理** | 向數千聯絡人發送，帶進度追蹤 |

---

## 🚀 快速開始

### 環境要求

- **Python 3.8+**
- SMTP 伺服器（Gmail、SendGrid、Mailgun 或任何 SMTP 服務）

### 安裝

```bash
# 克隆倉庫
git clone https://github.com/gitstq/MailForge-Pro.git
cd MailForge-Pro

# 直接運行（無需安裝！）
python -m src.main --help
```

### 配置 SMTP

```bash
# 設定 SMTP 伺服器
mailforge config set --key smtp.host --value smtp.gmail.com
mailforge config set --key smtp.port --value 587
mailforge config set --key smtp.username --value your@email.com
mailforge config set --key smtp.password --value your_app_password

# 測試連接
mailforge config test
```

### 發送你的第一個營銷活動

```bash
# 匯入聯絡人
mailforge contacts import --file contacts.csv --group subscribers

# 建立模板
mailforge template create --name welcome --subject "歡迎！"

# 試運行
mailforge send -c welcome -t welcome.html -co contacts.csv --dry-run

# 正式發送
mailforge send -c welcome -t welcome.html -co contacts.csv --subject "歡迎加入 MailForge！" --delay 2.0
```

---

## 📖 詳細使用指南

### 📤 發送營銷活動

```bash
# 基本發送
mailforge send -c campaign_name -t template.html -co contacts.csv

# 完整選項
mailforge send \
  -c newsletter \
  -t templates/newsletter.html \
  -co contacts.csv \
  --subject "月度通訊" \
  --from-name "我的公司" \
  --reply-to reply@company.com \
  --delay 1.5 \
  --limit 100 \
  --track \
  --unsubscribe
```

### 👥 聯絡人管理

```bash
# 從 CSV 匯入
mailforge contacts import --file subscribers.csv --group newsletter

# 從 JSON 匯入
mailforge contacts import --file data.json --format json --group vip

# 列出所有聯絡人
mailforge contacts list

# 按分組篩選
mailforge contacts list --group newsletter

# 搜尋聯絡人
mailforge contacts list --search "gmail"

# 移除聯絡人
mailforge contacts remove --email unwanted@example.com

# 列出分組
mailforge contacts groups
```

### 📝 模板管理

```bash
# 建立新模板
mailforge template create --name promo --subject "特別優惠" --output promo.html

# 列出可用模板
mailforge template list

# 預覽模板
mailforge template preview --file welcome.html --data sample.json
```

### 📊 活動統計

```bash
# 查看所有活動統計
mailforge stats

# 查看特定活動
mailforge stats --campaign welcome

# 匯出為 JSON
mailforge stats --format json
```

### 📝 模板語法

```html
<!-- 變數替換 -->
你好，{{name}}！你的郵箱是 {{email}}。

<!-- 條件判斷 -->
{%if premium%}
  <p>感謝你成為高級會員！</p>
{%endif%}

<!-- 迴圈 -->
{%for item in items%}
  <p>{{item.name}} - {{item.price}}</p>
{%endfor%}

<!-- 內建助手函數 -->
日期：{{date}} | 時間：{{time}} | 年份：{{year}}
```

---

## 💡 設計思路與迭代規劃

### 設計理念

1. **零依賴** — 一切基於 Python 標準庫運行
2. **隱私優先** — 資料不離開你的機器
3. **簡潔至上** — 清晰的 CLI，無需複雜配置
4. **可擴展** — 模組化架構，易於擴展

### 後續規劃

- [ ] Web UI 儀表盤
- [ ] IMAP 退信/失敗追蹤
- [ ] A/B 測試支援
- [ ] 定時發送
- [ ] 郵箱驗證 API 整合
- [ ] 插件系統

---

## 📦 打包與部署

```bash
# 直接運行（推薦）
git clone https://github.com/gitstq/MailForge-Pro.git
cd MailForge-Pro
python -m src.main [command]

# 安裝為套件
pip install .
mailforge [command]
```

---

## 🤝 貢獻指南

歡迎貢獻！請閱讀 [貢獻指南](CONTRIBUTING.md) 了解詳情。

---

## 📄 開源協議

本專案基於 MIT 協議開源 - 詳見 [LICENSE](LICENSE) 檔案。

---

<div align="center">

**由 [gitstq](https://github.com/gitstq) 用 ❤️ 打造**

⭐ 如果這個專案對你有幫助，請給個 Star！

</div>
