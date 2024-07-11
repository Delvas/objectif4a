#importation des modules
pip install streamlit-option-menu
from ast import Is
import datetime
from os import name
#from turtle import  color
import streamlit as st
from  streamlit_option_menu import option_menu 
from PIL import Image #pour lamanipulation des image
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt #pour la manpulaton des graphes
import seaborn as sns #pour la manpulaton des graphes
import plotly.express as px 
import plotly.figure_factory as ff
import altair as alt
from sklearn.preprocessing import StandardScaler
import pickle
from pathlib import Path
from tempfile import NamedTemporaryFile
import plotly.graph_objects as go 
import ManiPDF

##controle des warnings
import warnings
warnings.filterwarnings('ignore')
warnings.warn('do not show')


#configuration de la page
LOGO=Image.open("logoAI4.ico")
st.set_page_config(
    page_title="objectif4ai",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon=LOGO)


#sidebar
with st.sidebar:
    selected=option_menu(
        menu_title="OBJECTIF4AI",
    
       options= ["Home","Find_objectif","add_data","About"],
       icons=["house-gear","book","server","person-circle"],
       menu_icon="menu-button-wide-fill" ,
       default_index=0,
      styles={"icons":{"color":"black", "font-size":"25px"},
              "nav-link":{
                  "font-size":"25px",
                  "tex-align":"left",
                  "margin":"0px",
                  "--hover-color":"#33ffff",
              },
               "nav-link-selected":{"background-color":"#cc6633"} }
    ) 


#Accueil
if selected=="Home":
    st.title(f"Welcom to OBJECTIF4AI" )
    co=st.columns([1,2])
    with co[0]:
        logojpg=Image.open('logoAI4.png')
        st.image(logojpg,use_column_width=True)

    with co[1]:
        st.write(
        '''Je suis OBJECTIF4IA une IA (Intelligence Artificielle) conçue pour vous
        aider à trouver le bon objectif (vente) à assigner à un commercial. Je suis capable de vous aider 
        dans l'analyse et la rédaction de vos rapports.
        'Pour effectuer une simulation ➡ **Find_objectif**' 
        ''')
    

#Find_objcetif
if selected=="Find_objectif":
    st.title(f"Welcom to {selected}")
    st.subheader("Here we are going to find a object")
    col_find= st.columns((1,1,1),gap='medium')
#colone1: saisir les données	
    #première colonne saisir les données
    with col_find[0]:
        Exp = st.number_input(label="Expérience",min_value=0,max_value=10,step=1)
        Anc = st.number_input(label="Ancienneté",min_value=0,max_value=10,step=1)
        Ang = st.number_input(label="Anglais",min_value=0,max_value=100,step=1)
        
        
    
    ##affichage de l'objectif
    with col_find[1]:
        Esp = st.number_input(label=f"Espagnol",min_value=0,max_value=100,step=1)
        Fr = st.number_input(label="Français",min_value=0,max_value=100,step=1)
        Format =st.selectbox('Formation',('Certificat','Licence','Master'))
        st.write(" ",Format)
    #traitement des donnees
    index = ['Exp','Anc','Form','Fr','Ang','Esp']
    new_val=np.array([Exp,Anc,Format,Fr,Ang,Esp])
    news_val_affich=pd.Series(new_val,index=index)
    maping={'Certificat':0,'Licence':1,'Master':2}
    data_= pd.DataFrame(news_val_affich,index=index).T
    data_.replace({'Certificat':0,'Licence':1,'Master':2},inplace=True)

    with col_find[2]:
        #prediction
        try:
            with open('objectif4AI.pkl','rb') as f:
                model_rf=pickle.load(f)
        except:
            print(" le model n'a pa pu être chargé")
        #new_val.reshape(1,-1)
        pred=model_rf.predict(data_)
        
        st.write("Pour ce profil, l'objectif est:",data_)
        st.markdown(f" **l'objectif à atteindre est:**")
        st.subheader(f"{pred[0]} CFA &mdash;:tulip::cherry_blossom:") #:,
    
