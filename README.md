# similarity_engine
This application uses the Doc2Vec Model to find simillar PDF permit documents to ones selected by the user.

## Data
The input data for this application is saved in the following folders as PDF files. You can add more PDF documents to these folders as you start using this application
- boards_and_comissions
- similarity_engine
- business_licence
- dog_licence


The fieds extracted out of these PDF's are saved in the **raw_datafields** folder. The first column in each of these documents contain the pdf document name. The **script_for_saving_pdffields
python script is used for extracting out these fields**


## Setting Up
1. Have python 3X installed in your local machine

2. Add the python path to environment (follow this video)
    https://www.youtube.com/watch?v=Y2q_b4ugPWk
3. Once step 2 is completed, install the following packages by typing this in your command prompt

python -m pip install <packagename>
e.g
python -m pip install sklearn

Following packages need to be installed
gensim 
sklearn
easygui
nltk
tika 
pandas
pathlib
