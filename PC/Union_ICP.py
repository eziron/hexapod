from time import time
from pynput import keyboard as kb
from datetime import datetime
import os
import open3d as o3d
import numpy as np
import string

samp_PATH = "samples\\"

teclas = dict.fromkeys(list(string.ascii_lowercase),0)

estado = True
def on_press(key):
    for n in list(teclas):
        if(key == kb.KeyCode.from_char(n)):
            teclas[n] = 1

def on_release(key):
    global estado
    for n in list(teclas):
        if(key == kb.KeyCode.from_char(n)):
            teclas[n] = 0

    if key == kb.Key.esc:
        estado = False
        return False

def boton(A:bool,B:bool,val:float):
    if((not A) and B):
        return val
    elif(A and (not B)):
        return -val
    else:
        return 0.0

listener = kb.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

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
    time_ref = time()
    while(estado):

        if(time()-time_ref > 0.03):
            time_ref = time()

            if(teclas["q"]):
                reg_p2l = o3d.pipelines.registration.registration_icp(
                    source, target, threshold, np.identity(4),
                    o3d.pipelines.registration.TransformationEstimationPointToPoint(),
                    o3d.pipelines.registration.ICPConvergenceCriteria(max_iteration=1))
                
                source.transform(reg_p2l.transformation)
            else:
                source.translate([
                    boton(teclas["w"],teclas["s"],1.0),
                    boton(teclas["e"],teclas["d"],1.0),
                    boton(teclas["r"],teclas["f"],1.0),
                ])

                source.rotate(
                        o3d.geometry.get_rotation_matrix_from_axis_angle([
                                boton(teclas["t"],teclas["g"],0.01),
                                boton(teclas["y"],teclas["h"],0.01),
                                boton(teclas["u"],teclas["j"],0.01),
                            ],
                        )
                    )
        
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