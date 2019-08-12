import argparse
import os
import pydot
from keras.utils import plot_model

from trainer.train import create_tiny_model, get_anchors, get_classes, create_model

r'''
python plot_model.py --model_file "/path/to/your/model.h5" --anchors_file trainer/model_data/tiny_yolo_anchors.txt --classes_file trainer/model_data/voc_classes.txt --out_plot_file plot_image.png

'''


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_file", type=str)
    parser.add_argument("--anchors_file", type=str)
    parser.add_argument("--classes_file", type=str)
    parser.add_argument("--out_plot_file", type=str)

    args, _ = parser.parse_known_args()

    anchors_path = args.anchors_file
    classes_path = args.classes_file  # 'model_data/voc_classes.txt'
    model_path = args.model_file
    out_plot_path = args.out_plot_file

    class_names = get_classes(classes_path)
    num_classes = len(class_names)
    anchors = get_anchors(anchors_path)

    input_shape = (416, 416)  # multiple of 32, hw

    is_tiny_version = len(anchors) == 6  # default setting
    if is_tiny_version:
        model = create_tiny_model(input_shape, anchors, num_classes,
                                  freeze_body=2, weights_path=model_path)
    else:
        model = create_model(input_shape, anchors, num_classes,
                             freeze_body=2,
                             weights_path=model_path)  # make sure you know what you freeze
    plot_model(model, to_file=out_plot_path)


if __name__ == '__main__':
    main()
