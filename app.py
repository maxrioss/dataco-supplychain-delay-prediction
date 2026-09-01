import streamlit as st
import pandas as pd
import joblib

# Configuración de la interfaz
st.set_page_config(page_title="Predicción de Retrasos - Logística", layout="centered")

st.title("🚚 Predicción de Riesgo de Retraso en Envíos")
st.write("Ingrese los detalles de la orden para predecir si la entrega se retrasará.")

# Cargar modelo y columnas guardadas
@st.cache_resource
def load_assets():
    model = joblib.load('random_forest_model.pkl')
    columns = joblib.load('model_columns.pkl')
    return model, columns

model, model_columns = load_assets()

# Formulario de entrada de datos
st.subheader("Datos de la Orden")

shipping_mode = st.selectbox("Modo de Envío", ["Standard Class", "First Class", "Same Day", "Second Class"])
order_hour = st.slider("Hora de la Orden (0-23)", 0, 23, 12)
latitude = st.number_input("Latitud de Destino", value=18.25)
longitude = st.number_input("Longitud de Destino", value=-66.03)
sales = st.number_input("Ventas por Cliente ($)", value=100.0)

# Botón para predecir
if st.button("Evaluar Riesgo de Retraso"):
    # Crear un DataFrame con ceros alineado a las columnas que espera el modelo
    input_data = pd.DataFrame(0, index=[0], columns=model_columns)
    
    # Asignar los valores ingresados por el usuario
    if 'order hour' in input_data.columns:
        input_data['order hour'] = order_hour
    if 'Latitude' in input_data.columns:
        input_data['Latitude'] = latitude
    if 'Longitude' in input_data.columns:
        input_data['Longitude'] = longitude
    if 'Sales per customer' in input_data.columns:
        input_data['Sales per customer'] = sales
        
    # Mapear la variable categórica seleccionada a su columna OHE
    ship_col = f"Shipping Mode_{shipping_mode}"
    if ship_col in input_data.columns:
        input_data[ship_col] = 1

    # Realizar predicción
    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]

    st.markdown("---")
    if prediction == 1:
        st.error(f"⚠️ **ALTO RIESGO DE RETRASO** (Probabilidad: {probability:.1%})")
    else:
        st.success(f"✅ **ENTREGA A TIEMPO PROBABLE** (Probabilidad de retraso: {probability:.1%})")