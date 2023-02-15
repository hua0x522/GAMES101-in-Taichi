import taichi as ti 
from rasterizer import Rasterizer
from triangle import Triangle

ti.init()
w, h = 800, 800
gui = ti.GUI('homework1', (w, h), fast_gui=True)
MY_PI = 3.1415926

def get_view_matrix(eye_pos):
    return ti.Matrix([
        [1, 0, 0, -eye_pos[0]], 
        [0, 1, 0, -eye_pos[1]],
        [0, 0, 1, -eye_pos[2]],
        [0, 0, 0,           1]
    ])

def get_model_matrix(xy_angle, xz_angle):
    a = xy_angle / 180 * MY_PI
    b = xz_angle / 180 * MY_PI

    return ti.Matrix([
        [ti.cos(a), -ti.sin(a), 0, 0], 
        [ti.sin(a),  ti.cos(a), 0, 0],
        [        0,          0, 1, 0],
        [        0,          0, 0, 1]
    ]) @ \
    ti.Matrix([
        [ti.cos(b), 0, -ti.sin(b), 0],
        [0, 1, 0, 0],
        [ti.sin(b), 0, ti.cos(b), 0],
        [0, 0, 0, 1]
    ])

def get_projection_matrix(eye_fov, aspect_ratio, z_near, z_far):
    n, f = z_near, z_far
    fovY = eye_fov / 180 * MY_PI
    t = ti.tan(fovY / 2) * (-n)
    b = -t 
    r = aspect_ratio * t
    l = -r

    Mpersp = ti.Matrix([
        [n, 0, 0, 0],
        [0, n, 0, 0],
        [0, 0, n + f, - n * f],
        [0, 0, 1, 0]
    ])

    Mtrans = ti.Matrix([
        [1, 0, 0, -(r+l)/2],
        [0, 1, 0, -(t+b)/2],
        [0, 0, 1, -(n+f)/2],
        [0, 0, 0, 1]
    ])

    Mscale = ti.Matrix([
        [2/(r-l), 0, 0, 0],
        [0, 2/(t-b), 0, 0],
        [0, 0, 2/(n-f), 0],
        [0, 0, 0, 1]
    ])

    projection = Mscale @ Mtrans @ Mpersp
    
    return projection 


if __name__ == '__main__':
    rst = Rasterizer(w, h)
    xy_angle, xz_angle = 0, 0
    eye_pos = ti.Vector([0, 0, 5])
    triangle = Triangle()
    triangle.set_vertex(0, ti.Vector([-0.5, 0, 0]))
    triangle.set_vertex(1, ti.Vector([0, 0.5, 0]))
    triangle.set_vertex(2, ti.Vector([0.5, 0, 0]))

    while gui.running:
        rst.clean()
        rst.set_model(get_model_matrix(xy_angle, xz_angle))
        rst.set_view(get_view_matrix(eye_pos))
        rst.set_projection(get_projection_matrix(45, 1, 0.1, 50))
        rst.draw_triangle(triangle)
        
        gui.set_image(rst.frame_buf)
        gui.show()

        gui.get_event()
        if gui.is_pressed(ti.GUI.ESCAPE):
            gui.running = False
            break 
        elif gui.is_pressed('a'):
            xy_angle -= 5
        elif gui.is_pressed('d'):
            xy_angle += 5
        elif gui.is_pressed('w'):
            xz_angle -= 5
        elif gui.is_pressed('s'):
            xz_angle += 5
