import time
import keyboard
import pyperclip
from engine import Transpiler

# Global configuration for the default target language
TARGET_LANGUAGE = "python"

# Initialize the transpiler engine
engine = Transpiler()

def process_shorthand():
    """
    The main callback triggered by the global hotkey.
    Executes the text extraction, transpilation, and replacement workflow.
    """
    print("Hotkey triggered! Processing shorthand...")
    
    # Crucial: Sleep briefly to allow the user to release physical keys (Ctrl, Shift, Enter)
    # If they are still holding them, simulated keys will combine with physical keys and fail.
    time.sleep(0.4)
    
    # Save the user's current clipboard text
    original_clipboard = pyperclip.paste()
    
    try:
        # Clear clipboard to detect if copy actually succeeded
        pyperclip.copy("")
        
        # Simulate Ctrl + C
        keyboard.send("ctrl+c")
        
        # Give the OS some time to process the copy command
        time.sleep(0.2)
        
        # Extract text from the clipboard
        raw_shorthand = pyperclip.paste()
        
        if not raw_shorthand.strip():
            print("No text was selected or clipboard is empty (Ctrl+C failed).")
            return

        # Run it through the engine
        compiled_code = engine.transpile_text(raw_shorthand, lang=TARGET_LANGUAGE)
        
        # Copy the newly compiled code back to the clipboard
        pyperclip.copy(compiled_code)
        
        # Simulate Ctrl + V to paste
        keyboard.send("ctrl+v")
        
        # Add a tiny delay to allow paste to finish before restoring clipboard
        time.sleep(0.1)
        
        print("Successfully transpiled and replaced text.")
        
    except Exception as e:
        print(f"Error during transpilation process: {e}")
        
    finally:
        # Restore the user's original clipboard text
        time.sleep(0.1)
        pyperclip.copy(original_clipboard)

def main():
    """
    Starts the daemon and listens for the global hotkey.
    """
    hotkey = "f9"
    print(f"Starting Snapcode Daemon...")
    print(f"Listening for global hotkey: {hotkey.upper()}")
    print("-----------------------------------------------------------------")
    print("INSTRUCTIONS:")
    print("1. Keep this command prompt running in the background.")
    print("2. Open your text editor (VSCode, Notepad, etc.).")
    print("3. Type some shorthand, e.g., 'out Hello World'")
    print("4. Select/Highlight the text in your editor.")
    print("5. Press F9 on your keyboard.")
    print("-----------------------------------------------------------------")
    print(f"Target Language: {TARGET_LANGUAGE}")
    print("Press ESC to exit the daemon.")
    
    # Register the hotkey to trigger the process_shorthand function
    keyboard.add_hotkey(hotkey, process_shorthand)
    
    # Keep the script running until the user presses 'esc'
    keyboard.wait("esc")
    print("Snapcode Daemon stopped.")

if __name__ == "__main__":
    main()
