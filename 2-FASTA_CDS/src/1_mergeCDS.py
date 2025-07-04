import os
import argparse
from Bio import SeqIO
from collections import defaultdict

def get_fasta_files(directory):
    """获取目录下所有FASTA文件的路径"""
    fasta_extensions = ('.fasta', '.fa', '.fna', '.aln', '.fas')
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(fasta_extensions)]

def parse_fasta_files(fasta_files):
    """
    解析所有FASTA文件，返回一个字典：
    {样本名称: [序列1, 序列2, ...]}
    """
    sample_sequences = defaultdict(list)
    for fasta_file in fasta_files:
        print(f"Processing file: {fasta_file}")
        for record in SeqIO.parse(fasta_file, "fasta"):
            sample_id = record.id
            sequence = str(record.seq)
            sample_sequences[sample_id].append(sequence)
    return sample_sequences

def write_merged_fasta(sample_sequences, output_path):
    """将拼接后的序列写入一个FASTA文件"""
    with open(output_path, "w") as out_f:
        for sample_id, sequences in sorted(sample_sequences.items()):
            merged_sequence = ''.join(sequences)
            out_f.write(f">{sample_id}\n")
            # 为了提高可读性，可以每行写入60个字符
            for i in range(0, len(merged_sequence), 60):
                out_f.write(merged_sequence[i:i+60] + "\n")
    print(f"Merged alignment written to {output_path}")

def main(input_dir, output_file):
    fasta_files = get_fasta_files(input_dir)
    if not fasta_files:
        print("No FASTA files found in the specified directory.")
        return

    sample_sequences = parse_fasta_files(fasta_files)

    # 写入合并后的FASTA对齐文件
    write_merged_fasta(sample_sequences, output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge CDS sequences from multiple FASTA files.")
    parser.add_argument("-i", "--input_dir", required=True, help="Input directory containing FASTA files.")
    parser.add_argument("-o", "--output_file", required=True, help="Output file for merged sequences.")
    args = parser.parse_args()

    main(args.input_dir, args.output_file)
