import json
import re
import os
import subprocess
import tempfile
import black

class Transpiler:
    def __init__(self, config_path="languages.json"):
        """
        Initializes the Transpiler engine.
        Loads the language rules from the specified JSON configuration file.
        """
        self.config_path = config_path
        self.languages = self._load_config()

    def _load_config(self):
        """
        Loads the rules from the languages.json file.
        Returns an empty dictionary if the file doesn't exist or is invalid.
        """
        if not os.path.exists(self.config_path):
            print(f"Warning: Configuration file {self.config_path} not found.")
            return {}
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {self.config_path}: {e}")
            return {}

    def _format_args(self, match):
        """
        Helper method to format function arguments if the rule requires it.
        E.g., converts 'x y z' into 'x, y, z'
        """
        if not match:
            return ""
        args = match.split()
        return ", ".join(args)

    def transpile_text(self, raw_text, lang="python"):
        """
        Transpiles the raw text into the target language line-by-line.
        Applies rules from languages.json.
        Preserves original indentation levels.
        """
        if lang not in self.languages:
            print(f"Warning: Target language '{lang}' not found in configuration.")
            return raw_text

        rules = self.languages[lang].get("rules", [])
        transpiled_lines = []

        # 1. Syntax Translation
        for line in raw_text.splitlines():
            # Preserve indentation
            indent_match = re.match(r'^(\s*)', line)
            indent = indent_match.group(1) if indent_match else ""
            stripped_line = line.lstrip()

            if not stripped_line:
                transpiled_lines.append(line)
                continue

            matched = False
            for rule in rules:
                pattern = rule["pattern"]
                replacement = rule["replacement"]
                
                match = re.match(pattern, stripped_line)
                if match:
                    if rule.get("format_args", False) and len(match.groups()) > 1:
                        func_name = match.group(1)
                        args_str = match.group(2) if match.group(2) else ""
                        formatted_args = self._format_args(args_str)
                        
                        def replacer(m):
                            res = replacement.replace("\\1", m.group(1))
                            if args_str:
                                res = res.replace("\\2", formatted_args)
                            else:
                                res = res.replace("\\2", "")
                            return res
                        
                        new_code = re.sub(pattern, replacer, stripped_line)
                        transpiled_lines.append(indent + new_code)
                        matched = True
                        break
                    else:
                        new_code = re.sub(pattern, replacement, stripped_line)
                        transpiled_lines.append(indent + new_code)
                        matched = True
                        break
            
            # Fallback Rule: If no rules match, leave the line exactly as is
            if not matched:
                transpiled_lines.append(line)

        compiled_code = "\n".join(transpiled_lines)

        # 2. Auto-Formatting & Linting (Python only)
        if lang == "python":
            try:
                # Format with black
                compiled_code = black.format_str(compiled_code, mode=black.FileMode())
                
                # Lint with flake8
                with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode='w', encoding='utf-8') as f:
                    f.write(compiled_code)
                    temp_path = f.name
                
                # Run flake8 as a subprocess
                import sys
                result = subprocess.run([sys.executable, "-m", "flake8", temp_path], capture_output=True, text=True)
                os.remove(temp_path)

                lint_output = result.stdout.strip()
                if lint_output:
                    # Parse the lint output and append as comments
                    suggestions = []
                    for lint_line in lint_output.splitlines():
                        # Flake8 output format: path:line:col: code message
                        # Using regex to handle Windows paths (C:\...)
                        match = re.search(r':(\d+):\d+:\s*(.*)', lint_line)
                        if match:
                            line_num = match.group(1)
                            msg = match.group(2).strip()
                            suggestions.append(f"# SNAPCODE SUGGESTION (Line {line_num}): {msg}")
                    
                    if suggestions:
                        compiled_code = "\n".join(suggestions) + "\n\n" + compiled_code

            except Exception as e:
                print(f"Warning: Formatting/Linting failed: {e}")

        return compiled_code

# Quick standalone test if run directly
if __name__ == "__main__":
    test_code = """
var name = 5
fn myfunc a b
    loop 5
        out working
    ret a
    
class Engine
    pass
    
try
    out hi
catch err
    out error
finally
    out done
"""
    engine = Transpiler()
    print("--- Transpiled Code with Linting & Formatting ---")
    print(engine.transpile_text(test_code, "python"))
