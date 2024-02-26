import pytest
from splunk_parser import preprocess_config, parse_savedsearches  # Replace with your module name

@pytest.fixture()
def test_config():
    return """
    # Example savedsearches.conf content 
    [section1]
    option1 = value1 %something
    option2 = something_else

    [section2]
    # A line with a % that should remain
    option3 = a literal percentage: 100% 
    """

def test_preprocess_output(test_config):
    result = preprocess_config(test_config, "dummy_output.conf")  # Pass content directly

    # Assertions for the desired output
    assert "[section1]\n" in result  # Check for section header with newline
    assert "option1 = value1 %%something\n" in result  # Escaped '%'
    assert "option2 = something_else\n" in result
    assert "[section2]\n" in result
    assert "option3 = a literal percentage: 100%\n" in result  # No escaping here

def test_parse_savedsearches(test_config):
    result = parse_savedsearches(test_config)

    # Assertions for parsed output
    assert isinstance(result, dict)
    assert "section1" in result
    assert result["section1"]["option1"] == "value1 %something"  # Assuming no '%' handling during parsing
    assert "section2" in result
    assert result["section2"]["option3"] == "a literal percentage: 100%" 
