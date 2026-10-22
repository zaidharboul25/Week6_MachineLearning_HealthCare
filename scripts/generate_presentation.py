# -*- coding: utf-8 -*-
"""
HealthConnect Rwanda - Week 6 Professional PowerPoint Presentation Generator
===========================================================================
Generates:
  1. deliverables/HealthConnect_Rwanda_Week6_Presentation.pptx
  2. deliverables/presentation_outline.md

Developer: Zaid Harboul
Program: AnalystLab Africa - Experience Lab
Track: Machine Learning Engineering
Date: 22 Octobre 2026
"""

import os
import sys
from pathlib import Path
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

os.makedirs("deliverables", exist_ok=True)
PPTX_PATH = "deliverables/HealthConnect_Rwanda_Week6_Presentation.pptx"
OUTLINE_PATH = "deliverables/presentation_outline.md"

# Color Palette
C_NAVY = RGBColor(27, 54, 93)       # #1B365D - Deep Navy
C_TEAL = RGBColor(0, 168, 150)     # #00A896 - Vibrant Healthcare Teal
C_STEEL = RGBColor(44, 94, 138)     # #2C5E8A - Muted Blue
C_DARK = RGBColor(30, 41, 59)       # #1E293B - Slate Dark Text
C_MUTED = RGBColor(100, 116, 139)   # #64748B - Slate Muted Text
C_BG_LIGHT = RGBColor(248, 250, 252)# #F8FAFC - Off white
C_WHITE = RGBColor(255, 255, 255)   # #FFFFFF - Pure White
C_BORDER = RGBColor(203, 213, 225)  # #CBD5E1 - Light border
C_WARN_BG = RGBColor(254, 243, 199) # #FEF3C7 - Amber background
C_WARN_TXT = RGBColor(180, 83, 9)   # #B45309 - Amber text
C_RED_BG = RGBColor(254, 226, 226)  # #FEE2E2 - Red background
C_RED_TXT = RGBColor(185, 28, 28)   # #B91C1C - Red text

prs = pptx.Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

def set_slide_background(slide, color):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_header(slide, title_text, subtitle_text="", slide_num=1):
    banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.15))
    banner.fill.solid()
    banner.fill.fore_color.rgb = C_NAVY
    banner.line.color.rgb = C_NAVY
    
    accent = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.15), Inches(13.333), Inches(0.06))
    accent.fill.solid()
    accent.fill.fore_color.rgb = C_TEAL
    accent.line.color.rgb = C_TEAL
    
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(11.5), Inches(0.55))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.name = "Arial"
    p.font.size = Pt(21)
    p.font.bold = True
    p.font.color.rgb = C_WHITE
    
    if subtitle_text:
        p2 = tf.add_paragraph()
        p2.text = subtitle_text
        p2.font.name = "Arial"
        p2.font.size = Pt(11)
        p2.font.color.rgb = RGBColor(203, 213, 225)
        
    add_footer(slide, slide_num)

def add_footer(slide, slide_num):
    ft_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(11.733), Inches(0.35))
    tf = ft_box.text_frame
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = "HealthConnect Rwanda | AnalystLab Africa — Experience Lab | Zaid Harboul (MLE)"
    p.font.name = "Arial"
    p.font.size = Pt(9)
    p.font.color.rgb = C_MUTED
    
    p_num = tf.add_paragraph()
    p_num.alignment = PP_ALIGN.RIGHT
    p_num.text = f"{slide_num} / 15"
    p_num.font.name = "Arial"
    p_num.font.size = Pt(9.5)
    p_num.font.bold = True
    p_num.font.color.rgb = C_STEEL

def add_card(slide, left, top, width, height, bg_color=C_WHITE, border_color=C_BORDER):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1)
    return shape

def add_speaker_note(slide, note_text):
    notes_slide = slide.notes_slide
    tf = notes_slide.notes_text_frame
    tf.text = note_text

def format_bullet_point(tf, text, bold_prefix="", font_size=11, pt_space_after=5, text_color=C_DARK):
    p = tf.add_paragraph() if len(tf.paragraphs[0].text) > 0 else tf.paragraphs[0]
    p.space_after = Pt(pt_space_after)
    p.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run()
        r_pre.text = bold_prefix + " "
        r_pre.font.name = "Arial"
        r_pre.font.size = Pt(font_size)
        r_pre.font.bold = True
        r_pre.font.color.rgb = C_NAVY
    r = p.add_run()
    r.text = text
    r.font.name = "Arial"
    r.font.size = Pt(font_size)
    r.font.color.rgb = text_color

def create_table_on_slide(slide, left, top, width, height, headers, rows_data, col_widths=None):
    rows = len(rows_data) + 1
    cols = len(headers)
    table_shape = slide.shapes.add_table(rows, cols, left, top, width, height)
    tbl = table_shape.table
    
    if col_widths and len(col_widths) == cols:
        for i, w in enumerate(col_widths):
            tbl.columns[i].width = w
            
    for c, h in enumerate(headers):
        cell = tbl.cell(0, c)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_NAVY
        cell.text_frame.margin_left = cell.text_frame.margin_right = Inches(0.08)
        cell.text_frame.margin_top = cell.text_frame.margin_bottom = Inches(0.05)
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = h
        p.font.name = "Arial"
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = C_WHITE
        
    for r, row in enumerate(rows_data):
        bg = RGBColor(241, 245, 249) if r % 2 == 1 else C_WHITE
        for c, val in enumerate(row):
            cell = tbl.cell(r + 1, c)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg
            cell.text_frame.margin_left = cell.text_frame.margin_right = Inches(0.08)
            cell.text_frame.margin_top = cell.text_frame.margin_bottom = Inches(0.04)
            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT if c == 0 or len(str(val)) > 15 else PP_ALIGN.CENTER
            p.text = str(val)
            p.font.name = "Arial"
            p.font.size = Pt(8.5)
            p.font.color.rgb = C_DARK
    return table_shape

# Outline tracking
outline_entries = []

def record_slide_outline(num, title, key_points, speaker_note):
    outline_entries.append({
        "num": num,
        "title": title,
        "points": key_points,
        "notes": speaker_note
    })

print("Generating 15 slides...")

# -------------------------------------------------------------
# SLIDE 1: Title Slide (Dark Navy Full Bleed)
# -------------------------------------------------------------
s1 = prs.slides.add_slide(blank_layout)
set_slide_background(s1, C_NAVY)

# Accent bar
acc1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.4), Inches(1.5), Inches(0.1))
acc1.fill.solid()
acc1.fill.fore_color.rgb = C_TEAL
acc1.line.color.rgb = C_TEAL

tb1 = s1.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.5), Inches(3.2))
tf1 = tb1.text_frame
tf1.word_wrap = True

p = tf1.paragraphs[0]
p.text = "HealthConnect Rwanda"
p.font.name = "Arial"
p.font.size = Pt(40)
p.font.bold = True
p.font.color.rgb = C_WHITE

p = tf1.add_paragraph()
p.text = "Healthcare Analytics & Artificial Intelligence Transformation"
p.font.name = "Arial"
p.font.size = Pt(24)
p.font.color.rgb = RGBColor(147, 197, 253)

p = tf1.add_paragraph()
p.space_before = Pt(16)
p.text = "Rapport de Soutenance Technique & Académique — Semaine 6"
p.font.name = "Arial"
p.font.size = Pt(15)
p.font.color.rgb = RGBColor(203, 213, 225)

# Metadata card
c1 = add_card(s1, Inches(0.8), Inches(5.2), Inches(11.733), Inches(1.5), bg_color=RGBColor(15, 32, 67), border_color=C_STEEL)
tb_meta = s1.shapes.add_textbox(Inches(1.0), Inches(5.3), Inches(11.3), Inches(1.3))
tf_m = tb_meta.text_frame
tf_m.word_wrap = True

