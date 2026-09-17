"""Surface of revolution: profile C, parallels, p, p-bar, rotation angle v.

Run normally for an interactive window, or set PYVISTA_SCREENSHOT to a PNG path.
The callout text is in English; v is an angle, not a tangent vector.
"""
import os
import numpy as np
import pyvista as pv
import vtkmodules.vtkRenderingMatplotlib  # Register mathematical text rendering.
from vtkmodules.vtkRenderingCore import vtkRenderer, vtkBillboardTextActor3D

X_MIN, X_MAX = 0.80, 4.00
SHEAR_X, SHEAR_Y = 0.24, 0.19
VIEW = np.array([SHEAR_X, SHEAR_Y, 1.0])
VIEW /= np.linalg.norm(VIEW)


def profile_radius(x):
    """C1 cubic Hermite profile, with a flare, neck, and rounded shoulder."""
    knots = np.array([0.80, 1.80, 2.65, 3.25, 4.00])
    radii = np.array([1.50, 0.95, 1.33, 1.33, 0.96])
    slopes = np.array([-1.25, 0.0, 0.0, 0.0, -1.60])
    x = np.asarray(x)
    i = np.clip(np.searchsorted(knots, x, side="right")-1, 0, len(knots)-2)
    h = knots[i+1]-knots[i]
    t = (x-knots[i])/h
    return ((2*t**3-3*t**2+1)*radii[i] + (t**3-2*t**2+t)*h*slopes[i]
            + (-2*t**3+3*t**2)*radii[i+1] + (t**3-t**2)*h*slopes[i+1])


def surface_point(x, angle):
    x, angle = np.broadcast_arrays(x, angle)
    r = profile_radius(x)
    return np.stack([x, r*np.cos(angle), r*np.sin(angle)], axis=-1)


save_image = os.environ.get("PYVISTA_SCREENSHOT")
p = pv.Plotter(off_screen=save_image is not None, window_size=(1200, 720))
p.set_background("white")
p.enable_anti_aliasing("ssaa")
target = np.array([2.25, 0.55, 0.0])
p.camera_position = [target + np.array([0,0,30]), target, (0,1,0)]
p.camera.parallel_projection = True
p.camera.SetViewShear(SHEAR_X, SHEAR_Y, 1.0)
p.camera.parallel_scale = 2.50
p.camera.clipping_range = (0.1, 100)

# Construction lines use actual coordinates and the same camera in both layers.
front = vtkRenderer()
front.SetLayer(1)
front.SetActiveCamera(p.camera)
front.SetPreserveColorBuffer(True)
front.SetPreserveDepthBuffer(False)
front.InteractiveOff()
p.render_window.SetNumberOfLayers(2)
p.render_window.AddRenderer(front)


