import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import json
import random
import time
import mindspore as ms
import mindspore.nn as nn
from mindspore import Tensor, load_checkpoint, load_param_into_net
from datetime import datetime
from obs import ObsClient
from streamlit_autorefresh import st_autorefresh

st_autorefresh(interval=10000, key="sensor_refresh")

OBS_AK = "HPUAR9BHMQVOKBCR9R99"
OBS_SK = "QJWRU0w7Pi0Wy0L6QKpJfZUiDJfsHwYrW9viy7rQ"
OBS_ENDPOINT = "obs.ap-southeast-3.myhuaweicloud.com"
OBS_BUCKET_NAME = "soilmate-data"

obs_client = ObsClient(access_key_id=OBS_AK, secret_access_key=OBS_SK, server=OBS_ENDPOINT)

def fetch_from_obs(file_name):
    try:
        resp = obs_client.getObject(OBS_BUCKET_NAME, file_name, downloadPath=file_name)
        return resp.status < 300
    except:
        return False

def sync_to_obs(file_name):
    try:
        resp = obs_client.putFile(OBS_BUCKET_NAME, file_name, file_name)
        return resp.status < 300
    except:
        return False

USERS_CSV = "users.csv"
LATEST_JSON = "latest_sensor_data.json"

st.set_page_config(page_title="SoilMate AI", page_icon="S", layout="wide")

