import io
import numpy as np
import os
import sys
import time
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision

from matplotlib import pyplot as plt
import seaborn as sns


from .utils.context_manager import Timer
from .utils.decorators import deprecated, printable, return_string
from .utils.logger import Logger


class Args():
    def __init__(self, dataset_name) -> None:
        self.dataset: str = dataset_name
        self.b: int = settings[dataset_name]["b"]
        self.net: str = settings[dataset_name]["net"]
        self.weight: str = settings[dataset_name]["weight"]
        self.prune_weight: str = settings[dataset_name]["prune_weight"]
        self.quant_weight: str = settings[dataset_name]["quant_weight"]
        self.kd1: str = settings[dataset_name]["kd1"]
        self.kd1_weight: str = settings[dataset_name]["kd1_weight"]
        self.kd2: str = settings[dataset_name]["kd2"]
        self.kd2_weight: str = settings[dataset_name]["kd2_weight"]

settings = {
    "CIFAR10": {
        "b": 128,
        "net": "resnet110",
        "weight": "checkpoints/CIFAR10/resnet110/[CIFAR10]-[resnet110]-[Size=Large]-[Type=BEST]-[E=199].pth",
        "prune_weight": "checkpoints/Pruned/CIFAR10/resnet110/[CIFAR10]-[resnet110]-[Size=P]-[Spars=0.5]-[KD=True]-[T=4]-[A=0.5]-[PStep=5]-[Type=BEST]-[E=35].pth",
        "quant_weight": 'checkpoints/Quant/CIFAR10/resnet110/[CIFAR10]-[resnet110]-[Size=Q].pth',
        "kd1": "resnet20",
        "kd1_weight": "checkpoints/CIFAR10/resnet20/[CIFAR10]-[resnet20]-[Size=KD]-[Teacher=resnet110]-[T=8.0]-[A=0.2]-[Type=BEST]-[E=173].pth",
        "kd2": "squeezenet",
        "kd2_weight": "checkpoints/CIFAR10/squeezenet/[CIFAR10]-[squeezenet]-[Size=KD]-[Teacher=resnet110]-[T=8.0]-[A=0.2]-[Type=BEST]-[E=193].pth"
    },
    "CIFAR100": {
        "b": 128,
        "net": "WRN-40-2",
        "weight": "checkpoints/CIFAR100/WRN-40-2/[CIFAR100]-[WRN-40-2]-[Size=Large]-[Type=BEST]-[E=174].pth",
        "prune_weight": "checkpoints/Pruned/CIFAR100/WRN-40-2/[CIFAR100]-[WRN-40-2]-[Size=P]-[Spars=0.5]-[KD=True]-[T=4]-[A=0.5]-[PStep=5]-[Type=BEST]-[E=25].pth",
        "quant_weight": 'checkpoints/Quant/CIFAR100/WRN-40-2/[CIFAR100]-[WRN-40-2]-[Size=Q].pth',
        "kd1": "WRN-40-1",
        "kd1_weight": "checkpoints/CIFAR100/WRN-40-1/[CIFAR100]-[WRN-40-1]-[Size=KD]-[Teacher=WRN-40-2]-[T=9.0]-[A=0.5]-[Type=BEST]-[E=195].pth",
        "kd2": "WRN-20-2",
        "kd2_weight": "checkpoints/CIFAR100/WRN-20-2/[CIFAR100]-[WRN-20-2]-[Size=KD]-[Teacher=WRN-40-2]-[T=9.0]-[A=0.5]-[Type=BEST]-[E=184].pth"
    },
    "TinyImageNet": {
        "b": 16,
        "net": "resnet50",
        "weight": "checkpoints/TinyImageNet/resnet50/[TinyImageNet]-[resnet50]-[Info=Large]-[Type=BEST]-[E=195].pth",
        "prune_weight": "checkpoints/Pruned/TinyImageNet/resnet50/[TinyImageNet]-[resnet50]-[Size=P]-[Spars=0.5]-[PStep=5]-[Type=BEST]-[E=21].pth",
        "quant_weight": 'checkpoints/Quant/TinyImageNet/resnet50/[TinyImageNet]-[resnet50]-[Size=Q].pth',
        "kd1": "WRN-32-4",
        "kd1_weight": "checkpoints/TinyImageNet/WRN-32-4/[TinyImageNet]-[WRN-32-4]-[Size=KD]-[Teacher=resnet50]-[T=8.0]-[A=0.5]-[Type=BEST]-[E=165].pth",
        "kd2": "mobilenetv2",
        "kd2_weight": "checkpoints/TinyImageNet/mobilenetv2/[TinyImageNet]-[mobilenetv2]-[Size=KD]-[Teacher=resnet50]-[T=8.0]-[A=0.5]-[Type=BEST]-[E=174].pth"
    }
}

prefixs = {
    "CIFAR10": "c10",
    "CIFAR100": "c100",
    "TinyImageNet": "ti"
}

MENAs = {
    "CIFAR10": CIFAR10_MEAN_STD,
    "CIFAR100": CIFAR100_MEAN_STD,
    "TinyImageNet": TINY_IMAGENET_MEAN_STD
}


MEAN_STDs = {
    "CIFAR10": CIFAR10_MEAN_STD,
    "CIFAR100": CIFAR100_MEAN_STD,
    "TinyImageNet": TINY_IMAGENET_MEAN_STD
}