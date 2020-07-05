from PIL import Image
import os
from Model.ImageThumbItem import ImageThumbItem


def smart_crop_image(image_handle):
    width, height = image_handle.size
    if height > width:
        adjust = int((height - width) / 2)
        box = (0, adjust, width, height - adjust)
    else:
        adjust = int((width - height) / 2)
        box = (adjust, 0, width - adjust, height)

    return image_handle.crop(box)


def create_thumbnail(image_path, size=64):
    image = open(image_path, 'rb')
    thumb = smart_crop_image(Image.open(image))

    thumb.thumbnail((size, size))
    image.close()
    return thumb


def create_thumb_item(image_path, size=64):
    full_path = os.path.abspath(image_path)
    base_name = os.path.basename(full_path)
    thumb = create_thumbnail(full_path, size=size)
    return ImageThumbItem(base_name, full_path, thumb)


def create_composite_image(image_array, orientation='vertical', alignment='left'):
    is_vert = orientation == 'vertical'
    out_size_v = 0
    out_size_h = 0
    largest_width = 0
    largest_height = 0
    # This first round discovers information about each file provided.
    for img in image_array:
        with open(img.full_name, 'rb') as file_pointer:
            img_handle = Image.open(file_pointer)
            out_size_v += img_handle.height
            out_size_h += img_handle.width
            largest_width = max(largest_width, img_handle.width)
            largest_height = max(largest_height, img_handle.height)

    if is_vert:
        out_image = Image.new('RGB', (largest_width, out_size_v))
    else:
        out_image = Image.new('RGB', (out_size_h, largest_height))
    img_cursor = 0
    for img in image_array:
        with open(img.full_name, 'rb') as file_pointer:
            img_handle = Image.open(file_pointer).convert('RGB')

            if is_vert:
                if alignment == 'left':
                    x_offset = 0
                elif alignment == 'right':
                    x_offset = largest_width - img_handle.width
                else:
                    x_offset = int((largest_width - img_handle.width) / 2)

                out_image.paste(img_handle, box=(x_offset, img_cursor,
                                                 img_handle.width + x_offset, img_handle.height + img_cursor))
                img_cursor += img_handle.height
            else:

                if alignment == 'left':
                    y_offset = 0
                elif alignment == 'right':
                    y_offset = largest_height - img_handle.height
                else:
                    y_offset = int((largest_height - img_handle.height) / 2)

                out_image.paste(img_handle, box=(img_cursor, y_offset,
                                                 img_handle.width + img_cursor, img_handle.height + y_offset))
                img_cursor += img_handle.width
    return out_image
