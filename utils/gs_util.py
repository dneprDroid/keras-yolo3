from tensorflow.python.lib.io import file_io  # for better file I/O
import os
import io
from PIL import Image


def gs_open(path, mode='a'):
    return file_io.FileIO(path, mode)


def gs_copy_dir(src, dest):
    if not file_io.file_exists(src):
        raise Exception("Src dir doesn't exist at %s" % src)
    if not file_io.is_directory(src):
        gs_copy_file(src, dest)
        return
    if not file_io.file_exists(dest):
        file_io.create_dir(dest)
    for filename in file_io.list_directory(src):
        new_src = os.path.join(src, filename)
        new_dest = os.path.join(dest, filename)
        gs_copy_file(new_src, new_dest)


def gs_copy_file(src, dest):
    if not file_io.file_exists(src):
        raise Exception("Src file doesn't exist at %s" % src)
    if file_io.is_directory(src):
        gs_copy_dir(src, dest)
        return
    file_io.copy(src, dest, overwrite=True)


def gs_open_image(path):
    file = gs_open(path, "rb")
    image_data = file.read()
    file.close()
    return Image.open(io.BytesIO(image_data))
