import xml.etree.ElementTree as ET

def parse_calls(xml_tag):
    try:
        wrapped = f'<root xmlns:call="tool">{xml_tag}</root>'
        root = ET.fromstring(wrapped)

        results = []
        for elem in root:
            tag_name = elem.tag.rsplit('}', 1)[-1]
            results.append({
                "tool": tag_name,
                "args": elem.attrib
            })
        return results

    except ET.ParseError as e:
        return []
