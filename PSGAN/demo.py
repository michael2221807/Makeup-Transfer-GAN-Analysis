import argparse
from pathlib import Path

from PIL import Image
from psgan import Inference
from fire import Fire
import numpy as np

import faceutils as futils
from psgan import PostProcess
from setup import setup_config, setup_argparser
from imageio import imread, imsave
import glob
import os
import cv2

def preprocess(img):
    return (img / 255. - 0.5) * 2

def deprocess(img):
    return (img + 1) / 2

def main(save_path='./result/transferred_image.png'):
    parser = setup_argparser()
    parser.add_argument(
        "--source_path",
        default="./assets/images/non-makeup",
        metavar="FILE",
        help="path to source image")
    parser.add_argument(
        "--reference_dir",
        default="assets/images/makeup",
        help="path to reference images")
    parser.add_argument(
        "--speed",
        action="store_true",
        help="test speed")
    parser.add_argument(
        "--device",
        default="cpu",
        help="device used for inference")
    parser.add_argument(
        "--model_path",
        default="assets/models/G.pth",
        help="model for loading")

    args = parser.parse_args()
    config = setup_config(args)

    # Using the second cpu
    inference = Inference(
        config, args.device, args.model_path)
    postprocess = PostProcess(config)

    org_paths = glob.glob(os.path.join('assets', 'images', 'no_makeup', '*.*'))
    print(org_paths)

    img_size = 256
    count = 0
    for org_path in org_paths:
        count +=1

        source = Image.open(org_path).convert("RGB")
        source.thumbnail((256,256), Image.ANTIALIAS)
        no_makeup = np.array(source)
        # no_makeup = no_makeup[:, :, ::-1].copy() 

        
        reference_paths = list(Path(args.reference_dir).glob("*"))

        result = np.ones((2 * img_size, (len(reference_paths) + 1) * img_size, 3)) * 255
        result[img_size: 2 * img_size, : img_size] = no_makeup

        # np.random.shuffle(reference_paths)
        for i, reference_path in enumerate(reference_paths):
            if not reference_path.is_file():
                print(reference_path, "is not a valid file.")
                continue

            reference = Image.open(reference_path).convert("RGB")

            makeup = cv2.resize(imread(reference_path), (img_size, img_size))
            # Transfer the psgan from reference to source.
            image, face = inference.transfer(source, reference, with_face=True)
            source_crop = source.crop(
                (face.left(), face.top(), face.right(), face.bottom()))
            # image = postprocess(source_crop, image)

            image.thumbnail((256,256), Image.ANTIALIAS)
            print(image)
            result[:img_size, (i + 1) * img_size: (i + 2) * img_size] = makeup
            result[img_size: 2 * img_size, (i + 1) * img_size: (i + 2) * img_size] = image

            
            save_path = ".\\result\\result_{}.jpg".format(count)
            imsave(save_path, result)

            # print(image)

            if args.speed:
                import time
                start = time.time()
                for _ in range(100):
                    inference.transfer(source, reference)
                print("Time cost for 100 iters: ", time.time() - start)


if __name__ == '__main__':
    main()
