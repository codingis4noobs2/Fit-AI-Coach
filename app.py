# Importing libraries
import google.generativeai as genai
import streamlit as st
import pandas as pd


# Gemini and Streamlit Configuration
genai.configure(api_key=st.secrets["api_key"])
st.set_page_config(page_icon="💪", page_title="AI Fitness Coach", layout='centered')

generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 8192,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

model = genai.GenerativeModel(
    model_name="gemini-pro",
    generation_config=generation_config,
    safety_settings=safety_settings
)

# Caching Data, so that we don't have to read the file everytime
@st.cache_data
def get_countries_name():
    countries = pd.read_csv("countries.csv")
    return countries.name

country_list = get_countries_name()
build_options = [
    "Thin", 
	"Average",
	"Broad or Muscular", 
    "Significantly Overweight"
]

flexibility_options = [
    "Very flexible", 
    "Pretty flexible", 
    "Not that good", 
    "I'm not sure"
]

diet_preferences = [
    "Vegan", 
    "Vegetarian", 
    "Jain", 
    "Swaminarayan", 
    "Non-Vegetarian"
]

water_intake_options = [
    "Less than 2 glasses", 
    "About 2 glasses", 
    "2 to 6 glasses", 
    "More than 5 glasses"
]

sleep_duration_options = [
    "Less than 5 hours", 
    "5-6 hours", 
    "7-8 hours", 
    "More than 8 hours"
]

preferred_workout_duration = [
    "10-15 minutes", 
    "15-25 minutes", 
    "25+ minutes", 
    "Don't know"
]

workout_frequency_options = [
    "Almost every day", 
    "Several times per week", 
    "Several times per month", 
    "Never"
]

work_schedule_options = [
    "9 to 5", 
    "Night shifts", 
    "My hours are flexible", 
    "Not working/retired"
]

daily_activity_choices = [
    "I spend most of the day sitting", 
    "I take active breaks", 
    "I'm on my feet all day long"
]

body_sensitivity_choices = [
    "Sensitive back", 
    "Sensitive knees", 
    "None"
]

dream_goal_options = [
    "Build muscle & strength", 
    "Lose weight", 
    "Improve mobility", 
    "Develop flexibility", 
    "Improve overall fitness"
]

st.header("AI Fitness Coach🤖")
st.write(
    "<h4>Let's start, fill up the information in order to help me clearly understand you and your goals<h4>", 
    unsafe_allow_html=True
)

age_input = st.number_input("What is your age?", value=18, min_value=16)
selected_country = st.selectbox("Select Your Country (to provide recommendations based on what's available there):", country_list)
col1, col2 = st.columns(2)
with col1:
    height_cm = st.number_input("What is your height (in centimeters)?", value=168, min_value=100)
with col2:
    weight_kg = st.number_input("What is your weight (in kilograms)?", value=60, min_value=20)
calculated_bmi = round(weight_kg / ((height_cm/100) ** 2))
selected_build = st.selectbox("How would you describe your physical build?", build_options)
selected_flexibility = st.selectbox("How flexible are you?", flexibility_options)
selected_diet = st.selectbox("What type of diet do you prefer?", diet_preferences)
selected_water_intake = st.selectbox("What's your daily water intake?", water_intake_options)
selected_sleep_duration = st.selectbox("How much sleep do you usually get?", sleep_duration_options)
selected_workout_time = st.selectbox("How long do you want your workouts to be?", preferred_workout_duration)
selected_workout_frequency = st.selectbox("How often do you work out?", workout_frequency_options)
selected_work_schedule = st.selectbox("What is your work schedule like?", work_schedule_options)
selected_daily_activity = st.selectbox("How would you describe your typical day?", daily_activity_choices)
selected_body_sensitivity = ", ".join(st.multiselect("Do you struggle with any of the following? (Mutiple Options can be selected)", body_sensitivity_choices))
if "None" in selected_body_sensitivity:
    selected_body_sensitivity = ["None"]
else:
    selected_body_sensitivity = [sensitivity for sensitivity in selected_body_sensitivity if sensitivity != "None"]
st.write(selected_body_sensitivity)
bad_habits_input = st.text_area("Having any bad habits? Write it down here:", placeholder="For e.g. Watching TV while eating, Smoking")
bad_habits_input = "Nothing" if bad_habits_input == "" else bad_habits_input
selected_fitness_goal = st.selectbox("What Is Your Main Goal?", dream_goal_options)

prompt = "You are Jake, an expert body trainer and dietician who has helped multiple hollywood & bollywoods to get in the shape they want. " +\
"A new user has joined your academy, your job is to guide the user with proper exercise plan and diet plan in order to achieve his idea shape. " +\
"I will provide you with the user information, you have to strictly output in a markdown table form. "+\
"User Information: "+\
f"Age: {age_input}, "+\
f"Country of residence: {selected_country}, "+\
f"Height: {height_cm/100} in meters, "+\
f"Weight: {weight_kg} in kilograms, "+\
f"BMI: {calculated_bmi}, "+\
f"Current physical build: {selected_build}, "+\
f"Current body flexibility: {selected_flexibility}, "+\
f"Preferred Diet: {selected_diet}, "+\
f"Daily water intake: {selected_water_intake}, "+\
f"Usual sleep duration: {selected_sleep_duration}, "+\
f"How long workouts: {selected_workout_time}, "+\
f"Workout frequency: {selected_workout_frequency}, "+\
f"User work schedule: {selected_work_schedule}, "+\
f"Usual daily activity of user: {selected_daily_activity}, "+\
f"Body Struggles: {selected_body_sensitivity}, "+\
f"Bad Habits: {bad_habits_input}, "+\
f"Dream physique: {selected_fitness_goal}. "+\
f"Carefully design a diet and exercise plan keeping this all information in mind. Recommend Items which can be easily locally in user's country. Do not give Diet and Exercise table togethor and Give some recommendations. Separate Diet Plan, Exercise Plan, Recommendations by --- at the end."

if st.button("Submit"):
    if selected_body_sensitivity == "":
        st.error("Please select atleast any one of option from Body Sensitivity in order to continue")
    else:
        response = model.generate_content(prompt)
        st.write(response.text)
