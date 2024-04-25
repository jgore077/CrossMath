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
        
        
    
if __name__=="__main__":
    evaluator= ResultEvaluation('evaluation/qrels','evaluation/ndcg',relevanceLevel=2)
    evaluator.evaluate('evaluation/mbartbi')
    evaluator.evaluate('evaluation/mbartcross')
    evaluator.evaluate('evaluation/nllbbi')
    evaluator.evaluate('evaluation/nllbcross')
    evaluator.compareRuns('ces_Latn')