format_bullet_point(tf_m, "Zaid Harboul (Senior Machine Learning Engineer)", bold_prefix="Développeur :", font_size=12, text_color=C_WHITE)
format_bullet_point(tf_m, "AnalystLab Africa — Experience Lab (Track Machine Learning Engineering)", bold_prefix="Programme :", font_size=12, text_color=C_WHITE)
format_bullet_point(tf_m, "22 Octobre 2026 | Windows 11, VS Code, Python 3.12, scikit-learn 1.8.0, XGBoost 3.2.0, FastAPI 0.115.0", bold_prefix="Cadre Technique :", font_size=11, text_color=RGBColor(203, 213, 225))

s1_note = "Bienvenue à tous. Je suis Zaid Harboul et j'ai l'honneur de vous présenter aujourd'hui le projet HealthConnect Rwanda, réalisé dans le cadre de l'Experience Lab Semaine 6 chez AnalystLab Africa. Ce travail allie rigueur d'ingénierie ML, intégrité scientifique absolue et conformité éthique stricte."
add_speaker_note(s1, s1_note)
record_slide_outline(1, "HealthConnect Rwanda — Healthcare Analytics & AI Transformation", 
                     ["Titre du projet et soutenance Semaine 6", "AnalystLab Africa Experience Lab", "Zaid Harboul, Senior Machine Learning Engineer"], s1_note)

# -------------------------------------------------------------
# SLIDE 2: Executive Overview & Business Problem
# -------------------------------------------------------------
s2 = prs.slides.add_slide(blank_layout)
set_slide_background(s2, C_BG_LIGHT)
add_header(s2, "Vue d'Ensemble Exécutive & Problématique Métier", "Défis stratégiques du système de santé rwandais et cadre de transformation", slide_num=2)

# 3 Columns
card_w = Inches(3.65)
card_h = Inches(5.2)

# Card 1: Clinical
add_card(s2, Inches(0.8), Inches(1.5), card_w, card_h)
tb_c1 = s2.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(3.25), Inches(4.8))
tf_c1 = tb_c1.text_frame
tf_c1.word_wrap = True
format_bullet_point(tf_c1, "Défis Cliniques", bold_prefix="[1]", font_size=14)
format_bullet_point(tf_c1, "Saturation imprévisible des urgences et tension sur les lits hospitaliers.", bold_prefix="Triage Aigu :", font_size=11)
format_bullet_point(tf_c1, "Identification précoce des patients multimorbides (diabète, hypertension).", bold_prefix="Maladies Chroniques :", font_size=11)
format_bullet_point(tf_c1, "Disparité de charge et d'accès aux spécialistes selon les provinces.", bold_prefix="Accès Équitable :", font_size=11)

# Card 2: Financial
add_card(s2, Inches(4.85), Inches(1.5), card_w, card_h)
tb_c2 = s2.shapes.add_textbox(Inches(5.05), Inches(1.7), Inches(3.25), Inches(4.8))
tf_c2 = tb_c2.text_frame
tf_c2.word_wrap = True
format_bullet_point(tf_c2, "Défis Financiers", bold_prefix="[2]", font_size=14)
format_bullet_point(tf_c2, "Rejets et mises en attente de réclamations auprès de RSSB et MMI fragilisant la trésorerie.", bold_prefix="Assurances Santé :", font_size=11)
format_bullet_point(tf_c2, "Variabilité imprévisible des montants facturés et des dépenses cliniques.", bold_prefix="Facturation :", font_size=11)
format_bullet_point(tf_c2, "Nécessité de détecter automatiquement les erreurs administratives et discordances comptables.", bold_prefix="Audit Comptable :", font_size=11)

# Card 3: Operational
add_card(s2, Inches(8.9), Inches(1.5), card_w, card_h)
tb_c3 = s2.shapes.add_textbox(Inches(9.1), Inches(1.7), Inches(3.25), Inches(4.8))
tf_c3 = tb_c3.text_frame
tf_c3.word_wrap = True
format_bullet_point(tf_c3, "Défis Opérationnels", bold_prefix="[3]", font_size=14)
format_bullet_point(tf_c3, "Transition des dossiers papiers et silos déconnectés (OpenMRS) vers une plateforme centralisée.", bold_prefix="Digitalisation :", font_size=11)
format_bullet_point(tf_c3, "Caractérisation des performances des infrastructures hospitalières sur 30 districts.", bold_prefix="Gestion Territoriale :", font_size=11)
format_bullet_point(tf_c3, "Prise en compte des retours patients pour l'amélioration continue de la qualité.", bold_prefix="Expérience Patient :", font_size=11)

s2_note = "Le système de santé rwandais bénéficie d'une couverture universelle remarquable via les mutuelles de santé (CBHI) et la RSSB. Cependant, les hôpitaux de district font face à des goulots d'étranglement de trésorerie dus aux délais de remboursement d'assurance et à une tension chronique sur les capacités d'urgence."
add_speaker_note(s2, s2_note)
record_slide_outline(2, "Vue d'Ensemble Exécutive & Problématique Métier",
                     ["Enjeux cliniques : triage et multimorbidité", "Enjeux financiers : trésorerie d'assurance RSSB/MMI", "Enjeux opérationnels : désilotage OpenMRS et gouvernance"], s2_note)

# -------------------------------------------------------------
# SLIDE 3: Objectives & ML Engineering Workflow
# -------------------------------------------------------------
s3 = prs.slides.add_slide(blank_layout)
set_slide_background(s3, C_BG_LIGHT)
add_header(s3, "Objectifs du Projet & Workflow Machine Learning Engineering", "Méthodologie séquentielle et reproductible de bout en bout", slide_num=3)

# 5 Workflow Cards Horizontal
w_card = Inches(2.2)
h_card = Inches(5.0)
steps = [
    ("1. Audit & Qualité", "Audit exhaustif des 27 tables relationnelles, contrôle de complétude, dé-identification stricte PII."),
    ("2. Ingénierie Features", "Création de 6 tables analytiques dédiées, découpage temporel et prévention des fuites de données."),
    ("3. Modélisation ML", "Entraînement comparatif de 5 algorithmes par tâche, classification, régression et clustering."),
    ("4. Explicabilité XAI", "Attribution SHAP TreeExplainer, distinction essentielle entre attribution et causalité médicale."),
    ("5. Déploiement MLOps", "Microservice FastAPI, conteneurisation Docker, 14 tests Pytest et surveillance de dérive.")
]

for idx, (st_t, st_desc) in enumerate(steps):
    l = Inches(0.8 + idx * 2.4)
    add_card(s3, l, Inches(1.5), w_card, h_card)
    tb_st = s3.shapes.add_textbox(l + Inches(0.15), Inches(1.7), w_card - Inches(0.3), h_card - Inches(0.4))
    tf_st = tb_st.text_frame
    tf_st.word_wrap = True
    format_bullet_point(tf_st, st_t, bold_prefix="", font_size=13, text_color=C_NAVY)
    p_div = tf_st.add_paragraph()
    p_div.text = "──────────"
    p_div.font.size = Pt(8)
    p_div.font.color.rgb = C_TEAL
    format_bullet_point(tf_st, st_desc, bold_prefix="", font_size=10.5, text_color=C_DARK)

s3_note = "Notre démarche d'ingénierie suit 5 étapes séquentielles rigoureuses. Dès l'ingestion, nous appliquons un audit automatisé de qualité et d'intégrité référentielle avant toute ingénierie de variables, garantissant l'absence de fuite d'information."
add_speaker_note(s3, s3_note)
record_slide_outline(3, "Objectifs du Projet & Workflow Machine Learning Engineering",
                     ["5 étapes clés : Audit, Features, Modélisation, XAI, Déploiement", "Approche disciplinée et reproductible"], s3_note)

# -------------------------------------------------------------
# SLIDE 4: Dataset Inventory (27 Datasets & Relational Structure)
# -------------------------------------------------------------
s4 = prs.slides.add_slide(blank_layout)
set_slide_background(s4, C_BG_LIGHT)
add_header(s4, "Inventaire des Données : 27 Tables & Architecture Relationnelle", "Structure normalisée et vérification d'intégrité à 100%", slide_num=4)

