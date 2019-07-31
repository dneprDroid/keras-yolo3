# coding: utf-8

import xml.etree.ElementTree as ET
import os
import argparse
from gs_util import gs_open, gs_file_exists

'''

Example: `python utils/parse_voc_xml.py --voc_12_path model_data/VOCdevkit/VOC2012`

'''

names_dict = {}
cnt = 0
f = gs_open('model_data/voc_classes.txt', 'r').readlines()
for line in f:
    line = line.strip()
    names_dict[line] = cnt
    cnt += 1

parser = argparse.ArgumentParser()
parser.add_argument("--voc_12_path", help='VOC 12 path')
args = parser.parse_args()

# voc_12 = os.path.abspath('data/VOCdevkit/VOC2012')
voc_12_path = args.voc_12_path
if not voc_12_path:
    raise Exception('Please run with argument --voc_12_path <SOME_GS_PATH>, '
                    'example: `VOCdevkit/VOC2012` or `gs://VOCdevkit/VOC2012`')

voc_12 = os.path.abspath(voc_12_path)
if not gs_file_exists(voc_12):
    raise Exception('File doesn\'t exists at path: %s' % voc_12)

print('VOC 12 path: %s' % voc_12)

anno_path = [os.path.join(voc_12, 'Annotations')]
img_path = [os.path.join(voc_12, 'JPEGImages')]
print('Annotation path path: %s' % anno_path)
print('Images path path: %s' % img_path)

trainval_path = [os.path.join(voc_12, 'ImageSets', 'Main', 'trainval.txt')]
print('Train val. path: %s' % trainval_path)


# test_path = [os.path.join(voc_12, 'ImageSets', 'Main', 'test.txt')]


def parse_xml(path):
    tree = ET.parse(path)
    img_name = path.split('/')[-1][:-4]

    height = tree.findtext("./size/height")
    width = tree.findtext("./size/width")

    objects = [img_name, width, height]

    for obj in tree.findall('object'):
        difficult = obj.find('difficult').text
        if difficult == '1':
            continue
        name = obj.find('name').text
        bbox = obj.find('bndbox')
        xmin = bbox.find('xmin').text
        ymin = bbox.find('ymin').text
        xmax = bbox.find('xmax').text
        ymax = bbox.find('ymax').text

        name = str(names_dict[name])
        objects.extend([name, xmin, ymin, xmax, ymax])
    if len(objects) > 1:
        return objects
    else:
        return None


test_cnt = 0


def gen_test_txt(txt_path):
    global test_cnt
    f = gs_open(txt_path, 'w')

    for i, path in enumerate(test_path):
        img_names = gs_open(path, 'r').readlines()
        for img_name in img_names:
            img_name = img_name.strip()
            xml_path = anno_path[i] + '/' + img_name + '.xml'
            objects = parse_xml(xml_path)
            if objects:
                objects[0] = os.path.join(img_path[i], img_name + '.jpg')
                if os.path.exists(objects[0]):
                    test_cnt += 1
                    objects = ' '.join(objects) + '\n'
                    f.write(objects)
    f.close()


train_cnt = 0


def gen_train_txt(txt_path):
    global train_cnt
    f = gs_open(txt_path, 'w')

    for i, path in enumerate(trainval_path):
        img_names = gs_open(path, 'r').readlines()
        for img_name in img_names:
            img_name = img_name.strip()
            xml_path = anno_path[i] + '/' + img_name + '.xml'
            objects = parse_xml(xml_path)
            if objects:
                objects[0] = os.path.join(img_path[i], img_name + '.jpg')
                if os.path.exists(objects[0]):
                    train_cnt += 1
                    objects = ' '.join(objects) + '\n'
                    f.write(objects)
    f.close()


gen_train_txt('train.txt')
# gen_test_txt('val.txt')
