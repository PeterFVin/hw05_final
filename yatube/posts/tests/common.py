from django.core.files.uploadedfile import SimpleUploadedFile


def image(content, name: str = 'testimage.jpg') -> SimpleUploadedFile:
    # здесь создание изображения через пиллоу
    return SimpleUploadedFile(
        name=name,
        content=content,
        content_type='image/gif',
    )
