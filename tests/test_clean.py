import pytest
import pandas as pd
from clean import clean_string, clean_date, transform_customer_record, DataTransformationError
from validate import is_valid_customer, is_valid_manga


def test_clean_string_strips_whitespace():
    """Verifies extra padding spaces are removed cleanly."""
    assert clean_string("   tony stark   ") == "Tony Stark"

def test_clean_string_handles_casing():
    """Checks that title case and lower case rules are enforced."""
    assert clean_string("bruce banner", casing="title") == "Bruce Banner"
    assert clean_string("THOR@ASGARD.COM", casing="lower") == "thor@asgard.com"

def test_clean_string_handles_nulls():
    """Ensures None types or Pandas NaN objects gracefully revert to empty strings."""
    assert clean_string(None) == ""
    assert clean_string(float('nan')) == ""



def test_clean_date_parses_valid_formats():
    """Ensures standard strings convert cleanly to YYYY-MM-DD."""
    assert clean_date("2026/06/25") == "2026-06-25"
    assert clean_date("06-25-2026") == "2026-06-25"

def test_clean_date_parses_api_timestamps():
    """Verifies the new ISO 8601 handler catches Jikan API outputs successfully."""
    assert clean_date("1989-08-25T00:00:00+00:00") == "1989-08-25"

def test_clean_date_raises_custom_error_on_garbage():
    """Checks that unparseable dates explicitly raise our DataTransformationError."""
    with pytest.raises(DataTransformationError):
        clean_date("not-a-valid-date-string")


def test_is_valid_customer_checks():
    """Ensures invalid customer records fail validation."""
    valid_row = {"customer_id": 102, "name": "Bob Jones", "email": "bob@example.com"}
    invalid_row = {"customer_id": 101, "name": None, "email": "alice@example.com"}
    
    assert is_valid_customer(valid_row) is True
    assert is_valid_customer(invalid_row) is False

def test_is_valid_manga_checks():
    """Ensures incomplete API records fail validation."""
    valid_manga = {"mal_id": 2, "title": "Berserk"}
    invalid_manga = {"mal_id": None, "title": "Missing ID"}
    
    assert is_valid_manga(valid_manga) is True
    assert is_valid_manga(invalid_manga) is False