import streamlit as st
import pandas as pd
import numpy as np
import joblib
from pathlib import Path


def inject_custom_css() -> None:
    """Inject premium editorial styling for the first UI milestone."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

        :root {
            --ink: #182427;
            --muted: #5f6b6e;
            --paper: #f4ecdd;
            --panel: rgba(255, 251, 241, 0.76);
            --line: rgba(24, 36, 39, 0.14);
            --accent: #0f6a50;
            --accent-strong: #0b513e;
        }

        .stApp {
            font-family: 'Manrope', sans-serif;
            color: var(--ink);
            background:
                radial-gradient(1200px 560px at -10% -18%, #fff9ee 0%, rgba(255, 249, 238, 0.92) 42%, transparent 70%),
                radial-gradient(900px 450px at 105% -12%, #f8f0df 0%, rgba(248, 240, 223, 0.88) 38%, transparent 70%),
                linear-gradient(180deg, #f3ebda 0%, #ece3d1 100%);
        }

        h1, h2, h3 {
            font-family: 'Playfair Display', serif;
            letter-spacing: 0.01em;
            color: #132024;
        }

        [data-testid='stHeader'] {
            background: transparent;
        }

        [data-testid='stMetricValue'] {
            font-family: 'Playfair Display', serif;
        }

        div[data-testid='stNumberInput'],
        div[data-testid='stTextInput'],
        div[data-testid='stSelectbox'],
        div[data-testid='stSlider'] {
            background: var(--panel);
            border: 1px solid var(--line);
            border-radius: 14px;
            padding: 0.35rem 0.65rem;
            box-shadow: 0 10px 28px rgba(15, 27, 29, 0.05);
        }

        div[data-testid='stCheckbox'] {
            background: var(--panel);
            border: 1px solid var(--line);
            border-radius: 14px;
            padding: 0.35rem 0.65rem;
            margin: 0.2rem 0 0.6rem 0;
            box-shadow: 0 10px 28px rgba(15, 27, 29, 0.05);
        }

        div[data-testid='stCheckbox'] label {
            color: #203235;
            font-weight: 600;
        }

        div[data-testid='stSelectbox'] > div[data-baseweb='select'] > div,
        div[data-testid='stTextInput'] input,
        div[data-testid='stNumberInput'] input {
            background: rgba(255, 251, 241, 0.88);
            border-radius: 10px;
        }

        div[data-testid='stSlider'] [data-baseweb='slider'] div[role='slider'] {
            background: var(--accent);
            border-color: var(--accent-strong);
        }

        div[data-testid='stButton'] > button {
            background: linear-gradient(135deg, var(--accent-strong) 0%, var(--accent) 100%);
            color: #fdfbf4;
            border: none;
            border-radius: 14px;
            padding: 0.75rem 1rem;
            font-weight: 700;
            letter-spacing: 0.02em;
        }

        div[data-testid='stButton'] > button:hover {
            filter: brightness(1.06);
            transform: translateY(-1px);
        }

        .hero-kicker {
            text-transform: uppercase;
            letter-spacing: 0.18em;
            font-size: 0.74rem;
            font-weight: 700;
            color: var(--muted);
            margin-bottom: 0.25rem;
        }

        .hero-copy {
            max-width: 760px;
            color: #2d3f43;
            margin-top: 0.25rem;
            margin-bottom: 0;
            line-height: 1.55;
        }

        .control-intro {
            font-size: 0.9rem;
            color: var(--muted);
            margin-bottom: 0.4rem;
        }

        .control-label {
            font-size: 0.84rem;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            color: #2a3f44;
            margin-bottom: 0.1rem;
            font-weight: 700;
        }

        .stat-section-copy {
            color: var(--muted);
            margin-top: -0.15rem;
            margin-bottom: 0.6rem;
            font-size: 0.9rem;
        }

        .stat-card-head {
            display: flex;
            align-items: center;
            gap: 0.55rem;
            padding: 0.45rem 0.55rem;
            border: 1px solid var(--line);
            border-radius: 12px;
            margin-bottom: 0.35rem;
            background: linear-gradient(180deg, rgba(253, 248, 238, 0.9) 0%, rgba(247, 238, 223, 0.82) 100%);
        }

        .stat-card-icon {
            width: 1.9rem;
            height: 1.9rem;
            border-radius: 0.62rem;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: rgba(15, 106, 80, 0.13);
            border: 1px solid rgba(15, 106, 80, 0.22);
            font-size: 1.1rem;
            line-height: 1;
        }

        .stat-card-title {
            font-size: 0.84rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-weight: 800;
            color: #203235;
            line-height: 1.1;
        }

        .stat-card-subtitle {
            font-size: 0.74rem;
            color: var(--muted);
            line-height: 1.2;
            margin-top: 0.13rem;
        }

        .result-card {
            text-align: center;
            padding: 0.45rem 0 0.25rem;
        }

        .result-label {
            font-size: 0.84rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #4b5b5f;
            font-weight: 700;
            margin-bottom: 0.15rem;
        }

        .result-value {
            font-family: 'Playfair Display', serif;
            color: #1a2730;
            font-size: clamp(2rem, 4vw, 3.05rem);
            line-height: 1.05;
            font-weight: 700;
            font-variant-numeric: tabular-nums;
        }

        .result-currency {
            margin-right: 0.25rem;
        }

        @media (max-width: 900px) {
            .hero-copy {
                font-size: 0.95rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def init_profile_state() -> None:
    """Initialize session state for synchronized profile controls."""
    defaults = {
        "age_value": 25.0,
        "age_slider": 25.0,
        "age_input": 25.0,
        "height_value": 180.0,
        "height_slider": 180.0,
        "height_input": 180.0,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def sync_age_from_slider() -> None:
    value = float(st.session_state["age_slider"])
    st.session_state["age_value"] = value
    st.session_state["age_input"] = value


def sync_age_from_input() -> None:
    value = float(st.session_state["age_input"])
    st.session_state["age_value"] = value
    st.session_state["age_slider"] = value


def sync_height_from_slider() -> None:
    value = float(st.session_state["height_slider"])
    st.session_state["height_value"] = value
    st.session_state["height_input"] = value


def sync_height_from_input() -> None:
    value = float(st.session_state["height_input"])
    st.session_state["height_value"] = value
    st.session_state["height_slider"] = value


def render_stat_input_card(
    *,
    title: str,
    icon: str,
    subtitle: str,
    input_label: str,
    min_value: float,
    value: float,
    step: float,
    key: str,
) -> float:
    """Render a compact icon-based stat card with an input."""
    st.markdown(
        f"""
        <div class="stat-card-head">
            <span class="stat-card-icon">{icon}</span>
            <div>
                <div class="stat-card-title">{title}</div>
                <div class="stat-card-subtitle">{subtitle}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    return st.number_input(
        input_label,
        min_value=min_value,
        value=value,
        step=step,
        key=key,
        label_visibility="collapsed",
    )


