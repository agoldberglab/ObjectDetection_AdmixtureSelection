#!/usr/bin/env python

from icevision.all import *
import pandas as pd
import numpy as np
from sklearn.metrics import precision_score, recall_score
import sys

base_directory = sys.argv[1]
out_directory = sys.argv[2]
#model_directory = sys.argv[2]

#set directories
#root_dir = "/work/ih49/simulations/"
#base_dir = root_dir + base_directory + "/"

#testing run on full ancestry images
#path = Path(base_dir + model_directory + '/')

path = Path(base_directory + '/')

fnames = get_image_files(path)

pos = [int(re.search("pos-(.*)_seed", str(i)).group(1)) for i in fnames]
bbox_xmin = [math.ceil((i / 50e6) * 200) - 5 for i in pos]
labl_bbox = [[i, 0, i + 11, 200] for i in bbox_xmin]
image_id = [re.search("(.*.png)", str(i)).group(1) for i in fnames]

df = pd.DataFrame(list(zip(image_id, [200] * len(image_id), [200] * len(image_id), labl_bbox, [str(path) for i in image_id])), 
               columns =['image_id', 'width', 'height', 'bbox', 'source'])

class VariantParser(parsers.Parser, parsers.FilepathMixin, parsers.LabelsMixin, parsers.BBoxesMixin):
    pass
VariantParser.generate_template()

class VariantParser(parsers.FasterRCNN, parsers.FilepathMixin, parsers.SizeMixin):
    def __init__(self, df, source):
        self.df = df
        self.source = source

    def __iter__(self):
        yield from self.df.itertuples()

    def __len__(self):
        return len(self.df)

    def imageid(self, o) -> Hashable:
        return o.image_id

    def filepath(self, o) -> Union[str, Path]:
        return self.source / f"{o.image_id}"

    def image_width_height(self, o) -> Tuple[int, int]:
        return get_image_size(self.filepath(o))

    def labels(self, o) -> List[int]:
        return [1]

    def bboxes(self, o) -> List[BBox]:
        return [BBox.from_xyxy(*np.fromiter(o.bbox, dtype="int"))]

class_map = ClassMap(['selected_variant'])

parser = VariantParser(df, path)
train_rs, valid_rs = parser.parse(data_splitter=RandomSplitter([0, 1], seed=42))
valid_ds = Dataset(valid_rs)

valid_dl = faster_rcnn.valid_dl(valid_ds, batch_size=16, num_workers=4, shuffle=False)

backbone = faster_rcnn.backbones.resnet_fpn.resnet18(pretrained=True)

def precision_recall_metric(samples, preds, detection_threshold=0.5):
    sample_all_true = []
    pred_all_true = []
    for i in range(len(samples)):
        sample_bbox_true = [0] * 200
        sample_bbox_xmin, sample_bbox_xmax = samples[i]['bboxes'][0].xyxy[0:3:2]
        sample_bbox_true[sample_bbox_xmin:sample_bbox_xmax] = [1] * (sample_bbox_xmax - sample_bbox_xmin)
        sample_all_true.extend(sample_bbox_true)
        
        pred_bbox_true = [0] * 200
        bbox_pred = [preds[i]['bboxes'][e] for e in range(len(preds[i]['scores'])) if preds[i]['scores'][e] >= detection_threshold]
        if len(bbox_pred)>0:
            bbox_xaxis_pred = [bbox.xyxy[0:3:2] for bbox in bbox_pred]
            for j in bbox_xaxis_pred:
                bbox_min = round(j[0])
                bbox_max = round(j[1])
                if bbox_min < 0:
                    bbox_min = 0
                if bbox_max > 200:
                    bbox_max = 200
                pred_bbox_true[bbox_min:bbox_max] = [1] * (bbox_max - bbox_min)        
        pred_all_true.extend(pred_bbox_true)
    bbox_precision = precision_score(sample_all_true, pred_all_true, zero_division=1)
    bbox_recall = recall_score(sample_all_true, pred_all_true)
    return_dict = {"Precision": bbox_precision, "Recall": bbox_recall, "Threshold": detection_threshold}
    return return_dict

model = faster_rcnn.model(backbone=backbone, num_classes=len(class_map))
model.load_state_dict(torch.load('/work/ih49/object_localization_full-ancestry.model.pth', map_location=torch.device('cuda')))

infer_dl = faster_rcnn.infer_dl(valid_ds, batch_size=16)
samples, preds = faster_rcnn.predict_dl(model.cuda(), infer_dl, detection_threshold=0)

thresholds = np.linspace(0,1,10000)

precision_recall_curve = [precision_recall_metric(samples, preds, threshold) for threshold in thresholds]

pd.DataFrame(precision_recall_curve).to_csv(f"out_directory/object_localization_{base_directory}_{model_directory}_precision-recall.txt", sep='\t', header=True, index=False)