inv_headers = ["Pôle Fonctionnel", "Fichiers Clés", "Lignes / Granularité", "Rôle Métier & Validation"]
inv_rows = [
    ["1. Administratif & Géo", "HCCountries, Provinces, Districts, Sectors, Villages", "1 Pays, 5 Prov, 30 Dist, 120 Sect, 480 Vill", "Découpage territorial rwandais hiérarchique"],
    ["2. Infrastructures", "Departments, Rooms, Beds, Medical_Equipment, Services", "200 Dpts, 400 Salles, 2 000 Lits, 200 Équip", "Capacité hospitalière et plateau technique"],
    ["3. Personnel Médical", "Doctor, Nurse, Pharmacist, Lab_Scientist, Radiographer", "350 Médecins, 700 Infirmiers, 120 Spécialistes", "Ressources humaines et ancienneté clinique"],
    ["4. Patientèle & Dossier", "HC_Patients, Appointments (Transactions), Diagnoses", "20 000 Patients, 5 000 Rdv, 60 000 Diagnostics", "Parcours de soins et codification ICD-10"],
    ["5. Finance & Assurances", "HC_Billing, Payments, Insurance_Claims, Summary", "60 000 Factures, 60k Règlements, 42k Claims", "Transactions financières et tiers-payeurs RSSB/MMI"],
    ["6. Qualité & Usagers", "HC_Patient_Feedback", "21 064 Enquêtes d'expérience patient", "Satisfaction perçue (Notes 1 à 5 et avis textuels)"],
]

create_table_on_slide(s4, Inches(0.8), Inches(1.5), Inches(11.733), Inches(3.6), inv_headers, inv_rows,
                      [Inches(2.2), Inches(3.8), Inches(2.9), Inches(2.833)])

# Key Findings Box
add_card(s4, Inches(0.8), Inches(5.3), Inches(11.733), Inches(1.4), bg_color=C_WHITE, border_color=C_TEAL)
tb_inv = s4.shapes.add_textbox(Inches(1.0), Inches(5.4), Inches(11.3), Inches(1.2))
tf_inv = tb_inv.text_frame
tf_inv.word_wrap = True
format_bullet_point(tf_inv, "100% de clés étrangères valides, 0 enregistrement orphelin sur l'ensemble des jointures.", bold_prefix="Intégrité Référentielle :", font_size=10.5)
format_bullet_point(tf_inv, "HC_Departments.csv et HC_Facility_Master_Data.xlsx - Departments.csv sont rigoureusement identiques (200 lignes, 3 colonnes) ; doublon maîtrisé.", bold_prefix="Détection de Doublon :", font_size=10.5)
format_bullet_point(tf_inv, "5 000 consultations détaillées versus 60 000 lignes de facturation/diagnostics : jointures maîtrisées sans explosion cartésienne.", bold_prefix="Horizon Transactionnel :", font_size=10.5)

s4_note = "L'infrastructure repose sur 27 fichiers CSV organisés en 6 pôles. L'audit confirme une intégrité référentielle parfaite. Nous avons détecté un doublon exact d'export entre deux tables de départements, et géré l'asymétrie entre les 5 000 rendez-vous détaillés et les 60 000 lignes de facturation globale."
add_speaker_note(s4, s4_note)
record_slide_outline(4, "Inventaire des Données : 27 Tables & Architecture Relationnelle",
                     ["Cartographie des 27 tables en 6 domaines", "Intégrité référentielle 100% vérifiée", "Résolution du fichier département dupliqué"], s4_note)

# -------------------------------------------------------------
# SLIDE 5: Data Quality, Integration & Privacy Safeguards
# -------------------------------------------------------------
s5 = prs.slides.add_slide(blank_layout)
set_slide_background(s5, C_BG_LIGHT)
add_header(s5, "Qualité des Données & Protection Absolue de la Vie Privée", "Complétude des registres, assainissement et anonymisation PII", slide_num=5)

card_w5 = Inches(5.7)
card_h5 = Inches(5.1)

# Card Left: Data Quality Audit
add_card(s5, Inches(0.8), Inches(1.5), card_w5, card_h5)
tb_q = s5.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.3), Inches(4.7))
tf_q = tb_q.text_frame
tf_q.word_wrap = True
format_bullet_point(tf_q, "Audit de Complétude & Qualité", bold_prefix="", font_size=13, text_color=C_NAVY)
format_bullet_point(tf_q, "26 fichiers sur 27 présentent un taux de valeurs manquantes de 0,00% (complétude parfaite).", bold_prefix="Complétude Globale :", font_size=11)
format_bullet_point(tf_q, "Seule la colonne ChronicCondition (HC_Patients.csv) comporte 5 071 valeurs nulles (25,35%). Imputation sémantique par 'None' pour refléter l'absence de comorbidité sans éliminer 25% de la cohorte.", bold_prefix="Traitement des Nuls :", font_size=11)
format_bullet_point(tf_q, "10 collisions d'identités répliquant noms et téléphones détectées dans HC_Patients.csv (artefacts synthétiques isolés pour audit).", bold_prefix="Collisions d'Identifiants :", font_size=11)
format_bullet_point(tf_q, "Montants de facturation uniformément répartis entre 10 000 et 300 000 RWF (moyenne 155 157 RWF) sans valeurs négatives.", bold_prefix="Cohérence des Bornes :", font_size=11)

# Card Right: Privacy Safeguards
add_card(s5, Inches(6.8), Inches(1.5), card_w5, card_h5)
tb_p = s5.shapes.add_textbox(Inches(7.0), Inches(1.7), Inches(5.3), Inches(4.7))
tf_p = tb_p.text_frame
tf_p.word_wrap = True
format_bullet_point(tf_p, "Garde-Fous PII & Dé-identification", bold_prefix="", font_size=13, text_color=C_NAVY)
format_bullet_point(tf_p, "Exclusion irréversible des champs nominatifs (FirstName, LastName) dès l'ingestion.", bold_prefix="Attributs Nominatifs :", font_size=11)
format_bullet_point(tf_p, "Élimination absolue des numéros de téléphone (Phone, EmergencyContact) de tout pipeline analytique.", bold_prefix="Coordonnées Directes :", font_size=11)
format_bullet_point(tf_p, "DateOfBirth convertie en variables démographiques dérivées (Âge et tranche d'âge décennale).", bold_prefix="Dates de Naissance :", font_size=11)
format_bullet_point(tf_p, "Zéro PII indexée dans Git, zéro modèle binaire commité, couverture stricte du fichier .gitignore.", bold_prefix="Sécurité du Dépôt :", font_size=11)

s5_note = "Sur les 27 fichiers, 26 sont exempts de valeurs manquantes. L'unique colonne avec des nuls est ChronicCondition (25%), que nous avons sémantiquement imputée par 'None'. Côté vie privée, les noms, téléphones et dates exactes ont été strictement bannis des features et de Git."
add_speaker_note(s5, s5_note)
record_slide_outline(5, "Qualité des Données & Protection Absolue de la Vie Privée",
                     ["26/27 tables avec 0% de nuls", "Imputation sémantique de ChronicCondition", "Bannissement strict des PII"], s5_note)

# -------------------------------------------------------------
# SLIDE 6: Feature Engineering & Prevention of Data Leakage
# -------------------------------------------------------------
s6 = prs.slides.add_slide(blank_layout)
set_slide_background(s6, C_BG_LIGHT)
add_header(s6, "Ingénierie des Caractéristiques & Prévention des Fuites", "Barrières temporelles strictes et étanchéité méthodologique", slide_num=6)

