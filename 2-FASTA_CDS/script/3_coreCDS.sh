#############################
##第三步，提取每个基因的核心区域#
#############################
#!/bin/bash

# 设置输入和输出目录
INPUT_DIR="/mnt/f/幽门螺旋杆菌分析高速/CDS_Align"
OUTPUT_DIR="/mnt/f/幽门螺旋杆菌分析高速/Core_CDS_Align"
SCRIPT_PATH="/mnt/f/OneDrive/文档（科研）/脚本/Download/3-VCF2FASTA/2-FASTA_CDS/src/1-2_GetCoreCDS.py"

# 设置并行任务数（根据你的CPU核心数调整）
NUM_JOBS=4

# 检查 GNU Parallel 是否已安装
if ! command -v parallel &> /dev/null; then
    echo "错误: GNU Parallel 未安装。请安装后重试。"
    exit 1
fi

# 检查 Python 脚本是否存在
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "错误: Python 脚本 $SCRIPT_PATH 不存在。"
    exit 1
fi

# 创建输出目录（如果不存在）
if [ ! -d "$OUTPUT_DIR" ]; then
    echo "输出目录不存在，正在创建: $OUTPUT_DIR"
    mkdir -p "$OUTPUT_DIR"
    if [ $? -ne 0 ]; then
        echo "错误: 无法创建输出目录 $OUTPUT_DIR。"
        exit 1
    fi
fi

# 导出变量以供 parallel 使用
export SCRIPT_PATH
export OUTPUT_DIR

# 定义处理单个文件的函数
process_file() {
    INPUT_FILE="$1"
    FILENAME=$(basename "$INPUT_FILE")
    
    # 修改输出文件名：将 '_merged' 替换为 '_core'
    NEW_FILENAME="${FILENAME/_merged/_core}"
    OUTPUT_FILE="$OUTPUT_DIR/$NEW_FILENAME"

    echo "处理文件: $FILENAME -> $NEW_FILENAME"

    /bin/python3 "$SCRIPT_PATH" -i "$INPUT_FILE" -o "$OUTPUT_FILE"

    if [ $? -eq 0 ]; then
        echo "成功生成核心对齐文件: $OUTPUT_FILE"
    else
        echo "错误: 处理文件 $FILENAME 失败。"
    fi

    echo "----------------------------------------"
}

export -f process_file

# 使用 GNU Parallel 并行处理所有 .aln 文件
find "$INPUT_DIR" -type f -name "*.aln" | parallel -j "$NUM_JOBS" process_file {}

echo "所有文件处理完成。"


# ## 获取CDS（编码序列）的列表
# grep -P "NC_000915.1\s+Prodigal:002006\s+CDS" /mnt/d/幽门螺旋杆菌/Annotation/参考序列/NC_000915.gff > /mnt/d/幽门螺旋杆菌/Annotation/参考序列/posCDS.csv

# ## 准备dN/dS分析的序列：
# ## 移除终止密码子和在超过1%菌株中完全缺失的密码子（---）
# ## 输入：DATA/woHpGP_dnds.cvg70.aln  [global alignment], posCDS.csv [CDS位置]
# ## 输出：strains/strain_i.aln [每个菌株的所有CDS文件 -> 清理后的菌株序列],
# ##        CDS/CDS_i.aln [每个CDS的所有菌株文件 -> 清理后的CDS序列],
# ##        coreCDS.aln [所有CDS，所有菌株],
# ##        posCoreCDS.txt [保留CDS的位置 - 实际上没有CDS被移除]
# /bin/python3 s1_preprocess.py

# grep ">" coreCDS.aln | sort | uniq -d  # 查找重复的序列
# mv coreCDS.aln coreCDSclean.aln  # 重命名清理后的核心CDS文件
