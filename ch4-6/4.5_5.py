"""Figure (5): a trimmed, oriented hyperbolic paraboloid matching the reference.

Set PYVISTA_SCREENSHOT to save a PNG instead of opening a window.
"""

import os
import numpy as np
import pyvista as pv
from vtkmodules.vtkRenderingCore import vtkRenderer, vtkBillboardTextActor3D


# The reference has +x lower-right and +y upper-right.
azimuth, elevation = np.deg2rad([-35.0, 23.1])
VIEW = np.array([np.cos(elevation)*np.cos(azimuth),
                 np.cos(elevation)*np.sin(azimuth), np.sin(elevation)])
CAMERA_UP = np.array([0.0, 0.0, 1.0])
VIEW = VIEW / np.linalg.norm(VIEW)
RIGHT = np.cross(CAMERA_UP, VIEW)
RIGHT /= np.linalg.norm(RIGHT)
UP = np.cross(VIEW, RIGHT)

save_image = os.environ.get("PYVISTA_SCREENSHOT")
p = pv.Plotter(off_screen=save_image is not None, window_size=(1000, 700))
p.set_background("white")
p.enable_anti_aliasing("ssaa")
p.camera_position = [30.0 * VIEW, (0, 0, 0), CAMERA_UP]
p.camera.parallel_projection = True

# A second rendering layer shares the SAME camera and the SAME world-space
# actors. It makes textbook construction lines visible without moving them.
# In particular, all three coordinate axes really start at (0,0,0), even
# after rotating the view. There are no camera-direction translations.
front = vtkRenderer()
front.SetLayer(1)
front.SetActiveCamera(p.camera)
front.SetPreserveColorBuffer(True)
front.SetPreserveDepthBuffer(False)
front.InteractiveOff()
p.render_window.SetNumberOfLayers(2)
p.render_window.AddRenderer(front)
framing_points = []
surfaces = []


def add_surface(mesh):
    # Weld periodic seams and repeated polar vertices before outlining.
    mesh = mesh.extract_surface().clean(tolerance=1.0e-9)
    surfaces.append(mesh)
    framing_points.append(mesh.points)
    p.add_mesh(mesh, color="#91ECEB", smooth_shading=True, show_edges=False,
               ambient=0.85, diffuse=0.70, specular=0.08, specular_power=18,
               reset_camera=False, render=False)