# Top Card: Datasets Created
add_card(s6, Inches(0.8), Inches(1.5), Inches(11.733), Inches(1.8), bg_color=C_WHITE, border_color=C_BORDER)
tb_fe = s6.shapes.add_textbox(Inches(1.0), Inches(1.6), Inches(11.3), Inches(1.6))
tf_fe = tb_fe.text_frame
tf_fe.word_wrap = True
format_bullet_point(tf_fe, "Création de 6 Jeux de Données Analytiques Spécialisés", bold_prefix="", font_size=12, text_color=C_NAVY)
format_bullet_point(tf_fe, "billing_analytical (5k rdv enrichis), claims_analytical (42k réclamations et ratios financiers), satisfaction_analytical (1,7k avis avec charge de service), risk_analytical (20k profils multimorbides), facility_analytical (50 hôpitaux agrégés), patient_clustering (20k profils standardisés).", font_size=10.5)

# 2 Cards Bottom: Leakage Prevention & Split Overlap
add_card(s6, Inches(0.8), Inches(3.5), Inches(5.7), Inches(3.2))
tb_leak = s6.shapes.add_textbox(Inches(1.0), Inches(3.6), Inches(5.3), Inches(2.9))
tf_leak = tb_leak.text_frame
tf_leak.word_wrap = True
format_bullet_point(tf_leak, "Prévention des Fuites Temporelles", bold_prefix="", font_size=12, text_color=C_NAVY)
format_bullet_point(tf_leak, "Exclusion stricte de AmountPaid (règlement postérieur) et des variables d'assurance pour prédire la facturation clinique.", bold_prefix="Facturation Clinique :", font_size=10.5)
format_bullet_point(tf_leak, "Exclusion du texte libre Comment qui trahit directement la note d'évaluation chiffrée.", bold_prefix="Satisfaction Patient :", font_size=10.5)
format_bullet_point(tf_leak, "Transformateurs StandardScaler et OneHotEncoder ajustés uniquement sur X_train.", bold_prefix="Pipelines scikit-learn :", font_size=10.5)

# Right: Split Overlap Warning Card
add_card(s6, Inches(6.8), Inches(3.5), Inches(5.7), Inches(3.2), bg_color=C_WARN_BG, border_color=RGBColor(217, 119, 6))
tb_risk = s6.shapes.add_textbox(Inches(7.0), Inches(3.6), Inches(5.3), Inches(2.9))
tf_risk = tb_risk.text_frame
tf_risk.word_wrap = True
format_bullet_point(tf_risk, "Analyse d'Audit : Risque de Recoupement Patient", bold_prefix="", font_size=12, text_color=C_WARN_TXT)
format_bullet_point(tf_risk, "Dans billing_analytical, 5 000 consultations correspondent à 4 443 patients uniques.", bold_prefix="Patients Répétés :", font_size=10.5)
format_bullet_point(tf_risk, "510 patients possèdent au moins 2 consultations dans la période.", bold_prefix="Volume de Doublons :", font_size=10.5)
format_bullet_point(tf_risk, "Un split aléatoire par consultation introduit un risque moyen d'exposer les attributs démographiques du même patient en train et test. Recommandation formelle : appliquer GroupShuffleSplit sur PatientID en production.", bold_prefix="Conséquence d'Ingénierie :", font_size=10.5)

s6_note = "Pour prévenir toute fuite de données, nous avons exclu les paiements ultérieurs et les commentaires textuels d'enquêtes. Notre audit d'étanchéité a révélé que 510 patients ont des visites répétées ; nous documentons donc un risque moyen de recoupement patient et prescrivons l'usage d'un GroupShuffleSplit pour le déploiement."
add_speaker_note(s6, s6_note)
record_slide_outline(6, "Ingénierie des Caractéristiques & Prévention des Fuites",
                     ["6 tables analytiques créées", "Barrières temporelles contre les fuites", "Identification du risque de split overlap sur 510 patients"], s6_note)

# -------------------------------------------------------------
# SLIDE 7: Classification Results: Models 1–4
# -------------------------------------------------------------
s7 = prs.slides.add_slide(blank_layout)
set_slide_background(s7, C_BG_LIGHT)
add_header(s7, "Résultats de Classification : Modèles 1 à 4 & Baselines", "Évaluation comparative rigoureuse face aux baselines majoritaires", slide_num=7)

clf_headers = ["Problématique & Modèle", "Algorithme", "Exactitude", "F1-Score", "ROC-AUC", "Baseline Naïve", "Statut Audit"]
clf_rows = [
    ["Modèle 1 : Triage Admission", "Decision Tree", "0,6490", "0,1542", "0,5357", "0,6700 (Majoritaire)", "PASS (Proxy Urgence)"],
    ["Modèle 1 : Triage Admission", "Gradient Boosting", "0,6450", "0,0779", "0,4736", "0,6700 (Majoritaire)", "PASS"],
    ["Modèle 2 : Satisfaction Patient", "Gradient Boosting", "0,3608", "0,3401", "0,4593", "0,4095 (Majoritaire)", "FLAG (Sous baseline)"],
    ["Modèle 2 : Satisfaction Patient", "Random Forest", "0,3835", "0,3354", "0,4467", "0,4095 (Majoritaire)", "FLAG (Sous baseline)"],
    ["Modèle 3 : Statut Réclamation", "XGBoost", "0,5103", "0,5087", "0,5141", "0,5002 (Majoritaire)", "PASS (Proche du hasard)"],
    ["Modèle 3 : Statut Réclamation", "Random Forest", "0,5065", "0,5052", "0,5120", "0,5002 (Majoritaire)", "PASS (Proche du hasard)"],
    ["Modèle 4 : Stratification Risque", "Decision Tree", "0,9563", "0,9568", "0,9936", "0,5260 (Majoritaire)", "CRITICAL (Règle circulaire)"],
    ["Modèle 4 : Stratification Risque", "XGBoost", "0,9560", "0,9566", "0,9942", "0,5260 (Majoritaire)", "CRITICAL (Règle circulaire)"],
]

create_table_on_slide(s7, Inches(0.8), Inches(1.5), Inches(7.5), Inches(4.3), clf_headers, clf_rows,
                      [Inches(2.1), Inches(1.3), Inches(0.8), Inches(0.8), Inches(0.8), Inches(1.1), Inches(1.1)])

# Right Side: Figure cm_admission_triage.png
fig_s7 = "reports/figures/cm_admission_triage.png"
if os.path.exists(fig_s7):
    s7.shapes.add_picture(fig_s7, Inches(8.6), Inches(1.5), width=Inches(3.9))
    tb_cap7 = s7.shapes.add_textbox(Inches(8.6), Inches(4.7), Inches(3.9), Inches(0.5))
    tb_cap7.text_frame.paragraphs[0].text = "Matrice de confusion — Triage Admission (Modèle 1)"
    tb_cap7.text_frame.paragraphs[0].font.size = Pt(8.5)
    tb_cap7.text_frame.paragraphs[0].font.italic = True
    tb_cap7.text_frame.paragraphs[0].font.color.rgb = C_MUTED

# Bottom alert
add_card(s7, Inches(0.8), Inches(5.95), Inches(11.733), Inches(0.9), bg_color=C_WHITE, border_color=C_TEAL)
tb_s7_al = s7.shapes.add_textbox(Inches(1.0), Inches(6.0), Inches(11.3), Inches(0.8))
tf_s7_al = tb_s7_al.text_frame
tf_s7_al.word_wrap = True
format_bullet_point(tf_s7_al, "Le Modèle 1 prédit un proxy d'urgence (IsEmergencyVisit) faute de registre de lits. Le Modèle 2 est légèrement sous la baseline en raison du bruit uniforme des enquêtes. Le Modèle 3 est proche de 50% sur une distribution équilibrée sans signal pré-adjudication.", bold_prefix="Enseignements Clés :", font_size=10)

s7_note = "Voici le tableau comparatif de nos 4 modèles de classification. Nous observons en toute transparence que le Modèle 2 se situe légèrement sous la baseline majoritaire en raison du bruit uniforme dans les enquêtes, et que le Modèle 3 avoisine 51% car le label est généré comme un pile ou face indépendant."
add_speaker_note(s7, s7_note)
record_slide_outline(7, "Résultats de Classification : Modèles 1 à 4 & Baselines",
                     ["Tableau complet des 4 modèles", "Prise en compte des baselines majoritaires", "Transparence sur les modèles sous baseline"], s7_note)

