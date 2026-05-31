# Contributing to MailForge-Pro 📧

Thank you for your interest in contributing to MailForge-Pro! This document provides guidelines for contributing.

## 🌟 How to Contribute

### Reporting Bugs 🐛
1. Check if the bug has already been reported in [Issues](https://github.com/gitstq/MailForge-Pro/issues)
2. If not, create a new issue with:
   - Clear description of the bug
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Environment details (OS, Python version)

### Suggesting Features 💡
1. Open an issue with the `[Feature Request]` label
2. Describe the feature and its use case
3. Explain why it would be useful

### Submitting Code 📝
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Write/update tests if applicable
5. Commit with conventional commit messages:
   - `feat: add new feature`
   - `fix: fix a bug`
   - `docs: update documentation`
   - `refactor: code refactoring`
   - `test: add/update tests`
6. Push to your fork: `git push origin feature/your-feature-name`
7. Create a Pull Request

### Code Style 🎨
- Follow PEP 8 guidelines
- Use 4 spaces for indentation
- Add docstrings to all public functions and classes
- Keep functions focused and small
- Add comments for complex logic

### Pull Request Guidelines ✅
- PR title should follow conventional commit format
- Include a clear description of changes
- Reference related issues
- Ensure all tests pass
- No breaking changes without discussion

## 📋 Development Setup

```bash
# Clone the repo
git clone https://github.com/gitstq/MailForge-Pro.git
cd MailForge-Pro

# Run tests
python -m pytest tests/

# Run locally
python -m src.main --help
```

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.
