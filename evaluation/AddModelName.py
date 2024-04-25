import csv
import os


for file in os.listdir("mbartbi"):
    name = file.split('.')[0]
    with open(f"mbartbi/{name}.tsv", encoding='utf-8') as fd:
        rd = csv.reader(fd, delimiter="\t", quotechar='"')
        fd.seek(0)
        rows = [row for row in rd]
        with open(f"mbartbi/{name}.tsv", 'w', encoding='utf-8') as added_set:
            for row in rows:
                row[5] = "mbart-" + str(row[5])
                for i in range(1, len(row)):
                    row[i] = '\t' + row[i]
                row[5] += '\n'
                added_set.writelines(row)

for file in os.listdir("mbartcross"):
    name = file.split('.')[0]
    with open(f"mbartcross/{name}.tsv", encoding='utf-8') as fd:
        rd = csv.reader(fd, delimiter="\t", quotechar='"')
        fd.seek(0)
        rows = [row for row in rd]
        with open(f"mbartcross/{name}.tsv", 'w', encoding='utf-8') as added_set:
            for row in rows:
                row[5] = "mbart-" + str(row[5])
                for i in range(1, len(row)):
                    row[i] = '\t' + row[i]
                row[5] += '\n'
                added_set.writelines(row)

for file in os.listdir("nllbbi"):
    name = file.split('.')[0]
    with open(f"nllbbi/{name}.tsv", encoding='utf-8') as fd:
        rd = csv.reader(fd, delimiter="\t", quotechar='"')
        fd.seek(0)
        rows = [row for row in rd]
        with open(f"nllbbi/{name}.tsv", 'w', encoding='utf-8') as added_set:
            for row in rows:
                row[5] = "nllb-" + str(row[5])
                for i in range(1, len(row)):
                    row[i] = '\t' + row[i]
                row[5] += '\n'
                added_set.writelines(row)

for file in os.listdir("nllbcross"):
    name = file.split('.')[0]
    with open(f"nllbcross/{name}.tsv", encoding='utf-8') as fd:
        rd = csv.reader(fd, delimiter="\t", quotechar='"')
        fd.seek(0)
        rows = [row for row in rd]
        with open(f"nllbcross/{name}.tsv", 'w', encoding='utf-8') as added_set:
            for row in rows:
                row[5] = "nllb-" + str(row[5])
                for i in range(1, len(row)):
                    row[i] = '\t' + row[i]
                row[5] += '\n'
                added_set.writelines(row)