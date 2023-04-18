# M6 Group Assignments
Group members: Nadia, Nikolaj & Nicklas

This repository contains group assignments for BDS M6. A seperate folder is created for each assignment and the repository currently holds:
- [Group Assignment 1 - Notebook](Group_Assignment_1/Group_Assignment_1.ipynb)
- [Group Assignment 2 - Notebook](Group_Assignment_2/Group_Assignment_2-2.ipynb)
- [Group Assignment 3 - Notebook](Group_Assignment_3/Group_Assignment_3.ipynb)

## Group Assignment 1
This folder contains a SQLite database containing information about the 2.000 most cited documents on Scopus within the topic of Natural Language Processing.

A T5 summarization pipeline has then been applied from HuggingFace to generate super-summarized abstracts of 50 characters or less. This provides users with a quick overview of a documents' content. The model is demonstrated in Grad.io in which the user can select a document from the Scopus database or upload their own abstract/abstracts not available in the database. The interface then returns a super-summarized abstract.

## Group Assignment 2
This folder contains a notebook where Polars is used to do basic EDA and reading data. 

The data is loaded with Polars and consists of 2 datasets with official Baseball Data. A master file and a batting file is combined to make a large dataset. The data is then put through basic EDA and plotting of the data. 

## Group Assignment 3
This folder contains a machine learning model based on the baseball dataset used in group assignment 2. The model predicts the number of homeruns based on 4 inputs, namely weight, height, games played and at-bat. Using MLFlow, the hyperparameters, metrics and artifacts of 3 model experiments have been logged and saved along with structured and unstructured information related to the trained model.
