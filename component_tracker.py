import csv
import streamlit as st
import pandas as pd
from datetime import date
from datetime import datetime, timezone
from getpass import getuser
import pytz

from github import Github
from github import InputGitTreeElement


#Github url
url = 'https://github.com/luxlp/component_record/blob/main/h16_component_tracker.csv?raw=true'
t_url = 'https://github.com/luxlp/component_record/blob/main/in_door.csv?raw=true'
#date
def time_conversion():
    utc_now = pytz.utc.localize(datetime.utcnow())
    est = utc_now.astimezone(pytz.timezone('US/Eastern'))
    time_est = est.strftime('%m/%d/%y')
    return time_est
eastern_time_ = time_conversion()

#Page-Setup-----------------------------------------------------------------------------------------------------------
st.set_page_config(
    page_title='Component Tracker',
    page_icon=':computer:',
    layout='wide',
    initial_sidebar_state='auto'
)

#load the dataframe
def load_df():
    data = pd.read_csv(url)
    df = pd.DataFrame(data)
    return df.astype(str)
df_ = load_df()

#Main title of page
st.title('H16 Component Tracker :computer:')

#set columns
first_column, second_column = st.columns(2)

#Github Process
dataunlock = pd.read_csv(t_url, on_bad_lines='skip')
dfl = pd.DataFrame(dataunlock)

p_one = dfl.iloc[0,0]
p_two = dfl.iloc[1,0]
p_three = dfl.iloc[2,0]
unite = str(p_one + p_two + p_three)

df2_ = df_.to_csv(sep=',', index=False)

file_list = [df2_]
file_name = ['h16_component_tracker.csv']

commit_message = 'test python'

#github connection
user = 'luxlp'
password = unite
git = Github(user, password)

#connect to repo
repo = git.get_user('luxlp').get_repo('component_record')
#check file in repo
x = repo.get_contents('h16_component_tracker.csv')

#getbranches
x = repo.get_git_refs()
for y in x:
    print(y)

#ref
master_ref = repo.get_git_ref("heads/main")

def updategitfile(file_name, file_list, userid, pwd, Repo, commit_message = ''):
    if commit_message == '':
        commit_message = 'Data Updated - ' + eastern_time_
        
        git = Github(userid,pwd)
        repo = git.get_user().get_repo(Repo)
        master_ref = repo.get_git_ref('heads/main')
        master_sha = master_ref.object.sha
        base_tree = repo.get_git_tree(master_sha)
        element_list = list()
        for i in range(0, len(file_list)):
            element = InputGitTreeElement(file_name[i], '100644', 'blob', file_list[i])
            element_list.append(element)
        tree = repo.create_git_tree(element_list, base_tree)
        parent = repo.get_git_commit(master_sha)
        commit = repo.create_git_commit(commit_message, tree, [parent])
        master_ref.edit(commit.sha)
        print('Update complete')

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
                    df2_ = df_.to_csv(sep=',', index=False)
                    file_list = [df2_]
                    updategitfile(file_name, file_list, user, password, 'componenet_record', 'heads/main') 
                except:
                    pass
                finally:
                    df2_ = df_.to_csv(sep=',', index=False)
                    file_list = [df2_]
                    updategitfile(file_name, file_list, user, password, 'componenet_record', 'heads/main') 
                    
    
with second_column:
    st.write(df_.astype(str))
    def convert_df(df):
        return df.to_csv(index = False).encode('utf-8')
    
    csv = convert_df(df_)
    st.download_button(
        label = 'Download data as CSV',
        data = csv,
        file_name = f'{eastern_time_}_h16_component_tracker.csv',
        mime = 'text/csv'
    )
    

        
        
        