# 1. Page Configuration
st.set_page_config(page_title="Player Value Predictor", page_icon="⚽", layout="wide")
inject_custom_css()
init_profile_state()

# 2. Load ML Artifacts
# @st.cache_resource ensures the models are only loaded once and cached in memory
@st.cache_resource
def load_models():
    project_root = Path(__file__).resolve().parents[1]
    preprocessor_path = project_root / "models" / "preprocessor.joblib"
    model_path = project_root / "models" / "xgboost_champion.joblib"

    preprocessor = joblib.load(preprocessor_path)
    model = joblib.load(model_path)
    return preprocessor, model

preprocessor, model = load_models()


@st.cache_data
def load_country_options() -> tuple[list[str], list[str]]:
    """Load country dropdown values from training-known dataset columns."""
    project_root = Path(__file__).resolve().parents[1]
    candidate_files = [
        project_root / "data" / "eda_final_dataset.csv",
        project_root / "data" / "processed_valuations.csv",
    ]

    for data_path in candidate_files:
        if not data_path.exists():
            continue

        try:
            country_df = pd.read_csv(
                data_path,
                usecols=["country_of_citizenship", "country_name"],
            )
            citizenship_options = sorted(
                {
                    str(value).strip()
                    for value in country_df["country_of_citizenship"].dropna()
                    if str(value).strip()
                }
            )
            league_country_options = sorted(
                {
                    str(value).strip()
                    for value in country_df["country_name"].dropna()
                    if str(value).strip()
                }
            )
            if citizenship_options and league_country_options:
                return citizenship_options, league_country_options
        except Exception:
            continue

    # Fallback keeps app usable if source files are not available.
    return ["France"], ["France"]


