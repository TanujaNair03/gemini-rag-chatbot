

def get_css() -> str:

    
    css_string = f"""
    <style>

        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');


        :root {{
            --glass-bg: rgba(255, 255, 255, 0.08); /* Main glass background (white tint) */
            --glass-border: rgba(255, 255, 255, 0.25); /* Main glass border (white) */
            --text-color: #f0f0f0;
            --accent-primary: #e54c91; /* Pink */
            --accent-secondary: #ffc800; /* Yellow */
            --main-dark-bg: #1a1a2e; /* The "futuristic black" base color */
            /* --- NEW iMessage Colors --- */
            --imessage-blue: #007AFF;
            --imessage-gray: #E5E5EA;
        }}


        * {{
            font-family: 'Poppins', sans-serif; 
            box-sizing: border-box;
        }}

        html, body, .stApp {{
            min-height: 100vh;
            background-color: var(--main-dark-bg); /* Dark blue-purple base */
            
            /* Create a grid pattern using the accent color with low opacity */
            background-image: 
                repeating-linear-gradient(
                    to right, 
                    rgba(229, 76, 145, 0.1) 0,  /* 10% opaque accent pink */
                    rgba(229, 76, 145, 0.1) 1px, 
                    transparent 1px, 
                    transparent 80px /* Grid line every 80px */
                ),
                repeating-linear-gradient(
                    to bottom, 
                    rgba(229, 76, 145, 0.1) 0, 
                    rgba(229, 76, 145, 0.1) 1px, 
                    transparent 1px, 
                    transparent 80px
                );
            
            background-attachment: fixed; /* Grid stays in place on scroll */
            color: var(--text-color);
        }}

        .stApp::before {{
            content: none; 
        }}
        
        h1, h2, h3 {{
            color: #FFFFFF;
        }}

        /* --- 5. HIDE STREAMLIT CHROME --- */
        footer {{
            display: none !important;
        }}
        [data-testid="stSidebar"] {{
            background: transparent !important;
            border-right: none !important;
        }}


        
        .main .block-container {{
            background: var(--glass-bg);
            backdrop-filter: blur(25px);
            -webkit-backdrop-filter: blur(25px);
            border: 1px solid var(--glass-border);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
            border-radius: 15px;
            
            padding-top: 2rem;
            padding-left: 2rem;
            padding-right: 2rem;
            padding-bottom: 10rem;
            
            margin: 1rem;           
            min-height: 95vh;       
        }}

        /* *** THIS IS THE CHANGE *** */
        /* This is the SIDEBAR pane (accented pink glass) */
        [data-testid="stSidebar"] > div:first-child {{
            /* NEW: Use a pink-tinted glass instead of the white glass */
            background: rgba(229, 76, 145, 0.1); /* 10% opacity of your accent-primary */
            backdrop-filter: blur(25px);
            -webkit-backdrop-filter: blur(25px);
            /* NEW: Use the solid accent color for the border to make it pop */
            border: 1px solid var(--accent-primary); 
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
            border-radius: 15px;
            padding: 2rem;
            margin: 1rem; 
        }}



        div[data-testid*="stChatMessageContainer-user"],
        div[data-testid*="stChatMessageContainer-assistant"] {{
            background: transparent;
            border: none;
            box-shadow: none;
            padding: 0;
            margin-bottom: 10px;
        }}

        [data-testid="stChatMessageContainer-user"] .st-ag {{
            display: none !important;
        }}
        
        [data-testid="stChatMessageContainer-user"] {{
            padding-left: 0 !important;
            display: flex;
            justify-content: flex-end;
        }}

        [data-testid="stMarkdownContainer"] {{
            padding: 12px;
            max-width: 70%;
            word-wrap: break-word;
            display: inline-block; 
        }}

        [data-testid="stChatMessageContainer-assistant"] [data-testid="stMarkdownContainer"] {{
            background: var(--imessage-gray);
            border-radius: 20px 20px 20px 5px; 
            color: #000000 !important; 
        }}
        
        [data-testid="stChatMessageContainer-user"] [data-testid="stMarkdownContainer"] {{
            background: var(--imessage-blue);
            border-radius: 20px 20px 5px 20px;
            color: #ffffff !important;
        }}
        
        [data-testid="stChatMessageContainer-assistant"] [data-testid="stMarkdownContainer"] p {{
            color: #000000 !important;
        }}
        [data-testid="stChatMessageContainer-user"] [data-testid="stMarkdownContainer"] p {{
            color: #ffffff !important;
        }}

   
        [data-testid="stChatInput"] {{
            position: fixed;
            bottom: 1rem;   
            left: 50%;      
            transform: translateX(-50%);
            width: calc(100% - 28rem); 
            max-width: 900px; 
            background: rgba(0, 0, 0, 0.4); 
            backdrop-filter: blur(25px);
            -webkit-backdrop-filter: blur(25px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
            border-radius: 15px; 
            padding: 1rem 1.5rem; 
            z-index: 100; 
        }}
        
        [data-testid="stChatInput"] > div > div > label + div > div > textarea {{
            background: transparent; 
            border: none; 
            color: #FFFFFF;
        }}

        [data-testid="stChatInput"] > div > div > label + div > div > textarea::placeholder {{
            color: rgba(255, 255, 255, 0.6);
        }}

    
        .stButton > button {{
            width: 100%;
            background: var(--accent-primary) !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 8px !important;
            font-weight: bold !important;
            padding: 0.75rem !important;
            transition: background 0.2s ease !important;
        }}
        
        .stButton > button:hover {{
            background: var(--accent-secondary) !important;
            color: var(--main-dark-bg) !important; 
        }}

        [data-testid="stRadioButton"] div[aria-checked="true"] {{
            border-color: var(--accent-primary) !important;
        }}
        [data-testid="stRadioButton"] div[aria-checked="true"] > div:first-child {{
             background-color: var(--accent-primary) !important; 
        }}
        
        [data-testid="stFileUploader"] label {{
            font-size: 1rem !important;
            font-weight: 600 !important;
            color: var(--text-color) !important;
        }}
        [data-testid="stFileUploader"] section {{
            background: rgba(0,0,0,0.2);
            border: 1px dashed var(--glass-border);
            border-radius: 8px;
        }}
    </style>
    """
    return css_string