from math import radians,cos, sin
from time import sleep
import open3d as o3d
import numpy as np

def rotacion_xyz(rot_x=0.0,rot_y=0.0,rot_z=0.0):
    x = radians(rot_x)
    y = radians(rot_y)
    z = radians(rot_z)

    matris = np.zeros((4,4),np.float32)

    matris[0][0] = (cos(y+z)+cos(y-z))/2
    matris[0][1] = (-cos(x+y+z)+cos(x-y+z)-cos(x+y-z)+cos(x-y-z)+2*sin(x+z)-2*sin(x-z))/4
    matris[0][2] = (-2*cos(x+z)+2*cos(x-z)-sin(x+y+z)+sin(x-y+z)-sin(x+y-z)+sin(x-y-z))/4

    matris[1][0] = (-sin(y+z)+sin(y-z))/2
    matris[1][1] = (2*cos(x+z)+2*cos(x-z)+sin(x+y+z)-sin(x-y+z)-sin(x+y-z)+sin(x-y-z))/4
    matris[1][2] = (-cos(x+y+z)+cos(x-y+z)+cos(x+y-z)-cos(x-y-z)+2*sin(x+z)+2*sin(x-z))/4

    matris[2][0] = sin(y)
    matris[2][1] = (-sin(x+y)-sin(x-y))/2
    matris[2][2] = (cos(x+y)+cos(x-y))/2

    matris[3][3] = 1.0

    return matris

if __name__ == "__main__":
    target_raw = o3d.io.read_point_cloud("sync2.ply")
    source_raw = o3d.io.read_point_cloud("sync2.ply")

    #source = source_raw.remove_radius_outlier(5,100)[0]

    #source = source_raw.remove_statistical_outlier(50,100)[0]

    print(rotacion_xyz(0,45,45))
    print(o3d.geometry.get_rotation_matrix_from_axis_angle([0,45,45]))
    print(o3d.geometry.get_rotation_matrix_from_xyz([0,45,45]))

    #print(source_raw.transformation)
    #o3d.visualization.draw_geometries([target_raw,source_raw])
    #source_raw.transform(rotacion_xyz(45,0,0))
    #o3d.visualization.draw_geometries([target_raw,source_raw])
    #sync0
    #source_raw.translate([0,0,-800])

    """trans = [
            [ 0.0, -1.0,  0.0,  0.0], 
            [ 1.0,  0.0,  0.0,  0.0],
            [ 0.0,  0.0,  1.0,  0.0], 
            [ 0.0,  0.0,  0.0,  1.0]]
    source_raw.transform(trans)
    source_raw.transform(trans)
    source_raw.transform(trans)

    source_raw.translate([700,-1300,200])"""
    #o3d.visualization.draw_geometries([target_raw])
    #o3d.visualization.draw_geometries([source_raw])
    #o3d.visualization.draw_geometries([target_raw,source_raw])
    #o3d.visualization.draw_geometries([source])

    
    """source_raw.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=500, max_nn=50))
    target_raw.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=500, max_nn=50))

    source = source_raw.voxel_down_sample(voxel_size=1)
    target = target_raw.voxel_down_sample(voxel_size=1)

    vis = o3d.visualization.Visualizer()
    vis.create_window()
    vis.add_geometry(source)
    vis.add_geometry(target)
    
    icp_iteration = 100
    threshold = np.linspace(100,100,icp_iteration)
    #threshold = 300
    save_image = False

    for i in range(icp_iteration):
        reg_p2l = o3d.pipelines.registration.registration_icp(
            source, target, threshold[i], np.identity(4),
            #source, target, threshold, np.identity(4),
            o3d.pipelines.registration.TransformationEstimationPointToPoint(),
            o3d.pipelines.registration.ICPConvergenceCriteria(max_iteration=10))
        source.transform(reg_p2l.transformation)
        vis.update_geometry(source)
        vis.poll_events()
        vis.update_renderer()
        if save_image:
            vis.capture_screen_image("temp_%04d.jpg" % i)

    vis.destroy_window()
    o3d.utility.set_verbosity_level(o3d.utility.VerbosityLevel.Info)

    p1_load = np.asarray(source.points)
    p2_load = np.asarray(target.points)

    p3_load = np.concatenate((p1_load,p2_load), axis=0)

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(p3_load)

    pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=500, max_nn=30))
    pcd = pcd.voxel_down_sample(voxel_size=1)

    o3d.io.write_point_cloud("sync_ICP.ply", pcd)
    o3d.visualization.draw_geometries([pcd])"""

    