def add_curve(points, dashed=False, keep=None, width=2.0, on_top=True, name=None):
    points = np.asarray(points, dtype=float)
    if keep is None:
        keep = np.ones(len(points), dtype=bool)
    # Only line cells: implicit vertex cells would fill the gaps in dashes.
    mesh = pv.PolyData()
    mesh.points = points if on_top else points + 0.002*VIEW
    cells = []
    for i in range(len(points)-1):
        if keep[i] and keep[i+1] and (not dashed or (i//6) % 2 == 0):
            cells.extend([2, i, i+1])
    if not cells:
        return
    mesh.lines = np.asarray(cells, dtype=np.int64)
    actor = p.add_mesh(mesh, color="#202020", line_width=width,
                       lighting=False, reset_camera=False, render=False,
                       name=name)
    if on_top:
        front.AddActor(actor)


def add_axis(direction, length, label, on_top=True, dashed_until=0.0):
    direction = np.asarray(direction, dtype=float)
    direction /= np.linalg.norm(direction)
    origin = np.zeros(3)
    end = length * direction
    # Thin line shaft and a small cone keep different axis lengths consistent.
    projected_length = np.linalg.norm([direction @ RIGHT, direction @ UP])
    tip_height = 0.13 / max(projected_length, 0.15)
    shaft_end = end - tip_height * direction
    if dashed_until > 0.0:
        join = dashed_until * direction
        add_curve(np.linspace(origin, join, 160), dashed=True, on_top=on_top)
        add_curve([join, shaft_end], on_top=on_top, name=label+"-axis-shaft")
    else:
        add_curve([origin, shaft_end], on_top=on_top, name=label+"-axis-shaft")
    tip = pv.Cone(center=end-0.5*tip_height*direction, direction=direction,
                  height=tip_height, radius=0.035, resolution=32)
    actor = p.add_mesh(tip, color="black", lighting=False, reset_camera=False,
                       render=False, name=label+"-axis-tip")
    if on_top:
        front.AddActor(actor)
    label_point = end + 0.19 * direction / max(projected_length, 0.15)
    text = vtkBillboardTextActor3D()
    text.SetPosition(*label_point)
    text.SetInput(label)
    prop = text.GetTextProperty()
    prop.SetColor(0, 0, 0)
    prop.SetFontFamilyToTimes()
    prop.SetFontSize(32)
    prop.SetItalic(True)
    prop.SetJustificationToCentered()
    prop.SetVerticalJustificationToCentered()
    p.add_actor(text, name=label+"-axis-label", reset_camera=False, render=False)
    front.AddActor(text)
    framing_points.append(np.array([origin, end, label_point]))


def finish(number):
    # Fit the surface AND the actual arrow tips and labels in the same frame.
    points = np.vstack(framing_points)
    horizontal, vertical = points @ RIGHT, points @ UP
    center_h = 0.5 * (horizontal.min()+horizontal.max())
    center_v = 0.5 * (vertical.min()+vertical.max())
    target = center_h*RIGHT + center_v*UP
    aspect = p.window_size[0] / p.window_size[1]
    scale = max(np.ptp(vertical)/2 + 0.40, (np.ptp(horizontal)/2 + 0.40)/aspect)
    p.camera_position = [target+30.0*VIEW, target, CAMERA_UP]
    p.camera.parallel_projection = True
    p.camera.parallel_scale = scale
    p.camera.clipping_range = (0.1, 100.0)
    p.add_text("("+str(number)+")", position="upper_left", font="times",
               font_size=25, color="black")
    if save_image:
        p.show(screenshot=save_image)
    else:
        p.show()


def saddle_points(s, t):
    u = s + (0.35 - 0.115*(s + 0.9))*(1-t*t)
    lower = 0.70 - 0.30*t
    curvature = 0.275 - 0.125*t
    v = t*np.sqrt(((1.25 + curvature)*u*u - 0.8*u + lower)/2.2)
    return ((1.925*u + 0.96*v)[..., None]*RIGHT
            - v[..., None]*VIEW
            + (1.25*u*u - 0.8*u - 2.2*v*v)[..., None]*UP)

s, t = np.meshgrid(np.linspace(-0.9, 1.1, 200), np.linspace(-1, 1, 200), indexing="ij")
points = saddle_points(s,t)
surface = pv.StructuredGrid(points[...,0],points[...,1],points[...,2])
add_surface(surface)

# The underlying surface is
# P(u,v) = (1.925*u + 0.96*v)*RIGHT - v*VIEW
#          + (1.25*u**2 - 0.8*u - 2.2*v**2)*UP.
# Its height Hessian has determinant 2.5*(-4.4) = -11 < 0.
# The domain is curved to reproduce the source's lower boundaries.
u = s + (0.35 - 0.115*(s + 0.9))*(1-t*t)
lower, curvature = 0.70 - 0.30*t, 0.275 - 0.125*t
v = t*np.sqrt(((1.25+curvature)*u*u - 0.8*u + lower)/2.2)
du = 1.925*RIGHT + (2.5*u-0.8)[...,None]*UP
dv = 0.96*RIGHT - VIEW - (4.4*v)[...,None]*UP
normals = np.cross(du, dv).reshape(-1, 3, order="F")

def apparent_contour(camera):
    direction = np.array(camera.GetViewPlaneNormal())
    surface["view_normal"] = normals @ direction
    curve = surface.contour([0.0], scalars="view_normal")
    curve.points += 0.002*direction
    return curve

contour_actor = p.add_mesh(apparent_contour(p.camera), color="black",
                           line_width=2, lighting=False, reset_camera=False)
def update_contour(camera, event):
    contour_actor.mapper.SetInputData(apparent_contour(camera))
p.camera.AddObserver("ModifiedEvent", update_contour)
for fixed_s in (-0.9,1.1):
    tt=np.linspace(-1,1,500)
    add_curve(saddle_points(np.full_like(tt,fixed_s),tt),on_top=False)
for fixed_t in (-1,1):
    ss=np.linspace(-0.9,1.1,500)
    add_curve(saddle_points(ss,np.full_like(ss,fixed_t)),on_top=False)
add_axis((1, 0, 0), 4.4, "x", dashed_until=2.35)
add_axis((0, 1, 0), 4.1, "y", dashed_until=3.25)
add_axis((0, 0, 1), 2.8, "z")
finish(5)
