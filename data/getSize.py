import cv2
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

sets = ['train', 'test', 'val']

for image_set in sets:
    image_ids = open('data/ImageSets/%s.txt' % (image_set)).read().strip().split()
    for image_id in image_ids:
        image = cv2.imread('data/JPEGImages/%s.jpg' % (image_id))
        size = image.shape
        #h = size[0]     # 高度
        #w = size[1]     # 宽度
        #depth = size[2]  # 深度
        #print(image_id, size)
        tree = ET.parse('data/Annotations/%s.xml' % (image_id))
        root = tree.getroot()
        if root.find('size') is None:
            #print(root.find('size'))
            print(image_id)
            size_node = ET.Element('size')
            width_node = ET.SubElement(size_node, 'width')
            height_node = ET.SubElement(size_node, 'height')
            depth_node = ET.SubElement(size_node, 'depth')
            width_node.text = str(size[1])
            height_node.text = str(size[0])
            depth_node.text = str(size[2])
            root.append(size_node)
            tree.write('data/Annotations/%s.xml' % (image_id), encoding="utf-8", xml_declaration=True)
        else:
            print(image_id)
            size_node = root.find('size')
            size_node.find('width').text = str(size[1])
            size_node.find('height').text = str(size[0])
            size_node.find('depth').text = str(size[2])
            tree.write('data/Annotations/%s.xml' % (image_id), encoding="utf-8", xml_declaration=True)