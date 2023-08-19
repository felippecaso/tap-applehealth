"""Stream type classes for tap-applehealth."""

from __future__ import annotations

from singer_sdk import typing as th  # JSON Schema typing helpers

from typing import Iterable

from tap_applehealth.client import AppleHealthStream


class WorkoutsStream(AppleHealthStream):
    name = "apple_health_workouts"
    replication_key = None
    schema = th.PropertiesList(
        th.Property("workout_activity_type", th.StringType, required=True),
        th.Property("duration", th.StringType, required=True),
        th.Property("duration_unit", th.StringType, required=True),
        th.Property("source_name", th.StringType),
        th.Property("source_version", th.StringType, required=True),
        th.Property("device", th.StringType),
        th.Property("creation_date", th.DateTimeType, required=True),
        th.Property("start_date", th.DateTimeType, required=True),
        th.Property("end_date", th.DateTimeType, required=True),
        th.Property("metadata", th.ArrayType(
            th.ObjectType(
                th.Property("@key", th.StringType),
                th.Property("@value", th.StringType)
            )
        )),
    ).to_dict()

    def get_records(self, context: dict | None) -> Iterable[dict]:
        """Yield a generator of record-type dictionary objects.

        This function will yield a records based on the processed data.

        Args:
            context: An optional context as dictionary.

        Yields:
            yields: Records based on the processed data.
        """

        workouts = self._parse_xml(self.config.get("file_path"))["Workout"]

        workout_key_mapping = {
            "@workoutActivityType": "workout_activity_type",
            "@duration": "duration",
            "@durationUnit": "duration_unit",
            "@sourceName": "source_name",
            "@sourceVersion": "source_version",
            "@device": "device",
            "@creationDate": "creation_date",
            "@startDate": "start_date",
            "@endDate": "end_date",
            "MetadataEntry": "metadata",
        }

        for w in workouts:
            yield self._dict_rename_keys(w, workout_key_mapping)


class WorkoutStatisticsStream(AppleHealthStream):
    name = "apple_health_workout_statistics"
    replication_key = None

    schema = th.PropertiesList(
        th.Property("workout_activity_type", th.StringType),
        th.Property("workout_start_date", th.DateTimeType),
        th.Property("type", th.StringType),
        th.Property("start_date", th.DateTimeType),
        th.Property("end_date", th.DateTimeType),
        th.Property("sum", th.StringType),
        th.Property("unit", th.StringType),
    ).to_dict()

    def get_records(self, context: dict | None) -> Iterable[dict]:
        """Yield a generator of record-type dictionary objects.

        This function will yield a records based on the processed data.

        Args:
            context: An optional context as dictionary.

        Yields:
            yields: Records based on the processed data.
        """

        workouts = self._parse_xml(self.config.get("file_path"))["Workout"]

        workout_statistics_key_mapping = {
            "@type": "type",
            "@startDate": "start_date",
            "@endDate": "end_date",
            "@sum": "sum",
            "@unit": "unit",
        }

        for w in workouts:
            workout_statistics = w.get("WorkoutStatistics")
            if not workout_statistics:
                pass
            else:
                workout_ids = {
                    "workout_activity_type": w["@workoutActivityType"],
                    "workout_start_date": w["@startDate"]
                }
                if isinstance(workout_statistics, list):
                    for ws in workout_statistics:
                        ws_dict = workout_ids | ws
                        yield self._dict_rename_keys(ws_dict, workout_statistics_key_mapping)
                elif isinstance(workout_statistics, dict):
                    ws_dict = workout_ids | workout_statistics
                    yield self._dict_rename_keys(ws_dict, workout_statistics_key_mapping)
                else:
                    pass
