import pytest
from src.config import Settings
import os
from pydantic import ValidationError

def test_settings_initialization():
    settings = Settings()
    assert isinstance(settings, Settings)
    assert hasattr(settings, 'GROQ_API_KEY')

def test_env_file_loading():
    # Create a temporary .env file
    with open('.env.test', 'w') as f:
        f.write('GROQ_API_KEY=test_key')
    
    # Set the env_file for testing
    os.environ['ENV_FILE'] = '.env.test'
    
    settings = Settings()
    assert settings.GROQ_API_KEY == 'test_key'
    
    # Clean up
    os.remove('.env.test')
    del os.environ['ENV_FILE']

def test_groq_api_key_presence():
    settings = Settings()
    assert settings.GROQ_API_KEY is not None
    assert settings.GROQ_API_KEY != ''

@pytest.mark.parametrize("env_value,expected", [
    ('test_key', 'test_key'),
    ('', ''),
    (None, None)
])
def test_groq_api_key_values(env_value, expected):
    os.environ['GROQ_API_KEY'] = env_value if env_value is not None else ''
    settings = Settings()
    assert settings.GROQ_API_KEY == expected
    del os.environ['GROQ_API_KEY']

def test_missing_groq_api_key():
    if 'GROQ_API_KEY' in os.environ:
        del os.environ['GROQ_API_KEY']
    with pytest.raises(ValidationError):
        Settings()

def test_invalid_groq_api_key():
    os.environ['GROQ_API_KEY'] = '123'  # Assuming API key should be longer
    with pytest.raises(ValidationError):
        Settings()
    del os.environ['GROQ_API_KEY']

def test_settings_immutability():
    settings = Settings()
    initial_key = settings.GROQ_API_KEY
    with pytest.raises(AttributeError):
        settings.GROQ_API_KEY = 'new_key'
    assert settings.GROQ_API_KEY == initial_key

def test_env_file_priority():
    # Create a temporary .env file
    with open('.env.test', 'w') as f:
        f.write('GROQ_API_KEY=env_file_key')
    
    # Set the env_file for testing
    os.environ['ENV_FILE'] = '.env.test'
    os.environ['GROQ_API_KEY'] = 'env_var_key'
    
    settings = Settings()
    assert settings.GROQ_API_KEY == 'env_var_key'
    
    # Clean up
    os.remove('.env.test')
    del os.environ['ENV_FILE']
    del os.environ['GROQ_API_KEY']

def test_multiple_settings():
    settings1 = Settings()
    settings2 = Settings()
    assert settings1 is not settings2
    assert settings1.GROQ_API_KEY == settings2.GROQ_API_KEY