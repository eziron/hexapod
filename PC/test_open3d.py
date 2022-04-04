import open3d as o3d
import os

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
dir_samples = os.listdir("samples")
print(dir_samples)
pcd = []
for n in dir_samples:
    pcd.append(o3d.io.read_point_cloud("samples\\"+n))
#print(len(pcd.points))
o3d.visualization.draw_geometries(pcd)
"""

#pcd_low = pcd_low.voxel_down_sample(voxel_size=20)
#pcd_med = pcd_med.voxel_down_sample(voxel_size=20)
#pcd_high = pcd_high.voxel_down_sample(voxel_size=20)
#print(len(pcd_low.points),len(pcd_med.points),len(pcd_high.points))

#distances = pcd.compute_nearest_neighbor_distance()
#avg_dist = np.mean(distances)
#radius = 3 * avg_dist

#print(avg_dist)
#print(np.max(distances))
#print(np.min(distances))

#pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=100, max_nn=30))

#mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(pcd,o3d.utility.DoubleVector([radius, radius * 2]))
#mesh.compute_vertex_normals()
#o3d.visualization.draw_geometries([pcd, mesh])
#o3d.visualization.draw_geometries([pcd_low])
#o3d.visualization.draw_geometries([pcd_low,pcd_med,pcd_high])