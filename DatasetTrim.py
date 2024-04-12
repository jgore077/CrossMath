import csv
codes = ['zho_Hans', 'hin_Deva', 'npi_Deva', 'pes_Arab', 'ces_Latn', 'hrv_Latn', 'spa_Latn']

for code in codes:
    with open(f"datasets/{code}.tsv", encoding='utf-8') as fd:
        rd = csv.reader(fd, delimiter="\t", quotechar='"')
        fd.seek(0)
        rows = [row for row in rd]
        with open(f"datasets/{code}Trimmed.tsv", 'w', encoding='utf-8') as translated_set:
            for row in rows:
                row[2] = row[2][:2000]
                for i in range(1, len(row)):
                    row[i] = '\t' + row[i]
                row[3] += '\n'
                translated_set.writelines(row)


