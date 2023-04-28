{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyMvKvnPpou/S+oS8JVzWUc+",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/NadiaHolmlund/M6_Group_Assignments/blob/main/Group_Assignment_4/app.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!pip install streamlit"
      ],
      "metadata": {
        "id": "9vuNJW1mn5Na"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "nR9yB6FAn4jS"
      },
      "outputs": [],
      "source": [
        "import streamlit as st\n",
        "import pickle\n",
        "\n",
        "# Setting up page configurations\n",
        "st.set_page_config(\n",
        "    page_title=\"HR Prediction\",\n",
        "    page_icon=\"⚾\",\n",
        "    layout=\"wide\")\n",
        "\n",
        "# Loading the model\n",
        "@st.experimental_singleton\n",
        "def read_objects():\n",
        "    model = pickle.load(open('HR_model/model.pkl','rb'))\n",
        "\n",
        "    return model\n",
        "\n",
        "model = read_objects()\n",
        "\n",
        "def predict():\n",
        "    data = [[weight, height, G, AB]]\n",
        "    prediction = model.predict(data)[0]\n",
        "\n",
        "# Setting up the page\n",
        "weight = st.number_input('Weight')\n",
        "height = st.number_input('Height')\n",
        "G = st.number_input('G')\n",
        "ABCMeta = st.number_input('AB')\n",
        "\n",
        "# make a nice button that triggers creation of a new data-line in the format that the model expects and prediction\n",
        "if st.button('Predict! 🚀'):\n",
        "    # make a DF for categories and transform with one-hot-encoder\n",
        "    user_input = pd.DataFrame({'weight':weight,'height':height, 'G':G, 'AB':AB}, index=[0])\n",
        "\n",
        "    #run prediction for 1 new observation\n",
        "    predicted_value = model.predict(user_input)[0]\n",
        "\n",
        "    #print out result to user\n",
        "    st.metric(label=\"Predicted HR\", value=f'{round(predicted_value)} kr')"
      ]
    }
  ]
}