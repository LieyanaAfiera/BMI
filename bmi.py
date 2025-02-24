import streamlit as st
import pandas as pd
import io

# Streamlit page config
st.set_page_config(page_title="BMI Tracker", page_icon="⚖️", layout="centered")

# Custom CSS for professional styling
st.markdown(
    """
    <style>
        body { background-color: #F7F7F7; }
        .main-title { text-align: center; color: #4A4A4A; font-size: 32px; font-weight: bold; }
        .sub-title { text-align: center; color: #6D6D6D; font-size: 18px; }
        .bmi-card {
            padding: 15px; 
            border-radius: 10px; 
            background-color: #EDEDED;
            text-align: center;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
        }
        .bmi-category { font-size: 22px; font-weight: bold; color: #2C3E50; }
        .bmi-value { font-size: 28px; font-weight: bold; color: #1C2833; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title & Description
st.markdown("<h1 class='main-title'>BMI Tracker ⚖️</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Monitor your BMI and maintain a balanced lifestyle.</p>", unsafe_allow_html=True)

# Initialize session state for BMI records
if "bmi_data" not in st.session_state:
    st.session_state.bmi_data = []

# Sidebar for inputs
st.sidebar.header("Enter Your Details")
name = st.sidebar.text_input("Name")
weight = st.sidebar.number_input("Weight (kg)", min_value=1.0, format="%.2f")
height = st.sidebar.number_input("Height (m)", min_value=0.5, format="%.2f")

# Function to calculate BMI
def calculate_bmi(weight, height):
    return round(weight / (height ** 2), 2)

# Function to categorize BMI with professional labels
def categorize_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal Weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"

# Button to calculate and store BMI
if st.sidebar.button("Calculate & Save BMI", use_container_width=True):
    if name and weight > 0 and height > 0:
        bmi = calculate_bmi(weight, height)
        category = categorize_bmi(bmi)

        # Append to session state
        st.session_state.bmi_data.append({"Name": name, "Weight (kg)": weight, "Height (m)": height, "BMI": bmi, "Category": category})

        # Display result with a styled card
        st.markdown(
            f"""
            <div class='bmi-card'>
                <h3 style="color: #34495E;">{name}'s BMI Result</h3>
                <p class="bmi-value">{bmi}</p>
                <p class="bmi-category">{category}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Progress bar for BMI visualization
        st.progress(min(bmi / 40, 1.0))  # Normalizing BMI for progress bar
    else:
        st.error("Please enter valid details!")

# Display stored BMI records
if st.session_state.bmi_data:
    st.subheader("📜 BMI Records")

    df = pd.DataFrame(st.session_state.bmi_data)

    # Styled DataFrame
    st.dataframe(df.style.set_properties(**{"background-color": "#F5F5F5", "color": "#333"}))

    # Download as CSV
    st.download_button("📥 Download CSV", df.to_csv(index=False), "bmi_data.csv", "text/csv")

    # ✅ Fixed: Download as Excel
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
        writer.close()

    st.download_button(
        label="📥 Download Excel",
        data=excel_buffer.getvalue(),
        file_name="bmi_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
