import streamlit as st
import pandas as pd

st.set_page_config(page_title="2026 World Cup Pool Hub", layout="wide", page_icon="🏆")

# -------------------------------------------------------------
# 1. LIVE DATA CONNECTIONS (Google Sheets & Live Standings API)
# -------------------------------------------------------------
# Your active player tracking sheet
SHEET_URL = "https://docs.google.com/spreadsheets/d/10ROPQBPSBo-gsLvla_KkRNHqbzjxF1RTrnODUnCXiMI/edit?usp=drivesdk"

@st.cache_data(ttl=300) # Caches data for 5 minutes so it loads instantly but stays fresh
def load_all_data():
    try:
        # --- PART A: Load Custom Player Draws from Google Sheets ---
        clean_url = SHEET_URL.split("/edit")[0]
        csv_url_draws = f"{clean_url}/gviz/tq?tqx=out:csv&sheet=Draws"
        draws = pd.read_csv(csv_url_draws)
        
        # --- PART B: Fetch AUTOMATIC, LIVE 2026 Standings ---
        # Scrapes the live, official group tables dynamically
        url = "https://fbref.com/en/comps/1/WC-Stats"
        tables = pd.read_html(url)
        
        all_groups = []
        # Groups A through L are captured dynamically from the web matrix
        for i in range(1, 13): 
            df = tables[i].copy()
            df.columns = ['Pos', 'Team', 'Pts', 'GD'] # Normalize columns cleanly
            # Assign correct group letter based on table index loop
            df['Group'] = chr(64 + i) 
            all_groups.append(df)
            
        standings = pd.concat(all_groups, ignore_index=True)
        
        # Clean up country name suffixes appended by web servers
        standings['Team'] = standings['Team'].str.replace(r'\s*([a-z])\b.*', '', regex=True)
        
        return draws, standings
    except Exception as e:
        # Fallback to prevent app crashes if web scrapers hit a high-traffic rate limit
        st.error(f"Live Feed Syncing delayed. Error tracking: {e}")
        return pd.DataFrame(), pd.DataFrame()

draws_df, standings_df = load_all_data()

# -------------------------------------------------------------
# 2. GLOBAL CALCULATION LOGIC
# -------------------------------------------------------------
total_picks = len(draws_df) if not draws_df.empty else 0
total_pot = total_picks * 5

# -------------------------------------------------------------
# 3. HEADER & METRICS DISPLAY
# -------------------------------------------------------------
st.title("🏆 Soccer Team World Cup 2026 Pool Hub")
st.markdown("### ⚡ Live Standings Feed (Fully Automated) & Chip Tracker")
st.markdown("Standings, points, and goal differentials update automatically as matches finish. Your sheet only tracks player chip draws!")

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Live Pot", f"${total_pot}.00")
col2.metric("🎟️ Active Chips in Play", f"{total_picks} Draws")
col3.metric("🎫 Cost Per Chip Pull", "$5.00")

st.markdown("---")

# -------------------------------------------------------------
# 4. INTERFACE TABS
# -------------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["📊 Live Group Standings", "👥 Who Owns What?", "🏁 Payout Calculator"])

with tab1:
    st.subheader("Current Tournament Pools (Live Data)")
    if not standings_df.empty:
        group_list = sorted(standings_df["Group"].unique())
        selected_group = st.selectbox("Select a Pool to View:", group_list)
        
        filtered_data = standings_df[standings_df["Group"] == selected_group].sort_values(by=["Pts", "GD"], ascending=False)
        st.dataframe(filtered_data[['Pos', 'Team', 'Pts', 'GD']], use_container_width=True, hide_index=True)
    else:
        st.info("Syncing with tournament data server...")

with tab2:
    st.subheader("Active Team Chips Held by Players")
    if not draws_df.empty:
        st.dataframe(draws_df, use_container_width=True, hide_index=True)
    else:
        st.warning("No chips have been registered yet. Track draws on your master Google Sheet to populate this list.")

with tab3:
    st.subheader("Dynamic End-of-Tournament Pot Splitter")
    st.markdown("When a team lifts the trophy on July 19, select them below to calculate the payout divide.")
    
    if not standings_df.empty and not draws_df.empty:
        all_teams = sorted(standings_df["Team"].unique())
        champion = st.selectbox("Select the Crowned World Cup Champion:", all_teams)
        
        winning_tickets = draws_df[draws_df["Team Chosen"].str.contains(champion, case=False, na=False)] if not draws_df.empty else pd.DataFrame()
        winners_list = winning_tickets["Player"].tolist() if not winning_tickets.empty else []
        
        if st.button("Calculate Final Dividends"):
            if len(winners_list) > 0:
                payout_share = total_pot / len(winners_list)
                st.balloons()
                st.success(f"🎉 **{champion} has won the FIFA World Cup!**")
                st.markdown(f"### **The total pot of ${total_pot}.00 is split among {len(winners_list)} winner(s):**")
                
                for player in winners_list:
                    st.markdown(f"🥇 **{player}** wins **${payout_share:,.2f}**")
            else:
                st.error(f"Nobody pulled a chip for {champion}. The pot rolls over to the team party fund!")
    else:
        st.info("Data must be loaded in order to calculate tournament payouts.")
