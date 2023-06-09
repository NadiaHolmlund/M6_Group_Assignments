# -*- coding: utf-8 -*-
"""Group_Assignment_1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/NadiaHolmlund/M6_Group_Assignments/blob/main/Group_Assignment_1/Group_Assignment_1.ipynb

# Task

Develop a Proof-of-Concept version of an application that is querying a database to come provide an output to the user.

This can be for example:
- Selecting observations from database, performing prediction with a (beforehand fitted) SML model.
- Perform a UML procedure on observations queried from a database.
- Perform a semantic/similarity search for an user input, retrieve most similar docs from a database.

The data used should be non-trivial (eg.: enough observations,´maybe multiple tables, different types of data…)
 - The solution has to be self-contained. This can be done:
 - Within a colab using for grad.io. (Hint: An option is to save the database on github, and then load it in the colab).)
 - As a streamlit app (figure out how to make it self-contained).
 - (sky is the limit.)

Possible databases:
- SQL DB (eg. SQL-lite)
- NoSQL DB
 - Document (eg. tinyDB)
 - Vector (Eg. Faiss, Chroma)

# Solution

In the following, we have created a SQLite database containing information about the 2.000 most cited documents on Scopus within the topic of Natural Language Processing.

Subsequently, a T5 summarization pipeline has been applied from HuggingFace to generate super-summarized abstracts of 50 characters or less. This provides users with a quick overview of the documents' content. The model is demonstrated in Grad.io in which the user can select a document from the Scopus database or upload their own abstract/abstracts not available in the database. The interface then returns a super-summarized abstract.

# Imports
"""

!pip install gradio --q
!pip install transformers --q

import pandas as pd
import sqlite3
from transformers import pipeline
import gradio as gr
from IPython.display import Image

pd.set_option('max_colwidth', 1000)
pd.describe_option('max_colwidth')

"""# Creating the database"""

# Reading the CSV file into a Pandas DataFrame
df = pd.read_csv('https://raw.githubusercontent.com/NadiaHolmlund/M6_Group_Assignments/main/Group_Assignment_1/Data/Scopus_NLP.csv')

# Examining the DataFrame
df.head()

# Extracting columns to be included in the database
df_clean = df[['Authors', 'Title', 'Abstract']]

# Examining the DataFrame
df_clean.info()

# Converting columns from objects to strings
df_clean['Authors'] = df_clean['Authors'].astype(str)
df_clean['Title'] = df_clean['Title'].astype(str)
df_clean['Abstract'] = df_clean['Abstract'].astype(str)

# Re-examining the dataframe
df_clean.info()

# Creating a connection to the database
conn = sqlite3.connect('Scopus.db')

# Setting up a cursor (pointer to rows in database)
c = conn.cursor()

# Creating a new table for the 'Authors' column
create_authors_query = """
    CREATE TABLE IF NOT EXISTS authors_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        author TEXT
    );
"""
conn.execute(create_authors_query)

# Creating a new table for the 'Title' column
create_title_query = """
    CREATE TABLE IF NOT EXISTS title_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        author TEXT,
        FOREIGN KEY (author) REFERENCES authors_table (id)
    );
"""
conn.execute(create_title_query)

# Creating a new table for the 'Abstract' column
create_abstract_query = """
    CREATE TABLE abstract_table (
    id INTEGER PRIMARY KEY,
    abstract TEXT,
    title TEXT,
    summary TEXT,
    FOREIGN KEY (title) REFERENCES title_table(title)
);
"""
conn.execute(create_abstract_query)

# Inserting data into the 'authors_table'
authors = set()
for author_str in df_clean['Authors']:
    for author in author_str.split(','):
        authors.add(author.strip())
for author in authors:
    insert_author_query = "INSERT OR IGNORE INTO authors_table (author) VALUES (?);"
    conn.execute(insert_author_query, (author,))

# Inserting data into the 'title_table'
select_authors_query = "SELECT * FROM authors_table;"
authors = {row[1]: row[0] for row in conn.execute(select_authors_query)}
for title, author_str in zip(df_clean['Title'], df_clean['Authors']):
    title = title.replace("'", "''")
    insert_title_query = f"INSERT OR IGNORE INTO title_table (title, author) VALUES ('{title}', '{authors[author_str.split(', ')[0]]}');"
    conn.execute(insert_title_query)

# Inserting data into the 'abstract_table'
select_titles_query = "SELECT * FROM title_table;"
titles = {row[1]: row[0] for row in conn.execute(select_titles_query)}
for abstract, title in zip(df_clean['Abstract'], df_clean['Title']):
    insert_abstract_query = "INSERT INTO abstract_table (abstract, title, summary) VALUES (?, ?, '');"
    conn.execute(insert_abstract_query, (abstract, titles[title]))

