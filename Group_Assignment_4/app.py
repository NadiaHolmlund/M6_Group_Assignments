import streamlit as st
import pickle

# Setting up page configurations
st.set_page_config(
    page_title="HR Prediction",
    page_icon="⚾",
    layout="wide")

# Loading the model
@st.experimental_singleton
def read_objects():
    #model = pickle.load(open('HR_model/model.pkl','rb'))

    return model

model = read_objects()

def predict():
    data = [[weight, height, G, AB]]
    prediction = model.predict(data)[0]

# Setting up the page
weight = st.number_input('Weight')
height = st.number_input('Height')
G = st.number_input('G')
ABCMeta = st.number_input('AB')

# make a nice button that triggers creation of a new data-line in the format that the model expects and prediction
if st.button('Predict! 🚀'):
    # make a DF for categories and transform with one-hot-encoder
    user_input = pd.DataFrame({'weight':weight,'height':height, 'G':G, 'AB':AB}, index=[0])

    #run prediction for 1 new observation
    predicted_value = model.predict(user_input)[0]

    #print out result to user
    st.metric(label="Predicted HR", value=f'{round(predicted_value)} kr')
