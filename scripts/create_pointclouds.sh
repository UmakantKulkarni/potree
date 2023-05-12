#!/usr/bin/env bash

mydir=/home/kulkarnu
potreeConverter_path="$mydir/PotreeConverter/build/PotreeConverter"
potree_dir="$mydir/potree"

model=soldier
input_folder="$mydir/pcs_dataset/$model/Ply"
output_dir="$potree_dir/pointclouds/${model}_dynamic"
mkdir -p $output_dir

start_frame=536
end_frame=835

for frame_num in $(seq $start_frame $end_frame)
do
    echo $frame_num
    pdal translate $input_folder/${model}_vox10_0${frame_num}.ply $input_folder/${model}_vox10_${frame_num}.las
    mkdir -p $output_dir/$frame_num
    $potreeConverter_path $input_folder/${model}_vox10_${frame_num}.las -o $output_dir/$frame_num/
    rm -f $input_folder/${model}_vox10_${frame_num}.las
done

#rm -rf $mydir/pcs_dataset/$model