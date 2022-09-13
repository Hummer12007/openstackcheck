import math

from .ctx import context

@context
def get_volume(ctx):
    size = math.ceil(ctx.image.size / (1024**3)) + ctx.image.min_disk + 1
    volume = ctx.auth.create_volume(size, image=ctx.image.id)
    print('Created volume', volume.id)
    yield volume
    volume = ctx.auth.block_storage.get_volume(volume)
    ctx.auth.block_storage.wait_for_status(volume)
    ctx.auth.delete_volume(volume.id)
    ctx.auth.block_storage.wait_for_delete(volume)
    print('Deleted volume', volume.id)
