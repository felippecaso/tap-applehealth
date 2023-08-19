"""Stream type classes for tap-applehealth."""

from __future__ import annotations

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_applehealth.client import AppleHealthStream


class WorkoutsStream(AppleHealthStream):
    name = "workouts"
    xml_element_name = "Workout"
    replication_key = None
    primary_keys = ["workoutActivityType", "startDate"]
    schema = th.PropertiesList(
        th.Property("workoutActivityType", th.StringType, required=True),
        th.Property("duration", th.StringType, required=True),
        th.Property("durationUnit", th.StringType, required=True),
        th.Property("sourceName", th.StringType),
        th.Property("sourceVersion", th.StringType, required=True),
        th.Property("device", th.StringType),
        th.Property("creationDate", th.DateTimeType, required=True),
        th.Property("startDate", th.DateTimeType, required=True),
        th.Property("endDate", th.DateTimeType, required=True),
        th.Property(
            "MetadataEntry",
            th.ArrayType(
                th.ObjectType(
                    th.Property("key", th.StringType),
                    th.Property("value", th.StringType),
                ),
            ),
        ),
        th.Property(
            "WorkoutStatistics",
            th.ArrayType(
                th.ObjectType(
                    th.Property("type", th.StringType),
                    th.Property("startDate", th.DateTimeType),
                    th.Property("endDate", th.DateTimeType),
                    th.Property("sum", th.StringType),
                    th.Property("unit", th.StringType),
                ),
            ),
        ),
        th.Property(
            "WorkoutEvent",
            th.ArrayType(
                th.ObjectType(
                    th.Property("type", th.StringType),
                    th.Property("date", th.DateTimeType),
                    th.Property("duration", th.StringType),
                    th.Property("durationUnit", th.StringType),
                    th.Property(
                        "MetadataEntry",
                        th.ArrayType(
                            th.ObjectType(
                                th.Property("key", th.StringType),
                                th.Property("value", th.StringType),
                            ),
                        ),
                    ),
                ),
            ),
        ),
        th.Property(
            "WorkoutRoute",
            th.ArrayType(
                th.ObjectType(
                    th.Property("sourceName", th.StringType),
                    th.Property("sourceVersion", th.StringType),
                    th.Property("device", th.StringType),
                    th.Property("creationDate", th.DateTimeType, required=True),
                    th.Property("startDate", th.DateTimeType, required=True),
                    th.Property("endDate", th.DateTimeType, required=True),
                    th.Property(
                        "MetadataEntry",
                        th.ArrayType(
                            th.ObjectType(
                                th.Property("key", th.StringType),
                                th.Property("value", th.StringType),
                            ),
                        ),
                    ),
                    th.Property(
                        "FileReference",
                        th.ArrayType(
                            th.ObjectType(
                                th.Property("path", th.StringType),
                            ),
                        ),
                    ),
                ),
            ),
        ),
    ).to_dict()
