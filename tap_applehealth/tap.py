"""AppleHealth tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_applehealth.streams import (
    AppleHealthStream,
    WorkoutsStream,
)


class TapAppleHealth(Tap):
    """AppleHealth tap class."""

    name = "tap-applehealth"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "file_path",
            th.StringType,
            required=True,
            description="The file path of the export.xml file",
        ),
    ).to_dict()

    def discover_streams(self) -> list[AppleHealthStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            WorkoutsStream(self),
        ]


if __name__ == "__main__":
    TapAppleHealth.cli()
