import os
import fileinput
import re

def update_file(filepath):
    with fileinput.FileInput(filepath, inplace=True, backup='.bak') as file:
        for line in file:
            # Update import statements
            line = line.replace('from src.', 'from app.')
            line = line.replace('import src.', 'import app.')
            print(line, end='')

def process_test_files():
    test_files = [
        # Unit tests
        'tests/unit/test_ai_processor.py',
        'tests/unit/test_audio_utils.py',
        'tests/unit/test_command_handler.py',
        'tests/unit/test_config.py',
        'tests/unit/test_logging.py',
        'tests/unit/test_redline_generator.py',
        'tests/unit/test_voice_processor.py',
        
        # Integration tests
        'tests/integration/test_ai_processor.py',
        'tests/integration/test_audio_processing.py',
        'tests/integration/test_browser_interaction.py',
        'tests/integration/test_groq_integration.py',
        'tests/integration/test_integration.py',
        'tests/integration/test_main.py',
        
        # conftest
        'tests/conftest.py'
    ]
    
    for file in test_files:
        if os.path.exists(file):
            print(f"Updating {file}...")
            update_file(file)
            print(f"Updated {file}")
        else:
            print(f"Skipping {file} - not found")

if __name__ == "__main__":
    process_test_files() 