from typing import Tuple, List, Optional

import torch
from torchvision.transforms import (  # noqa: F401
    functional as _F,
    InterpolationMode,
)

horizontal_flip_image = _F.hflip


def horizontal_flip_bounding_box(bounding_box: torch.Tensor, *, image_size: Tuple[int, int]) -> torch.Tensor:
    bounding_box = bounding_box.clone()
    bounding_box[..., (0, 2)] = image_size[1] - bounding_box[..., (2, 0)]
    return bounding_box


_resize_image = _F.resize


def resize_image(
    image: torch.Tensor,
    size: List[int],
    interpolation: InterpolationMode = InterpolationMode.BILINEAR,
    max_size: Optional[int] = None,
    antialias: Optional[bool] = None,
) -> torch.Tensor:
    new_height, new_width = size
    num_channels, old_height, old_width = image.shape[-3:]
    batch_shape = image.shape[:-3]
    return _resize_image(
        image.reshape((-1, num_channels, old_height, old_width)),
        size=size,
        interpolation=interpolation,
        max_size=max_size,
        antialias=antialias,
    ).reshape(batch_shape + (num_channels, new_height, new_width))


def resize_segmentation_mask(
    segmentation_mask: torch.Tensor,
    size: List[int],
    interpolation: InterpolationMode = InterpolationMode.NEAREST,
    max_size: Optional[int] = None,
    antialias: Optional[bool] = None,
) -> torch.Tensor:
    return resize_image(
        segmentation_mask, size=size, interpolation=interpolation, max_size=max_size, antialias=antialias
    )


# TODO: handle max_size
def resize_bounding_box(
    bounding_box: torch.Tensor,
    *,
    old_image_size: List[int],
    new_image_size: List[int],
) -> torch.Tensor:
    old_height, old_width = old_image_size
    new_height, new_width = new_image_size
    ratios = torch.tensor((new_width / old_width, new_height / old_height))
    return bounding_box.view(-1, 2, 2).mul(ratios).view(bounding_box.shape)


center_crop_image = _F.center_crop

resized_crop_image = _F.resized_crop

affine_image = _F.affine

rotate_image = _F.rotate