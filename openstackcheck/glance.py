from glanceclient import client

from openstackcheck.config import env

image_id = env.str('GLANCE_IMAGE_ID', None)

image_id = 'ad4108df-d769-45ca-b5cf-b3cdc04be045'

def get_image_id(ctx):
    image_id = None
    if image_id:
        image_id = ctx.auth.get_image(image_id).id
    else:
        images = list(ctx.auth.list_images())
        if images:
            image_id = images[0].id

    if not image_id:
        raise ValueError('Glance image not found')

    print('Found image', image_id)

    return image_id
