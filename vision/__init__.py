from .datasets import CelebADataset
from .datasets import Rgb2NirDataset

Datasets = {
    "celeba": CelebADataset,
    "rgbnir": Rgb2NirDataset
}