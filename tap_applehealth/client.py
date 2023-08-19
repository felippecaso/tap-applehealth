"""Custom client handling, including AppleHealthStream base class."""

from __future__ import annotations

import xmltodict
import boto3

from singer_sdk.streams import Stream


def _get_s3_file_content(bucket_name: str, object_key: str) -> str:
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    return response['Body'].read().decode('utf-8')


class AppleHealthStream(Stream):
    """Stream class for AppleHealth streams."""

    @staticmethod
    def _parse_xml(file_path: str) -> dict:
        if file_path.startswith("s3://"):
            s3_bucket, s3_object_key = file_path[5:].split("/", 1)
            xml_content = _get_s3_file_content(s3_bucket, s3_object_key)
        else:
            with open(file_path) as f:
                xml_content = f.read()
        xml = xmltodict.parse(xml_content)
        data = xml["HealthData"]
        return data

    # @staticmethod
    # def _parse_xml(file_path: str):
    #     with open(file_path) as f:
    #         xml = xmltodict.parse(f.read())
    #         data = xml["HealthData"]
    #     return data

    @staticmethod
    def _dict_rename_keys(dict, key_mapping):
        return {v: dict.get(k, None) for k, v in key_mapping.items()}
