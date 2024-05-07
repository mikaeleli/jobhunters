"""
Image
"""

from django.db import models


# Class ripped from: https://www.crunchydata.com/blog/using-postgresqls-bytea-type-with-django
class Image(models.Model):
    """
    Image model.

    Stores image data as binary data.
    """

    image_data = models.BinaryField(null=True)
