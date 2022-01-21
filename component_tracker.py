import csv
import streamlit as st
import pandas as pd
from datetime import date
from datetime import datetime, timezone
from getpass import getuser
import pytz

from github import Github
from github import InputGitTreeElement


#get computer user
computer_user = getuser()
#dir
data_dir = fr'C:\Users\luis.peguero\Desktop\Eng_\humboldt16_component_tracker_'
#csv_file
csv_file = f'{data_dir}./humboldt16_component_tracker.csv'
#date
today_ = date.today().strftime('%m/%d/%y')
def time_conversion():
    utc_now = pytz.utc.localize(datetime.utcnow())
    est = utc_now.astimezone(pytz.timezone('US/Eastern'))
    time_est = est.strftime('%m/%d/%y')
    return time_est
eastern_time_ = time_conversion()

#Page-Setup-----------------------------------------------------------------------------------------------------------
st.set_page_config(
    page_title='Humboldt16 Component Tracker',
    page_icon=':Jack-O-Lantern:',
    layout='wide',
    initial_sidebar_state='auto'
)

#load the dataframe
def load_df():
    data = pd.read_csv(csv_file, on_bad_lines='skip')
    df = pd.DataFrame(data)
    return df.astype(str)
df_ = load_df()

#Main title of page
st.title('Humboldt16 Component Tracker :computer:')

#set columns
first_column, second_column = st.columns(2)

#set first column
with first_column:
    user_id = st.text_input('User')
    #server_sn = st.empty()
    if user_id:
        with st.form('my_form', clear_on_submit = True):
            a = st.text_input('server SN')
            b = st.text_input('PDB SN')
            c = st.text_input('Motherboard SN')
            d = st.text_area('DIMMS SN')
            e = st.text_input('NFC Adapter Board Sn')
            f = st.text_input('Riser Card SN')
            g = st.text_input('Annapurna Card SN')
            h = st.text_input('NFC Reader SN')
            i = st.text_input('Network Card SN')
            j = st.text_area('SSD SN')
            #selectb = st.selectbox(
            #'Select Component',
            #('PDB','Motherboard','DIMMS','NFC Adapter Board','Riser Card','Annapurna Card','NFC Reader','Network Card','SSD')
        #)
            #st.text_input(selectb)
            dfin = {
                'date' : eastern_time_,
                'user_id' : user_id,
                'server' : a,
                'pdb' : b,
                'motherboard' : c,
                'dimms' : d,
                'nfc_adapter_board' : e,
                'riser_card' : f,
                'annapurna_card' : g,
                'nfc_reader' : h,
                'network_card' : i,
                'ssd' : j
            }
            submitted = st.form_submit_button('Submit')
            if submitted:
                try:
                    df_ = df_.append(dfin, ignore_index= True)
                    df_.to_csv(csv_file, index = False)
                except:
                    pass
                    
    
with second_column:
    st.write(df_)
    def convert_df(df):
        return df.to_csv(index = False).encode('utf-8')
    
    csv = convert_df(df_)
    st.download_button(
        label = 'Download data as CSV',
        data = csv,
        file_name = f'{today_}_humboldt16_component_tracker.csv',
        mime = 'text/csv'
    )