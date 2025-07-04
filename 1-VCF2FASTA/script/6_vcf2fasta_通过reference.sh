#!/usr/bin/env bash
set -euo pipefail

VCF="/mnt/f/0_现代DNA处理流程/output/merge/merged.biallelic.vcf.gz"
SAMPLE_LIST="/mnt/f/0_现代DNA处理流程/output/merge/vcf.txt"
REF="/mnt/f/0_现代DNA处理流程/script/chrM.fasta"
OUTDIR="/mnt/f/0_现代DNA处理流程/output/fasta"
mkdir -p "$OUTDIR"

# # 索引
# bcftools index "$VCF"
# samtools faidx "$REF"

# 过滤掉空行，然后为每个样本生成 fasta
grep -v '^[[:space:]]*$' "$SAMPLE_LIST" | while read -r SAMPLE; do
  echo ">>> processing $SAMPLE"
  bcftools consensus \
    -f "$REF" \
    -s "$SAMPLE" \
    -o "$OUTDIR/${SAMPLE}.fasta" \
    "$VCF"
done

echo "► 所有样本的 fasta 已写入 $OUTDIR/"
