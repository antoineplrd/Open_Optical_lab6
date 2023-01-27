from Lightpath import Lightpath


class Line:

    def __init__(self, label, length, number_of_channel=10):
        self._label = label
        self._length = length
        self._successive = dict()
        self._number_of_channel = number_of_channel
        self._state = [1] * number_of_channel

    @property
    def label(self):
        return self._label

    @property
    def length(self):
        return self._length

    @property
    def successive(self):
        return self._successive

    @label.setter
    def label(self, value):
        self._label = value

    @length.setter
    def length(self, length):
        self._length = length

    @successive.setter
    def successive(self, value):
        self._successive = value

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state

    def latency_generation(self):
        result = self._length / ((2 / 3) * 299792458)
        return result

    def noise_generation(self, signal_power):
        return pow(10, -9) * signal_power * self._length

    def propagate(self, lightpath: Lightpath):
        self._state[lightpath.channel] = 0  # we change the actual line with channel between 1 and 10 to False
        lightpath.update_noise_power(self.noise_generation(lightpath.signal_power))
        lightpath.UpdateLatency(self.latency_generation())
        return self._successive.get(lightpath.path[1]).propagate(lightpath)

    def probe(self, signal_information):
        signal_information.update_noise_power(self.noise_generation(signal_information.signal_power))
        signal_information.UpdateLatency(self.latency_generation())
        return self._successive.get(signal_information.path[0]).probe(signal_information)

    @property
    def number_of_channel(self):
        return self._number_of_channel
