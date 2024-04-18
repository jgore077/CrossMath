# Multilingual-Math-Translation
This repository consists of all files needed to run our experiments in the field  of multilingual math search/translation.
<hr/>

If you wish to run any of the experiments in this repository the first step will be installing the required dependencys.
```
pip install -r requirements.txt
```
# Important information
Almost every file in this repository is meant to be ran on devices that have GPU's that support <b>CUDA</b>. This is because without <b>CUDA</b> the runtime of file in this repository may increase by a factor of three or greater. The scripts that do require <b>CUDA</b> will not run without out so having a GPU is a requirement to run this experiment.

# Scripts
We have multiple scripts in this repository that were used at some point during the research. They are used to generate data, convert data formats, and evaluate results. I will desccribe what the most important scripts do and how to run them in this section.
<hr/>


## TranslatedDatasetGenerator.py
This script will generate the datasets in the format needed to run them through the cross_encoder_mir_retreival.py. You should not run this script if you intend to just go straight to the results as it will overwrite all of the human validated sets and negatively impact the score.

```
python TranslatedDatasetGenerator.py
```

## ReviewerDatasetGenerator.py
This script was used to generate datasets for our reviewers. The original english sentence will be on the top line while the translated version will be on the bottom. It was done in this manner so that our validators could have a reference to what was translated. You shouldnt run this script if you intend to evaluate the results as it will also overwrite the human translations.

```
python ReviewerDatasetGenerator.py
```

## cross_encoder_mir_retreival.py

```
python evaluation/cross_encoder_mir_retreival.py
```

## ResultEvaluation.py
This script evaluates the precision and NCDG (Normalized Cumulative Distribution Gain) of the output of cross_encoder_mir_retreival.py using the ranx library. It will print out the name of the dataset and its `precision@10`, `ndcg@10`, `ndcg@100`, `ndcg@1000`

```
python ResultEvaluation.py
```
