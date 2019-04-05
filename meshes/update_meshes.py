import bpy
import mathutils

RESOLUTION = 3


# TODO: output fewer points for straight segments.
def segment_points(start, end, resolution):
    return mathutils.geometry.interpolate_bezier(
        start.co, start.handle_right, end.handle_left, end.co, resolution)


def segments(spline):
    for i in range(len(spline.bezier_points) - 1):
        yield (spline.bezier_points[i], spline.bezier_points[i + 1])
    if spline.use_cyclic_u and len(spline.bezier_points) >= 2:
        yield (spline.bezier_points[-1], spline.bezier_points[0])


def points(spline):
    points = [spline.bezier_points[0].co]
    for segment in segments(spline):
        seg_points = segment_points(
            segment[0], segment[1], RESOLUTION)[1:-1]
        points.extend(seg_points)
    return points


ship_mesh = bpy.context.blend_data.meshes['Ship']
ship_object = bpy.context.blend_data.objects['Ship']
collision_curve = bpy.context.blend_data.curves['Collision']

collision_points = points(collision_curve.splines[0])
ship_mesh['collision_shape'] = [
    c for p in collision_points for c in (p.x, p.y)]

bpy.ops.object.select_all(action='DESELECT')
ship_object.select_set(state=True)

bpy.ops.export_scene.gltf(
    filepath='meshes/ship.glb',
    export_selected=True,
    export_extras=True,
    export_apply=True,
)