def curve(points, dashed=False, on_top=True, width=1.4):
    points = np.asarray(points, dtype=float)
    mesh = pv.PolyData()
    mesh.points = points
    i = np.arange(len(points)-1)
    if dashed:
        i = i[(i//6) % 2 == 0]
    mesh.lines = np.c_[np.full(len(i), 2), i, i+1].ravel()
    actor = p.add_mesh(mesh, color="#202020", line_width=width,
                       lighting=False, reset_camera=False)
    if on_top:
        front.AddActor(actor)
    return actor


def label(point, text, size=27):
    actor = vtkBillboardTextActor3D()
    actor.SetPosition(*point)
    actor.SetInput(text)
    prop = actor.GetTextProperty()
    prop.SetFontFamilyToTimes()
    prop.SetFontSize(size)
    prop.SetColor(0,0,0)
    prop.SetJustificationToCentered()
    prop.SetVerticalJustificationToCentered()
    p.add_actor(actor, reset_camera=False)
    front.AddActor(actor)


def arrow(start, end, tip=0.12, radius=0.045):
    start, end = np.asarray(start, float), np.asarray(end, float)
    direction = end-start
    direction /= np.linalg.norm(direction)
    curve([start, end-tip*direction], width=1.5)
    actor = p.add_mesh(pv.Cone(center=end-tip*direction/2, direction=direction,
                              height=tip, radius=radius, resolution=32),
                       color="black", lighting=False, reset_camera=False)
    front.AddActor(actor)


# M(u,v) = (u, r(u) cos(v), r(u) sin(v)).
u, v = np.meshgrid(np.linspace(X_MIN,X_MAX,300),
                    np.linspace(0,2*np.pi,240), indexing="ij")
points = surface_point(u,v)
mesh = pv.StructuredGrid(points[...,0], points[...,1], points[...,2])
material = dict(color="#91ECEB", smooth_shading=True, show_edges=False,
                ambient=0.55, diffuse=0.90, specular=0.08, specular_power=18)
p.add_mesh(mesh.extract_surface().clean(tolerance=1e-9), **material)

# End disks are visual closures, as in the source illustration.
for end in (X_MIN,X_MAX):
    r, t = np.meshgrid(np.linspace(0,profile_radius(end),60),
                       np.linspace(0,2*np.pi,240),indexing="ij")
    disk = pv.StructuredGrid(np.full_like(r,end), r*np.cos(t), r*np.sin(t))
    cap_material = dict(material, color="#B8FAF8", lighting=False,
                        ambient=1.0, diffuse=0.0, specular=0.0)
    cap_actor = p.add_mesh(disk.extract_surface().clean(tolerance=1e-9), **cap_material)
    if end == X_MIN:
        # Textbook convention: display the left end section in full.
        front.AddActor(cap_actor)
    angles = np.linspace(0,2*np.pi,600)
    curve(surface_point(end,angles)+0.003*VIEW, width=1.3)

# Upper profile C and the corresponding lower meridian.
x = np.linspace(X_MIN,X_MAX,600)
curve(surface_point(x,0.0), width=1.5)
# Exact silhouette: -r'(x)*SHEAR_X + SHEAR_Y*cos(theta) + sin(theta) = 0.
slope = (profile_radius(x+1e-5)-profile_radius(x-1e-5))/(2e-5)
phase = np.arctan2(SHEAR_Y,1.0)
a = np.arcsin(np.clip(SHEAR_X*slope/np.sqrt(1+SHEAR_Y**2),-1,1))
curve(surface_point(x,a-phase),width=1.2)
curve(surface_point(x,np.pi-a-phase),width=1.2)


def parallel(x):
    # Front/rear semicircles selected by the viewing direction in the yz-plane.
    phase = np.arctan2(VIEW[2],VIEW[1])
    angles = np.linspace(phase-np.pi/2, phase+np.pi/2,300)
    curve(surface_point(x,angles))
    angles = np.linspace(phase+np.pi/2,phase+3*np.pi/2,300)
    curve(surface_point(x,angles), dashed=True)


U_POINT, V_ANGLE = 1.80, 1.05
parallel(U_POINT)
parallel(2.65)
center = np.array([U_POINT,0,0])
p_bar = surface_point(U_POINT,0.0)
p_point = surface_point(U_POINT,V_ANGLE)
curve([center,p_bar],width=1.15)
curve([center,p_point],width=1.15)
angles = np.linspace(0,V_ANGLE,80)
angle_arc = np.c_[np.full_like(angles,U_POINT),
                   0.23*np.cos(angles),0.23*np.sin(angles)]
curve(angle_arc,width=1.1)
actor = p.add_mesh(pv.Sphere(radius=0.047,center=p_point),color="black",
                   lighting=False,reset_camera=False)
front.AddActor(actor)
label(p_point+np.array([-0.15,0.18,0]),r"$\mathbf{p}$",31)
label(p_bar+np.array([0,0.24,0]),r"$\overline{\mathbf{p}}$",31)
label((U_POINT+0.015,0.36,0),r"$v$",29)
label((3.63,-0.83,0),r"$M$",33)

# Callouts to a parallel and to the generating profile.
parallel_target = surface_point(2.65,0.80)
arrow((parallel_target[0]-SHEAR_X*parallel_target[2],2.87,0), parallel_target)
label((2.97,2.82,0),"parallel",27)
arrow((3.36,2.07,0),surface_point(3.03,0.0),tip=0.10,radius=0.035)
label((3.97,2.13,0),"C: profile curve",28)

# +x right, +y up, +z lower-left. All axes meet at the actual origin.
curve(np.linspace((0,0,0),(4.12,0,0),500),dashed=True,width=1.1)
arrow((4.12,0,0),(4.98,0,0))
label((5.25,0,0),r"$x$",30)
label((5.20,-0.32,0),"rotation axis",22)
arrow((0,0,0),(0,2.60,0))
label((-0.18,2.57,0),r"$y$",30)
arrow((0,0,0),(0,0,6.50),tip=0.42)
label((-0.10,-0.06,6.7),r"$z$",30)

if save_image:
    p.show(screenshot=save_image)
else:
    p.show()