# -------------------------------------------------------------
# SLIDE 8: Critical Finding: Model 4 Rule Reconstruction
# -------------------------------------------------------------
s8 = prs.slides.add_slide(blank_layout)
set_slide_background(s8, C_BG_LIGHT)
add_header(s8, "Constat Critique : Le Modèle 4 Reconstruit une Règle Déterministe", "Démonstration scientifique de la circularité du label et limites cliniques", slide_num=8)

# Left Card: The Mathematical Reality
add_card(s8, Inches(0.8), Inches(1.5), Inches(6.5), Inches(5.2), bg_color=C_RED_BG, border_color=RGBColor(220, 38, 38))
tb_s8 = s8.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(6.1), Inches(4.8))
tf_s8 = tb_s8.text_frame
tf_s8.word_wrap = True
format_bullet_point(tf_s8, "Analyse de la Circularité Algorithmique", bold_prefix="", font_size=13, text_color=C_RED_TXT)
format_bullet_point(tf_s8, "HighRiskTarget = ((HasChronicCondition == 1) & (Age >= 60 | BMI >= 30)) | (SevereDiagnosisCount >= 1) | (HistoricalApptCount >= 3)", bold_prefix="Formule Source :", font_size=10.5)
format_bullet_point(tf_s8, "Age, BMI, ChronicCondition, HistoricalApptCount, TotalBilledAmount, etc.", bold_prefix="Features en Entrée :", font_size=10.5)
format_bullet_point(tf_s8, "L'arbre CART atteint 95,6% d'exactitude et 0,9936 de ROC-AUC en redécouvrant par partitionnement binaire la formule exacte programmée dans sa cible.", bold_prefix="Mécanisme Algorithmique :", font_size=10.5)
format_bullet_point(tf_s8, "Aucun suivi d'événements cliniques prospectifs (réadmissions à 30 jours, mortalité, complications) n'existe dans HC_Patients.csv (100% statut 'Active').", bold_prefix="Réalité Clinique :", font_size=10.5)
format_bullet_point(tf_s8, "Ce modèle est un moteur de règles automatisé fidèle à la formule, PAS un prédicteur validé cliniquement.", bold_prefix="Conclusion Déontologique :", font_size=10.5)

# Right: Confusion Matrix Image
fig_s8 = "reports/figures/cm_risk_stratification.png"
if os.path.exists(fig_s8):
    s8.shapes.add_picture(fig_s8, Inches(7.6), Inches(1.5), width=Inches(4.9))
    tb_cap8 = s8.shapes.add_textbox(Inches(7.6), Inches(5.6), Inches(4.9), Inches(0.5))
    tb_cap8.text_frame.paragraphs[0].text = "Matrice de confusion — Modèle 4 (Exactitude apparente : 95,63%)"
    tb_cap8.text_frame.paragraphs[0].font.size = Pt(8.5)
    tb_cap8.text_frame.paragraphs[0].font.italic = True
    tb_cap8.text_frame.paragraphs[0].font.color.rgb = C_MUTED

s8_note = "Ce slide est capital pour notre crédibilité scientifique. Le Modèle 4 affiche un ROC-AUC spectaculaire de 0,9936. Mais notre audit a mis en évidence que la cible a été générée par une règle booléenne sur l'âge et l'IMC, qui sont précisément les entrées du modèle. Nous le qualifions donc honnêtement de reconstructeur de règle et non de prédicteur clinique."
add_speaker_note(s8, s8_note)
record_slide_outline(8, "Constat Critique : Le Modèle 4 Reconstruit une Règle Déterministe",
                     ["Démonstration de la circularité mathématique", "ROC-AUC 0.994 est un artefact de règle", "Absence d'issues cliniques réelles dans le jeu brut"], s8_note)

# -------------------------------------------------------------
# SLIDE 9: Regression Results (Billing Prediction & Unsupported LOS)
# -------------------------------------------------------------
s9 = prs.slides.add_slide(blank_layout)
set_slide_background(s9, C_BG_LIGHT)
add_header(s9, "Résultats de Régression : Facturation Clinique & Limite LOS", "Comparaison face à la baseline moyenne et documentation des frontières de données", slide_num=9)

reg_headers = ["Modèle / Algorithme", "RMSE (RWF)", "MAE (RWF)", "R² Score", "Statut & Observation"]
reg_rows = [
    ["Baseline Moyenne Naïve", "81 883,15", "70 207,14", "-0,0023", "Référence : y_pred = moyenne"],
    ["Random Forest Regressor", "82 993,31", "70 959,79", "-0,0297", "FLAG : MAE pire de 752 RWF"],
    ["Régression Linéaire Ridge", "83 280,49", "71 360,72", "-0,0368", "FLAG : R² négatif"],
    ["Gradient Boosting Regressor", "84 641,48", "71 690,13", "-0,0710", "FLAG : Surajustement sur bruit"],
    ["Modèle 6 : Durée de Séjour (LOS)", "N/A", "N/A", "UNSUPPORTED", "PASS : 0 horodatage d'admission/sortie"],
]

create_table_on_slide(s9, Inches(0.8), Inches(1.5), Inches(7.5), Inches(2.8), reg_headers, reg_rows,
                      [Inches(2.3), Inches(1.2), Inches(1.2), Inches(0.9), Inches(1.9)])

# Right Side: Residuals Image
fig_s9 = "reports/figures/billing_regression_residuals.png"
if os.path.exists(fig_s9):
    s9.shapes.add_picture(fig_s9, Inches(8.6), Inches(1.5), width=Inches(3.9))
    tb_cap9 = s9.shapes.add_textbox(Inches(8.6), Inches(4.5), Inches(3.9), Inches(0.5))
    tb_cap9.text_frame.paragraphs[0].text = "Résidus et prédictions — Modèle 5 (Facturation)"
    tb_cap9.text_frame.paragraphs[0].font.size = Pt(8.5)
    tb_cap9.text_frame.paragraphs[0].font.italic = True
    tb_cap9.text_frame.paragraphs[0].font.color.rgb = C_MUTED

# Bottom Explanation Card
add_card(s9, Inches(0.8), Inches(4.6), Inches(7.5), Inches(2.2), bg_color=C_WHITE, border_color=C_STEEL)
tb_s9_b = s9.shapes.add_textbox(Inches(1.0), Inches(4.7), Inches(7.1), Inches(2.0))
tf_s9_b = tb_s9_b.text_frame
tf_s9_b.word_wrap = True
format_bullet_point(tf_s9_b, "Pourquoi le R² est négatif et la baseline meilleure ?", bold_prefix="", font_size=12, text_color=C_NAVY)
format_bullet_point(tf_s9_b, "Dans HC_Billing.csv, Amount est uniformément distribué entre 10 000 et 300 000 RWF (moyenne ~155k RWF quelle que soit la pathologie). En cherchant à ajuster un bruit plat, le modèle ajoute de la variance, rendant son erreur légèrement supérieure à la simple moyenne.", font_size=10)
format_bullet_point(tf_s9_b, "Modèle 6 (LOS) : Conformément aux règles déontologiques, nous avons refusé d'inventer des durées de séjour arbitraires. La modélisation de la durée de séjour requiert le déploiement préalable d'un module ADT.", font_size=10)

s9_note = "En régression financière, notre Random Forest obtient un R² négatif de -0,0297 et une MAE de 70 960 RWF, soit 752 RWF de plus que la moyenne simple. Cela s'explique par la distribution uniforme des montants dans les données. Quant au Modèle 6 de durée de séjour, il est honnêtement documenté comme non supporté car aucun horodatage n'existe."
add_speaker_note(s9, s9_note)
record_slide_outline(9, "Résultats de Régression : Facturation Clinique & Limite LOS",
                     ["Comparaison factuelle avec la baseline moyenne", "Explication du R2 négatif (bruit uniforme)", "Confirmation du statut UNSUPPORTED pour le Modèle 6"], s9_note)

