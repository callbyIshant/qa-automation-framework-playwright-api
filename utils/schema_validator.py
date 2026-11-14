"""
schema_validator.py — JSON Schema validation utility.

Validates API response bodies against JSON Schema files defined in schemas/.
"""

import json
from pathlib import Path
from typing import Union, Dict, Any
import jsonschema

SCHEMAS_DIR = Path(__file__).resolve().parent.parent / "schemas"
_SCHEMA_CACHE: Dict[str, Dict[str, Any]] = {}


def load_schema(schema_name: str) -> Dict[str, Any]:
    """
    Load and cache a JSON Schema from the schemas/ directory.
    
    :param schema_name: Name of the schema file (e.g. 'booking_schema.json')
    :return: Parsed JSON Schema dictionary
    """
    if not schema_name.endswith(".json"):
        schema_name = f"{schema_name}.json"

    if schema_name in _SCHEMA_CACHE:
        return _SCHEMA_CACHE[schema_name]

    schema_file = SCHEMAS_DIR / schema_name
    if not schema_file.is_file():
        raise FileNotFoundError(f"Schema file not found: {schema_file}")

    with open(schema_file, "r", encoding="utf-8") as f:
        schema = json.load(f)

    _SCHEMA_CACHE[schema_name] = schema
    return schema


def validate_json_schema(
    instance: Any,
    schema: Union[str, Dict[str, Any]],
) -> None:
    """
    Validate a JSON payload against a JSON schema.
    Raises jsonschema.ValidationError if validation fails.

    :param instance: Data to validate (dict or list)
    :param schema: Either a schema filename string or a schema dict
    """
    if isinstance(schema, str):
        schema_dict = load_schema(schema)
    else:
        schema_dict = schema

    jsonschema.validate(instance=instance, schema=schema_dict)


def is_valid_schema(
    instance: Any,
    schema: Union[str, Dict[str, Any]],
) -> bool:
    """
    Return True if the instance is valid against the schema, False otherwise.
    """
    try:
        validate_json_schema(instance, schema)
        return True
    except (jsonschema.ValidationError, jsonschema.SchemaError):
        return False
