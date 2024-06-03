import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pycountry
import plotly.figure_factory as ff
import numpy as np
from scipy.stats import norm
from scipy import stats
import random
import functions as ff
import main_analysis as main
import os

#######################################
# DATA LOADING
#######################################

st.set_page_config(layout='wide')

# Determine the base path
base_path = os.path.dirname(__file__)

# Loading data files
df = pd.read_csv(os.path.join(base_path, 'df2020.csv'))
df2018 = pd.read_csv(os.path.join(base_path, 'df2018.csv'))
full_data2018 = pd.read_csv(os.path.join(base_path, 'survey_results_sample_2018.csv'))
full_data2019 = pd.read_csv(os.path.join(base_path, 'survey_results_sample_2019.csv'))
full_df2020 = pd.read_csv(os.path.join(base_path, 'survey_results_sample_2020.csv'))
df2019 = pd.read_csv(os.path.join(base_path, 'df2019.csv'))

# Filter the 2020 dataframe
df2020 = df[df['SalaryUSD'] < 200000]

# Load CSS file
def local_css(file_name):
    css_path = os.path.join(base_path, file_name)
    with open(css_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

#######################################
# DATA PREPARATION FOR VISUALISATION
#######################################

# Dropping unnamed columns that might be present
df2018 = df2018.drop(df2018.columns[0], axis=1)
df2019 = df2019.drop(df2019.columns[0], axis=1)

# Renaming columns for consistency
full_data2018 = full_data2018.rename(columns={
    "Hobby": "Hobbyist",
    "RaceEthnicity": "Ethnicity",
    "YearsCoding": "YearsCode",
    "YearsCodingProf": "YearsCodePro",
    "JobSatisfaction": "JobSat",
    "FormalEducation": "EdLevel",
    "OperatingSystem": "OpSys"
})

# Data cleaning and transformation
df_ai = full_data2018[['AIDangerous', 'AIInteresting', 'AIResponsible', 'AIFuture']]
df2018['Gender'] = df2018['Gender'].replace({"Male": "Man", "Female": "Woman"})

full_data2018.rename(columns={'ConvertedSalary': 'SalaryUSD'}, inplace=True)

# Strip leading and trailing whitespace from all columns in df_ai
df_ai = df_ai.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

# Mapping for shorter versions
short_mapping = {
    'Algorithms making important decisions': 'Algorithms',
    'Artificial intelligence surpassing human intelligence ("the singularity")': 'AI Singularity',
    'Evolving definitions of "fairness" in algorithmic versus human decisions': 'Fairness Evolution',
    "Increasing automation of jobs": 'Automation',
    "The developers or the people creating the AI": 'Developers',
    "A governmental or other regulatory body": 'Government/Regulatory',
    "Prominent industry leaders": 'Industry Leaders',
    "Nobody": 'No Responsibility',
    "I'm excited about the possibilities more than worried about the dangers.": 'Excited about AI Future',
    "I'm worried about the dangers more than I'm excited about the possibilities.": 'Worried about AI Future',
    "I don't care about it, or I haven't thought about it.": 'Indifferent about AI Future'
}
df_ai.replace(short_mapping, inplace=True)

# Function to create value count plots for each column
def plot_value_counts(column_name):
    colors = ['skyblue', 'yellow']
    fig = px.bar(df_ai[column_name].value_counts().reset_index(), x='index', y=column_name, color_discrete_sequence=[random.choice(colors)])
    fig.update_layout(title=f'Value Counts for {column_name}', xaxis_title='Response', yaxis_title='Count')
    st.plotly_chart(fig)

#########################################################################

# Sidebar for year selection
year = st.sidebar.selectbox('Select Year', ['2018', '2019', '2020'])

if year == '2018':
    main.main_analysis(df2018)

    visual, analysis = st.columns((3, 1))
    with visual:
        st.title("Highest Paying Countries for Data Scientists")
        ff.heighest_paying(full_data2018)
    with analysis:
        highest_paying_ds_text = """
        <div class='analysis-container'>
            <div class='analysis-title'>Analysis: Data Scientist Market</div>
            <div class='analysis-text'>
                The top three countries with the highest mean annual salary of a data scientist are South Korea (253,315) in 2018, Ireland (275,851) in 2019, and the USA (118,863) in 2020. Apart from that, the mean salary of the rest of the countries is less than 200,000 per year. Japan provides the highest mean annual salary among Asian countries (118,969). Figures in Dollars $.
            </div>
        </div>
        """
        st.markdown(highest_paying_ds_text, unsafe_allow_html=True)

    with visual:
        st.title("Operating System")
        ff.plot_pie_plotly(full_data2018, 'OpSys')
    with analysis:
        operating_text = """
        <div class='analysis-container'>
            <div class='analysis-title'>Analysis: Operating Systems</div>
            <div class='analysis-text'>
                Windows is the dominating operating system used by people. OS and Linux are almost tied. The knowledge about the operating system can help developers decide to whom their audience is catered towards.
            </div>
        </div>
        """
        st.markdown(operating_text, unsafe_allow_html=True)

    with visual:
        st.title("Top IDEs")
        ff.plot_bar_plotly(full_data2018, "IDE", 10, 500, 800)
        ff.plot_pie_plotly(full_data2018, "IDE", 10, 550, 600)
    with analysis:
        top_ide_text = """
        <div class='analysis-container'>
            <div class='analysis-title'>Analysis: Top IDEs</div>
            <div class='analysis-text'>
                1.<b>Popular IDEs</b>: Visual Studio Code, Visual Studio, and Notepad++ are among the most widely used IDEs, with high user counts ranging from 25,870 to 26,280.
                \n2.<b>Text Editors</b>: Sublime Text, Vim, and IntelliJ are also popular choices, with user counts ranging from 19,477 to 21,810.
                \n3.<b>General-purpose Editors</b>: TextMate, Coda, and Light Table are also used, although they have lower user counts compared to other IDEs.
                \n4.<b>Emerging Trends</b>: IPython / Jupyter, Atom, and Emacs show significant adoption, indicating a growing interest in interactive computing environments, lightweight editors, and customizable text editors, respectively.
                \n5.<b>Industry Standard</b>: Xcode, primarily used for macOS and iOS development, maintains a substantial user base due to its integration with Apple's development ecosystem.
            </div>
        </div>
        """
        st.markdown(top_ide_text, unsafe_allow_html=True)

    ff.ai_graphs()

    ai_text = """
    <div class='analysis-container-extra'>
        <div class='analysis-title'>Analysis: AI Perception</div>
        <div class='analysis-text'>
            1.<b>AIDangerous</b>: The most commonly cited concern is "Algorithms making important decisions," followed closely by "Artificial intelligence surpassing human intelligence" and "Evolving definitions of fairness."
            "Increasing automation of jobs" is also a significant concern but appears to be less frequently mentioned compared to the other categories.
            \n2.<b>AIInteresting</b>: The most interesting aspect for respondents seems to be "Increasing automation of jobs," followed by "Algorithms making important decisions" and "Artificial intelligence surpassing human intelligence."
            "Evolving definitions of fairness" appears to be less intriguing to respondents compared to other categories.
            \n3.<b>AIResponsible</b>: The majority of respondents believe that responsibility lies with "The developers or the people creating the AI."
            Fewer respondents attribute responsibility to "A governmental or other regulatory body," "Prominent industry leaders," or "Nobody."
            \n4.<b>AIFuture</b>: A significant proportion of respondents express excitement about the future of AI, indicating that they are "Excited about the possibilities more than worried about the dangers."
            However, there is also a notable percentage of respondents who are "Worried about the dangers more than excited about the possibilities."
            A smaller portion of respondents either "Don't care about it" or "Haven't thought about it."
            \n5.Overall, these results suggest a complex and varied perspective on AI technology. While many see great potential in AI, there are also concerns about its implications, particularly regarding decision-making, automation of jobs, and the ethical considerations surrounding its development and regulation.
        </div>
    </div>
    """
    st.markdown(ai_text, unsafe_allow_html=True)

elif year == '2019':
    main.main_analysis(df2019)

    visual, analysis = st.columns((3, 1))
    with visual:
        st.title("Highest Paying Countries for Data Scientists")
        ff.heighest_paying_2019()
    with analysis:
        highest_paying_ds_text = """
        <div class='analysis-container'>
            <div class='analysis-title'>Analysis: Data Scientist Market</div>
            <div class='analysis-text'>
                The top three countries with the highest mean annual salary of a data scientist are South Korea (253,315) in 2018, Ireland (275,851) in 2019, and the USA (118,863) in 2020. Apart from that, the mean salary of the rest of the countries is less than 200,000 per year. Japan provides the highest mean annual salary among Asian countries (118,969). Figures in Dollars $.
            </div>
        </div>
        """
        st.markdown(highest_paying_ds_text, unsafe_allow_html=True)

else:
    main.main_analysis(df2020)

    visual, analysis = st.columns((3, 1))
    with visual:
        st.title("Highest Paying Countries for Data Scientists")
        ff.heighest_paying(df2020)
    with analysis:
        highest_paying_ds_text = """
        <div class='analysis-container'>
            <div class='analysis-title'>Analysis: Data Scientist Market</div>
            <div class='analysis-text'>
                The top three countries with the highest mean annual salary of a data scientist are South Korea (253,315) in 2018, Ireland (275,851) in 2019, and the USA (118,863) in 2020. Apart from that, the mean salary of the rest of the countries is less than 200,000 per year. Japan provides the highest mean annual salary among Asian countries (118,969). Figures in Dollars $.
            </div>
        </div>
        """
        st.markdown(highest_paying_ds_text, unsafe_allow_html=True)
