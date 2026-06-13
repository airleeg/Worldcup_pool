import streamlit as st
import pandas as pd

st.set_page_config(page_title="2026 World Cup Pool Hub", layout="wide", page_icon="🏆")

# -------------------------------------------------------------
# 1. LIVE DATA CONNECTION (Google Sheets Integration)
# -------------------------------------------------------------
# Replace this with your actual public "Anyone with link can view" Google Sheet URL
SHEET_URL = "https://docs.google.com/spreadsheets/d/10ROPQBPSBo-gsLvla_KkRNHqbzjxF1RTrnODUnCXiMI/edit?usp=drivesdk"
def load_data():
    try:
        # 1. Clean the end of your specific Google Sheet link to allow tab switching
        clean_url = SHEET_URL.split("/edit")[0]
        
        # 2. Build the correct direct download links for BOTH of your tabs
        csv_url_draws = f"{clean_url}/gviz/tq?tqx=out:csv&sheet=Draws"
        csv_url_standings = f"{clean_url}/gviz/tq?tqx=out:csv&sheet=Standings"
        
        # 3. Read the data tables into the app
        draws = pd.read_csv(csv_url_draws)
        standings = pd.read_csv(csv_url_standings)
        
        return draws, standings
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return pd.DataFrame(), pd.DataFrame()

draws_df, standings_df = load_data()

# -------------------------------------------------------------
# 2. GLOBAL CALCULATION LOGIC
# -------------------------------------------------------------
total_picks = len(draws_df) if not draws_df.empty else 0
total_pot = total_picks * 5

# -------------------------------------------------------------
# 3. HEADER & METRICS DISPLAY
# -------------------------------------------------------------
st.title("🏆 Soccer Team World Cup 2026 Pool Hub")
st.markdown("### Live Standings, Outright Odds & In-Person Chip Tracking")
st.markdown("Each week for the first 2 weeks, pick a chip randomly out of the bag for **$5**. Multiple players can pull the same team. The total pot is split among everyone aligned to the winning team at the end!")

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Live Pot", f"${total_pot}.00")
col2.metric("🎟️ Active Chips in Play", f"{total_picks} Draws")
col3.metric("🎫 Cost Per Chip Pull", "$5.00")

st.markdown("---")

# -------------------------------------------------------------
# 4. INTERFACE TABS
# -------------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["📊 Group Standings & Odds", "👥 Who Owns What?", "🏁 Payout Calculator"])

with tab1:
    st.subheader("Current Tournament Pools & Live Vegas Odds")
    if not standings_df.empty:
        # Dynamic filter dropdown
        group_list = sorted(standings_df["Group"].unique())
        selected_group = st.selectbox("Select a Pool to View:", group_list)
        
        # Filter and sort data cleanly
        filtered_data = standings_df[standings_df["Group"] == selected_group].sort_values(by=["Pts", "GD"], ascending=False)
        st.dataframe(filtered_data, use_container_width=True, hide_index=True)
    else:
        st.info("Awaiting tournament data initialization in your Google Sheet.")

with tab2:
    st.subheader("Active Team Chips Held by Players")
    if not draws_df.empty:
        st.dataframe(draws_df, use_container_width=True, hide_index=True)
    else:
        st.warning("No chips have been registered yet. Track draws on your master Google Sheet to populate this list.")

with tab3:
    st.subheader("Dynamic End-of-Tournament Pot Splitter")
    st.markdown("When a team lifts the trophy on July 19, select them below to see exactly who gets paid and how much.")
    
    if not standings_df.empty and not draws_df.empty:
        all_teams = sorted(standings_df["Team"].unique())
        champion = st.selectbox("Select the Crowned World Cup Champion:", all_teams)
        
        # Find all rows matching the champion selection
        winning_tickets = draws_df[draws_df["Team Chosen"] == champion]
        winners_list = winning_tickets["Player"].tolist()
        
        if st.button("Calculate Final Dividends"):
            if len(winners_list) > 0:
                payout_share = total_pot / len(winners_list)
                st.balloons()
                st.success(f"🎉 **{champion} has won the FIFA World Cup!**")
                st.markdown(f"### **The total pot of ${total_pot}.00 is split among {len(winners_list)} winner(s):**")
                
                # Render clean results
                for player in winners_list:
                    st.markdown(f"🥇 **{player}** wins **${payout_share:,.2f}**")
            else:
                st.error(f"Nobody pulled a chip for {champion} during Weeks 1 or 2! The pot rolls over to the team party fund.")
    else:
        st.info("Data must be loaded in order to calculate tournament payouts.")