if selected=="add_data":
    st.title(f"Welcom to {selected}")
    st.subheader(f"Here you can add the data fort start the analyse")

    #charger un fichier 
    #st.file_uploader()
    uploaded_file = st.file_uploader("Choose a csv file",type=["txt","csv","xlsx"])

    if uploaded_file is not None:
        extension= Path(uploaded_file.name).suffix.split('.')[1]
        #find file extension
        if extension=='csv':
            data=pd.read_csv(uploaded_file,encoding='latin')
        
        if extension=='xlsx':
            data=pd.read_excel(uploaded_file)
        if extension=='txt':
            data=pd.read_table(uploaded_file,sep=',')
        data.dropna(inplace=True)
        data.drop_duplicates(inplace=True)

        @st.cache
        def convert_df():
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return data.to_csv().encode('utf-8')
        
        data_csv=convert_df()
        #bouton de chargement
        st.download_button(
        label="Download data processed as CSV",
        data=data_csv,
        file_name='data_transform.csv',
        mime='text/csv',
        help='We are gong to load the data that you had transfomred'
       )
        
        st.write("Stats:",data.describe())
        colones= st.columns([1,3])
        with colones[0]:
            data_columns=data.columns.to_list() + [None]
            #couleurs=data.columns
            taille= [col for col in data.columns if np.issubdtype( data[col].dtype, np.number)]+[None] # type: ignore
            model=['scatter','Bar','hstograme','Violin']
            type_graph=st.selectbox("Type_graphe",model)
            Axe1=st.selectbox("Varable 1",data_columns)
            Axe2=st.selectbox("Varable 2",data_columns)
            couleur=st.selectbox("couleurs",data_columns)
            size=st.selectbox("Taille",taille)
        #df=data.copy
        with colones[1]:
            #scatter plot
            if  type_graph=='scatter':
                st.subheader(f'{type_graph}:{Axe1} vs {Axe2}')
                fig = px.scatter(data_frame=data,x=Axe1,y=Axe2,color=couleur,size=size,title=f'{type_graph}: {Axe1} vs {Axe2}')
                st.plotly_chart(fig,use_container_width=True )

            #Bar
            if  type_graph=='Bar':
                st.subheader(f'{type_graph}:{Axe1} vs {Axe2}')
                fig = px.bar(data_frame=data,x=Axe1,y=Axe2,color=couleur, pattern_shape=size,title=f'{type_graph}: {Axe1} vs {Axe2}')
                st.plotly_chart(fig,use_container_width=True )

            #
            if  type_graph=='hstograme':
                st.subheader(f'{type_graph}:{Axe1} vs {Axe2}')
                fig = px.histogram(data_frame=data,x=Axe1,y=Axe2,color=couleur,animation_frame=size,title=f'{type_graph}: {Axe1} vs {Axe2}')
                st.plotly_chart(fig,use_container_width=True )

            if  type_graph=='Violin':
                st.subheader(f'{type_graph}:{Axe1} vs {Axe2}')
                fig = px.violin(data_frame=data,x=Axe1,y=Axe2,color=couleur,title=f'{type_graph}: {Axe1} vs {Axe2}')
                st.plotly_chart(fig,use_container_width=True )

    
    if uploaded_file : # is not None:
       if st.button("rapport:📝"):
            col_rapport=st.columns(3)
            with col_rapport[0]:
                nom=st.text_input("Nom",key="Name")
                st.write(f"Mr/Mme :{nom}")
            with col_rapport[1]:
                prenom=st.text_input("Prénoms",key="firstname")
                st.write(f"{prenom}")
            with col_rapport[2]:
                fonction=st.text_input("Fonction",key="fnction")
                st.write(f"{fonction}")        
            date=str(datetime.datetime.today())[:-7]
            user_input=st.text_area("rapport")
            text_info = {1: [(f'{nom}', (121, 105)),(f'{prenom}', (130, 130)),
            (f'{fonction}', (121, 150)),('Rapport: OBjectf4AI', (135, 205)),
            (f'{user_input}', (73, 240)),(date, (490, 770))]}
            
            if st.button("valdé_rapport"):
                ManiPDF.add_text_to_pdf(text_info=text_info)
        
    if uploaded_file :
        st.download_button(label="Télécharger le rapport",data="",file_name='data_transform.csv', mime='text/csv',
            help='Télécharger le rapport')
                    

#debut de l'analyse            

   
#About
if selected=="About":
    st.title(f"{selected} is where you can find information about me")
    col= st.columns((1.,2.),gap='medium')
    #colone1: Photo auteur
    with col[0]:
        st.markdown(' ### Photo ')
        image = Image.open('PROFIL.png')
        st.image(image=image,caption='photo',use_column_width=True)
    #affichage CV
    with col[1]:
        #st.markdown('### cv ')
        st.markdown(
        """ 
        #### I'm Mathematiques Prof and Data Scientist.
        #### I love use Mathematiques and A.I for solve problem. 
        - ##### we can follow  me on 🤙:
            -  Facebook: [Delvas Allou](<http://www.facebook.com/delvasAllou?mibextid=ZbWKwL>)
            -  Linkdln: [Delvas Allou](<http://www.linkedln.com/in/delvas-allou-502113255>)
            -  Whatsap: [+225 0779840766](<https://wa.me/message/RTMP3GLK4J1>)  
            -  mail:    [email](<fidelallou@gmail.com>)

        """     )