# Selecting data from the tables to determine if JOIN works across the tables as intended
select_query = """
    SELECT authors_table.author, title_table.title, abstract_table.abstract
    FROM authors_table
    JOIN title_table ON authors_table.id = title_table.author
    JOIN abstract_table ON title_table.id = abstract_table.title
    LIMIT 5;
"""
cursor = conn.execute(select_query)
rows = cursor.fetchall()

# Print the results
for row in rows:
    print(row)

# Printing an overview of the tables
# Quering the schema for each table from the `sqlite_master` table
c.execute("SELECT name, sql FROM sqlite_master WHERE type='table' ORDER BY name")
schemas = c.fetchall()

# Printing the schema for each table
for schema in schemas:
    table_name, table_schema = schema
    print(f"Table: {table_name}\nSchema:\n{table_schema}\n")

# Printing information from the authors_table to test the database
c.execute("SELECT * FROM authors_table LIMIT 5")
authors_table = c.fetchall()
for author_name in authors_table:
    print(author_name)

# Printing information from the title_table to test the database
c.execute("SELECT * FROM title_table LIMIT 5")
title_table = c.fetchall()
for title in title_table:
    print(title)

# Printing information from the abstract_table to test the database
c.execute("SELECT * FROM abstract_table LIMIT 5")
abstract_table = c.fetchall()
for abstract in abstract_table:
    print(abstract)

"""# Summarization Pipeline using SQLite"""

# Loading a pre-trained text-summarization model from HuggingFace Transformers
summarizer = pipeline('summarization', model="t5-base", tokenizer="t5-base", framework="tf")

# Extracting abstracts for summarization
abstracts = conn.execute('SELECT abstract FROM abstract_table limit 10')

# Iterating over the abstracts and updating the summary for each one
for i, row in enumerate(abstracts):
    # Extracting the text of the current abstract
    abstract = row[0]
    
    # Summarizing the abstract using the pre-trained summarizer
    summary = summarizer(abstract, max_length=50, min_length=0, do_sample=False)[0]['summary_text']
    
    # Updating the 'summary' column in the abstract_table with the summary of the current abstract
    conn.execute('UPDATE abstract_table SET summary = ? WHERE rowid = ?', (summary, i+1))
    
# Commit the changes to the database
conn.commit()

# Define the SQL query
query = 'SELECT * FROM abstract_table LIMIT 10'

# Execute the query and convert the result to a DataFrame
df_summed = pd.read_sql_query(query, conn)

# Examining the first abstract
df_summed['abstract'][0]

# Examining the summarization of the first abstract
df_summed['summary'][0]

"""Based on above, we determine that the model summarizes the abstract to a satisfying extent.

# Grad.io

## Generate a summary of a title available in our Scopus Database

Unfortunately, there is an issue with the Grad.io interface, which causes the output to fail when submitting a Title from the dropdown menu. However, the code functions without the interface, hence we suspect the issue is related to the dropdown function in Grad.io.

The code is therefore presented with examples below for proof-of-concept, followed by the Grad.io interface design.
"""

# Loading a pre-trained text-summarization model from HuggingFace Transformers
summarizer = pipeline('summarization', model="t5-base", tokenizer="t5-base", framework="tf")

# Connecting to the SQLite database
conn = sqlite3.connect('Scopus.db')

# Defining the dropdown options
c = conn.cursor()
c.execute("SELECT DISTINCT title FROM title_table")
dropdown_options = [row[0] for row in c.fetchall()]

# Defining the function for summarization
def summary(selected_option):
    c.execute("SELECT abstract FROM abstract_table WHERE id = (SELECT id FROM title_table WHERE title = ?)", (selected_option,))
    abstract = c.fetchone()[0]
    summary = summarizer(abstract, max_length=50, min_length=0, do_sample=False)
    return summary[0]['summary_text']

# Printing the first three titles for proof-of-concept purposes
print(dropdown_options[0])
print(dropdown_options[1])
print(dropdown_options[2])

# Printing the first three abstracts for proof-of-concept purposes
c.execute("SELECT * FROM abstract_table LIMIT 3")
abstract_table = c.fetchall()
for abstract in abstract_table:
    print(abstract)

# Printing the summarization of the first three abstract for proof-of-concept purposes
print(summary(dropdown_options[0]))
print(summary(dropdown_options[1]))
print(summary(dropdown_options[2]))

# Unfortunately, this part of the code fails when submitting a title from the dropdown menu. We suspect the issue is related to the Grad.io dropdown function.

