
#############################
##第二步，每个基因生成对齐文件#
#############################
#!/bin/bash

# 设置输入和输出路径
input_base_dir="/mnt/f/幽门螺旋杆菌分析高速/CDS_sequences/Unfinished/"
output_base_dir="/mnt/f/幽门螺旋杆菌分析高速/CDS_Align"
script_path="/mnt/f/OneDrive/文档（科研）/脚本/Download/3-VCF2FASTA/2-FASTA_CDS/src/1_mergeCDS.py"

# 创建输出目录（如果不存在）
mkdir -p "$output_base_dir"

# 定义并行处理的函数
process_folder() {
    local input_dir="$1"
    local folder_name
    folder_name=$(basename "$input_dir")
    local output_file="$output_base_dir/${folder_name}_merged.aln"

    echo "Processing folder: $folder_name"
    /home/luolintao/miniconda3/envs/pyg/bin/python3 \
    "$script_path" -i "$input_dir" -o "$output_file"

    # 检查是否成功生成文件
    if [ -f "$output_file" ]; then
        echo "Output saved to $output_file"
    else
        echo "Error: Failed to generate output for $folder_name"
    fi
}

export -f process_folder
export script_path
export output_base_dir

# 使用 GNU parallel 并行处理所有子文件夹
find "$input_base_dir" -mindepth 1 -maxdepth 1 -type d | parallel -j $(nproc) process_folder {}

echo "All folders processed."

