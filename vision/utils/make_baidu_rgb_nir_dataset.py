import os
import shutil
import re
import numpy as np
from PIL import Image
from torch.utils.data import Dataset
from torchvision import transforms

IMAGE_EXTENSTOINS = [".png", ".jpg", ".jpeg", ".bmp"]
ATTR_ANNO = "list_attr_rgb2nir.txt"

def _is_image(fname):
    _, ext = os.path.splitext(fname)
    return ext.lower() in IMAGE_EXTENSTOINS

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--dataset-path',
        dest='dataset_path',
        help='Which folder to process (it should have subfolders testA, testB, trainA and trainB'
    )
    parser.add_argument(
        '--out-dataset-path',
        dest='out_dataset_path',
        help='Which folder to output images, according to glow dataset format'
    )
    args = parser.parse_args()

    dataset_folder = args.dataset_path
    out_dataset_folder = args.out_dataset_path
    print("input data path", dataset_folder)
    print("output data path", out_dataset_folder)

    images = {}
    attr = None
    assert os.path.exists(dataset_folder), "{} not exists".format(dataset_folder)
    if not os.path.exists(out_dataset_folder):
        os.makedirs(out_dataset_folder)

    list_attr_file = open(os.path.join(out_dataset_folder, ATTR_ANNO), 'w')
    list_attr_file.write("is_nir_img\n")

    for root, _, fnames in sorted(os.walk(dataset_folder)):
        print("root: ", root)
        for fname in sorted(fnames):
            print("fname: ", fname)
            if _is_image(fname):
                src_path = os.path.join(root, fname)
                _fname, _ext = os.path.splitext(fname)

                if root.endswith("A"):
                    _ofname = _fname + "_rgb" + _ext 
                    list_attr_file.write(_ofname)
                    list_attr_file.write(" ")
                    dst_path = os.path.join(out_dataset_folder, _ofname)
                    
                    list_attr_file.write("-1")
                    shutil.copy(src_path, dst_path)
                    list_attr_file.write("\n")
                elif root.endswith("B"):
                    _ofname = _fname + "_nir" + _ext 
                    list_attr_file.write(_ofname)
                    list_attr_file.write(" ")
                    dst_path = os.path.join(out_dataset_folder, _ofname)
                    
                    list_attr_file.write("1")
                    shutil.copy(src_path, dst_path)
                    list_attr_file.write("\n")
                #images[os.path.splitext(fname)[0]] = dst_path
    list_attr_file.close();
