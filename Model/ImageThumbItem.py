

class ImageThumbItem(object):
    """
        Data class for tracking an image on disk with its thumbnail.
    """

    def __init__(self, display_name, full_name, thumbnail):
        """
        Creates a new ThumbItem.
        :param display_name: The name of the image to display in lists and dialogs.
        :param full_name: The fully qualified path to the image.
        :param thumbnail: A PIL Image object containing the thumbnail image.
        """
        self.display_name = display_name
        self.full_name = full_name
        self.thumbnail = thumbnail

        self.q_thumb = self.thumbnail.toqpixmap()

    def get_thumbnail(self):
        """
        Gets a QPixmap of the thumbnail that can be redily displayed in Qt Widgets.
        :return: QPixmap - A Qt compatible pixmap representation of the object.
        """
        return self.q_thumb
