import streamlit as st
from database import *
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import joblib

if "model" not in st.session_state:
    st.session_state.model = None

if "encoders" not in st.session_state:
    st.session_state.encoders = None

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Heart Disease Prediction",
    page_icon="❤️",
    layout="wide"
)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "dataset_uploaded" not in st.session_state:
    st.session_state.dataset_uploaded = False

if "df" not in st.session_state:
    st.session_state.df = None

if "model" not in st.session_state:
    st.session_state.model = None

if "encoders" not in st.session_state:
    st.session_state.encoders = None

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------
st.markdown("""
<style>

/* Background */
.stApp{
    background:#0E1117;
}

/* Hide Streamlit Branding */
#MainMenu{
    visibility:hidden;
}
footer{
    visibility:hidden;
}
header{
    visibility:hidden;
}

/* Sidebar */
[data-testid="stSidebar"]{
    background:#262730;
}

[data-testid="stSidebar"] h1{
    color:white;
}

/* Main Title */
.main-title{
    font-size:60px;
    font-weight:800;
    color:white;
    margin-bottom:5px;
}

/* Subtitle */
.sub-title{
    font-size:20px;
    color:#B0B0B0;
    margin-bottom:30px;
}

/* Section Heading */
.section-title{
    font-size:46px;
    font-weight:700;
    color:white;
    margin-top:30px;
    margin-bottom:20px;
}

/* Green Welcome Box */
.welcome-box{
    background:#1E5631;
    color:white;
    padding:20px;
    border-radius:12px;
    font-size:22px;
    font-weight:bold;
}

/* Upload Box */
[data-testid="stFileUploader"]{
    background:#22232D;
    border-radius:12px;
    border:1px solid #444;
    padding:12px;
}

/* Buttons */
.stButton>button{
    width:100%;
    background:#238636;
    color:white;
    border-radius:10px;
    border:none;
    height:48px;
    font-size:18px;
    font-weight:bold;
}

.stButton>button:hover{
    background:#2EA043;
}

/* Metric Cards */
[data-testid="metric-container"]{
    background:#1B1D24;
    border:1px solid #333;
    padding:20px;
    border-radius:12px;
}

/* Tables */
[data-testid="stDataFrame"]{
    border-radius:12px;
}

/* Success Message */
.stSuccess{
    border-radius:12px;
}

/* Warning */
.stWarning{
    border-radius:12px;
}

/* Error */
.stError{
    border-radius:12px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# TITLE
# --------------------------------------------------
st.markdown(
"""
<h1 class='main-title'>
❤️ Heart Disease Prediction System
</h1>
<p class='sub-title'>
Upload Dataset ➜ Analyze ➜ Upload Model ➜ Predict
</p>
""",
unsafe_allow_html=True
)

st.divider()
# --------------------------------------------------
# LOGIN PAGE
# --------------------------------------------------

if st.session_state.logged_in == False:

    menu = st.radio(
        "Select",
        ["Login", "Register"],
        horizontal=True
    )

    st.write("")

    # ===================================================
    # REGISTER
    # ===================================================

    if menu == "Register":

        st.subheader("Create Account")

        fullname = st.text_input("Full Name")

        email = st.text_input("Email")

        username = st.text_input("Username")

        password = st.text_input(
            "Password",
            type="password"
        )

        confirm = st.text_input(
            "Confirm Password",
            type="password"
        )

        if st.button("Register", use_container_width=True):

            if fullname == "" or email == "" or username == "" or password == "" or confirm == "":
                st.error("Please fill all fields.")

            elif password != confirm:
                st.error("Passwords do not match.")

            else:

                status = register_user(
                    fullname,
                    email,
                    username,
                    password
                )

                if status:

                    st.success("Registration Successful ✅")

                else:

                    st.error("Username or Email already exists.")

    # ===================================================
    # LOGIN
    # ===================================================

    else:

        st.subheader("Login")

        username = st.text_input("Username")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login", use_container_width=True):

            user = login_user(
                username,
                password
            )

            if user:

                st.session_state.logged_in = True
                st.session_state.username = username

                st.success("Login Successful")

                st.rerun()

            else:

                st.error("Invalid Username or Password.")
# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

else:
    st.sidebar.title("❤️ Heart Disease")

    st.sidebar.markdown(
f"""
<div class="welcome-box">

Welcome

<br><br>

{st.session_state.username}

</div>
""",
unsafe_allow_html=True
)

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

    st.divider()

    st.header("🏠 Dashboard")

    st.info("Follow the steps below to predict Heart Disease.")

    # ======================================================
    # STEP 1 : DATASET UPLOAD
    # ======================================================

    st.markdown("---")
    st.markdown(
"<h2 class='section-title'>📂 Dataset Upload</h2>",
unsafe_allow_html=True
)

    uploaded_file = st.file_uploader(
        "Choose CSV File",
        type=["csv"]
    )

    if uploaded_file is not None:

        df = pd.read_csv(uploaded_file)

        st.session_state.df = df
        st.session_state.dataset_uploaded = True

        st.success("✅ Dataset Uploaded Successfully")
        # --------------------------------------------------
        # DATASET SESSION
        # --------------------------------------------------
        if "dataset_uploaded" not in st.session_state:
            st.session_state.dataset_uploaded = False

        if "df" not in st.session_state:
            st.session_state.df = None
         # ======================================================
         # STEP 2 : DATASET ANALYSIS
         # ======================================================

        if st.session_state.dataset_uploaded:

             df = st.session_state.df

             st.markdown("---")
             st.subheader("📊 Step 2 : Dataset Analysis")

             c1, c2, c3 = st.columns(3)

             c1.metric("Rows", df.shape[0])
             c2.metric("Columns", df.shape[1])
             c3.metric("Features", df.shape[1]-1)

             st.write("### Dataset Preview")
             st.dataframe(df.head())

             st.write("### Data Types")
             st.dataframe(df.dtypes.astype(str))

             st.write("### Missing Values")
             missing = df.isnull().sum()

             st.dataframe(
                 missing.reset_index().rename(
                     columns={
                         "index":"Column",
                         0:"Missing Values"
                     }
                 )
             )

             st.write("### Duplicate Rows")

             duplicates = df.duplicated().sum()

             if duplicates == 0:
                 st.success("No Duplicate Rows Found")
             else:
                 st.warning(f"{duplicates} Duplicate Rows Found")
             
        # ======================================================
        # STEP 3 : DATA VISUALIZATION
        # ======================================================

        if st.session_state.dataset_uploaded:

            df = st.session_state.df

            st.markdown("---")
            st.subheader("📈 Step 3 : Data Visualization")

            # ---------------------------------------
            # Target Class Distribution
            # ---------------------------------------

            if "HeartDisease" in df.columns:

                st.write("### ❤️ Heart Disease Distribution")

                fig, ax = plt.subplots(figsize=(6,4))

                sns.countplot(
                    x="HeartDisease",
                    data=df,
                    ax=ax
                )

                st.pyplot(fig)

            # ---------------------------------------
            # Correlation Heatmap
            # ---------------------------------------

            st.write("### 🔥 Correlation Heatmap")

            numeric_df = df.select_dtypes(include=np.number)

            fig, ax = plt.subplots(figsize=(10,6))

            sns.heatmap(
                numeric_df.corr(),
                annot=True,
                cmap="coolwarm",
                ax=ax
            )

            st.pyplot(fig)

            # ---------------------------------------
            # Feature Distribution
            # ---------------------------------------

            st.write("### 📊 Feature Distribution")

            numeric_columns = numeric_df.columns.tolist()

            feature = st.selectbox(
                "Select Feature",
                numeric_columns
            )

            fig, ax = plt.subplots(figsize=(7,4))

            sns.histplot(
                df[feature],
                kde=True,
                ax=ax
            )

            st.pyplot(fig)
        # ======================================================
        # STEP 4 : MODEL UPLOAD
        # ======================================================

        st.markdown("---")
        st.subheader("🤖 Step 4 : Upload Trained Model")

        model_file = st.file_uploader(
            "Upload model.pkl",
            type=["pkl"],
            key="model_upload"
        )

        encoder_file = st.file_uploader(
            "Upload label_encoders.pkl",
            type=["pkl"],
            key="encoder_upload"
        )

        if model_file and encoder_file:

            model = joblib.load(model_file)

            label_encoders = joblib.load(encoder_file)

            st.session_state.model = model
            st.session_state.encoders = label_encoders

            st.success("✅ Model Loaded Successfully")
        # ======================================================
        # STEP 5 : PATIENT DETAILS
        # ======================================================
        
        if st.session_state.model is not None:
        
            st.markdown("---")
            st.subheader("❤️ Step 5 : Enter Patient Details")
        
            col1, col2 = st.columns(2)
        
            with col1:
        
                age = st.number_input("Age", 1, 120, 45)
        
                sex = st.selectbox(
                    "Sex",
                    ["M", "F"]
                )
        
                chest = st.selectbox(
                    "Chest Pain Type",
                    ["ATA", "NAP", "ASY", "TA"]
                )
        
                resting_bp = st.number_input(
                    "Resting BP",
                    50,
                    250,
                    120
                )
        
                cholesterol = st.number_input(
                    "Cholesterol",
                    0,
                    700,
                    200
                )
        
                fasting_bs = st.selectbox(
                    "Fasting Blood Sugar",
                    [0,1]
                )
        
            with col2:
        
                resting_ecg = st.selectbox(
                    "Resting ECG",
                    ["Normal","ST","LVH"]
                )
        
                max_hr = st.number_input(
                    "Maximum Heart Rate",
                    60,
                    250,
                    150
                )
        
                exercise = st.selectbox(
                    "Exercise Angina",
                    ["N","Y"]
                )
        
                oldpeak = st.number_input(
                    "Old Peak",
                    0.0,
                    10.0,
                    1.0
                )
        
                st_slope = st.selectbox(
                    "ST Slope",
                    ["Up","Flat","Down"]
                            )
         
        # ======================================================
        # STEP 6 : PREDICTION
        # ======================================================
        
        if st.button("❤️ Predict Heart Disease", use_container_width=True):
        
            # Create DataFrame from user input
            input_df = pd.DataFrame({
        
                "Age": [age],
                "Sex": [sex],
                "ChestPainType": [chest],
                "RestingBP": [resting_bp],
                "Cholesterol": [cholesterol],
                "FastingBS": [fasting_bs],
                "RestingECG": [resting_ecg],
                "MaxHR": [max_hr],
                "ExerciseAngina": [exercise],
                "Oldpeak": [oldpeak],
                "ST_Slope": [st_slope]
        
            })
        
            # Encode categorical columns
            categorical = [
                "Sex",
                "ChestPainType",
                "RestingECG",
                "ExerciseAngina",
                "ST_Slope"
            ]
        
            for col in categorical:
                input_df[col] = st.session_state.encoders[col].transform(
                    input_df[col]
                )
        
            # Make Prediction
            prediction = st.session_state.model.predict(input_df)[0]
            probability = st.session_state.model.predict_proba(input_df)[0]
            
            st.write("Encoded Input")
            st.dataframe(input_df)
            
            st.write("Prediction:", prediction)
            st.write("Probability:", probability)
        
            # Confidence Score
            confidence = probability[prediction] * 100
        
            # ==========================================
            # Prediction Result
            # ==========================================
        
            st.markdown("---")
            st.subheader("📋 Prediction Result")
        
            if prediction == 1:
        
                st.error("❤️ Heart Disease Detected")
        
                st.write("### Recommendation")
                st.write("- Consult a Cardiologist.")
                st.write("- Exercise regularly.")
                st.write("- Maintain a healthy diet.")
                st.write("- Monitor blood pressure and cholesterol.")
        
            else:
        
                st.success("💚 No Heart Disease Detected")
        
                st.write("### Recommendation")
                st.write("- Continue your healthy lifestyle.")
                st.write("- Exercise regularly.")
                st.write("- Eat a balanced diet.")
                st.write("- Schedule regular health checkups.")
        
            st.metric(
                "Confidence Score",
                f"{confidence:.2f}%"
            )
        
            # Save Prediction History
            save_prediction(
                st.session_state.username,
                "Heart Disease" if prediction == 1 else "No Heart Disease",
                confidence
            )
        
            st.balloons()
            
                  
            
            
            
