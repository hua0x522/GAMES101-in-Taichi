import taichi as ti
from triangle import Triangle 

ti.init()

mat4f = ti.types.matrix(4, 4, ti.f32)

def to_vec4(v3, w=1.0):
    return ti.Vector([v3[0], v3[1], v3[2], w])

@ti.data_oriented
class Rasterizer:
    def __init__(self, w, h):
        self.width = w 
        self.height = h
        
        self.model = mat4f(0)
        self.view = mat4f(0)
        self.projection = mat4f(0)

        self.view_port = ti.Matrix([
            [w/2, 0, 0, w/2],
            [0, h/2, 0, h/2],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

        self.frame_buf = ti.Vector.field(n=3, dtype=float, shape=(w, h))
        self.depth_buf = ti.field(dtype=float, shape=(w, h))

    def set_model(self, model):
        self.model = model 
    
    def set_view(self, view):
        self.view = view 
    
    def set_projection(self, projection):
        self.projection = projection 

    
    def draw_line(self, begin, end):
        x1, y1 = begin[0], begin[1]
        x2, y2 = end[0], end[1]

        len = max(abs(x2 - x1), abs(y2 - y1))
        dx = (x2 - x1) / len 
        dy = (y2 - y1) / len  

        self.draw_line_kernel(x1, y1, dx, dy, int(len))


    @ti.kernel
    def draw_line_kernel(self, x1: float, y1: float, dx: float, dy: float, len: int):
        line_color = ti.Vector([1.0, 1.0, 1.0])
        
        for i in range(len):
            x = int(x1 + dx * i + 0.5)
            y = int(y1 + dy * i + 0.5)
            self.frame_buf[x, y] = line_color
        

    def draw_triangle(self, triangle: Triangle):
        mvp = self.projection @ self.view @ self.model
        
        v0 = self.view_port @ mvp @ to_vec4(triangle.vertex[0])
        v1 = self.view_port @ mvp @ to_vec4(triangle.vertex[1])
        v2 = self.view_port @ mvp @ to_vec4(triangle.vertex[2]) 

        v0 = v0 / v0[3]
        v1 = v1 / v1[3]
        v2 = v2 / v2[3]

        self.draw_line(v0, v1)
        self.draw_line(v1, v2)
        self.draw_line(v2, v0) 


    @ti.kernel
    def clean(self):
        for i, j in self.frame_buf:
            self.frame_buf[i, j] = ti.Vector([0, 0, 0]) 
