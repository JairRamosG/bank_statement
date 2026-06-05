def load_css():
    return """
    <style>
        .main { background-color: #fafafa; }
        footer { visibility: hidden; }
        #MainMenu { visibility: hidden; }
        [data-testid="stToolbar"] { display: none; }
        .stDeployButton { display: none; }
        [data-testid="stStatusWidget"] { display: none; }
        
        .hero-banner {
            background: linear-gradient(135deg, #ea667e 0%, #a13246 100%);
            padding: 50px 70px;
            text-align: center;
            margin: -1rem -1rem 2rem -1rem;
            border-radius: 0 0 20px 20px;
            box-shadow: 0 4px 20px rgba(161, 50, 70, 0.3);
        }
        
        .hero-banner h1 {
            color: white;
            font-size: 2.8em;
            font-weight: 800;
            margin-bottom: 8px;
            letter-spacing: -1px;
        }
        
        .hero-banner p {
            color: rgba(255,255,255,0.9);
            font-size: 1.1em;
            font-weight: 300;
            margin: 0;
        }

        .info-card {
            background: white;
            border-radius: 12px;
            padding: 20px;
            border-left: 4px solid #ea667e;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
            margin-bottom: 15px;
        }

        .stButton > button {
            background: linear-gradient(135deg, #ea667e 0%, #a13246 100%);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 14px 30px;
            font-size: 16px;
            font-weight: 600;
            width: 100%;
        }

        .stDownloadButton > button {
            background: white;
            color: #a13246;
            border: 2px solid #ea667e;
            border-radius: 10px;
            font-weight: 600;
        }

        .stDownloadButton > button:hover {
            background: #ea667e;
            color: white;
        }
    </style>
    """