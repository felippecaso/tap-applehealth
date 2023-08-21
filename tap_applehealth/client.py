"""Custom client handling, including AppleHealthStream base class."""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import TYPE_CHECKING, Iterable

import boto3
from lxml import etree
from singer_sdk.streams import Stream

if TYPE_CHECKING:
    from io import BufferedRandom


class AppleHealthStream(Stream):
    """Stream class for AppleHealth streams."""

    def _get_s3_object(self, bucket_name: str, object_key: str):  # noqa: ANN202
        aws_session = boto3.Session()
        s3_resource = aws_session.resource("s3")
        return s3_resource.Bucket(bucket_name).Object(object_key)

    def _parse_xml_element(self, element: etree.Element) -> dict:
        xml_row: dict = {}

        for attribute in element.attrib.items():
            key: str = attribute[0]
            value: str = attribute[1]
            xml_row[key] = value

        for child in element:
            if child.tag not in xml_row:
                xml_row[child.tag] = []
            xml_row[child.tag].append(self._parse_xml_element(child))

        return xml_row

    def _parse_xml_content(self, xml_content: BufferedRandom) -> Iterable[dict]:
        row = {}

        for _, element in etree.iterparse(
            xml_content,
            events=("end",),
            tag=self.xml_element_name,
        ):
            row = self._parse_xml_element(element)

            # Check if values are present for all pk properties
            if None not in [row[k] for k in self.primary_key_properties]:
                # Create id column
                row_id: str = " | ".join([row[k] for k in self.primary_key_properties])
                yield dict({"id": row_id}, **row)

            # Cleans elements for performance
            element.clear()
            if element.getparent() is not None:
                element.getparent().remove(element)

    def get_records(self, context: dict | None) -> Iterable[dict]:  # noqa: ARG002
        """Return a generator of row-type dictionary objects.

        Args:
            context: If partition context is provided, will read specifically
                from this data slice.

        Yields:
            One dict per record.
        """
        file_path: str = self.config.get("file_path")

        if file_path.startswith("s3://"):
            s3_bucket, s3_object_key = file_path[5:].split("/", 1)
            s3_object = self._get_s3_object(s3_bucket, s3_object_key)
            with tempfile.NamedTemporaryFile() as tmp_file:
                s3_object.download_fileobj(tmp_file)
                with Path(tmp_file.name).open("r+b") as xml_content:
                    yield from self._parse_xml_content(xml_content)

        else:
            with Path(file_path).open("r+b") as xml_content:
                yield from self._parse_xml_content(xml_content)