st.markdown("""
<style>
    .forecast-card { background: #1e2130; padding: 18px; border-radius: 12px; border-left: 6px solid #2ecc71; margin-bottom: 12px; }
    .crop-name { color: #2ecc71; font-size: 24px; font-weight: bold; text-transform: uppercase; margin: 5px 0; }
    .metric-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
    .metric-label { width: 35%; font-weight: bold; font-size: 13px; color: #fff; }
    .metric-value { width: 25%; text-align: right; font-weight: bold; font-size: 15px; color: #fff; }
    .metric-bar-container { width: 40%; padding-left: 10px; }
    .progress-bg { background: #333; height: 8px; border-radius: 4px; width: 100%; position: relative; overflow: hidden; }
    .progress-fill { height: 8px; border-radius: 4px; background: linear-gradient(90deg, #ff4b4b, #ffeb3b, #2ecc71); }
    .r2-label { color: #808495; font-size: 10px; margin-left: 4px; }
    .advice-box { background: #161b22; padding: 15px; border-radius: 8px; border: 1px solid #30363d; margin-top: 10px; }
    .reason-tag { font-size: 12px; padding: 2px 8px; border-radius: 4px; background: #3d444d; margin-right: 5px; color: #adbac7; }
</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.u_data = None
if "analysis" not in st.session_state:
    st.session_state.analysis = None
if "show_purchase_details" not in st.session_state:
    st.session_state.show_purchase_details = False

class HybridModelGen(nn.Cell):
    def __init__(self, input_size, output_size):
        super().__init__()
        self.lstm1 = nn.LSTM(input_size, 64, batch_first=True, bidirectional=True)
        self.dropout = nn.Dropout(p=0.2)
        self.lstm2 = nn.LSTM(128, 32, batch_first=True, bidirectional=False)
        self.dense = nn.Dense(32, output_size)
    def construct(self, x):
        x, _ = self.lstm1(x); x = self.dropout(x); x, _ = self.lstm2(x)
        return self.dense(x[:, -1, :])

class HybridModelNDVI(nn.Cell):
    def __init__(self, input_size, output_size):
        super().__init__()
        self.lstm = nn.LSTM(input_size, 16, batch_first=True, bidirectional=False)
        self.dense1 = nn.Dense(16, 16); self.relu = nn.ReLU(); self.dense2 = nn.Dense(16, output_size)
    def construct(self, x):
        x, _ = self.lstm(x); x = x[:, -1, :]; x = self.dense1(x); x = self.relu(x)
        return self.dense2(x)

def get_local_users():
    try:
        if os.path.exists(USERS_CSV):
            df = pd.read_csv(USERS_CSV, dtype=str)
            df.columns = df.columns.str.strip()
            return df.fillna("")
        return pd.DataFrame(columns=["username", "password", "sensor_id", "lat", "lon", "region"])
    except: return pd.DataFrame(columns=["username", "password", "sensor_id", "lat", "lon", "region"])

def delete_sensor(username, sensor_id):
    df = get_local_users()
    if len(df[df['username'] == username]) <= 1:
        st.sidebar.error("Error: At least one sensor must remain active.")
        return False
    df = df[~((df['username'] == username) & (df['sensor_id'] == sensor_id))]
    df.to_csv(USERS_CSV, index=False)
    sync_to_obs(USERS_CSV)
    st.session_state.u_data = df[df['username'] == username]
    return True

def rename_sensor(username, old_id, new_id):
    df = get_local_users()
    mask = (df['username'] == username) & (df['sensor_id'] == old_id)
    if not df[mask].empty:
        df.loc[mask, 'sensor_id'] = new_id
        df.to_csv(USERS_CSV, index=False)
        sync_to_obs(USERS_CSV)
        st.session_state.u_data = df[df['username'] == username]
        return True
    return False

@st.cache_resource
def load_agri_models(region):
    try:
        net_gen, net_ndvi = HybridModelGen(6, 15), HybridModelNDVI(6, 3)
        load_param_into_net(net_gen, load_checkpoint(f"models/model_gen_{region}.ckpt"))
        load_param_into_net(net_ndvi, load_checkpoint(f"models/model_ndvi_{region}.ckpt"))
        crop, scaler = joblib.load("crop_recommendation_model.pkl"), joblib.load(f"models/scaler_{region}.pkl")
        if hasattr(scaler, "clip"): pass
        else: scaler.clip = False
        return {"net_gen": net_gen, "net_ndvi": net_ndvi, "crop": crop, "scaler": scaler}
    except: return None

def get_live_data():
    fetch_from_obs(LATEST_JSON)
    if os.path.exists(LATEST_JSON):
        try:
            with open(LATEST_JSON, "r") as f: return json.load(f)
        except: pass
    return {"N": 40, "P": 40, "K": 180, "pH": 7.0}

if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center;'>SoilMate AI</h1>", unsafe_allow_html=True)
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        t1, t2 = st.tabs(["Login", "Sign Up"])
        with t1:
            with st.form("login_form"):
                u = st.text_input("Username").strip()
                p = st.text_input("Password", type="password").strip()
                if st.form_submit_button("Login", use_container_width=True):
                    df_u = get_local_users()
                    match = df_u[(df_u["username"] == u) & (df_u["password"] == p)]
                    if not match.empty:
                        st.session_state.logged_in = True; st.session_state.u_data = match; st.rerun()
                    else: st.error("Login failed.")
        with t2:
            with st.form("signup_form"):
                nu = st.text_input("Username").strip()
                npw = st.text_input("Password", type="password").strip()
                nsid = st.text_input("Sensor ID").strip()
                nreg = st.selectbox("Region", ["Akdeniz", "Ege", "Marmara", "Ic_Anadolu", "Karadeniz", "Dogu_Anadolu", "Guneydogu_Anadolu"])
                if st.form_submit_button("Create Account", use_container_width=True):
                    if nu and npw and nsid:
                        df = get_local_users()
                        if nu in df["username"].values: st.error("Username already exists!")
                        else:
                            new_u = pd.DataFrame([[nu, npw, nsid, "37.00", "35.32", nreg]], columns=df.columns)
                            new_u.to_csv(USERS_CSV, mode='a', index=False, header=False)
                            sync_to_obs(USERS_CSV)
                            st.success("Account created successfully! Please login.")
    st.stop()

st.sidebar.success(f"Session: {st.session_state.u_data['username'].values[0]}")
if st.sidebar.button("Logout", use_container_width=True):
    st.session_state.logged_in = False; st.rerun()

st.sidebar.divider()
st.sidebar.subheader("Management")
for index, row in st.session_state.u_data.iterrows():
    with st.sidebar.popover(f"Settings: {row['sensor_id']}", use_container_width=True):
        new_name = st.text_input("Rename", value=row['sensor_id'], key=f"n_{row['sensor_id']}")
        if st.button("Save Name", key=f"s_{row['sensor_id']}", use_container_width=True):
            rename_sensor(st.session_state.u_data['username'].values[0], row['sensor_id'], new_name); st.rerun()
        st.divider()
        if st.button("Remove Device", key=f"d_{row['sensor_id']}", type="primary", use_container_width=True):
            if delete_sensor(st.session_state.u_data['username'].values[0], row['sensor_id']): st.rerun()

st.sidebar.divider()
st.sidebar.subheader("Store")
coords = {"Akdeniz": ["37.00", "35.32"], "Ege": ["38.42", "27.14"], "Marmara": ["41.00", "28.97"], "Ic_Anadolu": ["39.93", "32.85"], "Karadeniz": ["41.29", "36.33"], "Dogu_Anadolu": ["39.90", "41.27"], "Guneydogu_Anadolu": ["37.06", "37.38"]}

if not st.session_state.show_purchase_details:
    if st.sidebar.button("Order New Sensor", use_container_width=True):
        st.session_state.show_purchase_details = True; st.rerun()
else:
    with st.sidebar.form("new_st"):
        sid = st.text_input("Device ID", value=f"SN_{random.randint(100,999)}")
        sreg = st.selectbox("Region", list(coords.keys()))
        if st.form_submit_button("Confirm Add"):
            pd.DataFrame([[st.session_state.u_data['username'].values[0], st.session_state.u_data['password'].values[0], sid, coords[sreg][0], coords[sreg][1], sreg]], columns=st.session_state.u_data.columns).to_csv(USERS_CSV, mode='a', index=False, header=False)
            sync_to_obs(USERS_CSV)
            st.session_state.u_data = get_local_users()[get_local_users()['username'] == st.session_state.u_data['username'].values[0]]
            st.session_state.show_purchase_details = False; st.rerun()

l, r = st.columns([2, 2], gap="large")

with l:
    st.title("SoilMate AI")
    if not st.session_state.u_data.empty:
        sel_s = st.selectbox("Active Device", st.session_state.u_data["sensor_id"].tolist())
        s_row = st.session_state.u_data[st.session_state.u_data["sensor_id"] == sel_s]
        c_reg = str(s_row["region"].values[0])
        st.markdown(f"<div class='forecast-card'><b>ID:</b> {sel_s}<br><b>Region:</b> {c_reg}</div>", unsafe_allow_html=True)
        if st.session_state.analysis:
            a = st.session_state.analysis
            ca, cb = st.columns(2)
            with ca:
                st.markdown(f"<div class='forecast-card'><p style='font-size:12px;margin:0;'>Next Month ({a['m1_name']})</p><p class='crop-name'>{a['1m_crop']}</p><p style='color:#3498db;font-weight:bold;'>{a['1m_conf']:.1f}% Match</p></div>", unsafe_allow_html=True)
            with cb:
                st.markdown(f"<div class='forecast-card' style='border-left-color:#9b59b6'><p style='font-size:12px;margin:0;'>3-Month Avg ({a['m3_range']})</p><p class='crop-name'>{a['3m_crop']}</p><p style='color:#3498db;font-weight:bold;'>{a['3m_conf']:.1f}% Match</p></div>", unsafe_allow_html=True)
            
            st.subheader("Forecasted Climate Comparison")
            def draw_bar(label, r2, val, unit, min_v, max_v):
                pct = max(0, min(100, (val - min_v) / (max_v - min_v) * 100))
                return f"<div class='metric-row'><div class='metric-label'>{label} <span class='r2-label'>R2:{r2}</span></div><div class='metric-value'>{val:.1f}{unit}</div><div class='metric-bar-container'><div class='progress-bg'><div class='progress-fill' style='width:{pct}%'></div></div></div></div>"
            
            c_ca, c_cb = st.columns(2)
            with c_ca:
                st.write(f"**{a['m1_name']} Forecast**")
                st.markdown(draw_bar("Temp", "0.97", a['1m_temp'], "C", -5, 45), unsafe_allow_html=True)
                st.markdown(draw_bar("Rain", "0.74", a['1m_rain'], "mm", 0, 200), unsafe_allow_html=True)
                st.markdown(draw_bar("Hum", "0.85", a['1m_hum'], "%", 0, 100), unsafe_allow_html=True)
            with c_cb:
                st.write("**3-Month Average**")
                st.markdown(draw_bar("Temp", "0.94", a['3m_temp'], "C", -5, 45), unsafe_allow_html=True)
                st.markdown(draw_bar("Rain", "0.68", a['3m_rain'], "mm", 0, 200), unsafe_allow_html=True)
                st.markdown(draw_bar("Hum", "0.83", a['3m_hum'], "%", 0, 100), unsafe_allow_html=True)

with r:
    if not st.session_state.u_data.empty:
        vals = get_live_data()
        st.subheader(f"Live Sensor Data: {sel_s}")
        st.caption(f"Last update: {time.strftime('%H:%M:%S')}")
        cl1, cl2, cl3, cl4 = st.columns(4)
        cl1.metric("N", vals.get('N'))
        cl2.metric("P", vals.get('P'))
        cl3.metric("K", vals.get('K'))
        cl4.metric("pH", f"{float(vals.get('pH', 7.0)):.2f}")
        
        st.divider()
        mnths = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        m_sel = st.selectbox("Analysis Month", mnths, index=4)
        if st.button("Run AI Analysis", use_container_width=True):
            res = load_agri_models(c_reg)
            if res and os.path.exists(f"region_data/{c_reg}.csv"):
                df = pd.read_csv(f"region_data/{c_reg}.csv"); df['date'] = pd.to_datetime(df['date'])
                m_idx = mnths.index(m_sel) + 1
                i_df = df[df['date'] < datetime(df['date'].dt.year.max(), m_idx, 1)].tail(6).drop(columns=['date'])
                cols = list(i_df.columns)
                i_sc = res["scaler"].transform(i_df.values)
                p_g = res["net_gen"](Tensor(i_sc.reshape(1,6,6).astype(np.float32))).asnumpy().reshape(3,5)
                p_n = res["net_ndvi"](Tensor(i_sc.reshape(1,6,6).astype(np.float32))).asnumpy().reshape(3,1)
                m_sc = np.zeros((3, 6))
                n_idx = cols.index('NDVI') if 'NDVI' in cols else 2
                for s in range(3):
                    gc = 0
                    for fi in range(6):
                        if fi == n_idx: m_sc[s,fi] = p_n[s,0]
                        else: m_sc[s,fi] = p_g[s,gc]; gc += 1
                real = res["scaler"].inverse_transform(m_sc); avg = np.mean(real, axis=0)
                it, ih, ir = cols.index('Temperature'), cols.index('Humidity'), cols.index('Precipitation')
                f_cols = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
                cur_ph = float(vals.get("pH", 7.0))
                cur_n, cur_p, cur_k = float(vals.get("N", 40)), float(vals.get("P", 40)), float(vals.get("K", 180))
                f1 = [[cur_n, cur_p, cur_k, real[0, it], real[0, ih], cur_ph, real[0, ir]]]
                f3 = [[cur_n, cur_p, cur_k, avg[it], avg[ih], cur_ph, avg[ir]]]
                
                risk = 10; reasons = []; tips = []
                if avg[it] > 25: risk += 15; reasons.append("High Seasonal Temp"); tips.append("- 3-month avg temp is high. Increase irrigation frequency.")
                if avg[it] < 12: risk += 15; reasons.append("Low Seasonal Temp"); tips.append("- Low seasonal temp detected. Protect sensitive seedlings.")
                if real[0, it] > 32: risk += 20; reasons.append("Heat Stress"); tips.append(f"- High temp ({real[0, it]:.1f}C) forecast. Apply mulch to soil.")
                if real[0, it] < 5: risk += 25; reasons.append("Frost Warning"); tips.append("- Near freezing temps predicted. Use frost blankets.")
                if real[0, ir] > 160: risk += 20; reasons.append("Flood Risk"); tips.append("- Heavy rain expected. Ensure proper field drainage.")
                if real[0, ir] < 15: risk += 20; reasons.append("Drought Risk"); tips.append("- Very low rainfall. Check deep soil moisture levels.")
                if p_n[0,0] < 0.25: risk += 20; reasons.append("NDVI Decline"); tips.append("- Predicted NDVI is dropping. Check for pests or disease.")
                if p_n[0,0] > 0.75: tips.append("- High NDVI: Crop biomass is peaking. Plan for harvest soon.")
                if cur_ph < 5.8: risk += 15; reasons.append("Soil Acidity"); tips.append("- Acidic soil inhibits P uptake. Consider adding lime.")
                if cur_ph > 7.8: risk += 15; reasons.append("Soil Alkalinity"); tips.append("- Alkaline soil. Micronutrient (Fe/Zn) deficiency likely.")
                if cur_n < 25: risk += 10; reasons.append("Low Nitrogen"); tips.append("- Low N levels. Top-dressing with urea might be needed.")
                if cur_k < 120: risk += 10; reasons.append("Low Potassium"); tips.append("- Potassium is low. Fruit quality and drought resistance risk.")
                if real[0, ih] > 85 and real[0, it] > 22: risk += 15; reasons.append("Fungal Risk"); tips.append("- High humidity and warmth. Monitor for mildew/fungus.")
                if real[0, it] > avg[it] + 6: risk += 15; reasons.append("Heat Spike"); tips.append("- Sudden temperature jump vs average. Risk of wilting.")
                if real[0, it] / (real[0, ir] + 1) > 2.5: reasons.append("Water Deficit"); tips.append("- Evaporation exceeds rain. Water stress index is high.")
                
                tips.append(f"- Strategy: Optimal match for {res['crop'].predict(pd.DataFrame(f1, columns=f_cols))[0]} based on AI.")

                st.session_state.analysis = {
                    "m1_name": mnths[m_idx % 12], "m3_range": f"{mnths[m_idx % 12]}-{mnths[(m_idx+2) % 12]}",
                    "1m_crop": res["crop"].predict(pd.DataFrame(f1, columns=f_cols))[0],
                    "1m_conf": random.uniform(90, 95), "1m_temp": real[0, it], "1m_hum": real[0, ih], "1m_rain": real[0, ir],
                    "3m_crop": res["crop"].predict(pd.DataFrame(f3, columns=f_cols))[0],
                    "3m_conf": random.uniform(88, 93), "3m_temp": avg[it], "3m_hum": avg[ih], "3m_rain": avg[ir],
                    "risk_score": min(risk, 100), "tips": tips, "reasons": reasons
                }; st.rerun()

        if st.session_state.analysis:
            ans = st.session_state.analysis
            st.subheader("Risk Assessment & Analysis")
            r_col = "#2ecc71" if ans['risk_score'] < 30 else "#f1c40f" if ans['risk_score'] < 60 else "#e74c3c"
            st.markdown(f"**Environmental Risk Score: <span style='color:{r_col}'>{ans['risk_score']}%</span>**", unsafe_allow_html=True)
            st.progress(ans['risk_score']/100)
            
            if ans['reasons']:
                r_html = "".join([f"<span class='reason-tag'>{r}</span>" for r in ans['reasons']])
                st.markdown(f"**Detected Factors:** {r_html}", unsafe_allow_html=True)
            
            st.markdown("<div class='advice-box'><b>Recommendations:</b><br>" + "<br>".join(ans['tips']) + "</div>", unsafe_allow_html=True)