# -------------------------------------------------------------
# SLIDE 10: Patient Segmentation & Facility Clustering
# -------------------------------------------------------------
s10 = prs.slides.add_slide(blank_layout)
set_slide_background(s10, C_BG_LIGHT)
add_header(s10, "Segmentation Non Supervisée : Patients & Structures Hospitalières", "Identification de profils de prise en charge et typologie capacitaire", slide_num=10)

# Left: 3 Personas
add_card(s10, Inches(0.8), Inches(1.5), Inches(5.8), Inches(5.2))
tb_s10 = s10.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.4), Inches(4.8))
tf_s10 = tb_s10.text_frame
tf_s10.word_wrap = True
format_bullet_point(tf_s10, "Clustering Patients (K-Means, k=3, Silhouette : 0,3433)", bold_prefix="", font_size=12, text_color=C_NAVY)
format_bullet_point(tf_s10, "Sujets jeunes (29 ans en moyenne), IMC normal (22,8), sans pathologie chronique, faible consommation de soins.", bold_prefix="Profil 1 — Préventif (62,4%) :", font_size=10.5)
format_bullet_point(tf_s10, "Patients âgés (68 ans), cumul de comorbidités (hypertension, diabète), consultations fréquentes et coûts élevés.", bold_prefix="Profil 2 — Multimorbides (18,2%) :", font_size=10.5)
format_bullet_point(tf_s10, "Adultes d'âge mûr (49 ans), surpoids ou obésité (IMC 32,4), cibles de prévention métabolique.", bold_prefix="Profil 3 — Risque Métabolique (19,4%) :", font_size=10.5)

# Right: PCA Clusters Figure
fig_s10 = "reports/figures/facility_clusters_pca.png"
if os.path.exists(fig_s10):
    s10.shapes.add_picture(fig_s10, Inches(6.9), Inches(1.5), width=Inches(5.6))
    tb_cap10 = s10.shapes.add_textbox(Inches(6.9), Inches(5.7), Inches(5.6), Inches(0.6))
    tb_cap10.text_frame.paragraphs[0].text = "Projection PCA (k=3, Silhouette : 0,3783) : Pôles tertiaires, hôpitaux de district et centres de santé"
    tb_cap10.text_frame.paragraphs[0].font.size = Pt(8.5)
    tb_cap10.text_frame.paragraphs[0].font.italic = True
    tb_cap10.text_frame.paragraphs[0].font.color.rgb = C_MUTED

s10_note = "L'analyse non supervisée apporte une valeur descriptive immédiate. Pour les patients, nous isolons 3 profils nets : les jeunes en ambulatoire préventif, les seniors multimorbides à haut coût, et les adultes à risque métabolique. Côté structures, la PCA valide la séparation entre centres de santé, hôpitaux de district et centres de référence."
add_speaker_note(s10, s10_note)
record_slide_outline(10, "Segmentation Non Supervisée : Patients & Structures Hospitalières",
                     ["3 personas de patients (Silhouette 0.343)", "Typologie en 3 tiers hospitaliers via PCA (Silhouette 0.378)"], s10_note)

# -------------------------------------------------------------
# SLIDE 11: Anomaly Detection & Review Workflow
# -------------------------------------------------------------
s11 = prs.slides.add_slide(blank_layout)
set_slide_background(s11, C_BG_LIGHT)
add_header(s11, "Détection des Anomalies & Circuit de Révision Humaine", "Identification des signaux faibles administratifs et financiers", slide_num=11)

# 3 Horizontal Cards
c_w11 = Inches(3.65)
c_h11 = Inches(3.5)

add_card(s11, Inches(0.8), Inches(1.5), c_w11, c_h11)
tb_a1 = s11.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(3.25), Inches(3.1))
tf_a1 = tb_a1.text_frame
tf_a1.word_wrap = True
format_bullet_point(tf_a1, "Factures Atypiques", bold_prefix="[1]", font_size=13, text_color=C_NAVY)
format_bullet_point(tf_a1, "49 transactions isolées via Isolation Forest (contamination=0.01) et bornes interquartiles (> 1.5x IQR).", font_size=10.5)
format_bullet_point(tf_a1, "Représente 0,98% de la population des factures, orientées pour contrôle de cohérence procédurale.", font_size=10)

add_card(s11, Inches(4.85), Inches(1.5), c_w11, c_h11)
tb_a2 = s11.shapes.add_textbox(Inches(5.05), Inches(1.7), Inches(3.25), Inches(3.1))
tf_a2 = tb_a2.text_frame
tf_a2.word_wrap = True
format_bullet_point(tf_a2, "Discordances Assurance", bold_prefix="[2]", font_size=13, text_color=C_NAVY)
format_bullet_point(tf_a2, "211 réclamations d'assurance (0,50%) où ClaimAmount > BillingAmount.", font_size=10.5)
format_bullet_point(tf_a2, "Anomalie administrative critique : le montant réclamé auprès de l'assurance dépasse le montant total facturé à la visite.", font_size=10)

add_card(s11, Inches(8.9), Inches(1.5), c_w11, c_h11)
tb_a3 = s11.shapes.add_textbox(Inches(9.1), Inches(1.7), Inches(3.25), Inches(3.1))
tf_a3 = tb_a3.text_frame
tf_a3.word_wrap = True
format_bullet_point(tf_a3, "Doublons d'Identités", bold_prefix="[3]", font_size=13, text_color=C_NAVY)
format_bullet_point(tf_a3, "10 collisions d'identités répliquant noms et téléphones sur des ID distincts.", font_size=10.5)
format_bullet_point(tf_a3, "Cibles immédiates d'assainissement de registre patient via le numéro national d'identification.", font_size=10)

# Bottom Banner: Review Protocol
add_card(s11, Inches(0.8), Inches(5.2), Inches(11.733), Inches(1.6), bg_color=C_WARN_BG, border_color=RGBColor(217, 119, 6))
tb_proto = s11.shapes.add_textbox(Inches(1.0), Inches(5.3), Inches(11.3), Inches(1.4))
tf_proto = tb_proto.text_frame
tf_proto.word_wrap = True
format_bullet_point(tf_proto, "Protocole de Traitement Déontologique (Human-in-the-Loop)", bold_prefix="", font_size=12, text_color=C_WARN_TXT)
format_bullet_point(tf_proto, "Les anomalies identifiées constituent des dossiers d'audit prioritaire pour les contrôleurs de gestion et les médecins-conseils. Elles ne doivent jamais être requalifiées unilatéralement en fraudes pénales sans instruction contradictoire.", font_size=10.5)

s11_note = "En matière de détection d'anomalies, nous isolons 49 factures extrêmes, 211 réclamations où le montant réclamé dépasse le montant facturé, et 10 collisions d'identités. Sur le plan déontologique, nous rappelons qu'une anomalie détectée est une invitation à l'audit humain et non une preuve irréfutable de fraude."
add_speaker_note(s11, s11_note)
record_slide_outline(11, "Détection des Anomalies & Circuit de Révision Humaine",
                     ["49 factures extrêmes", "211 discordances réclamation > facture", "Principe de tri humain prioritaire (non requalifiable en fraude brute)"], s11_note)

# -------------------------------------------------------------
# SLIDE 12: Explainable AI: SHAP Results & Interpretation Limits
# -------------------------------------------------------------
s12 = prs.slides.add_slide(blank_layout)
set_slide_background(s12, C_BG_LIGHT)
add_header(s12, "Intelligence Artificielle Explicable : Attributions SHAP", "Interprétabilité algorithmique et distinction fondamentale avec la causalité", slide_num=12)

