from .ctx import resource
from openstackcheck.config import env

glance_image = env.str('GLANCE_IMAGE', None)

@resource
def get_image(ctx):
    image = None
    if glance_image:
        image = ctx.auth.get_image(glance_image)
    else:
        images = list(ctx.auth.list_images())
        if images:
            image = images[0]

    if not image:
        raise ValueError('Glance image not found')

    print('Found image', image.id)

    return image
