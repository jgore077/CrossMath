import csv
import os

class FormatConverter():
    
    def __init__(self,setPath:str,storePath:str='datasets') -> None:
         self.setPath=setPath
         self.fullSetPath=os.path.join('reviewersets/',setPath)
         self.storePath=storePath
         
    def convert(self):
        with open(self.fullSetPath, encoding='utf-8') as fd:
                    rd = csv.reader(fd, delimiter="\t", quotechar='"')
                    fd.seek(0)
                    rows = [row for row in rd]
                    with open(f"{self.storePath}/{self.setPath}", 'w', encoding='utf-8') as translated_set:
                        index = 0
                        for row in rows:
                            if (index % 2) == 1:
                                for i in range(1, len(row)):
                                    row[i] = '\t' + row[i]
                                row[3] += '\n'
                                translated_set.writelines(row)
                            index = index + 1


if __name__=="__main__":
    converter=FormatConverter('hrv_Latn.tsv')
    converter.convert()