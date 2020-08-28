from abc import ABCMeta, abstractmethod

from shapely.ops import triangulate
from shapely.geometry import MultiPoint

from .utils import registry


class Polygonizer(metaclass=ABCMeta):
    """
    Takes in a PIL Image and (optionally) a list of shapely points and returns a list of shapely polygons.
    Output should be independent of the order of points.
    """

    @abstractmethod
    def forward(self, image=None, points=None, polygons=None, *args, **kwargs):
        pass

    def __call__(self, image=None, points=None, polygons=None, *args, **kwargs):
        polygons = self.forward(image, points, *args, **kwargs)["polygons"]
        polygons = self.simplify(polygons)
        output = {"polygons": polygons}
        output.setdefault("image", image)
        output.setdefault("points", points)
        return output

    @staticmethod
    def simplify(polygons):
        # TODO: Merge small polygons
        return polygons


@registry.register("Polygonizer", "DelaunayTriangulator")
class DelaunayTriangulator(Polygonizer):
    def __init__(self):
        super().__init__()

    def forward(self, image=None, points=None, polygons=None):
        if not isinstance(points, MultiPoint):
            points = MultiPoint(points)
        triangles = triangulate(points)
        return {"polygons": triangles}