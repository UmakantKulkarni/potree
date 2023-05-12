#!/usr/bin/env bash
#potree specific

mydir=/home/kulkarnu

sudo apt-get -y install libpcl-dev python3-pcl pcl-tools cmake libgl1-mesa-glx xvfb libtbb-dev pdal git unzip

cd $mydir
git clone https://github.com/UmakantKulkarni/potree

cd $mydir
git clone https://github.com/potree/PotreeConverter
cd PotreeConverter
mkdir build
cd build
cmake ../
make

cd $mydir
mkdir pcs_dataset
cd pcs_dataset

#Static point cloud dataset - https://mpeg-pcc.org/index.php/pcc-content-database/8i-voxelized-surface-light-field-8ivslf-dataset/

wget https://mpeg-pcc.org/Downloads/8i/single%20frame/soldier_viewdep_vox12.zip
unzip soldier_viewdep_vox12.zip
pdal translate soldier_viewdep_vox12.ply soldier_viewdep_vox12.las
mkdir -p $mydir/potree/pointclouds/soldier_static
$mydir/PotreeConverter/build/PotreeConverter soldier_viewdep_vox12.las -o $mydir/potree/pointclouds/soldier_static/

#Dynamic Point cloud dataset - http://plenodb.jpeg.org/pc/8ilabs
wget http://plenodb.jpeg.org/pc/8ilabs/soldier.zip
unzip soldier.zip

rm -f soldier_viewdep_vox12.ply soldier_viewdep_vox12.las

#https://geotiles.nl/
#wget https://ns_hwh.fundaments.nl/hwh-ahn/AHN3/LAZ/C_25GN1.LAZ
#pdal translate C_25GN1.LAZ C_25GN1.las
#las2las -i C_25GN1.las -o C_25GN1_repaired.las
#mkdir netherland
#$mydir/PotreeConverter/build/PotreeConverte C_25GN1_repaired.las -o netherland/

#Dynamic Point cloud dataset - http://plenodb.jpeg.org/pc/8ilabs
#wget http://plenodb.jpeg.org/pc/8ilabs/longdress.zip
#unzip longdress.zip
#cd longdress/Ply
#vi concatenate_pipeline.json
#[    {        "type": "readers.ply",        "filename": "/opt/vs/longdress/Ply/*.ply"    },    {        "type": "filters.merge"    },    {        "type": "writers.ply",        "filename": "output.ply"    }]
#pdal pipeline concatenate_pipeline.json
#pdal translate /opt/vs/longdress/Ply/output.ply -o output.las
