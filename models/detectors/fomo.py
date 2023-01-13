import cv2
import torch
import torch.nn as nn
from mmdet.core import bbox2result
from mmdet.models.detectors.single_stage import SingleStageDetector
from mmdet.models.builder import DETECTORS, build_backbone, build_head, build_neck


@DETECTORS.register_module()
class Fomo(SingleStageDetector):

    def __init__(self,
                 backbone,
                 neck=None,
                 head=None,
                 train_cfg=None,
                 test_cfg=None,
                 pretrained=None,
                 init_cfg=None):
        super().__init__(backbone, neck, head, train_cfg, test_cfg,
                         pretrained, init_cfg)
        self.backbone = build_backbone(backbone)
        self.bbox_head = build_head(head)
        if neck:
            self.neck = build_neck(neck)

    def forward(self, img, target, flag=False, return_loss=True, **kwargs):
        if flag:
            return self.forward_dummy(img)
        else:
            if return_loss:
                x=self.extract_feat(img)
                result = self.bbox_head(x)
                return self.bbox_head.loss(result,target)
            else:
                return self.forward_test(img,label=target)

    def forward_test(self, imgs,  **kwargs):

        x = self.extract_feat(imgs[0])

        result = self.bbox_head(x)

        return self.bbox_head.post_handle(result,kwargs['label'])