@st.cache_data
def load_club_options() -> list[tuple[int, str]]:
    """Load searchable club options and map display names to Transfermarkt IDs."""
    project_root = Path(__file__).resolve().parents[1]
    club_file = project_root / "data" / "processed_valuations.csv"
    fallback = [(583, "Paris Saint-Germain")]

    if not club_file.exists():
        return fallback

    try:
        club_df = pd.read_csv(
            club_file,
            usecols=["current_club_id", "current_club_name"],
        )
        club_df = club_df.dropna(subset=["current_club_id", "current_club_name"]).copy()
        club_df["current_club_name"] = club_df["current_club_name"].astype(str).str.strip()
        club_df = club_df[club_df["current_club_name"] != ""]

        club_df["current_club_id"] = pd.to_numeric(club_df["current_club_id"], errors="coerce")
        club_df = club_df.dropna(subset=["current_club_id"])
        club_df["current_club_id"] = club_df["current_club_id"].astype(int)

        # Some IDs can have multiple aliases; keep the most frequent label.
        counts = (
            club_df.groupby(["current_club_id", "current_club_name"])
            .size()
            .reset_index(name="count")
            .sort_values(
                by=["current_club_id", "count", "current_club_name"],
                ascending=[True, False, True],
            )
        )
        best_names = counts.drop_duplicates(subset=["current_club_id"], keep="first")

        club_options = [
            (int(row.current_club_id), str(row.current_club_name))
            for row in best_names.itertuples(index=False)
        ]
        club_options.sort(key=lambda item: item[1].lower())
        return club_options or fallback
    except Exception:
        return fallback


citizenship_options, league_country_options = load_country_options()
club_options = load_club_options()

# 3. Header
st.markdown('<p class="hero-kicker">Player Valuation Studio</p>', unsafe_allow_html=True)
st.title("⚽ Professional Footballer Market Value Predictor")
st.markdown("""
This application uses an advanced **XGBoost Machine Learning model**
to estimate a football player's market value based on their profile, club prestige, and performance statistics.
""")
st.markdown(
    '<p class="hero-copy">Build a profile with interactive controls and get an instant valuation signal. ',
    unsafe_allow_html=True,
)
st.divider()

# 4. User Inputs Section
st.header("Enter Player Data")

POSITION_TO_SUBPOSITIONS = {
    "Attack": ["Centre-Forward", "Left Winger", "Right Winger"],
    "Midfield": ["Central Midfield", "Attacking Midfield", "Defensive Midfield"],
    "Defender": ["Centre-Back", "Right-Back", "Left-Back"],
    "Goalkeeper": ["Goalkeeper"],
}

FOOT_DISPLAY_TO_VALUE = {
    "Right": "right",
    "Left": "left",
    "Both": "both",
}

