import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
import warnings
warnings.filterwarnings('ignore')

# ==================== CONFIGURATION DE LA PAGE ====================
st.set_page_config(
    page_title="Dashboard Analyse Offres d'Emploi",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CSS PERSONNALISÉ AMÉLIORÉ ====================
st.markdown("""
<style>
    /* Thème principal */
    .main-header {
        font-size: 2.8rem;
        color: #1E3A8A;
        font-weight: bold;
        margin-bottom: 0.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 4px solid #3B82F6;
        animation: fadeIn 0.8s ease-out;
    }
    
    .sub-header {
        font-size: 2rem;
        color: #1E40AF;
        font-weight: bold;
        margin-top: 1.5rem;
        margin-bottom: 1.5rem;
        padding-left: 15px;
        border-left: 5px solid #10B981;
    }
    
    .section-header {
        font-size: 1.5rem;
        color: #374151;
        font-weight: 600;
        margin-top: 1.2rem;
        margin-bottom: 0.8rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #E5E7EB;
    }
    
    /* Cartes de métriques */
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 15px;
        padding: 1.8rem;
        border: 2px solid #E5E7EB;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        height: 100%;
        transition: all 0.3s ease;
        animation: slideUp 0.5s ease-out;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
        border-color: #3B82F6;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E3A8A;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 1rem;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    
    /* Indicateurs de tendance */
    .trend-indicator {
        font-size: 0.9rem;
        font-weight: 500;
        padding: 3px 8px;
        border-radius: 12px;
        display: inline-block;
        margin-left: 10px;
    }
    
    .trend-up {
        background-color: #D1FAE5;
        color: #065F46;
    }
    
    .trend-down {
        background-color: #FEE2E2;
        color: #991B1B;
    }
    
    /* ==================== ONGLETS AMÉLIORÉS ==================== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background-color: #F8FAFC;
        padding: 12px;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        border: 1px solid #E5E7EB;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 15px 25px;
        background-color: #FFFFFF;
        border: 2px solid #E5E7EB;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        color: #374151;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        border-color: #3B82F6;
        background-color: #EFF6FF;
        color: #1E40AF;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%);
        color: white !important;
        border-color: #3B82F6;
        box-shadow: 0 4px 6px rgba(59, 130, 246, 0.3);
    }
    
    .stTabs [data-baseweb="tab"] [data-testid="stMarkdownContainer"] p {
        font-size: 1rem;
        font-weight: 600;
        color: inherit;
    }
    
    /* Conteneurs de graphiques */
    .chart-container {
        background: white;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #E5E7EB;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
        animation: fadeIn 0.6s ease-out;
    }
    
    /* Cartes d'insights */
    .insight-card {
        background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%);
        border-radius: 12px;
        padding: 1.5rem;
        border-left: 5px solid #0EA5E9;
        margin-bottom: 1rem;
        box-shadow: 0 2px 6px rgba(14, 165, 233, 0.1);
    }
    
    .insight-title {
        font-weight: bold;
        color: #0369A1;
        margin-bottom: 0.5rem;
        font-size: 1.1rem;
    }
    
    .insight-text {
        color: #0C4A6E;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    
    /* Conteneur de carte amélioré */
    .map-container {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        border: 1px solid #E5E7EB;
        background: white;
        padding: 10px;
    }
    
    .map-controls {
        background: white;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        border: 1px solid #E5E7EB;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Sidebar améliorée */
    .sidebar-header {
        font-size: 1.3rem;
        color: #1E3A8A;
        font-weight: bold;
        margin-bottom: 1.2rem;
        padding-bottom: 0.8rem;
        border-bottom: 2px solid #E5E7EB;
    }
    
    /* Badges */
    .badge {
        display: inline-block;
        padding: 0.25em 0.6em;
        font-size: 75%;
        font-weight: 700;
        line-height: 1;
        text-align: center;
        white-space: nowrap;
        vertical-align: baseline;
        border-radius: 10px;
        margin: 0 2px;
    }
    
    .badge-primary {
        color: #fff;
        background-color: #3B82F6;
    }
    
    .badge-success {
        color: #fff;
        background-color: #10B981;
    }
    
    .badge-warning {
        color: #fff;
        background-color: #F59E0B;
    }
    
    /* Tableaux améliorés */
    .dataframe {
        width: 100%;
        border-collapse: collapse;
    }
    
    .dataframe th {
        background-color: #F3F4F6;
        color: #374151;
        font-weight: 600;
        padding: 12px;
        text-align: left;
        border-bottom: 2px solid #E5E7EB;
    }
    
    .dataframe td {
        padding: 10px 12px;
        border-bottom: 1px solid #E5E7EB;
    }
    
    .dataframe tr:hover {
        background-color: #F9FAFB;
    }
    
    /* Nouveaux styles pour fonctionnalités avancées */
    .feature-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        border: 2px solid #E5E7EB;
        transition: all 0.3s ease;
        height: 180px;
    }
    
    .feature-card:hover {
        border-color: #3B82F6;
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
    }
    
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 15px;
        color: #3B82F6;
    }
    
    .feature-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #1E40AF;
        margin-bottom: 10px;
    }
    
    .feature-desc {
        color: #6B7280;
        font-size: 0.9rem;
        line-height: 1.4;
    }
    
    /* Filtres améliorés */
    .filter-group {
        background: #F9FAFB;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        border: 1px solid #E5E7EB;
    }
    
    .filter-title {
        font-weight: 600;
        color: #374151;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ==================== FONCTIONS UTILITAIRES ====================
@st.cache_data
def load_data():
    """Charge les données depuis le fichier CSV"""
    try:
        # Essayez différents chemins de fichier
        file_paths = [
            '../data/processed/jobs_enriched.csv',
            'data/processed/jobs_enriched.csv',
            'jobs_enriched.csv',
            'dataset_final.csv',
            'offres_emploi.csv'
        ]
        
        df = None
        for file_path in file_paths:
            try:
                df = pd.read_csv(file_path)
                st.success(f"✅ Données chargées depuis : {file_path}")
                break
            except Exception as e:
                continue
        
        if df is None:
            # Créer un dataset de démonstration
            st.warning("⚠️ Aucun fichier de données trouvé. Utilisation des données de démonstration.")
            df = create_demo_data()
        
        # Conversion des types si nécessaire
        if 'scraped_at' in df.columns:
            df['scraped_at'] = pd.to_datetime(df['scraped_at'])
        
        return df
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement des données : {str(e)}")
        return create_demo_data()

def create_demo_data():
    """Crée des données de démonstration pour le dashboard"""
    np.random.seed(42)
    
    n_offers = 500
    
    # Régions et villes françaises principales
    villes_regions = [
        ('Paris', 'Île-de-France'), ('Lyon', 'Auvergne-Rhône-Alpes'),
        ('Marseille', 'Provence-Alpes-Côte d\'Azur'), ('Toulouse', 'Occitanie'),
        ('Bordeaux', 'Nouvelle-Aquitaine'), ('Lille', 'Hauts-de-France'),
        ('Nantes', 'Pays de la Loire'), ('Strasbourg', 'Grand Est'),
        ('Nice', 'Provence-Alpes-Côte d\'Azur'), ('Rennes', 'Bretagne'),
        ('Grenoble', 'Auvergne-Rhône-Alpes'), ('Montpellier', 'Occitanie'),
        ('Reims', 'Grand Est'), ('Saint-Étienne', 'Auvergne-Rhône-Alpes'),
        ('Le Havre', 'Normandie'), ('Toulon', 'Provence-Alpes-Côte d\'Azur'),
        ('Angers', 'Pays de la Loire'), ('Dijon', 'Bourgogne-Franche-Comté'),
        ('Brest', 'Bretagne'), ('Limoges', 'Nouvelle-Aquitaine')
    ]
    
    villes = [v[0] for v in villes_regions]
    regions = [v[1] for v in villes_regions]
    
    data = {
        'offre_id': range(1000, 1000 + n_offers),
        'titre': np.random.choice([
            'Data Analyst', 'Data Scientist', 'Développeur Python', 
            'Ingénieur Machine Learning', 'Analyste Business Intelligence',
            'Chef de Projet IT', 'DevOps Engineer', 'Full Stack Developer',
            'Product Manager', 'UX/UI Designer', 'Marketing Digital',
            'Commercial B2B', 'Responsable RH', 'Contrôleur de Gestion',
            'Ingénieur Logiciel', 'Architecte Cloud', 'Expert Cybersecurity',
            'Consultant SAP', 'Business Analyst', 'Chargé de Communication'
        ], n_offers),
        'entreprise': np.random.choice([
            'Google', 'Amazon', 'Microsoft', 'Apple', 'Meta',
            'TotalEnergies', 'BNP Paribas', 'Air France', 'EDF', 'Orange',
            'Capgemini', 'Accenture', 'Sopra Steria', 'Atos', 'Thales',
            'Sanofi', 'L\'Oréal', 'LVMH', 'Renault', 'Airbus'
        ], n_offers),
        'localisation': np.random.choice(villes, n_offers),
        'contrat': np.random.choice(['CDI', 'CDD', 'Stage', 'Alternance'], n_offers, p=[0.7, 0.2, 0.05, 0.05]),
        'domaine': np.random.choice([
            'Secteur informatique', 'Banque & Finance', 'Industrie Manufacturière',
            'Services aux Entreprises', 'Distribution & Commerce', 'Santé & Social',
            'Marketing & Communication', 'Ressources Humaines', 'Consulting',
            'Bâtiment & Construction', 'Transport & Logistique', 'Énergie',
            'Aéronautique', 'Automobile', 'Télécommunications'
        ], n_offers),
        'region': np.random.choice(regions, n_offers),
        'experience_requise': np.random.choice([0, 1, 2, 3, 5, 8, 10], n_offers),
        'salaire_impute': np.random.normal(3500, 1500, n_offers),
        'cluster_mots_cles': np.random.choice([1, 2, 3, 4, 5], n_offers),
        'salaire_categorie': np.random.choice([0, 1], n_offers, p=[0.6, 0.4]),
        'salaire_pred_categorie_nn': np.random.choice([0, 1], n_offers, p=[0.55, 0.45]),
        'salaire_proba_bas': np.random.uniform(0, 1, n_offers),
        'salaire_proba_haut': np.random.uniform(0, 1, n_offers),
    }
    
    df = pd.DataFrame(data)
    df['salaire_impute'] = df['salaire_impute'].clip(1500, 8000)
    df['salaire_proba_haut'] = df['salaire_proba_haut'] / (df['salaire_proba_bas'] + df['salaire_proba_haut'])
    df['scraped_at'] = pd.date_range(start='2024-01-01', periods=n_offers, freq='D')
    
    # Assigner les régions correspondant aux villes
    ville_to_region = dict(villes_regions)
    df['region'] = df['localisation'].map(ville_to_region)
    
    return df

# Coordonnées GPS des principales villes françaises
VILLE_COORDINATES = {
    'Paris': {'lat': 48.8566, 'lon': 2.3522},
    'Lyon': {'lat': 45.7640, 'lon': 4.8357},
    'Marseille': {'lat': 43.2965, 'lon': 5.3698},
    'Toulouse': {'lat': 43.6047, 'lon': 1.4442},
    'Bordeaux': {'lat': 44.8378, 'lon': -0.5792},
    'Lille': {'lat': 50.6292, 'lon': 3.0573},
    'Nantes': {'lat': 47.2184, 'lon': -1.5536},
    'Strasbourg': {'lat': 48.5734, 'lon': 7.7521},
    'Nice': {'lat': 43.7102, 'lon': 7.2620},
    'Rennes': {'lat': 48.1173, 'lon': -1.6778},
    'Grenoble': {'lat': 45.1885, 'lon': 5.7245},
    'Montpellier': {'lat': 43.6108, 'lon': 3.8767},
    'Reims': {'lat': 49.2583, 'lon': 4.0317},
    'Saint-Étienne': {'lat': 45.4397, 'lon': 4.3872},
    'Le Havre': {'lat': 49.4944, 'lon': 0.1079},
    'Toulon': {'lat': 43.1242, 'lon': 5.9281},
    'Angers': {'lat': 47.4784, 'lon': -0.5632},
    'Dijon': {'lat': 47.3220, 'lon': 5.0415},
    'Brest': {'lat': 48.3904, 'lon': -4.4861},
    'Limoges': {'lat': 45.8336, 'lon': 1.2611}
}

def prepare_map_data(df):
    """Prépare les données pour la carte de France"""
    df_map = df.copy()
    
    # Ajouter les coordonnées GPS
    df_map['lat'] = None
    df_map['lon'] = None
    
    # Assigner les coordonnées des villes connues
    for ville, coords in VILLE_COORDINATES.items():
        mask = df_map['localisation'] == ville
        df_map.loc[mask, 'lat'] = coords['lat']
        df_map.loc[mask, 'lon'] = coords['lon']
    
    # Pour les villes non mappées, utiliser des coordonnées aléatoires
    missing_mask = df_map['lat'].isna()
    if missing_mask.any():
        # Centre de la France
        center_lat = 46.603354
        center_lon = 1.888334
        
        np.random.seed(42)
        # Assigner des coordonnées uniques pour chaque ville manquante
        unique_villes = df_map.loc[missing_mask, 'localisation'].unique()
        for ville in unique_villes:
            ville_mask = df_map['localisation'] == ville
            # Ajouter un petit décalage pour chaque ville
            offset_lat = np.random.uniform(-0.8, 0.8)
            offset_lon = np.random.uniform(-0.8, 0.8)
            df_map.loc[ville_mask, 'lat'] = center_lat + offset_lat
            df_map.loc[ville_mask, 'lon'] = center_lon + offset_lon
    
    return df_map

def create_enhanced_map(filtered_map, map_type="scatter", color_by="domaine", size_by="salaire"):
    """Crée une carte améliorée avec différents types de visualisation"""
    
    if len(filtered_map) == 0:
        return None
    
    # Préparer les données pour la carte
    if size_by == "salaire" and 'salaire_impute' in filtered_map.columns:
        filtered_map['point_size'] = (filtered_map['salaire_impute'] / filtered_map['salaire_impute'].max()) * 25 + 5
    else:
        filtered_map['point_size'] = 10
    
    # Créer la carte selon le type choisi
    if map_type == "scatter":
        fig = px.scatter_mapbox(
            filtered_map,
            lat='lat',
            lon='lon',
            color=color_by if color_by in filtered_map.columns else None,
            size='point_size',
            hover_name='titre',
            hover_data={
                'entreprise': True,
                'domaine': True,
                'contrat': True,
                'salaire_impute': ':.0f' if 'salaire_impute' in filtered_map.columns else False,
                'localisation': True,
                'region': True,
                'experience_requise': True if 'experience_requise' in filtered_map.columns else False
            },
            size_max=20,
            zoom=5,
            center={"lat": 46.603354, "lon": 1.888334},
            height=600,
            color_discrete_sequence=px.colors.qualitative.Set3 if color_by in filtered_map.columns else None
        )
        
        fig.update_traces(
            marker=dict(
                opacity=0.8,
                sizemode='diameter'
            )
        )
    
    elif map_type == "density":
        # Carte de densité
        fig = px.density_mapbox(
            filtered_map,
            lat='lat',
            lon='lon',
            z='salaire_impute' if 'salaire_impute' in filtered_map.columns else None,
            radius=20,
            hover_name='localisation',
            hover_data={
                'nombre_offres': filtered_map.groupby('localisation').transform('count')['offre_id'] if 'offre_id' in filtered_map.columns else None,
                'salaire_moyen': filtered_map.groupby('localisation')['salaire_impute'].transform('mean') if 'salaire_impute' in filtered_map.columns else None
            },
            zoom=5,
            center={"lat": 46.603354, "lon": 1.888334},
            height=600,
            color_continuous_scale='Viridis'
        )
    
    else:  # cluster
        # Carte avec clustering
        fig = px.scatter_mapbox(
            filtered_map,
            lat='lat',
            lon='lon',
            color='cluster_mots_cles' if 'cluster_mots_cles' in filtered_map.columns else color_by,
            size='point_size',
            hover_name='titre',
            hover_data={
                'entreprise': True,
                'domaine': True,
                'cluster_mots_cles': True if 'cluster_mots_cles' in filtered_map.columns else False,
                'salaire_impute': ':.0f' if 'salaire_impute' in filtered_map.columns else False
            },
            size_max=20,
            zoom=5,
            center={"lat": 46.603354, "lon": 1.888334},
            height=600,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
    
    # Configuration commune
    fig.update_layout(
        mapbox_style="carto-positron",  # Style clair et lisible
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="rgba(255, 255, 255, 0.9)",
            font=dict(size=10),
            title="",
            bordercolor="#E5E7EB",
            borderwidth=1
        ),
        paper_bgcolor='white'
    )
    
    return fig

def create_comparison_chart(df, domain_1, domain_2):
    """Crée un graphique de comparaison entre deux domaines"""
    
    df_domain1 = df[df['domaine'] == domain_1]
    df_domain2 = df[df['domaine'] == domain_2]
    
    if len(df_domain1) == 0 or len(df_domain2) == 0:
        return None
    
    # Préparer les données pour la comparaison
    comparison_data = []
    
    for domaine, df_dom in [(domain_1, df_domain1), (domain_2, df_domain2)]:
        if len(df_dom) > 0:
            comparison_data.append({
                'Domaine': domaine,
                'Nombre offres': len(df_dom),
                'Salaire moyen': df_dom['salaire_impute'].mean() if 'salaire_impute' in df_dom.columns else 0,
                'Salaire médian': df_dom['salaire_impute'].median() if 'salaire_impute' in df_dom.columns else 0,
                '% Haut salaire': df_dom['salaire_pred_categorie_nn'].mean() * 100 if 'salaire_pred_categorie_nn' in df_dom.columns else 0,
                'Expérience moyenne': df_dom['experience_requise'].mean() if 'experience_requise' in df_dom.columns else 0
            })
    
    comparison_df = pd.DataFrame(comparison_data)
    
    # Créer un graphique en barres groupées
    fig = go.Figure()
    
    metrics = ['Salaire moyen', 'Salaire médian', '% Haut salaire', 'Expérience moyenne']
    colors = ['#3B82F6', '#10B981', '#8B5CF6', '#F59E0B']
    
    for i, metric in enumerate(metrics):
        if metric in comparison_df.columns:
            fig.add_trace(go.Bar(
                name=metric,
                x=comparison_df['Domaine'],
                y=comparison_df[metric],
                marker_color=colors[i % len(colors)],
                text=comparison_df[metric].apply(lambda x: f'{x:,.0f}€' if 'Salaire' in metric else f'{x:.1f}%' if '%' in metric else f'{x:.1f}'),
                textposition='outside'
            ))
    
    fig.update_layout(
        title=f"Comparaison : {domain_1} vs {domain_2}",
        barmode='group',
        height=400,
        plot_bgcolor='white',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

def show_home_page(df):
    """Affiche la page d'accueil"""
    st.markdown('<h1 class="main-header">Dashboard Analyse des Offres d\'Emploi</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                   border-radius: 15px; padding: 30px; color: white; margin-bottom: 20px;'>
            <h2 style='color: white; margin-bottom: 20px;'>Analyse du Marché de l'Emploi Français</h2>
            <p style='font-size: 1.1rem; margin-bottom: 10px;'>
            Ce dashboard interactif vous permet d'analyser en temps réel les tendances du marché de l'emploi 
            français grâce à des données enrichies et des modèles prédictifs avancés.
            </p>
            <div style='margin-top: 20px;'>
                <span class='badge badge-primary'>Cartographie Interactive</span>
                <span class='badge badge-success'>Analyse Prédictive</span>
                <span class='badge badge-warning'>Clustering Thématique</span>
                <span class='badge badge-warning'>Dashboard Dynamique</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Calcul des statistiques
        salaire_median = df['salaire_impute'].median() if 'salaire_impute' in df.columns else 0
        taux_haut = df['salaire_pred_categorie_nn'].mean() * 100 if 'salaire_pred_categorie_nn' in df.columns else 0
        clusters = df['cluster_mots_cles'].nunique() if 'cluster_mots_cles' in df.columns else 0
        
        stats_html = """
        <div style='background: white; border-radius: 15px; padding: 25px; 
                   border: 2px solid #E5E7EB; box-shadow: 0 4px 12px rgba(0,0,0,0.1);'>
            <h3 style='color: #1E3A8A; margin-bottom: 20px;'>Vue d'ensemble</h3>
            <div style='margin-top: 20px;'>
                <div style='display: flex; justify-content: space-between; margin-bottom: 15px; padding-bottom: 10px; border-bottom: 1px solid #E5E7EB;'>
                    <span style='color: #64748B;'>Offres analysées</span>
                    <strong style='color: #1E3A8A;'>{:,}</strong>
                </div>
                <div style='display: flex; justify-content: space-between; margin-bottom: 15px; padding-bottom: 10px; border-bottom: 1px solid #E5E7EB;'>
                    <span style='color: #64748B;'>Salaire médian</span>
                    <strong style='color: #10B981;'>{:,.0f}€</strong>
                </div>
                <div style='display: flex; justify-content: space-between; margin-bottom: 15px; padding-bottom: 10px; border-bottom: 1px solid #E5E7EB;'>
                    <span style='color: #64748B;'>Taux haut salaire</span>
                    <strong style='color: #F59E0B;'>{:.1f}%</strong>
                </div>
                <div style='display: flex; justify-content: space-between;'>
                    <span style='color: #64748B;'>Clusters identifiés</span>
                    <strong style='color: #8B5CF6;'>{}</strong>
                </div>
            </div>
        </div>
        """.format(len(df), salaire_median, taux_haut, clusters)
        st.markdown(stats_html, unsafe_allow_html=True)
    
    # Fonctionnalités principales
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<h3 style="color: #1E3A8A; margin-bottom: 20px;">Fonctionnalités Principales</h3>', unsafe_allow_html=True)
    
    feat_col1, feat_col2, feat_col3 = st.columns(3)
    
    features = [
        {
            "icon": "🗺️",
            "title": "Cartographie Avancée",
            "desc": "Visualisez la répartition géographique avec différents modes: points, densité, clustering.",
            "color": "#3B82F6"
        },
        {
            "icon": "📈",
            "title": "Analyse Prédictive",
            "desc": "Modèles ML pour prédire les salaires et identifier les tendances du marché.",
            "color": "#10B981"
        },
        {
            "icon": "🔍",
            "title": "Recherche Intelligente",
            "desc": "Recherche avancée par compétences, région, domaine et fourchette de salaire.",
            "color": "#8B5CF6"
        }
    ]
    
    for i, (col, feat) in enumerate(zip([feat_col1, feat_col2, feat_col3], features)):
        with col:
            st.markdown(f"""
            <div class='feature-card'>
                <div class='feature-icon'>{feat['icon']}</div>
                <div class='feature-title'>{feat['title']}</div>
                <div class='feature-desc'>{feat['desc']}</div>
            </div>
            """, unsafe_allow_html=True)

# ==================== APPLICATION PRINCIPALE ====================
def main():
    # Titre principal
    st.markdown('<h1 class="main-header">Dashboard Analyse des Offres d\'Emploi</h1>', unsafe_allow_html=True)
    st.markdown("### Analyse avancée des tendances du marché de l'emploi français")
    
    # Chargement des données
    with st.spinner('Chargement des données...'):
        df = load_data()
        df_map = prepare_map_data(df)
    
    # Sidebar - Filtres
    with st.sidebar:
        st.markdown('<div class="sidebar-header">FILTRES AVANCÉS</div>', unsafe_allow_html=True)
        
        # Filtre par région
        regions = ['Toutes'] + sorted(df['region'].dropna().unique().tolist())
        selected_region = st.selectbox("Région", regions, index=0)
        
        # Filtre par domaine
        domaines = ['Tous'] + sorted(df['domaine'].dropna().unique().tolist())
        selected_domaine = st.selectbox("Domaine", domaines, index=0)
        
        # Filtre par type de contrat
        contrats = ['Tous'] + sorted(df['contrat'].dropna().unique().tolist())
        selected_contrat = st.selectbox("Contrat", contrats, index=0)
        
        # Filtre par salaire
        if 'salaire_impute' in df.columns:
            min_salaire = float(df['salaire_impute'].min())
            max_salaire = float(df['salaire_impute'].max())
            salaire_range = st.slider(
                "Plage de salaire (€)",
                min_value=min_salaire,
                max_value=max_salaire,
                value=(min_salaire, max_salaire)
            )
        
        # Filtre par probabilité de haut salaire
        if 'salaire_proba_haut' in df.columns:
            proba_range = st.slider(
                "Probabilité haut salaire",
                min_value=0.0,
                max_value=1.0,
                value=(0.0, 1.0),
                step=0.05
            )
        
        # Filtre par expérience requise
        if 'experience_requise' in df.columns:
            exp_range = st.slider(
                "Années d'expérience",
                min_value=int(df['experience_requise'].min()),
                max_value=int(df['experience_requise'].max()),
                value=(int(df['experience_requise'].min()), int(df['experience_requise'].max()))
            )
        
        st.markdown("---")
        
        # Statistiques rapides dans la sidebar
        st.markdown("### Statistiques Globales")
        col_sb1, col_sb2 = st.columns(2)
        with col_sb1:
            st.metric("Total offres", f"{len(df):,}")
        with col_sb2:
            if 'salaire_impute' in df.columns:
                st.metric("Salaire moyen", f"{df['salaire_impute'].mean():,.0f}€")
        
        st.markdown("---")
        
        # Mode comparaison
        st.markdown("### Mode Comparaison")
        if st.button("Activer comparaison de domaines", use_container_width=True):
            st.session_state.comparison_mode = True
        
        if st.session_state.get('comparison_mode', False):
            domain_1 = st.selectbox("Domaine 1", domaines[1:], index=0)
            domain_2 = st.selectbox("Domaine 2", domaines[1:], index=min(1, len(domaines)-2))
            
            if st.button("Comparer", use_container_width=True):
                st.session_state.compare_domains = [domain_1, domain_2]
    
    # Application des filtres
    filtered_df = df.copy()
    filtered_map = df_map.copy()
    
    if selected_region != 'Toutes':
        filtered_df = filtered_df[filtered_df['region'] == selected_region]
        filtered_map = filtered_map[filtered_map['region'] == selected_region]
    
    if selected_domaine != 'Tous':
        filtered_df = filtered_df[filtered_df['domaine'] == selected_domaine]
        filtered_map = filtered_map[filtered_map['domaine'] == selected_domaine]
    
    if selected_contrat != 'Tous':
        filtered_df = filtered_df[filtered_df['contrat'] == selected_contrat]
        filtered_map = filtered_map[filtered_map['contrat'] == selected_contrat]
    
    if 'salaire_impute' in filtered_df.columns:
        filtered_df = filtered_df[
            (filtered_df['salaire_impute'] >= salaire_range[0]) & 
            (filtered_df['salaire_impute'] <= salaire_range[1])
        ]
        filtered_map = filtered_map[
            (filtered_map['salaire_impute'] >= salaire_range[0]) & 
            (filtered_map['salaire_impute'] <= salaire_range[1])
        ]
    
    if 'salaire_proba_haut' in filtered_df.columns:
        filtered_df = filtered_df[
            (filtered_df['salaire_proba_haut'] >= proba_range[0]) & 
            (filtered_df['salaire_proba_haut'] <= proba_range[1])
        ]
        filtered_map = filtered_map[
            (filtered_map['salaire_proba_haut'] >= proba_range[0]) & 
            (filtered_map['salaire_proba_haut'] <= proba_range[1])
        ]
    
    if 'experience_requise' in filtered_df.columns:
        filtered_df = filtered_df[
            (filtered_df['experience_requise'] >= exp_range[0]) & 
            (filtered_df['experience_requise'] <= exp_range[1])
        ]
    
    # Métriques principales
    st.markdown('<div class="section-header">METRIQUES CLES</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-value">{:,}</div>'.format(len(filtered_df)), unsafe_allow_html=True)
        st.markdown('<div class="metric-label">TOTAL OFFRES</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        if 'salaire_pred_categorie_nn' in filtered_df.columns:
            taux_haut_salaire = filtered_df['salaire_pred_categorie_nn'].mean() * 100
        else:
            taux_haut_salaire = 0
        
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-value">{:.1f}%</div>'.format(taux_haut_salaire), unsafe_allow_html=True)
        st.markdown('<div class="metric-label">HAUTS SALAIRES</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        if 'salaire_impute' in filtered_df.columns:
            salaire_moyen = filtered_df['salaire_impute'].mean()
        else:
            salaire_moyen = 0
        
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-value">{:,.0f}€</div>'.format(salaire_moyen), unsafe_allow_html=True)
        st.markdown('<div class="metric-label">SALAIRE MOYEN</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        if 'cluster_mots_cles' in filtered_df.columns:
            clusters_uniques = filtered_df['cluster_mots_cles'].nunique()
        else:
            clusters_uniques = 0
        
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-value">{}</div>'.format(clusters_uniques), unsafe_allow_html=True)
        st.markdown('<div class="metric-label">CLUSTERS UNIQUES</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ==================== ONGLETS AMÉLIORÉS ====================
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "ACCUEIL", 
        "CARTE INTERACTIVE", 
        "VUE D'ENSEMBLE", 
        "ANALYSE CLUSTER", 
        "ANALYSE SALARIALE", 
        "PREDICTIONS",
        "DETAILS OFFRES"
    ])
    
    # Onglet 1: Accueil
    with tab1:
        show_home_page(filtered_df)
    
    # Onglet 2: Carte Interactive (AMÉLIORÉ)
    with tab2:
        st.markdown('<h2 class="sub-header">Carte Interactive des Offres d\'Emploi</h2>', unsafe_allow_html=True)
        
        if len(filtered_map) > 0:
            # Contrôles de la carte
            col_map_controls1, col_map_controls2, col_map_controls3 = st.columns(3)
            
            with col_map_controls1:
                map_type = st.selectbox(
                    "Type de visualisation",
                    options=["Points", "Densité", "Cluster"],
                    index=0,
                    help="Choisissez le type de visualisation de la carte"
                )
            
            with col_map_controls2:
                color_by = st.selectbox(
                    "Couleur par",
                    options=["Domaine", "Région", "Contrat", "Cluster"],
                    index=0,
                    help="Choisissez la variable pour la couleur des points"
                )
            
            with col_map_controls3:
                size_by = st.selectbox(
                    "Taille par",
                    options=["Salaire", "Expérience", "Uniforme"],
                    index=0,
                    help="Choisissez la variable pour la taille des points"
                )
            
            # Créer la carte améliorée
            map_type_dict = {"Points": "scatter", "Densité": "density", "Cluster": "cluster"}
            color_by_dict = {"Domaine": "domaine", "Région": "region", "Contrat": "contrat", "Cluster": "cluster_mots_cles"}
            size_by_dict = {"Salaire": "salaire", "Expérience": "experience", "Uniforme": "uniforme"}
            
            fig_map = create_enhanced_map(
                filtered_map, 
                map_type=map_type_dict[map_type],
                color_by=color_by_dict[color_by],
                size_by=size_by_dict[size_by]
            )
            
            if fig_map:
                st.markdown('<div class="map-container">', unsafe_allow_html=True)
                st.plotly_chart(fig_map, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Statistiques sous la carte
                col_map_stats1, col_map_stats2, col_map_stats3 = st.columns(3)
                
                with col_map_stats1:
                    st.markdown('<div class="insight-card">', unsafe_allow_html=True)
                    st.markdown('<div class="insight-title">Ville la plus active</div>', unsafe_allow_html=True)
                    if 'localisation' in filtered_map.columns:
                        ville_counts = filtered_map['localisation'].value_counts()
                        if not ville_counts.empty:
                            top_ville = ville_counts.index[0]
                            count = ville_counts.iloc[0]
                            st.markdown(f'<div class="insight-text"><strong>{top_ville}</strong><br>{count} offres</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col_map_stats2:
                    st.markdown('<div class="insight-card">', unsafe_allow_html=True)
                    st.markdown('<div class="insight-title">Salaire maximum</div>', unsafe_allow_html=True)
                    if 'salaire_impute' in filtered_map.columns:
                        max_salary = filtered_map['salaire_impute'].max()
                        st.markdown(f'<div class="insight-text"><strong>{max_salary:,.0f}€</strong><br>Salaire maximum</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col_map_stats3:
                    st.markdown('<div class="insight-card">', unsafe_allow_html=True)
                    st.markdown('<div class="insight-title">Diversité géographique</div>', unsafe_allow_html=True)
                    unique_villes = filtered_map['localisation'].nunique() if 'localisation' in filtered_map.columns else 0
                    st.markdown(f'<div class="insight-text"><strong>{unique_villes}</strong> villes différentes</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Téléchargement des données de la carte
                st.download_button(
                    label="📥 Télécharger les données géographiques",
                    data=filtered_map[['titre', 'entreprise', 'localisation', 'region', 'domaine', 'salaire_impute', 'lat', 'lon']].to_csv(index=False),
                    file_name="donnees_geographiques.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.warning("Données insuffisantes pour afficher la carte")
        else:
            st.warning("Aucune donnée disponible pour les filtres sélectionnés")
    
    # Onglet 3: Vue d'ensemble
    with tab3:
        st.markdown('<h2 class="sub-header">Vue d\'ensemble du marché</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Top domaines
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<div class="section-header">Top 10 Domaines</div>', unsafe_allow_html=True)
            if 'domaine' in filtered_df.columns:
                domain_count = filtered_df['domaine'].value_counts().head(10)
                fig = px.bar(
                    domain_count, 
                    x=domain_count.values, 
                    y=domain_count.index,
                    orientation='h',
                    color=domain_count.values,
                    color_continuous_scale='Blues',
                    labels={'x': 'Nombre d\'offres', 'y': ''}
                )
                fig.update_layout(showlegend=False, height=400)
                st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            # Répartition par contrat
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<div class="section-header">Répartition par Contrat</div>', unsafe_allow_html=True)
            if 'contrat' in filtered_df.columns:
                contrat_count = filtered_df['contrat'].value_counts()
                fig = px.pie(
                    contrat_count, 
                    values=contrat_count.values, 
                    names=contrat_count.index,
                    hole=0.4
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Onglet 4: Analyse Cluster
    with tab4:
        st.markdown('<h2 class="sub-header">Analyse par Cluster de Mots-clés</h2>', unsafe_allow_html=True)
        
        if 'cluster_mots_cles' in filtered_df.columns:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<div class="section-header">Distribution des Clusters</div>', unsafe_allow_html=True)
                cluster_dist = filtered_df['cluster_mots_cles'].value_counts().sort_index()
                fig = px.bar(
                    x=cluster_dist.index.astype(str),
                    y=cluster_dist.values,
                    labels={'x': 'Cluster', 'y': 'Nombre d\'offres'},
                    color=cluster_dist.values,
                    color_continuous_scale='Viridis'
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<div class="section-header">Statistiques par Cluster</div>', unsafe_allow_html=True)
                cluster_stats = filtered_df.groupby('cluster_mots_cles').agg({
                    'salaire_impute': 'mean',
                    'experience_requise': 'mean',
                    'salaire_proba_haut': 'mean'
                }).round(2)
                
                cluster_stats.columns = ['Salaire Moyen', 'Expérience Moyenne', 'Probabilité Haut Salaire']
                cluster_stats['Probabilité Haut Salaire'] = cluster_stats['Probabilité Haut Salaire'] * 100
                
                st.dataframe(
                    cluster_stats,
                    use_container_width=True,
                    height=400
                )
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("La colonne 'cluster_mots_cles' n'est pas disponible dans les données")
    
    # Onglet 5: Analyse Salariale
    with tab5:
        st.markdown('<h2 class="sub-header">Analyse Salariale Détaillée</h2>', unsafe_allow_html=True)
        
        if 'salaire_impute' in filtered_df.columns:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<div class="section-header">Distribution des Salaires</div>', unsafe_allow_html=True)
                fig = px.histogram(
                    filtered_df, 
                    x='salaire_impute',
                    nbins=30,
                    marginal='box',
                    color_discrete_sequence=['#3B82F6']
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<div class="section-header">Salaire par Domaine</div>', unsafe_allow_html=True)
                salaire_by_domaine = filtered_df.groupby('domaine')['salaire_impute'].mean().sort_values(ascending=False).head(10)
                fig = px.bar(
                    x=salaire_by_domaine.values,
                    y=salaire_by_domaine.index,
                    orientation='h',
                    color=salaire_by_domaine.values,
                    color_continuous_scale='Viridis',
                    labels={'x': 'Salaire moyen (€)', 'y': ''}
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Nouvelle fonctionnalité: Analyse par expérience
            if 'experience_requise' in filtered_df.columns:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<div class="section-header">Relation Salaire-Expérience</div>', unsafe_allow_html=True)
                
                exp_salary = filtered_df.groupby('experience_requise').agg({
                    'salaire_impute': ['mean', 'std', 'count']
                }).round(2)
                
                exp_salary.columns = ['Salaire Moyen', 'Écart-Type', 'Nombre']
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=exp_salary.index,
                    y=exp_salary['Salaire Moyen'],
                    mode='lines+markers',
                    name='Salaire moyen',
                    line=dict(color='#3B82F6', width=3)
                ))
                
                fig.update_layout(
                    height=400,
                    xaxis_title="Expérience (années)",
                    yaxis_title="Salaire moyen (€)",
                    showlegend=True
                )
                
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("La colonne 'salaire_impute' n'est pas disponible dans les données")
    
    # Onglet 6: Prédictions
    with tab6:
        st.markdown('<h2 class="sub-header">Analyse Prédictive</h2>', unsafe_allow_html=True)
        
        if 'salaire_pred_categorie_nn' in filtered_df.columns:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<div class="section-header">Performance du Modèle</div>', unsafe_allow_html=True)
                
                # Calcul des métriques
                if 'salaire_categorie' in filtered_df.columns:
                    accuracy = (filtered_df['salaire_categorie'] == filtered_df['salaire_pred_categorie_nn']).mean() * 100
                    precision = filtered_df[filtered_df['salaire_pred_categorie_nn'] == 1]['salaire_categorie'].mean() * 100
                    
                    col_met1, col_met2 = st.columns(2)
                    with col_met1:
                        st.metric("Accuracy", f"{accuracy:.1f}%")
                    with col_met2:
                        st.metric("Précision", f"{precision:.1f}%")
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<div class="section-header">Distribution des Prédictions</div>', unsafe_allow_html=True)
                
                pred_counts = filtered_df['salaire_pred_categorie_nn'].value_counts().sort_index()
                
                # CORRECTION: Vérifier qu'il y a au moins 2 catégories
                if len(pred_counts) >= 2:
                    # S'assurer que les noms correspondent aux valeurs
                    names = ['Bas salaire', 'Haut salaire']
                    values = []
                    
                    # Récupérer les valeurs dans l'ordre (0 puis 1)
                    for i in range(2):
                        if i in pred_counts.index:
                            values.append(pred_counts[i])
                        else:
                            values.append(0)  # Valeur 0 si la catégorie n'existe pas
                    
                    fig = px.pie(
                        values=values,
                        names=names,
                        color=names,
                        color_discrete_map={'Bas salaire': '#EF4444', 'Haut salaire': '#10B981'}
                    )
                    fig.update_layout(height=300)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    # Si une seule catégorie, afficher un message
                    if len(pred_counts) == 1:
                        categorie = 'Bas salaire' if 0 in pred_counts.index else 'Haut salaire'
                        count = pred_counts.iloc[0]
                        st.markdown(f"**Toutes les prédictions sont en : {categorie}**")
                        st.markdown(f"**Nombre :** {count}")
                    else:
                        st.info("Aucune donnée de prédiction disponible")
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Nouvelle fonctionnalité: Prédiction interactive
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<div class="section-header">Simulateur de Salaire</div>', unsafe_allow_html=True)
            
            col_sim1, col_sim2, col_sim3 = st.columns(3)
            
            with col_sim1:
                sim_domaine = st.selectbox(
                    "Domaine",
                    options=sorted(filtered_df['domaine'].unique()) if 'domaine' in filtered_df.columns else [],
                    index=0,
                    key="sim_domaine"
                )
            
            with col_sim2:
                sim_experience = st.slider(
                    "Expérience (années)",
                    min_value=0,
                    max_value=20,
                    value=5,
                    key="sim_experience"
                )
            
            with col_sim3:
                sim_region = st.selectbox(
                    "Région",
                    options=['Toutes'] + sorted(filtered_df['region'].unique().tolist()) if 'region' in filtered_df.columns else ['Toutes'],
                    index=0,
                    key="sim_region"
                )
            
            # Calcul de la prédiction
            sim_df = filtered_df[filtered_df['domaine'] == sim_domaine].copy() if sim_domaine else filtered_df.copy()
            
            if sim_region != 'Toutes':
                sim_df = sim_df[sim_df['region'] == sim_region]
            
            if 'experience_requise' in sim_df.columns:
                sim_df = sim_df[sim_df['experience_requise'] <= sim_experience + 2]
                sim_df = sim_df[sim_df['experience_requise'] >= sim_experience - 2]
            
            if len(sim_df) > 0:
                salaire_estime = sim_df['salaire_impute'].mean() if 'salaire_impute' in sim_df.columns else 0
                proba_haut = sim_df['salaire_proba_haut'].mean() * 100 if 'salaire_proba_haut' in sim_df.columns else 0
                
                col_res1, col_res2 = st.columns(2)
                with col_res1:
                    st.metric("Salaire estimé", f"{salaire_estime:,.0f}€")
                with col_res2:
                    st.metric("Probabilité haut salaire", f"{proba_haut:.1f}%")
            else:
                st.info("Aucune donnée disponible pour ces critères")
            
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("Les colonnes de prédiction ne sont pas disponibles dans les données")
    
    # Onglet 7: Détails des Offres (NOUVEAU)
    with tab7:
        st.markdown('<h2 class="sub-header">Détails des Offres d\'Emploi</h2>', unsafe_allow_html=True)
        
        # Options d'affichage
        col_filter1, col_filter2, col_filter3 = st.columns(3)
        
        with col_filter1:
            sort_by = st.selectbox(
                "Trier par",
                options=["Salaire (décroissant)", "Salaire (croissant)", "Expérience", "Date"],
                index=0
            )
        
        with col_filter2:
            items_per_page = st.selectbox(
                "Offres par page",
                options=[10, 25, 50, 100],
                index=0
            )
        
        with col_filter3:
            # Filtre par probabilité
            min_proba = st.slider(
                "Probabilité minimum haut salaire",
                min_value=0.0,
                max_value=1.0,
                value=0.0,
                step=0.1
            )
        
        # Application des filtres supplémentaires
        display_df = filtered_df.copy()
        
        if 'salaire_proba_haut' in display_df.columns:
            display_df = display_df[display_df['salaire_proba_haut'] >= min_proba]
        
        # Tri
        sort_columns = {
            "Salaire (décroissant)": ('salaire_impute', False),
            "Salaire (croissant)": ('salaire_impute', True),
            "Expérience": ('experience_requise', False),
            "Date": ('scraped_at', False)
        }
        
        if sort_by in sort_columns:
            sort_col, sort_asc = sort_columns[sort_by]
            if sort_col in display_df.columns:
                display_df = display_df.sort_values(sort_col, ascending=sort_asc)
        
        # Colonnes à afficher
        display_cols = ['titre', 'entreprise', 'localisation', 'domaine', 'contrat', 'experience_requise', 'salaire_impute']
        
        if 'salaire_proba_haut' in display_df.columns:
            display_cols.append('salaire_proba_haut')
        
        if 'cluster_mots_cles' in display_df.columns:
            display_cols.append('cluster_mots_cles')
        
        # Affichage des données
        st.markdown(f"**{len(display_df)} offres trouvées**")
        
        if len(display_df) > 0:
            # Préparer l'affichage
            display_data = display_df[display_cols].head(items_per_page).copy()
            
            # Formater les colonnes
            if 'salaire_impute' in display_data.columns:
                display_data['salaire_impute'] = display_data['salaire_impute'].apply(lambda x: f"{x:,.0f}€")
            
            if 'salaire_proba_haut' in display_data.columns:
                display_data['salaire_proba_haut'] = display_data['salaire_proba_haut'].apply(lambda x: f"{x:.1%}")
            
            # Afficher le tableau
            st.dataframe(
                display_data,
                use_container_width=True,
                height=500
            )
            
            # Téléchargement
            csv_data = display_df[display_cols].to_csv(index=False)
            st.download_button(
                label="📥 Télécharger toutes les offres (CSV)",
                data=csv_data,
                file_name="offres_filtrees.csv",
                mime="text/csv",
                use_container_width=True
            )
        else:
            st.info("Aucune offre ne correspond aux critères sélectionnés")
    
    # Section de comparaison si activée
    if st.session_state.get('compare_domains'):
        domain_1, domain_2 = st.session_state.compare_domains
        
        st.markdown("---")
        st.markdown(f'<h3 style="color: #1E3A8A;">Comparaison : {domain_1} vs {domain_2}</h3>', unsafe_allow_html=True)
        
        fig_comparison = create_comparison_chart(df, domain_1, domain_2)
        
        if fig_comparison:
            st.plotly_chart(fig_comparison, use_container_width=True)
        
        # Détails de la comparaison
        col_comp1, col_comp2 = st.columns(2)
        
        with col_comp1:
            df_domain1 = df[df['domaine'] == domain_1]
            if len(df_domain1) > 0:
                st.markdown(f"**{domain_1}**")
                st.metric("Nombre d'offres", len(df_domain1))
                if 'salaire_impute' in df_domain1.columns:
                    st.metric("Salaire moyen", f"{df_domain1['salaire_impute'].mean():,.0f}€")
        
        with col_comp2:
            df_domain2 = df[df['domaine'] == domain_2]
            if len(df_domain2) > 0:
                st.markdown(f"**{domain_2}**")
                st.metric("Nombre d'offres", len(df_domain2))
                if 'salaire_impute' in df_domain2.columns:
                    st.metric("Salaire moyen", f"{df_domain2['salaire_impute'].mean():,.0f}€")
    
    # Footer
    st.markdown("---")
    
    col_footer1, col_footer2 = st.columns(2)
    
    with col_footer1:
        st.markdown(f"""
        **Dernière mise à jour**  
        {datetime.now().strftime("%d/%m/%Y à %H:%M")}  
        **Total des offres**  
        {len(df):,}
        """)
    
    with col_footer2:
        if 'salaire_impute' in df.columns:
            salaire_moyen = df['salaire_impute'].mean()
            st.markdown(f"""
            **Salaire moyen global**  
            {salaire_moyen:,.0f}€  
            **Version**  
            4.0 - Dashboard Amélioré
            """)

# ==================== LANCEMENT DE L'APPLICATION ====================
if __name__ == "__main__":
    # Initialisation des états de session
    if 'comparison_mode' not in st.session_state:
        st.session_state.comparison_mode = False
    if 'compare_domains' not in st.session_state:
        st.session_state.compare_domains = None
    
    # Lancement de l'application
    main()