"""Custom client handling, including AppleHealthStream base class."""

from __future__ import annotations

from typing import Iterable

import boto3
from lxml import etree
from singer_sdk.streams import Stream


class AppleHealthStream(Stream):
    """Stream class for AppleHealth streams."""

    def _get_s3_as_tmp_file(self, bucket_name: str, object_key: str) -> str:
        aws_session = boto3.Session()
        s3_resource = aws_session.resource("s3")
        s3_object = s3_resource.Bucket(bucket_name).Object(object_key)
        tmp_file = f"/tmp/{object_key.split('/')[-1].strip()}"
        s3_object.download_file(tmp_file)
        return tmp_file

    def _get_xml_contents(self, file_path: str) -> dict:
        if file_path.startswith("s3://"):
            s3_bucket, s3_object_key = file_path[5:].split("/", 1)
            xml_file = self._get_s3_as_tmp_file(s3_bucket, s3_object_key)
        else:
            xml_file = file_path
        return open(xml_file, mode="rb")

    def _parse_xml(self, element: str) -> dict:
        xml_row = {}

        for attribute in element.attrib.items():
            key: str = attribute[0]
            value: str = attribute[1]
            xml_row[key] = value

        for child in element:
            if child.tag not in xml_row:
                xml_row[child.tag] = []
            xml_row[child.tag].append(self._parse_xml(child))

        return xml_row

    def get_records(self, context: dict | None) -> Iterable[dict]:
        xml_content = self._get_xml_contents(self.config.get("file_path"))

        row = {}

        for _, element in etree.iterparse(
            xml_content, events=("end",), tag=self.xml_element_name,
        ):
            row = self._parse_xml(element)

            # Assumes we have values for primary_keys colunns
            primary_key_not_null = True

            # Check each primary key in the row to make
            # sure it has a value. If one does not have value,
            # prevents the record from being yielded
            for key_col in self.primary_keys:
                if row.get(key_col) is None:
                    primary_key_not_null = False

            if primary_key_not_null:
                yield dict(row)

            # Cleans elements for performance
            element.clear()
            if element.getparent() is not None:
                element.getparent().remove(element)
