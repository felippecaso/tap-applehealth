"""Tests standard tap features using the built-in SDK tests library."""


from singer_sdk.testing import get_tap_test_class

from tap_applehealth.tap import TapAppleHealth

SAMPLE_CONFIG = {
    "file_path": "/data/example_export.xml",
}

# Run standard built-in tap tests from the SDK:
TestTapAppleHealth = get_tap_test_class(
    tap_class=TapAppleHealth,
    config=SAMPLE_CONFIG,
)
