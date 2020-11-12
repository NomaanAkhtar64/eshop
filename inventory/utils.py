import os
from sys import getsizeof
from io import BytesIO
from PIL import Image
from django.core.files.base import File
from django.core.files.uploadhandler import InMemoryUploadedFile
from random import randint


class HexGenerator:
    def __init__(self, len: int):
        self.start = int("a" * len, 16)
        self.end = int("f" * len, 16)

    def generate(self):
        return hex(randint(self.start, self.end)).replace("0x", "")


def get_ext(filename):
    out = ""
    len_ = len(filename)
    for i in range(len_):
        char = filename[(len_ - (i + 1))]

        if char == ".":
            out = filename[len_ - i :]
            break
    return out


def get_rgb_image(base_image):
    if base_image.mode != "RGB":
        im = Image.new("RGB", base_image.size, (255, 255, 255))
        im.paste(base_image, mask=base_image.split()[3])
    else:
        im = base_image

    return im


def make_thumbnail_field(size, reciever, source):
    # extToFormat = {
    #     "jpeg": "JPEG",
    #     "jpg": "JPEG",
    #     "webp": "WebP",
    #     "png": "PNG",
    # }
    # ext = get_ext(str(source)).lower()
    base_image = Image.open(source.path)
    im = get_rgb_image(base_image)

    io = BytesIO()
    im.thumbnail(size)
    im.save(io, "JPEG", quality=85)

    return InMemoryUploadedFile(
        io, "ImageField", reciever.name, "image/jpeg", getsizeof(io), None
    )


# def resize_image(size, field):
#     base_image = Image.open(field.path)
#     out_file_path = ".".join(field.path.split(".")[:-1]) + ".jpg"
#     # out_name = os.path.split(out_file_path)[-1]

#     im = get_rgb_image(base_image)
#     base_image.close()

#     im.thumbnail(size)
#     im.save(out_file_path, "JPEG", quality=85)

#     im.close()
#     safe_delete(field.path)

#     return out_file_path


def remove_ext(path):
    return ".".join(path.split(".")[:-1])


def compress_and_resize_image(field, size):
    io = BytesIO()
    with field.open() as f:
        im = Image.open(f)
        im = get_rgb_image(im)
        im.thumbnail(size)
        im.save(io, "JPEG", quality=85)

    return (remove_ext(field.name) + ".jpg", File(io))


def safe_delete(path: str):
    if os.path.isfile(path):
        os.remove(path)
