from glanceclient import client

from openstackcheck.config import env

image_id = env.str('GLANCE_IMAGE_ID', None)

def get_image_id(ctx):
    with client.Client('2', session=ctx.auth) as glance:
        if image_id:
            image = glance.images.get(image_id)
        else:
            image = next(iter(glance.images.list()))
    return image
