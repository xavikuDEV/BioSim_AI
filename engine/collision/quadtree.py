# engine/collision/quadtree.py
class Quadtree:
    def __init__(self, boundary, capacity):
        self.boundary = boundary # [x, z, w, h]
        self.capacity = capacity
        self.entities = []
        self.divided = False

    def subdivide(self):
        x, z, w, h = self.boundary
        nw = [x - w/2, z + h/2, w/2, h/2]
        ne = [x + w/2, z + h/2, w/2, h/2]
        sw = [x - w/2, z - h/2, w/2, h/2]
        se = [x + w/2, z - h/2, w/2, h/2]
        
        self.northwest = Quadtree(nw, self.capacity)
        self.northeast = Quadtree(ne, self.capacity)
        self.southwest = Quadtree(sw, self.capacity)
        self.southeast = Quadtree(se, self.capacity)
        self.divided = True

    def insert(self, entity_id, pos):
        # Si la entidad no está en este cuadrante, fuera
        if not self.contains(pos): return False

        if len(self.entities) < self.capacity:
            self.entities.append(entity_id)
            return True
        else:
            if not self.divided: self.subdivide()
            return (self.northwest.insert(entity_id, pos) or 
                    self.northeast.insert(entity_id, pos) or 
                    self.southwest.insert(entity_id, pos) or 
                    self.southeast.insert(entity_id, pos))

    def contains(self, pos):
        x, z, w, h = self.boundary
        return (x - w <= pos[0] <= x + w and 
                z - h <= pos[2] <= z + h)

    def query(self, pos, radius, found):
        if not self.contains(pos): return found
        
        for eid in self.entities:
            found.append(eid)
            
        if self.divided:
            self.northwest.query(pos, radius, found)
            self.northeast.query(pos, radius, found)
            self.southwest.query(pos, radius, found)
            self.southeast.query(pos, radius, found)
        return found