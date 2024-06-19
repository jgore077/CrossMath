from ranx import Qrels, Run, evaluate, compare
import os

from pathlib import Path

class ResultEvaluation():
    def __init__(self,qrelsPath:str,ndcgPath:str,relevanceLevel:int=1) -> None:
        self.qrelsPath=qrelsPath
        self.qrelFiles=[f'{self.qrelsPath}/{file}' for file in os.listdir(self.qrelsPath)]
        # Used to correlate qrel sets with their respective ARQmath sets
        self.qrelDict={
            'qrel_task1_2020.tsv':'a1',
            'qrel_task1_2021.tsv':'a2',
            'qrel_task1_2022.tsv':'a3',
        }
        
        self.relevanceLevel=relevanceLevel
        self.runs={
            
        }
        
    def evaluate(self,resultsPath:str):
        resultFiles=[f'{resultsPath}/{file}' for file in os.listdir(resultsPath)]
        qrelFiles=[f'{self.qrelsPath}/{file}' for file in os.listdir(self.qrelsPath)]
        for qrel in qrelFiles:
            qrels = Qrels.from_file(qrel, kind="trec")
            qrels.set_relevance_level(self.relevanceLevel)
            # Finds the corresponding sets for each qrel
            for result in [resultFile for resultFile in resultFiles if self.qrelDict[os.path.basename(qrel)] in resultFile]:    
                run = Run.from_file(result, kind="trec")
                self.runs[result]=run
                # The croatian results have a serious error within them, they are longer than other sets
                temp = evaluate(qrels, run, ["precision@5","ndcg@5"],make_comparable=True) # temp is a dictionary
                print(result)
                print(temp)
                
    # Deprecated but not removing as it provides some extra information
    def compareRuns(self,modelName:str,compareModel:str):
        keys=[key for key in self.runs.keys() if modelName in key]
        invertedQrelDict=dict((v, k) for k, v in self.qrelDict.items())
        for key in keys:
            # print(f'{self.qrelsPath}/{invertedQrelDict[Path(key).stem[-2:]]}')
            # print(key,f'{compareModel}/{os.path.basename(key)}')
            result=compare(
                qrels=Qrels.from_file(f'{self.qrelsPath}/{invertedQrelDict[Path(key).stem[-2:]]}',kind="trec"),
                runs=[self.runs[key],self.runs[f'{compareModel}/{os.path.basename(key)}']],
                metrics=["precision@10", "ndcg@10"],
                max_p=0.05,
                stat_test='student',
            )
            print(result)
        
    def compareRuns(self,floresCode:str)->None:
        keys=[key for key in self.runs.keys() if floresCode in key]
        invertedQrelDict=dict((v, k) for k, v in self.qrelDict.items())
        invertedQrelDictKeys=invertedQrelDict.keys()
        for arqMathCode in invertedQrelDictKeys:
            test=[self.runs[key] for key in keys if arqMathCode in key]
            qrel=Qrels.from_file(f'{self.qrelsPath}/{invertedQrelDict[arqMathCode]}',kind="trec")
            qrel.set_relevance_level(self.relevanceLevel)
            result=compare(
                qrels=qrel,
                runs=[self.runs[key] for key in keys if arqMathCode in key],
                metrics=["precision@10", "ndcg@10"],
                max_p=0.05,
                stat_test='student',
            )
            print(result)
    
    
    def generateQueryScores(self,resultPath:str,floresCode:str)->None:
        invertedQrelDict=dict((v, k) for k, v in self.qrelDict.items())
        invertedQrelDictKeys=invertedQrelDict.keys()
        resultFiles=[file for file in os.listdir(resultPath) if floresCode in file]
        # Sort based on which arqmath set to match with invertedQrelDictKeys
        # 'a1'<'a2'==True
        resultFiles.sort(key=lambda file: file[-6:-4])
        fullQrelIDS=[]
        fullResults=[]
        for qrelKey,resultFile in zip(invertedQrelDictKeys,resultFiles):
            qrels = Qrels.from_file(f'{self.qrelsPath}/{invertedQrelDict[qrelKey]}', kind="trec")
            qrels.set_relevance_level(self.relevanceLevel)
            run = Run.from_file(f'{resultPath}/{resultFile}', kind="trec")
            temp = evaluate(qrels, run, ["precision@10"],make_comparable=False,return_mean=False) # temp is a dictionary
            fullResults.extend(temp)
            fullQrelIDS.extend(qrels.get_query_ids())
        if not os.path.exists('evaluation/precisions'):
            os.mkdir('evaluation/precisions')
        with open(f'evaluation/precisions/{floresCode}_precision.tsv','w',encoding='utf-8') as precisionTsv:
            for id,score in zip(fullQrelIDS,fullResults):
                precisionTsv.write(f'{id}\t{score}\n')
                
    def calculateAverageAssessementForQrels(self)->int:
        numCounted=0
        countDict={}
        for file in os.listdir(self.qrelsPath):
            with open(f'{self.qrelsPath}/{file}','r',encoding='utf-8') as qrel:
                for line in qrel.readlines():
                    line=line.split('\t')
                    numCounted+=1
                    if countDict.get(line[0])==None:
                        countDict[line[0]]=1
                        continue
                    countDict[line[0]]+=1
        return numCounted//len(countDict.keys())
            
    
if __name__=="__main__":
    evaluator= ResultEvaluation('evaluation/qrels','evaluation/ndcg',relevanceLevel=2)
    print(f'Average Number Of Assessments per question in the Qrel Corpus: {evaluator.calculateAverageAssessementForQrels()}')
    evaluator.evaluate('evaluation/mbartbi')
    evaluator.evaluate('evaluation/mbartcross')
    evaluator.evaluate('evaluation/nllbbi')
    evaluator.evaluate('evaluation/nllbcross')
    
    print('English (Baseline)')
    evaluator.compareRuns('eng_Latn')
    print('Czech')
    evaluator.compareRuns('ces_Latn')
    print('Czech')
    evaluator.compareRuns('ces_Latn')
    print('Croatian')
    evaluator.compareRuns('hrv_Latn')
    print('Spanish')
    evaluator.compareRuns('spa_Latn')
    print('Farsi/Persian')
    evaluator.compareRuns('pes_Arab')
    print('Nepali')
    evaluator.compareRuns('npi_Deva')
    print('Hindi')
    evaluator.compareRuns('hin_Deva')

    evaluator.generateQueryScores('evaluation/nllbbi','ces_Latn')
    evaluator.generateQueryScores('evaluation/nllbbi','hrv_Latn')
    evaluator.generateQueryScores('evaluation/nllbbi','spa_Latn')
    evaluator.generateQueryScores('evaluation/nllbbi','pes_Arab')
    evaluator.generateQueryScores('evaluation/nllbbi','eng_Latn')