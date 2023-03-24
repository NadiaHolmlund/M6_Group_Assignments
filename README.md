# M6 Group Assignments
Group members: Nadia, Nikolaj & Nicklas

This repository contains group assignments for BDS M6. A seperate folder is created for each assignment and the repository currently holds:
- [Group Assignment 1 - Notebook](Group_Assignment_1/Group_Assignment_1.ipynb)

## Group Assignment 1
This folder contains a SQLite database containing information about the 2.000 most cited documents on Scopus within the topic of Natural Language Processing.

A T5 summarization pipeline has then been applied from HuggingFace to generate super-summarized abstracts of 50 characters or less. This provides users with a quick overview of a documents' content. The model is demonstrated in Grad.io in which the user can select a document from the Scopus database or upload their own abstract/abstracts not available in the database. The interface then returns a super-summarized abstract.
