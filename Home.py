# Imports
import streamlit as st
from streamlit_echarts import st_echarts
import pandas as pd

# Functions
def disable_protein(): 
    st.session_state['disable_protein'] = True
    
@st.cache_data
def get_hydration_graph(): 
    x_vals = [10, 11.5, 12, 13.3, 15]
    y_vals = [hydration(item) * 100 for item in x_vals]
    data = [list(item) for item in zip(x_vals, y_vals)]
    
    option = {
        'xAxis': {
            'type': 'value',
            'min': min(x_vals) - 1,
            'max': max(x_vals) + 1,
            'name': 'Protein Content [%]',
            
            'nameLocation': 'middle',
            'nameGap': 50
        },
        'yAxis': {
            'type': 'value',
            'min': round(min(y_vals) - 5),
            'max': round(max(y_vals) + 5),
            'name': 'Hydration [%]',
            'nameLocation': 'middle',
            'nameGap': 50
        },
        'series': [{
            'data': data,
            'type': 'line'
        }]
    }
    return option
    
# hydration = lambda p: 0.056 * p + 0.01
hydration = lambda p: ((.75 - .65) / (13.3 - 11.5)) * p + .65 - ((.75 - .65) / (13.3 - 11.5)) * 11.5

# Setup
st.session_state['protein'] = '11.5'
if 'disable_protein' not in st.session_state.keys():
    st.session_state['disable_protein'] = False

# App
st.title('Dough Hydration Calculator')

g_flour, g_starter = float(st.text_input('Grams of Flour', '750')), float(st.text_input('Grams of Starter (Assumed 100% Hydration)', '100'))
p_input, p_preset = st.columns(2)
protein = p_input.text_input('Protein Percentage', st.session_state['protein'], disabled=st.session_state['disable_protein'])
protein_preset = p_preset.selectbox('Presets', ['11.5 (Kirkland Signature AP)', '12 (Beksul Bread Flour)', '13.3 (King Arthur Bread Flour)'], index=None, on_change=disable_protein)
if protein_preset is not None:
    st.session_state['protein'] = protein_preset.split(' ')[0]
    
else: 
    if st.session_state['disable_protein'] == True: 
        st.session_state['disable_protein'] = False
        st.rerun()
        
    st.session_state['protein'] = protein
    
if st.button('Calculate Additional Water (g)'): 
    flour_hydration = hydration(float(st.session_state['protein']))
    st.write('You will need to add ', round(flour_hydration * (g_flour + g_starter) - g_starter),  ' g water, ending up with a dough hydrated at ', round(flour_hydration * 100, 1), ' %')
    
option = get_hydration_graph()
st_echarts(options=option, height='500px')
    