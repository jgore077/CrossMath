from ranx import Qrels, Run, evaluate

class ResultEvaluation():
    def __init__(self,resultsPath) -> None:
        self.resultsPath=resultsPath
    
    def evaluate(self):
       
        qrels = Qrels.from_file("qrel_file", kind="trec")
        run = Run.from_file("results/roberta.tsv", kind="trec")
        print(evaluate(qrels, run, "precision@10"))
        temp = evaluate(qrels, run, ["map@100", "mrr@10", "ndcg@10"]) # temp is a dictionary
        #per query results
        evaluate(qrels, run, ["map@100", "mrr@10", "ndcg@10"], return_mean=False)

        
    
if __name__=="__main__":
    evalutor= ResultEvaluation('evaluation/results')