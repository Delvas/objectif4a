import pandas as pd
import numpy as np
import re
import PyPDF2 as PDF

### créaton du modules

import fitz  # PyMuPDF
import datetime

def add_text_to_pdf(text_info):
    # Ouvrir le fichier PDF existant
    pdf_document = fitz.open("rapport_Vierge.pdf")

    # Parcourir chaque élément de text_info pour ajouter du texte aux emplacements spécifiés
    for page_number, texts in text_info.items():
        page = pdf_document [0] #[page_number - 1]  Les pages sont indexées à partir de 0
        for text, position in texts:
            # Ajouter le texte à la position spécifiée
            page.insert_text(position, text, fontsize=12,color=(0, 0, 0))

    # Enregistrer le PDF modifié
    pdf_document.save("rapport_by_objectif4ai.pdf")

