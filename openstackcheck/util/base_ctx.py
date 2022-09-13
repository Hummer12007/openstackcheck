from contextlib import ExitStack

class BaseContext(ExitStack):
    def acquire(self, name, cm):
        res = self.enter_context(cm)
        self.callback(lambda: delattr(self, name))
        setattr(self, name, res)
        return res
    def acquire_res(self, name, res, exit_cb=None):
        setattr(self, name, res)
        if exit_cb:
            self.callback(exit_cb, res)
        self.callback(lambda: delattr(self, name))
        return res
