#!/bin/bash

# 定义输入目录
INPUT_DIR="/mnt/f/1_唐小琼项目/1_准备工作/data/Final_CSV_files/"

# 定义参考序列和输出目录
REFERENCE_FASTA="/mnt/d/幽门螺旋杆菌/参考序列/NC_000915.fasta"
OUTPUT_DIR="/mnt/d/幽门螺旋杆菌/Script/分析结果/1-序列处理流/output/merge_fasta/不考虑InDel/"

# 检查输出目录是否存在，不存在则创建
mkdir -p "$OUTPUT_DIR"

# 使用GNU Parallel并行处理所有CSV文件
find "$INPUT_DIR" -type f -name "*.csv" | parallel -j 4 /home/luolintao/miniconda3/envs/pyg/bin/python3 /mnt/f/OneDrive/文档（科研）/脚本/Download/3-VCF2FASTA/1-VCF2FASTA/script/6_csv_fasta_noInDel.py {} "$REFERENCE_FASTA" "$OUTPUT_DIR"

echo "所有CSV文件已成功转换为FASTA格式。"
