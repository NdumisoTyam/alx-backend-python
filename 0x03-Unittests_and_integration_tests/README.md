# 🧪 Unit Tests for `utils.access_nested_map`

This module contains unit tests for the `access_nested_map` function defined in `utils.py`. The tests are written using Python's `unittest` framework and enhanced with `parameterized` to cover multiple input scenarios efficiently.

## ✅ Purpose

The `access_nested_map` function retrieves values from nested dictionaries using a tuple path. These tests ensure the function behaves correctly for:

- Simple key access
- Nested dictionary access
- Deeply nested key resolution

## 📂 File Structure
alx-backend-python/ └── 0x03-Unittests_and_integration_tests/ ├── utils.py └── test_utils.py ← This file


## 🧪 Test Cases

The following input combinations are tested:

| Nested Map              | Path         | Expected Result |
|------------------------|--------------|-----------------|
| `{"a": 1}`             | `("a",)`     | `1`             |
| `{"a": {"b": 2}}`      | `("a",)`     | `{"b": 2}`      |
| `{"a": {"b": 2}}`      | `("a", "b")` | `2`             |

## 🚀 Running the Tests

Make sure you have `parameterized` installed:

```bash
pip install parameterized