# We use columns to create a clean grid layout
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("👤 Player Profile")
    st.markdown(
        '<p class="control-intro">Use the slider for quick tuning and the numeric input for exact values.</p>',
        unsafe_allow_html=True,
    )

    st.markdown('<p class="control-label">Age at Valuation</p>', unsafe_allow_html=True)
    age_slider_col, age_input_col = st.columns([3.2, 1])
    with age_slider_col:
        st.slider(
            "Age Slider",
            min_value=15.0,
            max_value=45.0,
            step=0.1,
            key="age_slider",
            on_change=sync_age_from_slider,
            label_visibility="collapsed",
        )
    with age_input_col:
        st.number_input(
            "Age Exact",
            min_value=15.0,
            max_value=45.0,
            step=0.1,
            key="age_input",
            on_change=sync_age_from_input,
            format="%.1f",
            label_visibility="collapsed",
        )
    age = float(st.session_state["age_value"])

    st.markdown('<p class="control-label">Height (cm)</p>', unsafe_allow_html=True)
    height_slider_col, height_input_col = st.columns([3.2, 1])
    with height_slider_col:
        st.slider(
            "Height Slider",
            min_value=150.0,
            max_value=210.0,
            step=1.0,
            key="height_slider",
            on_change=sync_height_from_slider,
            label_visibility="collapsed",
        )
    with height_input_col:
        st.number_input(
            "Height Exact",
            min_value=150.0,
            max_value=210.0,
            step=1.0,
            key="height_input",
            on_change=sync_height_from_input,
            format="%.1f",
            label_visibility="collapsed",
        )
    height = float(st.session_state["height_value"])

    position = st.selectbox("Position", ["Attack", "Midfield", "Defender", "Goalkeeper"])
    sub_position = st.selectbox("Sub-Position", POSITION_TO_SUBPOSITIONS[position])
    foot_display = st.selectbox("Foot", ["Right", "Left", "Both"])
    foot = FOOT_DISPLAY_TO_VALUE[foot_display]
    citizenship_default_index = citizenship_options.index("France") if "France" in citizenship_options else 0
    citizenship = st.selectbox(
        "Country of Citizenship",
        options=citizenship_options,
        index=citizenship_default_index,
        help="Type to search countries from the training dataset.",
    )

with col2:
    st.subheader("🏟️ Club & League Context")
    st.markdown(
        '<p class="control-intro">Search clubs by name, or switch to manual Transfermarkt ID when needed.</p>',
        unsafe_allow_html=True,
    )
    valuation_year = st.number_input("Valuation Year", min_value=2000, max_value=2030, value=2026, step=1)

    use_manual_club_id = st.checkbox(
        "Use manual club ID",
        value=False,
        help="Enable this if you cannot find a club name in the searchable list.",
    )
    if use_manual_club_id:
        club_id = st.number_input("Current Club ID (Transfermarkt)", min_value=1, value=583, step=1)
    else:
        default_club_index = next(
            (idx for idx, (club_value, _) in enumerate(club_options) if club_value == 583),
            0,
        )
        selected_club = st.selectbox(
            "Current Club (Transfermarkt)",
            options=club_options,
            index=default_club_index,
            format_func=lambda item: f"{item[1]} (ID: {item[0]})",
            help="Type to search club names and auto-fill the Transfermarkt ID.",
        )
        club_id = int(selected_club[0])

    league_default_index = league_country_options.index("France") if "France" in league_country_options else 0
    country_name = st.selectbox(
        "League Country",
        options=league_country_options,
        index=league_default_index,
        help="Type to search countries from the training dataset.",
    )
    is_major_league = st.selectbox("Is Major National League?", ["True", "False"])

with col3:
    st.subheader("🏆 Career Pedigree (Lifetime Stats)")
    st.markdown(
        '<p class="stat-section-copy">Lifetime totals shown as profile cards.</p>',
        unsafe_allow_html=True,
    )

    car_minutes = render_stat_input_card(
        title="Career Minutes",
        icon="🕒",
        subtitle="Total minutes played",
        input_label="Career Minutes",
        min_value=0.0,
        value=0.0,
        step=90.0,
        key="car_minutes_input",
    )
    car_goals = render_stat_input_card(
        title="Career Goals",
        icon="⚽",
        subtitle="Goals across all competitions",
        input_label="Career Goals",
        min_value=0.0,
        value=0.0,
        step=1.0,
        key="car_goals_input",
    )
    car_assists = render_stat_input_card(
        title="Career Assists",
        icon="🎯",
        subtitle="Direct goal contributions",
        input_label="Career Assists",
        min_value=0.0,
        value=0.0,
        step=1.0,
        key="car_assists_input",
    )
    car_yellow = render_stat_input_card(
        title="Career Yellows",
        icon="🟨",
        subtitle="Disciplinary yellow cards",
        input_label="Career Yellows",
        min_value=0.0,
        value=0.0,
        step=1.0,
        key="car_yellow_input",
    )
    car_red = render_stat_input_card(
        title="Career Reds",
        icon="🟥",
        subtitle="Disciplinary red cards",
        input_label="Career Reds",
        min_value=0.0,
        value=0.0,
        step=1.0,
        key="car_red_input",
    )

