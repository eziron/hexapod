from hashlib import new
import open3d as o3d
import os
import numpy as np
from datetime import datetime
samp_PATH = "samples\\"

def save_pcd(pcd,base_name:str):
    dt_string = datetime.now().strftime(base_name+"-%d%m%Y-%H%M%S.ply")
    o3d.io.write_point_cloud(samp_PATH+dt_string, pcd)


dir_samples = os.listdir("samples")
if(len(dir_samples) == 1):
    n = 0
else:
    for i in range(len(dir_samples)):
        if(".ply" in dir_samples[i]):
            print("["+str(i)+"] = ",dir_samples[i])


    n = int(input("selecciona el archivo: "))

pcd = o3d.io.read_point_cloud("samples\\"+dir_samples[n])
print(len(pcd.points))
o3d.visualization.draw_geometries([pcd])


"""
pcd = pcd.remove_statistical_outlier(nb_neighbors=100, std_ratio=2)[0]
pcd = pcd.remove_statistical_outlier(nb_neighbors=100, std_ratio=5)[0]
print(len(pcd.points))
o3d.visualization.draw_geometries([pcd])
"""
"""
pcd = pcd.remove_radius_outlier(nb_points=25, radius=50)[0]
print(len(pcd.points))
o3d.visualization.draw_geometries([pcd])
"""

#Ball pivoting
"""
print('run Ball pivoting reconstruction')
distances = pcd.compute_nearest_neighbor_distance()
avg_dist = np.mean(distances)
radius = 3 * avg_dist

print(avg_dist,radius)
print(np.max(distances))
print(np.min(distances))

pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=radius, max_nn=30))

radii = [radius*2, radius*10, radius*20, radius*30]
mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(pcd, o3d.utility.DoubleVector(radii))
mesh.compute_vertex_normals()
#o3d.visualization.draw_geometries([pcd, mesh])
o3d.visualization.draw_geometries([mesh])
"""
#Alpha shapes
"""
print('run Alpha shapes reconstruction')
alpha = 0.03
print(f"alpha={alpha:.3f}")
pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=100, max_nn=30))
mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(pcd, alpha)
mesh.compute_vertex_normals()
o3d.visualization.draw_geometries([mesh])
"""
#Poisson surface reconstruction
"""
print('run Poisson surface reconstruction')
pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=100, max_nn=30))
with o3d.utility.VerbosityContextManager(o3d.utility.VerbosityLevel.Debug) as cm:
    mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=9)

mesh.compute_vertex_normals()
o3d.visualization.draw_geometries([mesh])
"""


