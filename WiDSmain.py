import streamlit as st
import pandas as pd
import numpy as np
from urllib.request import urlopen
import json
import plotly.graph_objects as go
import plotly.offline 
import plotly.figure_factory as ff
from PIL import Image
import random
import decimal
from operator import add, sub
import math
from pathlib import Path
import re 
from pandas.api.types import CategoricalDtype


#st.markdown('<style>body{background-color: Black;}</style>',unsafe_allow_html=True)

#data imports 
fulldata = pd.read_csv('StreamlitFullDataset.csv')
selectZipData = pd.read_csv('StreamlitZipCodeDataset.csv')


## Project Description

maps = st.container() 
zip_drilldown = st.container() 
 
## Section 2: EFF and Predicted Maps 
with maps: 

	st.title("A RIGHT TO KNOW")
	
	st.header("Based on data from 5266 Police Departments and all FIPS localities in the United States, we were able to determine the amount of digital force you are under!") 
	
	st.markdown ("The Digital Force Index (DFI) quantifies the amount of digital force police departments use against their citizens. With a __high__ DFI, you may see more than one highly invasive technologies, such as Face Recognition and Predictive Policting. If your community's DFI is __low__, the police departments in your community may be using police accountability technologies, such as Body-worn Cameras. With a __mid__ DFI, you are more likely to see more than one invasive technology alongside a police accountability technology.")		

	#st.markdown("Hover over the map to see the DFI for specific communities.")

	colorscale = ['rgb(255.0, 36.0, 36.0)', 'rgb(41.0, 220.0, 44.0)', 'rgb(255.0, 218.0, 36.0)']

	order_list = ['low', 'mid', 'high']

	fig = ff.create_choropleth(fips=fulldata['FIPS'], values=fulldata['cat_DF'], 
		colorscale=colorscale) #, order=order_list)

	layer2 = go.Figure(data=fig)
	st.plotly_chart(layer2, use_container_width=True)

## Section 3: Drill Down with Zip Code 

with zip_drilldown: 

	st.title("Find out what technologies are being used in your community!")
	#st.markdown("Brief outline of the project and goals")
	selectZipData['zip_code'] = selectZipData['zip_code'].astype(float)
	selectZipData['zip_code'] = selectZipData['zip_code'].astype(int)
	#selectZipData = selectZipData.sort_values(by=['zip_code'], ascending=True)
	selectZipData['zip_code'] = selectZipData['zip_code'].astype(str)
	selectZipData['zip_code'] = [str(item).zfill(5) for item in selectZipData['zip_code']]

	selectZipData['techlist'] = selectZipData['techlist'].astype(str)

	user_zip = st.selectbox("You may select or type in your zip code in the dropdown menu below:", selectZipData['zip_code'])

	user_zip = int(user_zip) 
	selectZipData['zip_code'] = selectZipData['zip_code'].astype(int)

	techlist = selectZipData[selectZipData['zip_code']==user_zip]['techlist'].values 
	techlist = np.array2string(techlist)
	techlist = techlist.replace('[', '').replace(']', '').replace("'", '').replace("'", '')

	rating = selectZipData[selectZipData['zip_code']==user_zip]['cat_DF'].values
	rating = np.array2string(rating)
	rating = rating.replace('[', '').replace(']', '').replace("'", '').replace("'", '')


	if rating == 'high':
		col1, col2 = st.columns([2, 5])
		image = Image.open('images/high-DFI.png')
		with col1:
			st.image(image, width=64)
		with col2:
			st.error("High Digital Force")
			#st.markdown('<h1 style="color: white;">High Digital Force</h1>', unsafe_allow_html=True)

		st.markdown('<h2 style="color: white;">Your Community has at least a 30% likelihood of having the following technologies:</h3>', unsafe_allow_html=True)
		string1 = "<h2 style='text-align: center; color: white;'>"
		string2 = "</h2> <br> <br>"
		string = string1 + techlist + string2
		st.markdown(string, unsafe_allow_html=True)

	elif rating == 'mid': 
		col1, col2 = st.columns([2, 5])
		image = Image.open('images/medium-DFI.png')
		with col1:
			st.image(image, width=64)
		with col2:
			st.warning("Medium Digital Force")
			#st.markdown('<h1 style="color: white;">Medium Digital Force</h1>', unsafe_allow_html=True)

		st.markdown('<h2 style="color: white;">Your Community has at least a 30% likelihood of having the following technologies:</h3>', unsafe_allow_html=True)
		string1 = "<h2 style='text-align: center; color: white;'>"
		string2 = "</h2> <br> <br>"
		string = string1 + techlist + string2
		st.markdown(string, unsafe_allow_html=True)

	elif rating == 'low': 
		col1, col2 = st.columns([2, 5])
		image = Image.open('images/low-DFI.png')
		with col1:
			st.image(image, width=64)
		with col2:
			st.success("Low Digital Force")
			#st.markdown('<h1 style="color: white;">Low Digital Force</h1>', unsafe_allow_html=True)

		st.markdown('<h2 style="color: white;">Your Community has at least a 30% likelihood of having the following technologies:</h3>', unsafe_allow_html=True)
		string1 = "<h2 style='text-align: center; color: white;'>"
		string2 = "</h2> <br> <br>"
		string = string1 + techlist + string2
		st.markdown(string, unsafe_allow_html=True)	    	


	st.markdown("For more information on these technologies and others, visit [Electronic Fountiers Foundation](https://atlasofsurveillance.org/glossary)." , unsafe_allow_html=True)

