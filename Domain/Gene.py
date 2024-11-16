from haversine import haversine # type: ignore

class Gene:
    __distancesTable = {}

    def __init__(self, name, lat, lng):
        self.name = name
        self.lat = lat
        self.lng = lng

    def getDistanceTo(self, dest):
        origin = (self.lat, self.lng)
        dest = (dest.lat, dest.lng)

        forward_key = origin + dest
        backward_key = dest + origin

        if forward_key in Gene.__distancesTable:
            return Gene.__distancesTable[forward_key]

        if backward_key in Gene.__distancesTable:
            return Gene.__distancesTable[backward_key]

        dist = int(haversine(origin, dest))
        Gene.__distancesTable[forward_key] = dist

        return dist

