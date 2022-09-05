from contextlib import contextmanager

from cinderclient import client

@contextmanager
def get_cinder(ctx):
    with client.Client('3', session=ctx.auth) as cinder:
        yield cinder

@contextmanager
def get_volume(ctx):
    image = ctx.cinder.volumes.create(1, ctx.image_id)
    yield image
    image.delete()
