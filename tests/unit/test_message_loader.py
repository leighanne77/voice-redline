def test_message_system_basics():
    loader = MessageLoader()
    
    # 1. Test basic message retrieval
    assert loader.get_message(MessageType.COMMAND_DELETE) == "Deleting selected text"
    
    # 2. Test message with parameters
    assert loader.get_message(
        MessageType.COMMAND_REPLACE,
        new_text="test"
    ) == "Replacing selected text with: test"
    
    # 3. Test error handling
    with pytest.raises(ValueError):
        loader.get_message("not_an_enum")
        
    # 4. Test all enum values are mapped
    for message_type in MessageType:
        assert message_type in MESSAGE_OUTPUTS 