from ranx import Qrels, Run, evaluate, compare
import os
from pathlib import Path

class ResultEvaluation():
    def __init__(self,qrelsPath,ndcgPath,relevanceLevel) -> None:
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
        
    def evaluate(self,resultsPath):
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
                temp = evaluate(qrels, run, ["precision@10","ndcg@10", "ndcg@100", "ndcg@1000"],make_comparable=True) # temp is a dictionary
                print(result)
                print(temp)
                
    def compareRuns(self,modelName:str,compareModel:str):
        keys=[key for key in self.runs.keys() if modelName in key]
        invertedQrelDict=dict((v, k) for k, v in self.qrelDict.items())
        for key in keys:
            # print(f'{self.qrelsPath}/{invertedQrelDict[Path(key).stem[-2:]]}')
            # print(key,f'{compareModel}/{os.path.basename(key)}')
            print(compare(
                qrels=Qrels.from_file(f'{self.qrelsPath}/{invertedQrelDict[Path(key).stem[-2:]]}',kind="trec"),
                runs=[self.runs[key],self.runs[f'{compareModel}/{os.path.basename(key)}']],
                metrics=["precision@10", "ndcg@10"],
                max_p=0.05,
                stat_test='student',
            ))
            
        pass
        
    
if __name__=="__main__":
    evaluator= ResultEvaluation('evaluation/qrels','evaluation/ndcg',1)
    evaluator.evaluate('evaluation/mbartbi')
    evaluator.evaluate('evaluation/mbartcross')
    evaluator.evaluate('evaluation/nllbbi')
    evaluator.evaluate('evaluation/nllbcross')
    evaluator.compareRuns('evaluation/mbartbi','evaluation/nllbbi')
