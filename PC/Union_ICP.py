from datetime import datetime
import os
import open3d as o3d
import numpy as np

samp_PATH = "samples\\"

if __name__ == "__main__":
    dir_samples = os.listdir("samples")
    if(len(dir_samples) < 2):
        exit()
    else:
        for i in range(len(dir_samples)):
            if(".ply" in dir_samples[i]):
                print("["+str(i)+"] = ",dir_samples[i])

        n = int(input("selecciona el archivo base: "))
        samp_dir1 = dir_samples[n]
        n = int(input("selecciona el archivo a ajustar: "))
        samp_dir2 = dir_samples[n]

    target_raw = o3d.io.read_point_cloud(samp_PATH+samp_dir1)
    source_raw = o3d.io.read_point_cloud(samp_PATH+samp_dir2)

    source_raw.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=500, max_nn=50))
    target_raw.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=500, max_nn=50))

    source = source_raw.voxel_down_sample(voxel_size=1)
    target = target_raw.voxel_down_sample(voxel_size=1)

    vis = o3d.visualization.Visualizer()
    vis.create_window()
    vis.add_geometry(source)
    vis.add_geometry(target)
    
    threshold = 300
    estado = True
    while(estado):
        reg_p2l = o3d.pipelines.registration.registration_icp(
            source, target, threshold, np.identity(4),
            o3d.pipelines.registration.TransformationEstimationPointToPoint(),
            o3d.pipelines.registration.ICPConvergenceCriteria(max_iteration=10))
        
        source.transform(reg_p2l.transformation)
        
        vis.update_geometry(source)
        vis.poll_events()
        vis.update_renderer()


    vis.destroy_window()
    o3d.utility.set_verbosity_level(o3d.utility.VerbosityLevel.Info)

    p1_load = np.asarray(source.points)
    p2_load = np.asarray(target.points)
    p3_load = np.concatenate((p1_load,p2_load), axis=0)

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(p3_load)

    pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=500, max_nn=30))
    pcd = pcd.voxel_down_sample(voxel_size=1)

    dt_string = datetime.now().strftime("lidar_ICP-%d%m%Y-%H%M%S.ply")
    o3d.io.write_point_cloud(samp_PATH+dt_string, pcd)