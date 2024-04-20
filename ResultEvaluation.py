from ranx import Qrels, Run, evaluate
import os

class ResultEvaluation():
    def __init__(self,resultsPath,qrelsPath,ndcgPath,relevanceLevel) -> None:
        self.resultsPath=resultsPath
        self.qrelsPath=qrelsPath
        # Used to correlate qrel sets with their respective ARQmath sets
        self.qrelDict={
            'qrel_task1_2020.tsv':'a1',
            'qrel_task1_2021.tsv':'a2',
            'qrel_task1_2022.tsv':'a3',
        }
        self.relevanceLevel=relevanceLevel
    
    def evaluate(self):
        resultFiles=[f'{self.resultsPath}/{file}' for file in os.listdir(self.resultsPath)]
        qrelFiles=[f'{self.qrelsPath}/{file}' for file in os.listdir(self.qrelsPath)]
        for qrel in qrelFiles:
            qrels = Qrels.from_file(qrel, kind="trec")
            qrels.set_relevance_level(self.relevanceLevel)
            # Finds the corresponding sets for each qrel
            for result in [resultFile for resultFile in resultFiles if self.qrelDict[os.path.basename(qrel)] in resultFile]:    
                run = Run.from_file(result, kind="trec")
                temp = evaluate(qrels, run, ["precision@10","ndcg@10", "ndcg@100", "ndcg@1000"]) # temp is a dictionary
                print(result)
                print(temp)

        
    
if __name__=="__main__":
    evaluator= ResultEvaluation('evaluation/results','evaluation/qrels','evaluation/ndcg',2)
    evaluator.evaluate()
