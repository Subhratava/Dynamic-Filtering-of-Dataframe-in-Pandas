import streamlit as st
from st_aggrid import AgGrid
from st_aggrid.shared import JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import pandas as pd
import plotly.express as px
import functools
chart = functools.partial(st.plotly_chart, use_container_width=True)
lst1 = []
col = []

def filter(cols,df):
    # add the key choices_len to the session_state
    if not "choices_len" in st.session_state:
        st.session_state["choices_len"] = 0
    
    # c_up contains the form
    # c_down contains the add and remove buttons
    c_up = st.sidebar.container()
    c_down = st.sidebar.container()

    with c_up:
        with st.form("myForm"):
            c1 = st.container() # c1 contains choices
            cf = st.container()
            c2 = st.container() # c2 contains submit button
            with c2:
                st.form_submit_button("Refresh")

    with c_down:
        col_l, _, col_r = st.columns((4,4,4))
        with col_l:
            if st.button("Add "):
                st.session_state["choices_len"] += 1

        with col_r:
            if st.button("Remove ") and st.session_state["choices_len"] > 1:
                st.session_state["choices_len"] -= 1
                st.session_state.pop(f'{st.session_state["choices_len"]}')

    options = {}
    for x in range(st.session_state["choices_len"]): # create many choices
        with c1:
            option = st.selectbox(f"Filter {x + 1}", cols,key=f"{x}")
            if option != None :
                f = st.selectbox(f'Value {x+1}',df[option].unique(),key = f"{99+x}")
                options[option] = f

    return options
    # reads values from the session_state using the key.
    # also doesn't return an option if the value is empty
    #st.selectbox("myOptions", options=[
        #st.session_state[f"{x}"] for x in range(st.session_state["choices_len"]) if not st.session_state[f"{x}"] == ''])

def main() -> None:
    global lst1
    global col
    
    st.header("Your template")
    st.subheader("Upload your xlsx, xls, csv file")
    uploaded_data = st.file_uploader(
        "Drag and Drop or Click to Upload", type=[".csv",'xls','xlsx'], accept_multiple_files=False
    )
    if uploaded_data is None:
        st.info("Please Upload data to proceed")
        #uploaded_data = open("example.csv", "r")
    else:
        st.success("Uploaded your file!")
        if '.csv' in uploaded_data.name:
            df = pd.read_csv(uploaded_data)
            col = list(df.columns)
        else:
            df = pd.read_excel(uploaded_data)
            col = list(df.columns)
            


    st.sidebar.subheader("Choose appropiate filters")
    if uploaded_data is not None:
        filters = filter(col,df)
        print(filters)
        #query = ' & '.join([f'`{k}`=={v}' for k, v in filters.items()])
        #print(query)
        df_filtered = df.loc[(df[list(filters)] == pd.Series(filters)).all(axis=1)]
        st.dataframe(df_filtered)

if __name__ == "__main__":
    st.set_page_config(
        "Your Label",
        "📊",
        initial_sidebar_state="expanded",
        layout="wide",
    )
    main()