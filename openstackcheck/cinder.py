from contextlib import contextmanager

@contextmanager
def get_volume(ctx):
    volume = ctx.auth.create_volume(1, image=ctx.image_id)
    print('Created volume', volume.id)
    yield volume
    ctx.auth.delete_volume(volume.id)
    print('Deleted volume', volume.id)