st.subheader("📈 Recent Form (Last 365 Days)")
st.markdown(
    '<p class="stat-section-copy">Recent form cards stay constrained by career totals.</p>',
    unsafe_allow_html=True,
)
rcol1, rcol2, rcol3, rcol4, rcol5 = st.columns(5)
with rcol1:
    rec_minutes = render_stat_input_card(
        title="Minutes (365d)",
        icon="🕒",
        subtitle="Recent time on pitch",
        input_label="Minutes Played (365d)",
        min_value=car_minutes,
        value=car_minutes,
        step=90.0,
        key="rec_minutes_input",
    )
with rcol2:
    rec_goals = render_stat_input_card(
        title="Goals (365d)",
        icon="⚽",
        subtitle="Recent scoring output",
        input_label="Goals (365d)",
        min_value=car_goals,
        value=car_goals,
        step=1.0,
        key="rec_goals_input",
    )
with rcol3:
    rec_assists = render_stat_input_card(
        title="Assists (365d)",
        icon="🎯",
        subtitle="Recent chance creation",
        input_label="Assists (365d)",
        min_value=car_assists,
        value=car_assists,
        step=1.0,
        key="rec_assists_input",
    )
with rcol4:
    rec_yellow = render_stat_input_card(
        title="Yellows (365d)",
        icon="🟨",
        subtitle="Recent discipline profile",
        input_label="Yellow Cards (365d)",
        min_value=car_yellow,
        value=car_yellow,
        step=1.0,
        key="rec_yellow_input",
    )
with rcol5:
    rec_red = render_stat_input_card(
        title="Reds (365d)",
        icon="🟥",
        subtitle="Recent red-card incidents",
        input_label="Red Cards (365d)",
        min_value=car_red,
        value=car_red,
        step=1.0,
        key="rec_red_input",
    )

st.divider()

# 5. Prediction Logic & Button
# We use a large, primary button to trigger the calculation
if st.button("🔮 Predict Market Value", use_container_width=True, type="primary"):
    
    # Pack the inputs into a dictionary matching the exact training column names
    input_data = {
        'current_club_id': club_id,
        'position': position,
        'sub_position': sub_position,
        'foot': foot,
        'height_in_cm': height,
        'country_of_citizenship': citizenship,
        'age_at_valuation': age,
        'country_name': country_name,
        'is_major_national_league': is_major_league, # String 'True'/'False' just like our training setup
        'career_minutes_played': car_minutes,
        'career_goals': car_goals,
        'career_assists': car_assists,
        'career_yellow_cards': car_yellow,
        'career_red_cards': car_red,
        'recent_365d_minutes_played': rec_minutes,
        'recent_365d_goals': rec_goals,
        'recent_365d_assists': rec_assists,
        'recent_365d_yellow_cards': rec_yellow,
        'recent_365d_red_cards': rec_red,
        'valuation_year': valuation_year
    }
    
    # Convert dictionary to a 1-row DataFrame
    input_df = pd.DataFrame([input_data])
    
    try:
        # Show a quick loading spinner for UX
        with st.spinner("Calculating valuation..."):
            
            # 1. Apply the Preprocessing Pipeline
            processed_data = preprocessor.transform(input_df)
            
            # 2. Make the Prediction (Returns Log Space)
            log_prediction = model.predict(processed_data)[0]
            
            # 3. Reverse the Log Transformation
            actual_prediction_eur = np.expm1(log_prediction)
        
        # Display the result beautifully!
        st.success("Analysis Complete!")
        
        # Use columns to center the big metric number
        _, center_col, _ = st.columns([1, 2, 1])
        with center_col:
            st.markdown(
                f"""
                <div class="result-card">
                    <div class="result-label">Estimated Market Value</div>
                    <div class="result-value"><span class="result-currency">€</span>{actual_prediction_eur:,.0f}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        
    except Exception as e:
        st.error(f"An error occurred during calculation. Please check your inputs. Error details: {e}")