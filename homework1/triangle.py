import taichi as ti 

ti.init()

@ti.data_oriented
class Triangle:
    def __init__(self):
        self.vertex     = ti.Vector.field(n=3, dtype=float, shape=(3))
        self.color      = ti.Vector.field(n=3, dtype=float, shape=(3))
        self.tex_coords = ti.Vector.field(n=2, dtype=float, shape=(3))
        self.normal     = ti.Vector.field(n=3, dtype=float, shape=(3))

    def set_vertex(self, ind, ver):
        self.vertex[ind] = ver

    def set_normal(self, ind, n):
        self.normal[ind] = n 

    def set_color(self, ind, r, g, b):
        if r < 0.0 or r > 255. or g < 0.0 or g > 255. or b < 0.0 or b > 255. :
            raise("Invalid color values")
        self.color[ind] = ti.Vector([r / 255, g / 255, b / 255]) 
    
    def set_tex_coord(self, ind, s, t):
        self.tex_coords[ind] = ti.Vector([s, t])
    

if __name__ == '__main__':
    tri = Triangle()
    vertex = ti.Vector([1, 1, 1])
    tri.set_vertex(0, vertex)