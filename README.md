# Snapcode Transpiler

An ultra-lightweight, high-performance developer tool that allows you to write rapid, minimalist shorthand syntax in ANY plain text editor and instantly compile it into valid, production-ready source code.

## Setup Instructions

1. **Install Dependencies**
   Ensure you have Python 3.x installed. Install the required libraries using pip:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Daemon**
   Start the background daemon process:
   ```bash
   python vibe_daemon.py
   ```
   The daemon will run quietly in the background, listening for the global hotkey.

## How to Use

1. Open **any** text editor (VSCode, Notepad, Sublime Text, etc.).
2. Type some shorthand syntax. For example:
   ```text
   fn calculate_sum a b
       out calculating...
       return a + b
   ```
3. **Highlight** (select) the shorthand text.
4. Press the global hotkey: `F9`.
5. The selected text will instantly be replaced with valid code (defaults to Python):
   ```python
   def calculate_sum(a, b):
       print("calculating...")
       return a + b
   ```

*Note: If a line doesn't match any shorthand rules, it will be left exactly as is.*

## Adding a New Language

The engine uses deterministic regex rules defined in `languages.json`. You can easily add support for a new language (like C++ or Go) by adding a new object to the JSON file.

### Example: Adding Go support
Open `languages.json` and add a new "go" section:

```json
{
  "go": {
    "rules": [
      {
        "pattern": "^out\\s+(.*)$",
        "replacement": "fmt.Println(\"\\1\")",
        "description": "Output statement"
      },
      {
        "pattern": "^fn\\s+([a-zA-Z_][a-zA-Z0-9_]*)(?:\\s+(.*))?$",
        "replacement": "func \\1(\\2) {",
        "format_args": true,
        "description": "Function definition"
      }
    ]
  }
}
```

Then, change the `TARGET_LANGUAGE` variable in `vibe_daemon.py` to `"go"`:
```python
TARGET_LANGUAGE = "go"
```
Restart the daemon, and your shorthand will now compile to Go!