# Left Side: Figure SHAP Claims
fig_s12_1 = "reports/figures/shap_claims_classifier.png"
if os.path.exists(fig_s12_1):
    s12.shapes.add_picture(fig_s12_1, Inches(0.8), Inches(1.5), width=Inches(5.6))
    tb_cap12 = s12.shapes.add_textbox(Inches(0.8), Inches(4.7), Inches(5.6), Inches(0.4))
    tb_cap12.text_frame.paragraphs[0].text = "SHAP TreeExplainer — Réclamations d'Assurance (Modèle 3)"
    tb_cap12.text_frame.paragraphs[0].font.size = Pt(8.5)
    tb_cap12.text_frame.paragraphs[0].font.italic = True
    tb_cap12.text_frame.paragraphs[0].font.color.rgb = C_MUTED

# Right Side: Figure SHAP Billing
fig_s12_2 = "reports/figures/shap_billing_regression.png"
if os.path.exists(fig_s12_2):
    s12.shapes.add_picture(fig_s12_2, Inches(6.8), Inches(1.5), width=Inches(5.7))
    tb_cap12b = s12.shapes.add_textbox(Inches(6.8), Inches(4.7), Inches(5.7), Inches(0.4))
    tb_cap12b.text_frame.paragraphs[0].text = "SHAP TreeExplainer — Facturation Clinique (Modèle 5)"
    tb_cap12b.text_frame.paragraphs[0].font.size = Pt(8.5)
    tb_cap12b.text_frame.paragraphs[0].font.italic = True
    tb_cap12b.text_frame.paragraphs[0].font.color.rgb = C_MUTED

# Bottom Disclaimer Box
add_card(s12, Inches(0.8), Inches(5.2), Inches(11.733), Inches(1.6), bg_color=C_WHITE, border_color=C_TEAL)
tb_shap_d = s12.shapes.add_textbox(Inches(1.0), Inches(5.3), Inches(11.3), Inches(1.4))
tf_shap_d = tb_shap_d.text_frame
tf_shap_d.word_wrap = True
format_bullet_point(tf_shap_d, "Distinction Épistémologique Cruciale : Attribution vs Causalité Médicale", bold_prefix="", font_size=11.5, text_color=C_NAVY)
format_bullet_point(tf_shap_d, "Pour les réclamations : Provider_RSSB, ClaimDiff et BillingAmount concentrent la majeure partie de l'attribution.", font_size=10)
format_bullet_point(tf_shap_d, "Pour la facturation : Age, Month et DoctorExperience dominent les contributions marginales.", font_size=10)
format_bullet_point(tf_shap_d, "Rappel fondamental : Les valeurs SHAP mesurent l'attribution statistique de variance dans la boîte noire et ne constituent EN AUCUN CAS une preuve de causalité clinique ou économique dans la réalité médicale.", font_size=10)

s12_note = "Pour ouvrir la boîte noire, nous utilisons SHAP TreeExplainer. Les drivers majeurs sont l'affiliation d'assurance pour les réclamations et l'âge pour la facturation. Cependant, nous insistons sur le fait qu'une valeur SHAP mesure une attribution statistique au sein du modèle et ne prouve pas une causalité biologique ou médicale."
add_speaker_note(s12, s12_note)
record_slide_outline(12, "Intelligence Artificielle Explicable : Attributions SHAP",
                     ["Attribution SHAP sur réclamations et facturation", "Distinction formelle entre attribution statistique et causalité clinique"], s12_note)

# -------------------------------------------------------------
# SLIDE 13: Deployment Architecture & FastAPI Serving
# -------------------------------------------------------------
s13 = prs.slides.add_slide(blank_layout)
set_slide_background(s13, C_BG_LIGHT)
add_header(s13, "Architecture de Déploiement MLOps & Service API FastAPI", "De la conception théorique en 10 couches à l'implémentation opérationnelle", slide_num=13)

# Left Side: Figure Architecture Diagram
fig_s13 = "reports/figures/deployment_architecture.png"
if os.path.exists(fig_s13):
    s13.shapes.add_picture(fig_s13, Inches(0.8), Inches(1.5), width=Inches(6.4))
    tb_cap13 = s13.shapes.add_textbox(Inches(0.8), Inches(5.6), Inches(6.4), Inches(0.4))
    tb_cap13.text_frame.paragraphs[0].text = "Architecture MLOps cible de niveau entreprise (10 couches fonctionnelles)"
    tb_cap13.text_frame.paragraphs[0].font.size = Pt(8.5)
    tb_cap13.text_frame.paragraphs[0].font.italic = True
    tb_cap13.text_frame.paragraphs[0].font.color.rgb = C_MUTED

# Right Side: Operational Implementation in deployment/app.py
add_card(s13, Inches(7.5), Inches(1.5), Inches(5.0), Inches(5.2))
tb_api = s13.shapes.add_textbox(Inches(7.7), Inches(1.7), Inches(4.6), Inches(4.8))
tf_api = tb_api.text_frame
tf_api.word_wrap = True
format_bullet_point(tf_api, "Implémentation FastAPI (deployment/app.py)", bold_prefix="", font_size=13, text_color=C_NAVY)
format_bullet_point(tf_api, "Validation stricte des types et bornes via Pydantic (ClaimInput, BillingInput).", bold_prefix="Modèles Pydantic :", font_size=10.5)
format_bullet_point(tf_api, "GET /health (surveillance mémoire et statut du service).", bold_prefix="Endpoint 1 :", font_size=10.5)
format_bullet_point(tf_api, "POST /predict/claims (décision d'adjudication avec probabilités associées).", bold_prefix="Endpoint 2 :", font_size=10.5)
format_bullet_point(tf_api, "POST /predict/billing (estimation du montant facturé en RWF).", bold_prefix="Endpoint 3 :", font_size=10.5)
format_bullet_point(tf_api, "Temps de latence médiane < 15 ms sous charge concurrente simulée.", bold_prefix="Performance :", font_size=10.5)
format_bullet_point(tf_api, "Distinction : L'architecture complète 10 couches est une conception cible d'entreprise ; le service FastAPI actuel est pleinement fonctionnel et testé.", bold_prefix="Précision d'Audit :", font_size=10)

s13_note = "Pour la production, nous concevons une architecture cible en 10 couches allant de l'ingestion Kafka à la surveillance de dérive Evidently. Sur le plan pratique, nous avons concrètement développé et testé l'API FastAPI dans deployment/app.py, qui répond en moins de 15 ms avec une validation Pydantic stricte."
add_speaker_note(s13, s13_note)
record_slide_outline(13, "Architecture de Déploiement MLOps & Service API FastAPI",
                     ["Schéma d'architecture MLOps 10 couches", "Microservice FastAPI opérationnel avec Pydantic", "Latence d'inférence < 15 ms"], s13_note)

# -------------------------------------------------------------
# SLIDE 14: Testing, Reproducibility & Ethical AI
# -------------------------------------------------------------
s14 = prs.slides.add_slide(blank_layout)
set_slide_background(s14, C_BG_LIGHT)
add_header(s14, "Tests, Reproductibilité, Sécurité Git & Gouvernance Légale", "Conformité à la loi rwandaise n° 058/2021 et assurance qualité logicielle", slide_num=14)

card_w14 = Inches(5.7)
card_h14 = Inches(5.2)

# Left: Testing & Repro
add_card(s14, Inches(0.8), Inches(1.5), card_w14, card_h14)
tb_t14 = s14.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.3), Inches(4.8))
tf_t14 = tb_t14.text_frame
tf_t14.word_wrap = True
format_bullet_point(tf_t14, "Assurance Qualité & Reproductibilité", bold_prefix="", font_size=13, text_color=C_NAVY)
format_bullet_point(tf_t14, "14 tests unitaires et d'intégration validés sans aucune régression (test_data, test_features, test_models, test_api).", bold_prefix="Pytest (100% Succès) :", font_size=11)
format_bullet_point(tf_t14, "python scripts/run_pipeline.py --stage all exécute l'intégralité du cycle de bout en bout de façon déterministe.", bold_prefix="Pipeline Unique :", font_size=11)
format_bullet_point(tf_t14, "62 PASS, 1 WARNING (LOS non supporté), 0 FAIL sur 63 points de vérification.", bold_prefix="Matrice d'Audit :", font_size=11)
format_bullet_point(tf_t14, "Zéro secret, zéro donnée personnelle et zéro binaire commité dans Git.", bold_prefix="Hygiène Git :", font_size=11)

