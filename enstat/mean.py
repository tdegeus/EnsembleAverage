import numpy as np

def _expand_array1d(data, size):

    tmp = np.zeros((size), data.dtype)
    tmp[: data.size] = data
    return tmp

class Dynamic1d:

    def __init__(self, size=None, dtype=None):

        self.first = None
        self.size = size
        self.dtype = dtype

    def _allocate(self, data):

        if self.first is not None:
            return

        size = self.size if self.size is not None else data.size
        dtype = self.dtype if self.dtype is not None else data.dtype

        self.first = np.zeros((size), dtype)
        self.norm = np.zeros((size), np.int64)

    def _expand(self, data):

        if data.size <= self.first.size:
            return

        self.first = _expand_array1d(self.first, data.size)
        self.norm = _expand_array1d(self.norm, data.size)

    def add_sample(self, data):

        assert data.ndim == 1

        self._allocate(data)
        self._expand(data)

        self.first[: data.size] += data
        self.norm[: data.size] += 1

    def mean(self):

        return self.first / np.where(self.norm > 0, self.norm, 1)

if __name__ == "__main__":

    average = Dynamic1d()
    average.add_sample(np.array([1, 2, 3]))
    average.add_sample(np.array([1, 2]))
    average.add_sample(np.array([1]))
    assert np.allclose(average.mean(), np.array([1, 2, 3]))