#!/bin/bash
##################################
##第一步，拆分成每个基因的fasta文件#
##################################
# 定义变量
BASE_DIR='/mnt/f/OneDrive/文档（科研）/脚本/Download/3-VCF2FASTA/2-FASTA_CDS'
PYTHON3_PATH="/home/luolintao/miniconda3/envs/pyg/bin/python3"
cds_file="${BASE_DIR}/conf/posCDS.csv" # ! 注意，这是幽门螺旋杆菌的CDS位置文件

# todo : 修改为实际的输入和输出路径
output_folder="/mnt/f/幽门螺旋杆菌分析高速/CDS_sequences"
input_folder="/mnt/f/幽门螺旋杆菌分析高速/split_sequences"

# 使用 parallel 处理所有 fasta 文件
ls $input_folder/*.fasta | parallel -j 10 ${PYTHON3_PATH} \
    "${BASE_DIR}/1_ExtractCDS.py" \
    --fasta {} --cds $cds_file --output $output_folder

