import argparse
import xml.etree.ElementTree as ET
from os import getcwd
from utils.gs_util import gs_open, gs_file_exists


parser = argparse.ArgumentParser()
parser.add_argument("--voc_path", help='path to VOC dataset, example: gs://VOCdevkit', type=str)
args = parser.parse_args()
voc_path = args.voc_path.replace("\\", "/")
if not gs_file_exists(voc_path):
    raise Exception("Can't find VOC dir at path: %s" % voc_path)

# sets=[('2007', 'train'), ('2007', 'val'), ('2007', 'test')]
sets=[('2012', 'train')]

classes_file = gs_open('model_data/voc_classes.txt', 'r')
# classes = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]
classes = classes_file.read().splitlines()

print('Classes: %s' % classes)

def convert_annotation(year, image_id, list_file):
    in_file = gs_open(voc_path + '/VOC%s/Annotations/%s.xml'%(year, image_id))
    tree=ET.parse(in_file)
    root = tree.getroot()

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text))
        list_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))


for year, image_set in sets:
    image_ids = gs_open(voc_path + '/VOC%s/ImageSets/Main/%s.txt'%(year, image_set)).read().strip().split()
    list_file = gs_open('%s_%s.txt'%(year, image_set), 'w')
    for image_id in image_ids:
        list_file.write('%s/VOC%s/JPEGImages/%s.jpg'%(voc_path, year, image_id))
        convert_annotation(year, image_id, list_file)
        list_file.write('\n')
    list_file.close()