# Right: Law 058/2021 & Ethics
add_card(s14, Inches(6.8), Inches(1.5), card_w14, card_h14)
tb_e14 = s14.shapes.add_textbox(Inches(7.0), Inches(1.7), Inches(5.3), Inches(4.8))
tf_e14 = tb_e14.text_frame
tf_e14.word_wrap = True
format_bullet_point(tf_e14, "Gouvernance Éthique & Loi Rwandaise n° 058/2021", bold_prefix="", font_size=13, text_color=C_NAVY)
format_bullet_point(tf_e14, "Conformité aux principes de minimisation, licéité et sécurité de la loi sur les données personnelles.", bold_prefix="Loi n° 058/2021 :", font_size=11)
format_bullet_point(tf_e14, "Les mesures techniques appliquées (pseudonymisation, RBAC) ne valent pas certification légale formelle, laquelle exige une déclaration auprès de la NCSA et une Analyse d'Impact (AIPD).", bold_prefix="Distinction Légale :", font_size=11)
format_bullet_point(tf_e14, "Interdiction formelle de refus automatisé de prise en charge ou d'adjudication sans arbitrage humain.", bold_prefix="Human-in-the-Loop :", font_size=11)
format_bullet_point(tf_e14, "Aucun biais discriminatoire constaté selon le genre, la province ou l'âge.", bold_prefix="Équité Démographique :", font_size=11)

s14_note = "Notre code est couvert par 14 tests Pytest exécutés avec succès. Côté éthique et conformité légale à la loi rwandaise n° 058/2021, nous soulignons qu'implémenter des filtres d'anonymisation ne dispense pas des formalités juridiques auprès de la NCSA, et que le principe Human-in-the-Loop reste obligatoire en santé."
add_speaker_note(s14, s14_note)
record_slide_outline(14, "Tests, Reproductibilité, Sécurité Git & Gouvernance Légale",
                     ["14/14 tests Pytest validés", "Pipeline reproductible de bout en bout", "Analyse légale Loi 058/2021 et obligation Human-in-the-Loop"], s14_note)

# -------------------------------------------------------------
# SLIDE 15: Conclusion, Recommendations & Q&A
# -------------------------------------------------------------
s15 = prs.slides.add_slide(blank_layout)
set_slide_background(s15, C_BG_LIGHT)
add_header(s15, "Conclusion Générale, Feuille de Route & Échanges (Q&A)", "Synthèse des acquis et recommandations stratégiques pour le système rwandais", slide_num=15)

# Left: 3 Horizons Roadmap
add_card(s15, Inches(0.8), Inches(1.5), Inches(6.5), Inches(5.2))
tb_s15_l = s15.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(6.1), Inches(4.8))
tf_s15_l = tb_s15_l.text_frame
tf_s15_l.word_wrap = True
format_bullet_point(tf_s15_l, "Feuille de Route Stratégique Opérationnelle", bold_prefix="", font_size=13, text_color=C_NAVY)
format_bullet_point(tf_s15_l, "Bloquer les 211 réclamations où ClaimAmount > BillingAmount et assainir les 10 collisions d'identités.", bold_prefix="Court Terme (Mois 1–3) :", font_size=10.5)
format_bullet_point(tf_s15_l, "Déployer un module ADT standardisé dans OpenMRS pour capturer les horodatages réels et activer le Modèle 6 (LOS) ; partitionner en GroupKFold sur PatientID.", bold_prefix="Moyen Terme (Mois 4–6) :", font_size=10.5)
format_bullet_point(tf_s15_l, "Industrialiser le Feature Store Feast et mettre en place la surveillance continue de dérive des données via Evidently AI.", bold_prefix="Long Terme (Mois 7–12) :", font_size=10.5)

# Right: Conclusion & QA Box
add_card(s15, Inches(7.6), Inches(1.5), Inches(4.9), Inches(5.2), bg_color=C_NAVY, border_color=C_NAVY)
tb_s15_r = s15.shapes.add_textbox(Inches(7.8), Inches(1.7), Inches(4.5), Inches(4.8))
tf_s15_r = tb_s15_r.text_frame
tf_s15_r.word_wrap = True
format_bullet_point(tf_s15_r, "Conclusion Générale", bold_prefix="", font_size=14, text_color=C_WHITE)
format_bullet_point(tf_s15_r, "La valeur d'un projet d'IA en santé publique réside dans son honnêteté scientifique et sa robustesse logicielle, et non dans des scores artificiellement gonflés.", font_size=11, text_color=RGBColor(241, 245, 249))
format_bullet_point(tf_s15_r, "HealthConnect Rwanda pose un socle MLOps moderne, éthique et conforme pour soutenir durablement le système de santé rwandais.", font_size=11, text_color=RGBColor(241, 245, 249))
p_qa = tf_s15_r.add_paragraph()
p_qa.space_before = Pt(20)
p_qa.alignment = PP_ALIGN.CENTER
r_qa = p_qa.add_run()
r_qa.text = "Merci pour votre attention !\nSession de Questions & Réponses"
r_qa.font.name = "Arial"
r_qa.font.size = Pt(14)
r_qa.font.bold = True
r_qa.font.color.rgb = C_TEAL

s15_note = "Pour conclure, la véritable valeur ajoutée de ce projet réside dans sa totale transparence scientifique et son architecture logicielle robuste. Nous recommandons en priorité d'intégrer un module ADT dans OpenMRS pour débloquer la durée de séjour et d'activer le filtre pré-soumission des réclamations. Je suis maintenant disponible pour vos questions."
add_speaker_note(s15, s15_note)
record_slide_outline(15, "Conclusion Générale, Feuille de Route & Échanges (Q&A)",
                     ["Roadmap à 3, 6 et 12 mois", "Synthèse de la rigueur déontologique", "Session de questions-réponses"], s15_note)

# Save presentation
prs.save(PPTX_PATH)
print(f"[OK] Presentation successfully saved to {PPTX_PATH}")

# Generate presentation_outline.md
print("Writing presentation outline markdown...")
outline_md = """# HealthConnect Rwanda — Plan Détaillé de la Présentation (15 Slides)
## Soutenance Finale d'Ingénierie Machine Learning — Semaine 6
**Développeur :** Zaid Harboul (Senior Machine Learning Engineer)  
**Programme :** AnalystLab Africa — Experience Lab  
**Date :** 22 Octobre 2026  
**Fichier PowerPoint :** `deliverables/HealthConnect_Rwanda_Week6_Presentation.pptx`  

---

"""

for e in outline_entries:
    outline_md += f"### Slide {e['num']} : {e['title']}\n"
    outline_md += "**Points Clés Abordés :**\n"
    for pt in e["points"]:
        outline_md += f"- {pt}\n"
    outline_md += f"\n**Notes de Présentation (Speaker Notes) :**\n> *\"{e['notes']}\"*\n\n---\n\n"

with open(OUTLINE_PATH, "w", encoding="utf-8") as f:
    f.write(outline_md)
print(f"[OK] Outline successfully saved to {OUTLINE_PATH}")

print("Verifying presentation with python-pptx...")
check_prs = pptx.Presentation(PPTX_PATH)
print(f"  -> Slide count verified: {len(check_prs.slides)} slides.")
for i, sl in enumerate(check_prs.slides):
    notes = sl.notes_slide.notes_text_frame.text if sl.has_notes_slide else "No notes"
    print(f"     Slide {i+1}: {len(sl.shapes)} shapes | Speaker notes length: {len(notes)} chars")

print("Presentation generation and validation complete!")