# Creating the Gradio interface
demo = gr.Interface(
    title="Generate a summary of a title available in our Scopus Database",
    fn=summary,
    inputs=gr.inputs.Dropdown(choices=dropdown_options, type="value", label="Select a Title from Scopus"),
    outputs=gr.outputs.Textbox(label="Generated Summary"),
)

# Launching the interface
demo.launch()

# Below is the full code for the Grad.io application

# Loading a pre-trained text-summarization model from HuggingFace Transformers
summarizer = pipeline('summarization', model="t5-base", tokenizer="t5-base", framework="tf")

# Connecting to the SQLite database
conn = sqlite3.connect('Scopus.db')

# Defining the dropdown options
c = conn.cursor()
c.execute("SELECT DISTINCT title FROM title_table")
dropdown_options = [row[0] for row in c.fetchall()]

# Defining the function for summarization
def summary(selected_option):
    c.execute("SELECT abstract FROM abstract_table WHERE id = (SELECT id FROM title_table WHERE title = ?)", (selected_option,))
    abstract = c.fetchone()[0]
    summary = summarizer(abstract, max_length=50, min_length=0, do_sample=False)
    return summary[0]['summary_text']

# Creating the Gradio interface
demo = gr.Interface(
    title="Generate a summary of a title available in our Scopus Database",
    fn=summary,
    inputs=gr.inputs.Dropdown(choices=dropdown_options, type="value", label="Select a Title from Scopus"),
    outputs=gr.outputs.Textbox(label="Generated Summary"),
)

# Launching the interface
demo.launch()

"""## Generate a summary of your own abstract/abstracts not available in our Scopus Database

Note that this interface is not connected to the Scopus database, since the input is user-defined.
"""

# Loading a pre-trained text-summarization model from HuggingFace Transformers
summarizer = pipeline('summarization', model="t5-base", tokenizer="t5-base", framework="tf")

# Defining the function for summarization
def summary(abstract):
    summary = summarizer(abstract, max_length=50, min_length=0, do_sample=False)
    return summary[0]['summary_text']

# Defining examples
examples = [
    ["Recent methods for learning vector space representations of words have succeeded in capturing fine-grained semantic and syntactic regularities using vector arithmetic, but the origin of these regularities has remained opaque. We analyze and make explicit the model properties needed for such regularities to emerge in word vectors. The result is a new global logbilinear regression model that combines the advantages of the two major model families in the literature: global matrix factorization and local context window methods. Our model efficiently leverages statistical information by training only on the nonzero elements in a word-word cooccurrence matrix, rather than on the entire sparse matrix or on individual context windows in a large corpus. The model produces a vector space with meaningful substructure, as evidenced by its performance of 75% on a recent word analogy task. It also outperforms related models on similarity tasks and named entity recognition. © 2014 Association for Computational Linguistics."],
    ["We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers. Unlike recent language representation models (Peters et al., 2018a; Radford et al., 2018), BERT is designed to pre-train deep bidirectional representations from unlabeled text by jointly conditioning on both left and right context in all layers. As a result, the pre-trained BERT model can be fine-tuned with just one additional output layer to create state-of-the-art models for a wide range of tasks, such as question answering and language inference, without substantial task-specific architecture modifications. BERT is conceptually simple and empirically powerful. It obtains new state-of-the-art results on eleven natural language processing tasks, including pushing the GLUE score to 80.5% (7.7% point absolute improvement), MultiNLI accuracy to 86.7% (4.6% absolute improvement), SQuAD v1.1 question answering Test F1 to 93.2 (1.5 point absolute improvement) and SQuAD v2.0 Test F1 to 83.1 (5.1 point absolute improvement). © 2019 Association for Computational Linguistics"],
    ["In this paper, we propose a novel neural network model called RNN Encoder- Decoder that consists of two recurrent neural networks (RNN). One RNN encodes a sequence of symbols into a fixedlength vector representation, and the other decodes the representation into another sequence of symbols. The encoder and decoder of the proposed model are jointly trained to maximize the conditional probability of a target sequence given a source sequence. The performance of a statistical machine translation system is empirically found to improve by using the conditional probabilities of phrase pairs computed by the RNN Encoder-Decoder as an additional feature in the existing log-linear model. Qualitatively, we show that the proposed model learns a semantically and syntactically meaningful representation of linguistic phrases. © 2014 Association for Computational Linguistics."],
]

# Creating the Gradio interface
demo = gr.Interface(
    title="Generate a summary of your own abstract/abstracts not available in our Scopus Database",
    fn=summary,
    inputs=gr.inputs.Textbox(lines=5, label="Input Abstract"),
    outputs=gr.outputs.Textbox(label="Generated Summary"),
    examples=examples
)

# Launching the interface
demo.launch(share=True)

"""# Closing the Database Connection"""

conn.close()