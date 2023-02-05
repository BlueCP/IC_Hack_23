import argparse
from brand_recogniser_model.src.keras_yolo3.yolo import YOLO
import pathlib
import os
from PIL import Image
from timeit import default_timer as timer

from brand_recogniser_model.src.logos import detect_logo, match_logo
# from logos import detect_logo, match_logo

from brand_recogniser_model.src.similarity import load_brands_compute_cutoffs
from brand_recogniser_model.src.utils import load_extractor_model, load_features, model_flavor_from_name, parse_input, pad_image

def get_model(init=True):
    sim_threshold = 0.7

    FLAGS = {}

    # parameters for model

    wdir = pathlib.Path().resolve()
    src_dir = os.path.join(pathlib.Path().resolve(), 'brand_recogniser_model', 'src')

    FLAGS['input_image'] = os.path.join(wdir, 'test_image.jpg')
    FLAGS['brand_logos'] = os.path.join(wdir, 'brand_logos')
    FLAGS['output_path'] = os.path.join(wdir, 'shots')
    FLAGS['weights_path'] = os.path.join(src_dir, 'keras_yolo3', 'yolo_weights_logos.h5')
    FLAGS['anchors_path'] = os.path.join(src_dir, 'keras_yolo3', 'model_data', 'yolo_anchors.txt')
    FLAGS['classes_path'] = os.path.join(src_dir,  'data_classes.txt')
    FLAGS['confidence'] = 0.4
    # good default choices: inception_logo_features_200_trunc2, vgg16_logo_features_128
    FLAGS['features'] = os.path.join(src_dir, 'inception_logo_features_200_trunc2.hdf5')
    FLAGS['fpr'] = 0.95

    # define YOLO logo detector
    if init:
        get_model.yolo = YOLO(**{"model_path": FLAGS['weights_path'],
           "anchors_path": FLAGS['anchors_path'],
           "classes_path": FLAGS['classes_path'],
           "score" : FLAGS['confidence'],
           "gpu_num" : 1,
           "model_image_size" : (416, 416),
           }
        )
    yolo = get_model.yolo

    brand_paths = [os.path.join(FLAGS['brand_logos'], f) for f in os.listdir(FLAGS['brand_logos']) if os.path.isfile(os.path.join(FLAGS['brand_logos'], f))]
    # input_paths = [FLAGS['input_image']]

    # labels to draw on images - could also be read from filename
    input_labels = [ os.path.basename(s).split('test_')[-1].split('.')[0] for s in brand_paths]

    # get Inception/VGG16 model and flavor from filename
    model_name, flavor = model_flavor_from_name(FLAGS['features'])
    ## load pre-processed LITW features database
    features, brand_map, input_shape = load_features(FLAGS['features'])

    ## load inception model
    if init:
        get_model.model, get_model.preprocess_input, get_model.input_shape = load_extractor_model(model_name, flavor)
    model = get_model.model
    preprocess_input = get_model.preprocess_input
    input_shape = get_model.input_shape

    my_preprocess = lambda x: preprocess_input(pad_image(x, input_shape))

    # compute cosine similarity between input brand images and all LogosInTheWild logos
    print(brand_paths)
    print(model)
    print(features)
    print(sim_threshold)

    if init:
        (img_input, feat_input, sim_cutoff, (bins, cdf_list)) = load_brands_compute_cutoffs(brand_paths, (model, my_preprocess), features, sim_threshold)
        get_model.feat_input = feat_input
        get_model.sim_cutoff = sim_cutoff
        get_model.bins = bins
        get_model.cdf_list = cdf_list
        get_model.img_input = img_input
    feat_input = get_model.feat_input
    sim_cutoff = get_model.sim_cutoff
    bins = get_model.bins
    cdf_list = get_model.cdf_list

    # cycle trough input images, look for logos and then match them against inputs
    return {
        'yolo': yolo,
        'model': model,
        'my_preprocess': my_preprocess,
        'feat_input': feat_input,
        'sim_cutoff': sim_cutoff,
        'bins': bins,
        'cdf_list': cdf_list,
        'input_labels': input_labels,
        'output_path': FLAGS['output_path']
    }
#
# def predict_logo(input_image_path, kwawrgs):
#     yolo = kwawrgs['yolo']
#     model = kwawrgs['model']
#     my_preprocess = kwawrgs['my_preprocess']
#     feat_input = kwawrgs['feat_input']
#     sim_cutoff = kwawrgs['sim_cutoff']
#     bins = kwawrgs['bins']
#     cdf_list = kwawrgs['cdf_list']
#     input_labels = kwawrgs['input_labels']




#     output_path = FLAGS['output_path']
#
#     prediction, image = detect_logo(yolo, input_image_path, save_img = True,
#                                     save_img_path = output_path,
#                                     postfix='_logo')
#     print(prediction)
#     text, bbox_list_list = match_logo(image, prediction, (model, my_preprocess), input_image_path,
#                       (feat_input, sim_cutoff, bins, cdf_list, input_labels),
#                       save_img = True, save_img_path=output_path)
#     print(text)
#     print(bbox_list_list)
#
#     return prediction, text, bbox_list_list