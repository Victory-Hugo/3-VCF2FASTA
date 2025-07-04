#!/usr/bin/python3

## python 3.10.0
## 脚本用于从比对的基因组中提取CDS（编码序列）
## 并只保留属于核心基因组的CDS

## 读取比对文件
strain = []  # 保存菌株名称
sequence = []  # 保存序列
CDS = []  # 保存CDS
with open("/mnt/d/幽门螺旋杆菌/Script/分析结果/merged_fasta/merged.fasta", 'r') as f:
    for l in f:
        iline = l.rstrip('\n').split()
        if(iline[0][0] == '>'):  # 如果行以'>'开头，表示是菌株名称
            strain.append(iline[0])
        else:  # 否则是序列数据
            sequence.append(iline[0])
            CDS.append([])

nbSeq = len(sequence)  # 序列的数量

## 仅保留属于CDS的位点
## pos - 1 因为在Python中，第一个索引是0，而第一个位点的位置应该是1
## 注意还需要将密码子（codon）置于“正确”的阅读方向
## 如果链（第6列）是负链（-），需要反转密码子方向（还需要使用互补核苷酸）
## 因为这会影响密码子产生的氨基酸，进而直接影响dN和dS值
## 还需注意CDS的相位（第8列）；如果不是CDS，相位=‘.’
## 对于“CDS”类型的特征，相位表示特征相对于阅读框开始的位置
## 相位可以是0、1或2之一，表示要从该特征的开头移除的碱基数以到达下一个密码子的第一个碱基
## 注意在HpGlobal中，所有CDS的相位都是0
posCDS = []
ix = 0
with open("/mnt/d/幽门螺旋杆菌/Annotation/参考序列/posCDS.csv", "r") as f:
    for l in f:
        print(ix); ix += 1
        iline = l.rstrip('\n').split("\t")
        i1 = int(iline[3]) - 1
        i2 = int(iline[4]) - 1
        if iline[6] == '+':  # 正链
            posCDS.append(list(range(i1, i2+1)))
            for i in range(0, nbSeq):
                seq = sequence[i][i1:(i2+1)]
                CDS[i].append(seq)
        if iline[6] == '-':  # 负链
            posCDS.append(list(range(i2, i1-1, -1)))
            for i in range(0, nbSeq):
                seq = sequence[i][(i2):(i1-1):-1]
                seqRev = ["T" if seq[iseq] == "A" else "A" if seq[iseq] == "T" else "C" if seq[iseq] == "G" else "G" if seq[iseq] == "C" else "-" for iseq in range(0, len(seq))]
                CDS[i].append(''.join(seqRev))

## 分别保存每个CDS的基因序列
for i in range(0, len(CDS[0])):
    with open("CDS/" + str(i) + ".aln", "w") as f:
        for j in list(range(0,nbSeq)):
            f.write(strain[j] + "\n")
            [f.write(k) for k in CDS[j][i]]
            f.write("\n")

CDS = [[k for j in i for k in j] for i in CDS]
posCDS = [j for i in posCDS for j in i]
nbCDS = len(CDS[0])

## 删除不在至少99%序列中的密码子
## 计算所需的最小序列数
th = int(nbSeq/100)
CDSfilter = [[] for i in range(0,nbSeq)]
posCDScore = []
for i in range(0, nbCDS, 3):
    ## 按密码子分组
    ## 获取所有序列的相同密码子
    seq = [j[i] + j[i+1] + j[i+2] for j in CDS] 
    print(i)
    if (seq.count('---') <= th) and (seq.count('TAG') == 0) and (seq.count('TAA') == 0) and (seq.count('TGA') == 0):
        ## 如果该密码子满足上述所有条件，则保留
        ## 仅保留缺失序列少于阈值的密码子
        ## 如果所有核苷酸都缺失，则视为缺失密码子
        ## 是否还需要处理部分缺失的核苷酸？
        ## 如果至少有一个菌株中存在终止密码子（TAG、TAA、TGA），也需要删除密码子
        ## （另一种方法：可以将终止密码子替换为缺口，然后像处理其他缺失密码子一样处理，即仅在超过1%的菌株缺失此密码子时才删除密码子）
        ## 终止密码子：TAG, TAA, TGA
        ## 另外，保存密码子的真实位置
        posCDScore.append([posCDS[i:(i+3)]])
        for j in range(0,nbSeq):
            CDSfilter[j].append(seq[j])

posCDScore = [k for i in posCDScore for j in i for k in j]

## 将新的比对结果写入不同的文件
with open("/mnt/d/幽门螺旋杆菌/Script/分析结果/merged_fasta/coreCDS.aln", 'a') as f:
    for i in list(range(0,nbSeq)):
        f.write(strain[i] + "\n")
        [f.write(j) for j in CDSfilter[i]]
        f.write("\n")

## 还需保存序列
## 每个菌株一个文件
## 将数据集中的第一个菌株重命名为参考（与26695相同，但避免重复）
strain[0] = "Reference"
for i in list(range(0, nbSeq)):
    with open("strains/" + strain[i][1:] + ".fasta", 'w') as f:
        f.write(strain[i] + "\n")
        [f.write(j) for j in CDSfilter[i]]
        f.write("\n")

## 以及保留的不同核心CDS的真实位置
## 按新比对文件的顺序
## 注意：Python中的索引基于从0开始（posCDS基于索引，第一个索引=0 -> 这里的位置与gff文件中的位置有1的偏差）
## !! 在查看GWAS中显著位点的等位基因时需要考虑这一点
with open("/mnt/d/幽门螺旋杆菌/Script/分析结果/merged_fasta/posCoreCDS.txt", 'w') as f:
    [f.write(str(i + 1) + '\n') for i in posCDScore]
