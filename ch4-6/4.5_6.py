"""Figure (6): double cone x^2+y^2=(SLOPE*z)^2 with a common apex at zero.

Set PYVISTA_SCREENSHOT to save a PNG instead of opening a window.
"""

import os
import numpy as np
import pyvista as pv
from vtkmodules.vtkRenderingCore import vtkRenderer, vtkBillboardTextActor3D
from vtkmodules.vtkFiltersHybrid import vtkPolyDataSilhouette


# Textbook oblique projection: x lower-left, y horizontal, z vertical.
# Camera shear changes the view only; all mesh and axis coordinates stay real.
SHEAR_X, SHEAR_Y = 0.42, 0.35
CAMERA_DIRECTION = np.array([1.0, 0.0, 0.0])
CAMERA_UP = np.array([0.0, 0.0, 1.0])
VIEW = np.array([1.0, SHEAR_X, SHEAR_Y])
VIEW /= np.linalg.norm(VIEW)
# Covectors projecting a world-space point to the two screen coordinates.
RIGHT = np.array([-SHEAR_X, 1.0, 0.0])
UP = np.array([-SHEAR_Y, 0.0, 1.0])
SCREEN_RIGHT = np.array([0.0, 1.0, 0.0])
SCREEN_UP = np.array([0.0, 0.0, 1.0])

save_image = os.environ.get("PYVISTA_SCREENSHOT")
p = pv.Plotter(off_screen=save_image is not None, window_size=(900, 800))
p.set_background("white")
p.enable_anti_aliasing("ssaa")
p.camera_position = [30.0 * CAMERA_DIRECTION, (0, 0, 0), CAMERA_UP]
p.camera.parallel_projection = True
p.camera.SetViewShear(SHEAR_X, SHEAR_Y, 1.0)

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
    outline = vtkPolyDataSilhouette()
    outline.SetInputData(mesh)
    outline.SetCamera(p.camera)
    outline.SetDirectionToSpecifiedVector()
    outline.SetVector(*p.camera.GetViewPlaneNormal())
    # Keep the silhouette correct for both oblique views and mouse rotation.
    p.camera.AddObserver("ModifiedEvent", lambda camera, event, edge=outline:
                         edge.SetVector(*camera.GetViewPlaneNormal()))
    outline.SetEnableFeatureAngle(False)
    outline.SetBorderEdges(False)  # Rims are drawn separately, often dashed.
    p.add_mesh(outline, color="#202020", line_width=1.8, lighting=False,
               reset_camera=False, render=False)


def add_curve(points, dashed=False, keep=None, width=2.0, on_top=True, name=None):
    points = np.asarray(points, dtype=float)
    if keep is None:
        keep = np.ones(len(points), dtype=bool)
    # Only line cells: implicit vertex cells would fill the gaps in dashes.
    mesh = pv.PolyData()
    mesh.points = points
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
    target = center_h*SCREEN_RIGHT + center_v*SCREEN_UP
    aspect = p.window_size[0] / p.window_size[1]
    scale = max(np.ptp(vertical)/2 + 0.40, (np.ptp(horizontal)/2 + 0.40)/aspect)
    p.camera_position = [target+30.0*CAMERA_DIRECTION, target, CAMERA_UP]
    p.camera.parallel_projection = True
    p.camera.parallel_scale = scale
    p.camera.clipping_range = (0.1, 100.0)
    p.add_text("("+str(number)+")", position="upper_left", font="times",
               font_size=25, color="black")
    if save_image:
        p.show(screenshot=save_image)
    else:
        p.show()


SLOPE, Z_MAX = 0.60, 2.10
t, h = np.meshgrid(np.linspace(0, 2*np.pi, 240),
                   np.linspace(0.0, Z_MAX, 130), indexing="ij")
for sign in (1.0, -1.0):
    r = SLOPE*h
    add_surface(pv.StructuredGrid(r*np.cos(t), r*np.sin(t), sign*h))
    rim_t = np.linspace(0, 2*np.pi, 480)
    rim = np.c_[SLOPE*Z_MAX*np.cos(rim_t), SLOPE*Z_MAX*np.sin(rim_t),
                np.full_like(rim_t, sign*Z_MAX)]
    add_curve(rim, dashed=True)

# Small annotation circle centered on the actual singular point.
t = np.linspace(0, 2*np.pi, 120)
add_curve(0.14*(np.cos(t)[:, None]*SCREEN_RIGHT + np.sin(t)[:, None]*SCREEN_UP))
add_axis((1, 0, 0), 5.45, "x")
add_axis((0, 1, 0), 2.65, "y")
add_axis((0, 0, 1), 2.95, "z")
finish(6)
