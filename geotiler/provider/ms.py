﻿"""
>>> p = RoadProvider()
>>> p.getTileUrls(Coordinate(25322, 10507, 16)) #doctest: +ELLIPSIS
('http://r....ortho.tiles.virtualearth.net/tiles/r0230102122203031.png?g=90&shading=hill',)
>>> p.getTileUrls(Coordinate(25333, 10482, 16)) #doctest: +ELLIPSIS
('http://r....ortho.tiles.virtualearth.net/tiles/r0230102033330212.png?g=90&shading=hill',)

>>> p = AerialProvider()
>>> p.getTileUrls(Coordinate(25322, 10507, 16)) #doctest: +ELLIPSIS
('http://a....ortho.tiles.virtualearth.net/tiles/a0230102122203031.jpeg?g=90',)
>>> p.getTileUrls(Coordinate(25333, 10482, 16)) #doctest: +ELLIPSIS
('http://a....ortho.tiles.virtualearth.net/tiles/a0230102033330212.jpeg?g=90',)

>>> p = HybridProvider()
>>> p.getTileUrls(Coordinate(25322, 10507, 16)) #doctest: +ELLIPSIS
('http://h....ortho.tiles.virtualearth.net/tiles/h0230102122203031.jpeg?g=90',)
>>> p.getTileUrls(Coordinate(25333, 10482, 16)) #doctest: +ELLIPSIS
('http://h....ortho.tiles.virtualearth.net/tiles/h0230102033330212.jpeg?g=90',)
"""

from math import pi

from ..core import Coordinate
from ..geo import MercatorProjection, deriveTransformation
from .base import IMapProvider

import random
from .. import tiles

class AbstractProvider(IMapProvider):
    def __init__(self):
        # the spherical mercator world tile covers (-π, -π) to (π, π)
        t = deriveTransformation(-pi, pi, 0, 0, pi, pi, 1, 0, -pi, -pi, 0, 1)
        self.projection = MercatorProjection(0, t)

    def getZoomString(self, coordinate):
        return tiles.toMicrosoft(int(coordinate.column), int(coordinate.row), int(coordinate.zoom))

    @property
    def tile_width(self):
        return 256

    @property
    def tile_height(self):
        return 256

class RoadProvider(AbstractProvider):
    def get_tile_urls(self, coordinate):
        return ('http://r%d.ortho.tiles.virtualearth.net/tiles/r%s.png?g=90&shading=hill' % (random.randint(0, 3), self.getZoomString(self.sourceCoordinate(coordinate))),)

class AerialProvider(AbstractProvider):
    def get_tile_urls(self, coordinate):
        return ('http://a%d.ortho.tiles.virtualearth.net/tiles/a%s.jpeg?g=90' % (random.randint(0, 3), self.getZoomString(self.sourceCoordinate(coordinate))),)

class HybridProvider(AbstractProvider):
    def get_tile_urls(self, coordinate):
        return ('http://h%d.ortho.tiles.virtualearth.net/tiles/h%s.jpeg?g=90' % (random.randint(0, 3), self.getZoomString(self.sourceCoordinate(coordinate))),)

if __name__ == '__main__':
    import doctest
    doctest.testmod()