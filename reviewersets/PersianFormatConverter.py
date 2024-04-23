import csv
import os


class FormatConverter():

    def __init__(self, setPath: str, storePath: str = 'datasets') -> None:
        self.setPath = setPath
        self.fullSetPath = os.path.join('reviewersets/', setPath)
        self.storePath = storePath

    def convert(self):
        with open(self.fullSetPath, encoding='utf-8') as fd:
            rd = csv.reader(fd, delimiter="\t", quotechar='"')
            fd.seek(0)
            rows = [row for row in rd]
            with open(f"{self.storePath}/{self.setPath}", 'w', encoding='utf-8') as translated_set:
                for row in rows:
                    newRow = [row[0], row[6], row[7], row[3]]
                    for i in range(1, len(newRow)):
                        newRow[i] = '\t' + newRow[i]
                    newRow[3] += '\n'
                    translated_set.writelines(newRow)



if __name__ == "__main__":
    converter = FormatConverter('pes_Arab.tsv')
    converter.convert()