import unittest
from xml.etree import ElementTree as ET

from finalize_epub import OPF_NS, finalize


class EpubMetadataTests(unittest.TestCase):
    def test_finalizer_replaces_managed_properties_and_is_idempotent(self):
        package = f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="{OPF_NS}" version="3.0">
  <metadata>
    <meta property="belongs-to-collection">Old Series</meta>
    <meta property="group-position">9</meta>
  </metadata>
</package>
""".encode()

        finalized = finalize(package)
        metadata = ET.fromstring(finalized).find(f"{{{OPF_NS}}}metadata")
        properties = {}
        for element in metadata.findall(f"{{{OPF_NS}}}meta"):
            properties.setdefault(element.attrib["property"], []).append(element.text)

        self.assertEqual(properties["belongs-to-collection"], ["The Geometry of Meaning"])
        self.assertEqual(properties["collection-type"], ["series"])
        self.assertEqual(properties["group-position"], ["2"])
        self.assertEqual(properties["dcterms:audience"], ["General adult"])
        self.assertEqual(finalize(finalized), finalized)


if __name__ == "__main__":
    unittest.main()