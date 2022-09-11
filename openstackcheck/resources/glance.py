from openstackcheck.config import env

glance_image_id = env.str('GLANCE_IMAGE_ID', None)

def get_image_id(ctx):
    image_id = None
    if glance_image_id:
        image_id = ctx.auth.get_image(glance_image_id).id
    else:
        images = list(ctx.auth.list_images())
        if images:
            image_id = images[0].id

    if not image_id:
        raise ValueError('Glance image not found')

    print('Found image', image_id)

    return image_id
