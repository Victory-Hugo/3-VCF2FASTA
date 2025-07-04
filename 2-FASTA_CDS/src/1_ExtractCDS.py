import argparse
from Bio import SeqIO
import os
import glob

# 定义互补碱基字典，添加默认逻辑处理非标准字符
complementary_bases = {
    'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C', '-': '-', 'N': 'N'
}

# 提取反向互补序列时处理未知碱基
def get_complementary_sequence(sequence):
    return ''.join(
        complementary_bases.get(base, 'N')  # 如果不是标准碱基，默认为'N'
        for base in reversed(sequence)
    )

# 主函数
def process_fasta(fasta_file_path, cds_file_path, output_base_folder):
    # 读取CSV文件，解析CDS信息
    cds_info = []
    with open(cds_file_path, 'r') as csv_file:
        for line in csv_file:
            fields = line.strip().split('\t')
            cds_info.append({
                'start': int(fields[3]) - 1,  # 起始位置 (0基准)
                'end': int(fields[4]) - 1,  # 终止位置 (0基准)
                'strand': fields[6]  # 链方向
            })

    fasta_file_name = os.path.basename(fasta_file_path)  # 获取文件名，例如 "3697.fasta"
    
    # 逐条处理fasta文件中的序列
    with open(fasta_file_path, 'r') as fasta_file:
        for record in SeqIO.parse(fasta_file, 'fasta'):  # 逐条解析fasta文件中的序列
            sequence = str(record.seq)
            
            # 提取每个CDS区域的序列
            for cds_idx, cds in enumerate(cds_info):
                start = cds['start']
                end = cds['end']
                strand = cds['strand']
                
                # 提取序列
                if strand == '+':  # 正链
                    extracted_sequence = sequence[start:end + 1]
                elif strand == '-':  # 反链
                    extracted_sequence = get_complementary_sequence(sequence[start:end + 1])
                else:
                    continue
                
                # 按CDS编号创建文件夹
                cds_folder = os.path.join(output_base_folder, f"CDS_{cds_idx + 1}")
                os.makedirs(cds_folder, exist_ok=True)  # 确保文件夹存在
                
                # 保存到对应CDS文件夹中，以原始fasta文件名保存
                output_file = os.path.join(cds_folder, fasta_file_name)
                with open(output_file, 'w') as out_file:
                    out_file.write(f">{fasta_file_name}\n")
                    out_file.write(extracted_sequence + '\n')

        print(f"处理完成: {fasta_file_name}")

# 命令行参数解析
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a single fasta file based on CDS annotations.")
    parser.add_argument("--fasta", required=True, help="Path to the input fasta file.")
    parser.add_argument("--cds", required=True, help="Path to the CDS annotation file (CSV).")
    parser.add_argument("--output", required=True, help="Base output folder for the CDS sequences.")
    args = parser.parse_args()

    # 调用主函数
    process_fasta(args.fasta, args.cds, args.output)
