# Tests

This folder contains unit tests for the py-care application.

## Running Tests

```powershell
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=src --cov-report=html

# Run specific test file
python -m pytest tests/test_config_manager.py
```

## Test Structure

```
tests/
├── __init__.py
├── test_config_manager.py    # Tests for configuration loading
├── test_scheduler.py          # Tests for reminder scheduling
├── test_dialog.py             # Tests for dialog display (may require mocking)
├── test_tray_icon.py          # Tests for system tray functionality
└── fixtures/
    └── test_config.yaml       # Sample config for testing
```

## Testing Guidelines

### What to Test

1. **Configuration Management**:
   - Valid YAML parsing
   - Default value fallbacks
   - Invalid configuration handling
   - Type validation

2. **Scheduler Logic**:
   - Timer accuracy
   - Message sequencing
   - Start/stop functionality
   - Thread safety

3. **Dialog Behavior** (with mocking):
   - Message display
   - Auto-dismiss timing
   - Manual dismiss handling

4. **Integration Tests**:
   - Full application flow
   - Config reload
   - Error recovery

### Setting Up Testing

1. **Install test dependencies**:
   ```powershell
   pip install pytest pytest-cov pytest-mock
   ```

2. **Add to requirements-dev.txt** (create this file):
   ```
   pytest>=7.4.0
   pytest-cov>=4.1.0
   pytest-mock>=3.11.0
   ```

### Example Test

```python
# tests/test_config_manager.py
import pytest
from src.config_manager import ConfigManager

def test_default_config_loads():
    """Test that default configuration loads without file."""
    config = ConfigManager('nonexistent.yaml')
    assert config.get_interval_minutes() == 20
    assert len(config.get_messages()) > 0

def test_custom_interval():
    """Test loading custom interval from config."""
    # Test implementation
    pass
```

## Continuous Integration

Consider adding CI/CD with:
- **GitHub Actions**: `.github/workflows/tests.yml`
- **Pre-commit hooks**: Run tests before commits
- **Code coverage goals**: Aim for >80% coverage

## Test Coverage Goals

- Config Manager: 90%+
- Scheduler: 85%+
- Dialog: 70%+ (UI testing is complex)
- Tray Icon: 70%+ (system tray is platform-dependent)
- Overall: 80%+

---

**Tests help ensure reliability and make refactoring safer!**
