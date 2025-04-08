import os
import tempfile
import yaml
from app_utils import load_yaml_config


def test_load_yaml_config():
    """
    Test the load_yaml_config function to ensure it correctly loads YAML content.
    """
    # Create a temporary YAML file
    yaml_content = {
        "name": "Test Config",
        "version": 1.0,
        "features": ["feature1", "feature2", "feature3"],
    }
    with tempfile.NamedTemporaryFile(
        delete=False, suffix=".yaml", mode="w"
    ) as temp_file:
        yaml.dump(yaml_content, temp_file)
        temp_file_path = temp_file.name

    try:
        # Load the YAML file using the function
        loaded_content = load_yaml_config(temp_file_path)

        # Assert the loaded content matches the original content
        assert loaded_content == yaml_content, (
            f"Expected {yaml_content}, got {loaded_content}"
        )
    finally:
        # Clean up the temporary file
        os.remove(temp_file_path)
