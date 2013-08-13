import logging as log
import colorsys
import random


def clip(low, input, high):
    return min(max(input, low), high)



class Fixture:

    def __init__(self, data=None, controller=None):
        self._strand = 0
        self._address = 0
        self._type = "linear"
        self._pixels = 32
        self._pos1 = (10, 10)
        self._pos2 = (50, 50)
        self._locked = False

        if data is not None:
            self.unpack(data)

        self._controller = controller

        self._pixel_data = (0, 0, 0) * self._pixels

    def __repr__(self):
        return "[%d:%d]*%d" % (self._strand, self._address, self._pixels)

    def strand(self):
        return self._strand

    def set_strand(self, strand):
        self._strand = strand

    def address(self):
        return self._address

    def set_address(self, address):
        self._address = address

    def pixels(self):
        return self._pixels

    def set_pixels(self, pixels):
        self._pixels = pixels

    def pos1(self):
        return self._pos1

    def set_pos1(self, pos1):
        self._pos1 = pos1

    def pos2(self):
        return self._pos2

    def set_pos2(self, pos2):
        self._pos2 = pos2

    def destroy(self):
        pass
    
    def request_destruction(self):
        self._controller.delete_fixture(self)


    def unpack(self, data):
        self._strand = data.get("strand", 0)
        self._address = data.get("address", 0)
        self._type = data.get("type", "")
        self._pixels = data.get("pixels", 0)
        self._pos1 = data.get("pos1", [0, 0])
        self._pos2 = data.get("pos2", [0, 0])

    def pack(self):
        return {
                'strand': self._strand,
                'address': self._address,
                'type': self._type,
                'pixels': self._pixels,
                'pos1': self._pos1,
                'pos2': self._pos2
                }

    def fixture_move_callback(self, fixture):
        self._pos1 = map(int, fixture.drag1.pos().toTuple())
        self._pos2 = map(int, fixture.drag2.pos().toTuple())
        fixture.update_geometry()

    def blackout(self):
        self._pixel_data = [(0, 0, 0)] * self._pixels

    def set(self, pixel, color):
        assert isinstance(color, tuple), "Color must be a 3-tuple (R, G, B)"
        pixel_index = pixel * 3
        self._pixel_data[pixel_index:pixels_index + 3] = color

    def set_all(self, color):
        assert isinstance(color, tuple), "Color must be a 3-tuple (R, G, B)"
        self._pixel_data = list(color) * self._pixels

    def set_array(self, color_array):
        if len(color_array) != self.pixels():
            raise ValueError("set_array argument length must match fixture pixel count")
        self._pixel_data = color_array

    def set_flat_array(self, color_array, bgr=False, color_mode="RGB8"):
        if len(color_array) != 3 * self.pixels():
            print len(color_array)
            raise ValueError("set_flat_array argument length must match fixture pixel count")
        is_hlsf32 = color_mode == "HLSF32"

        # Common case
        if color_mode == 'RGB8':
            self._pixel_data = color_array
        else:
            for i, base_offset in enumerate(xrange(0, len(self._pixel_data)*3, 3)):
                if is_hlsf32:
                    hls = color_array[base_offset], color_array[base_offset + 1], color_array[base_offset + 2]
                    rgb = colorsys.hls_to_rgb(*hls)
                    red, green, blue = tuple([int(clip(0.0, 255.0 * channel, 255.0)) for channel in rgb])
                else:
                    red, green, blue = color_array[base_offset], color_array[base_offset + 1], color_array[base_offset + 2]

                if bgr:
                    self._pixel_data[i] = (blue, green, red)
                else:
                    self._pixel_data[i] = (red, green, blue)

    def random_color(self):
        r, g, b = [int(255.0 * c) for c in colorsys.hsv_to_rgb(random.random(), 1.0, 1.0)]
        self.set_all((r, g, b))
