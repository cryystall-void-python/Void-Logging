import warnings


class Stat:

    def __init__(self):
        self.value = 0
        self.has_changed = False

    def reset(self):
        self.value = 0
        self.has_changed = False

    def __iadd__(self, other):
        if not isinstance(other, (float, int)):
            warnings.warn(f"Operation with type {type(other)} unsupported")

        self.value += other

        return self

    def __isub__(self, other):
        if not isinstance(other, (float, int)):
            warnings.warn(f"Operation with type {type(other)} unsupported")

        self.value -= other

        return self