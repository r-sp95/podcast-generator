import yaml
import xml.etree.ElementTree as xml_tree

with open('feed.yaml', 'r') as file:
    yaml_data = yaml.safe_load(file)

    # Fixed: Use '=' instead of '-' for assignment
    # Fixed: Added missing commas between dictionary items
    rss_element = xml_tree.Element('rss', {
        'version': '2.0',
        'xmlns:itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd',
        'xmlns:content': 'http://purl.org/rss/1.0/modules/content/'
    })

    # Fixed: Variable name consistency (channel_tree vs channel_element)
    channel_element = xml_tree.SubElement(rss_element, 'channel')

    link_prefix = yaml_data['link']

    xml_tree.SubElement(channel_element, 'title').text = yaml_data['title']
    xml_tree.SubElement(channel_element, 'format').text = yaml_data['format']
    xml_tree.SubElement(channel_element, 'subtitle').text = yaml_data['subtitle']
    # Fixed: 'items:author' should be 'itunes:author'
    xml_tree.SubElement(channel_element, 'itunes:author').text = yaml_data['author']
    xml_tree.SubElement(channel_element, 'description').text = yaml_data['description']
    xml_tree.SubElement(channel_element, 'itunes:image', {'href': link_prefix + yaml_data['image']})
    xml_tree.SubElement(channel_element, 'language').text = yaml_data['language']
    xml_tree.SubElement(channel_element, 'link').text = link_prefix
    
    xml_tree.SubElement(channel_element, 'itunes:category', {'text': yaml_data['category']})

    # Fixed: Removed space between 'yaml_data' and '[' 
    # Fixed: 'item' should likely be 'items' (plural)
    for item in yaml_data['item']:
        # Fixed: Should be (channel_element, 'item') not ('channel_element', item)
        item_element = xml_tree.SubElement(channel_element, 'item')

        xml_tree.SubElement(item_element, 'title').text = item['title']
        xml_tree.SubElement(item_element, 'itunes:author').text = yaml_data['author']
        xml_tree.SubElement(item_element, 'description').text = item['description']
        xml_tree.SubElement(item_element, 'itunes:duration').text = item['duration']
        xml_tree.SubElement(item_element, 'pubDate').text = item['published']
        # Fixed: Removed duplicate 'title' element (already added above)

        # Fixed: 'length' should be converted to string
        enclosure = xml_tree.SubElement(item_element, 'enclosure', {
            'url': link_prefix + item['file'],
            'type': 'audio/mpeg',
            'length': str(item['length'])
        })

# Fixed: Indentation - this should be outside the 'with' block
output_tree = xml_tree.ElementTree(rss_element)
# Fixed: 'TRUE' should be 'True' (Python boolean)
output_tree.write('podcast.xml', encoding='UTF-8', xml_declaration=True)
