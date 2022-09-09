from contextlib import contextmanager

@contextmanager
def get_volume(ctx):
    volume = ctx.auth.create_volume(1, image=ctx.image_id)
    print('Created volume', volume.id)
    yield volume
    volume = ctx.auth.block_storage.get_volume(volume)
    ctx.auth.block_storage.wait_for_status(volume)
    ctx.auth.delete_volume(volume.id)
    ctx.auth.block_storage.wait_for_delete(volume)
    print('Deleted volume', volume.id)
