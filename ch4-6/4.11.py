"""Parametrized surface of revolution, with g(u), h(u), and rotation angle v.

x(u,v) = (g(u), h(u)*cos(v), h(u)*sin(v)), 0 <= u <= 1.
Callouts are in English. Set PYVISTA_SCREENSHOT to save a PNG.
"""
import os
import numpy as np
import pyvista as pv
import vtkmodules.vtkRenderingMatplotlib
from vtkmodules.vtkRenderingCore import vtkRenderer, vtkBillboardTextActor3D

SHEAR_X, SHEAR_Y = 0.24, 0.19
VIEW = np.array([SHEAR_X, SHEAR_Y, 1.0])
VIEW /= np.linalg.norm(VIEW)


def g(u):
    return 0.65 + 3.25*np.asarray(u)


def h(u):
    return 0.98 + 1.50*(np.asarray(u)-0.5)**2


def surface_point(u, v):
    u, v = np.broadcast_arrays(u,v)
    return np.stack([g(u),h(u)*np.cos(v),h(u)*np.sin(v)],axis=-1)


save_image = os.environ.get("PYVISTA_SCREENSHOT")
p = pv.Plotter(off_screen=save_image is not None, window_size=(1100, 720))
p.set_background("white")
p.enable_anti_aliasing("ssaa")
target = np.array([1.72, 0.15, 0.0])
p.camera_position = [target + np.array([0,0,30]), target, (0,1,0)]
p.camera.parallel_projection = True
p.camera.SetViewShear(SHEAR_X, SHEAR_Y, 1.0)
p.camera.parallel_scale = 2.55
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


# Smooth cyan surface, sampled periodically in the angular coordinate.
u,v = np.meshgrid(np.linspace(0,1,240),np.linspace(0,2*np.pi,240),indexing="ij")
points = surface_point(u,v)
mesh = pv.StructuredGrid(points[...,0],points[...,1],points[...,2])
p.add_mesh(mesh.extract_surface().clean(tolerance=1e-9),color="#91ECEB",
           smooth_shading=True,show_edges=False,ambient=0.55,diffuse=0.90,
           specular=0.08,specular_power=18)

# The right end is filled, while the left parallel has a dashed rear half.
r,t = np.meshgrid(np.linspace(0,h(1),50),np.linspace(0,2*np.pi,240),indexing="ij")
cap = pv.StructuredGrid(np.full_like(r,g(1)),r*np.cos(t),r*np.sin(t))
p.add_mesh(cap.extract_surface().clean(tolerance=1e-9),color="#B8FAF8",
           lighting=False,ambient=1,diffuse=0,specular=0)
curve(surface_point(1,np.linspace(0,2*np.pi,600)),width=1.4)


def parallel(u):
    phase = np.arctan2(VIEW[2],VIEW[1])
    a = np.linspace(phase-np.pi/2,phase+np.pi/2,300)
    curve(surface_point(u,a))
    a = np.linspace(phase+np.pi/2,phase+3*np.pi/2,300)
    curve(surface_point(u,a),dashed=True)


U_POINT, V_ANGLE = 0.50, 1.02
parallel(0.0)
parallel(U_POINT)

# Upper and lower generating meridians.
u_line = np.linspace(0,1,500)
curve(surface_point(u_line,0.0),width=1.5)
curve(surface_point(u_line,np.pi),width=1.5)

x0,r0 = float(g(U_POINT)),float(h(U_POINT))
center = np.array([x0,0,0])
point = surface_point(U_POINT,V_ANGLE)
curve([center,(x0,r0,0)],width=1.1)
curve([center,point],width=1.1)
a = np.linspace(0,V_ANGLE,80)
curve(np.c_[np.full_like(a,x0),0.24*np.cos(a),0.24*np.sin(a)],width=1.1)
actor=p.add_mesh(pv.Sphere(radius=0.041,center=point),color="black",
                 lighting=False,reset_camera=False)
front.AddActor(actor)
label(point+np.array([-0.37,0.18,0]),r"$\mathbf{x}(u,v)$",30)
label((x0-0.02,0.45,0),r"$v$",27)
label((1.52,1.63,0),r"$(g(u),h(u),0)$",29)

# Radius h(u): a vertical double-headed dimension with an extension line.
dim_x=x0+0.74
curve([(x0,r0,0),(dim_x+0.17,r0,0)],width=1.0)
arrow((dim_x,r0/2,0),(dim_x,r0,0),tip=0.10,radius=0.032)
arrow((dim_x,r0/2,0),(dim_x,0,0),tip=0.10,radius=0.032)
label((dim_x+0.28,r0/2,0),r"$h(u)$",29)

# Schematic g(u) dimension beneath the surface, positioned like the reference.
# Its endpoints are annotation anchors, not additional points on the surface.
left=np.array([-1.64,-1.43,0.0])
right=np.array([x0-0.16,-1.43,0.0])
mid=(left+right)/2
arrow(mid+np.array([-0.34,0,0]),left,tip=0.12,radius=0.035)
arrow(mid+np.array([0.34,0,0]),right,tip=0.12,radius=0.035)
label(mid,r"$g(u)$",29)


def callout(start, control, end):
    s=np.linspace(0,1,90)[:,None]
    start,control,end=map(lambda q:np.asarray(q,float),(start,control,end))
    pts=(1-s)**2*start+2*s*(1-s)*control+s*s*end
    curve(pts[:-8],width=1.15)
    arrow(pts[-9],end,tip=0.085,radius=0.026)


# A parallel has fixed u; a meridian has fixed v.
callout((x0+0.48,-1.48,0),(x0+0.49,-0.94,0),surface_point(U_POINT,3.80))
label((x0+0.43,-1.69,0),"parallel",27)
callout((4.13,-1.54,0),(3.68,-1.62,0),surface_point(0.88,np.pi))
label((4.10,-1.77,0),"meridian",27)

# The same oblique camera projects x right, y up, and z lower-left.
curve([(0,0,0),(g(0),0,0)],width=1.1)
curve(np.linspace((g(0),0,0),(g(1),0,0),500),dashed=True,width=1.1)
arrow((g(1),0,0),(5.0,0,0))
label((5.08,-0.16,0),r"$x$",30)
arrow((0,0,0),(0,2.25,0))
label((-0.18,2.25,0),r"$y$",30)
arrow((0,0,0),(0,0,8.0),tip=0.38,radius=0.04)
label((-0.1,-0.05,8.05),r"$z$",30)

if save_image:
    p.show(screenshot=save_image)
else:
    p.show()
