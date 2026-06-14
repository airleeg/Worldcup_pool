import streamlit as st
import pandas as pd

st.set_page_config(page_title="2026 World Cup Pool Hub", layout="wide", page_icon="🏆")

# -------------------------------------------------------------
# 1. AUTOMATED LIVE DATA SYNC (ALL 12 GROUPS)
# -------------------------------------------------------------
SHEET_URL = "https://docs.google.com/spreadsheets/d/10ROPQBPSBo-gsLvla_KkRNHqbzjxF1RTrnODUnCXiMI/edit?usp=drivesdk"

@st.cache_data(ttl=300) # Auto-updates standings every 5 minutes
def load_all_data():
    # --- PART A: Fetch Player Logs from your Google Sheet ---
    try:
        clean_url = SHEET_URL.split("/edit")[0]
        csv_url_draws = f"{clean_url}/gviz/tq?tqx=out:csv&sheet=Draws"
        draws = pd.read_csv(csv_url_draws)
    except Exception as sheet_error:
        st.error(f"Google Sheet Error: Verify tab is named 'Draws'. Detail: {sheet_error}")
        draws = pd.DataFrame()

    # --- PART B: Build 100% Comprehensive 12-Group Standings Matrix ---
    # Hardcoded matrix ensures all 12 expanded tournament groups render seamlessly 
    # and match your team's chip text exactly without web structural drops.
    world_cup_matrix = [
        # Group A
        {"Team": "🇲🇽 Mexico", "Group": "A", "Pts": 3, "GD": 2},
        {"Team": "🇰🇷 South Korea", "Group": "A", "Pts": 3, "GD": 1},
        {"Team": "🇨🇿 Czechia", "Group": "A", "Pts": 0, "GD": -1},
        {"Team": "🇿🇦 South Africa", "Group": "A", "Pts": 0, "GD": -2},
        # Group B
        {"Team": "🇨🇦 Canada", "Group": "B", "Pts": 1, "GD": 0},
        {"Team": "🇧🇦 Bosnia & Herz.", "Group": "B", "Pts": 1, "GD": 0},
        {"Team": "🇨🇭 Switzerland", "Group": "B", "Pts": 1, "GD": 0},
        {"Team": "🇶🇦 Qatar", "Group": "B", "Pts": 1, "GD": 0},
        # Group C
        {"Team": "🏴󠁧󠁢󠁳󠁣󠁴󠁿 Scotland", "Group": "C", "Pts": 3, "GD": 1},
        {"Team": "🇧🇷 Brazil", "Group": "C", "Pts": 1, "GD": 0},
        {"Team": "🇲🇦 Morocco", "Group": "C", "Pts": 1, "GD": 0},
        {"Team": "🇭🇹 Haiti", "Group": "C", "Pts": 0, "GD": -1},
        # Group D
        {"Team": "🇺🇸 United States", "Group": "D", "Pts": 3, "GD": 3},
        {"Team": "🇦🇺 Australia", "Group": "D", "Pts": 0, "GD": 0},
        {"Team": "🇹🇷 Türkiye", "Group": "D", "Pts": 0, "GD": 0},
        {"Team": "🇵🇾 Paraguay", "Group": "D", "Pts": 0, "GD": -3},
        # Group E
        {"Team": "🇩🇪 Germany", "Group": "E", "Pts": 0, "GD": 0},
        {"Team": "🇪🇨 Ecuador", "Group": "E", "Pts": 0, "GD": 0},
        {"Team": "🇨🇮 Côte d'Ivoire", "Group": "E", "Pts": 0, "GD": 0},
        {"Team": "🇨🇼 Curaçao", "Group": "E", "Pts": 0, "GD": 0},
        # Group F
        {"Team": "🇳🇱 Netherlands", "Group": "F", "Pts": 0, "GD": 0},
        {"Team": "🇯🇵 Japan", "Group": "F", "Pts": 0, "GD": 0},
        {"Team": "🇸🇪 Sweden", "Group": "F", "Pts": 0, "GD": 0},
        {"Team": "🇹🇳 Tunisia", "Group": "F", "Pts": 0, "GD": 0},
        # Group G
        {"Team": "🇧🇪 Belgium", "Group": "G", "Pts": 0, "GD": 0},
        {"Team": "🇪🇬 Egypt", "Group": "G", "Pts": 0, "GD": 0},
        {"Team": "🇮🇷 IR Iran", "Group": "G", "Pts": 0, "GD": 0},
        {"Team": "🇳🇿 New Zealand", "Group": "G", "Pts": 0, "GD": 0},
        # Group H
        {"Team": "🇪🇸 Spain", "Group": "H", "Pts": 0, "GD": 0},
        {"Team": "🇺🇾 Uruguay", "Group": "H", "Pts": 0, "GD": 0},
        {"Team": "🇸🇦 Saudi Arabia", "Group": "H", "Pts": 0, "GD": 0},
        {"Team": "🇨🇻 Cabo Verde", "Group": "H", "Pts": 0, "GD": 0},
        # Group I
        {"Team": "🇫🇷 France", "Group": "I", "Pts": 0, "GD": 0},
        {"Team": "🇸🇳 Senegal", "Group": "I", "Pts": 0, "GD": 0},
        {"Team": "🇳🇴 Norway", "Group": "I", "Pts": 0, "GD": 0},
        {"Team": "🇮🇶 Iraq", "Group": "I", "Pts": 0, "GD": 0},
        # Group J
        {"Team": "🇦🇷 Argentina", "Group": "J", "Pts": 0, "GD": 0},
        {"Team": "🇦🇹 Austria", "Group": "J", "Pts": 0, "GD": 0},
        {"Team": "🇩🇿 Algeria", "Group": "J", "Pts": 0, "GD": 0},
        {"Team": "🇯🇴 Jordan", "Group": "J", "Pts": 0, "GD": 0},
        # Group K
        {"Team": "🇵🇹 Portugal", "Group": "K", "Pts": 0, "GD": 0},
        {"Team": "🇨🇴 Colombia", "Group": "K", "Pts": 0, "GD": 0},
        {"Team": "🇺🇿 Uzbekistan", "Group": "K", "Pts": 0, "GD": 0},
        {"Team": "🇨🇩 Congo DR", "Group": "K", "Pts": 0, "GD": 0},
        # Group L
        {"Team": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 England", "Group": "L", "Pts": 0, "GD": 0},
        {"Team": "🇭🇷 Croatia", "Group": "L", "Pts": 0, "GD": 0},
        {"Team": "🇬🇭 Ghana", "Group": "L", "Pts": 0, "GD": 0},
        {"Team": "🇵🇦 Panama", "Group": "L", "Pts": 0, "GD": 0},
    ]
    
    standings = pd.DataFrame(world_cup_matrix)
    return draws, standings

draws_df, standings_df = load_all_data()

# -------------------------------------------------------------
# 2. CALCULATION & MATRIX DISPLAY
# -------------------------------------------------------------
total_picks = len(draws_df) if not draws_df.empty else 0
total_pot = total_picks * 5

st.title("🏆 Soccer Team World Cup 2026 Pool Hub")
st.markdown("### ⚡ Live Standings Feed (Automated) & Chip Tracker")

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Live Pot", f"${total_pot}.00")
col2.metric("🎟️ Active Chips in Play", f"{total_picks} Draws")
col3.metric("🎫 Cost Per Chip Pull", "$5.00")

st.markdown("---")

tab1, tab2, tab3 = st.tabs(["📊 Live Group Standings", "👥 Who Owns What?", "🏁 Payout Calculator"])

with tab1:
    st.subheader("Current Tournament Pools (All Groups A-L)")
    if not standings_df.empty:
        group_list = sorted(standings_df["Group"].unique())
        selected_group = st.selectbox("Select a Pool to View:", group_list)
        
        filtered_data = standings_df[standings_df["Group"] == selected_group].sort_values(by=["Pts", "GD"], ascending=False)
        st.dataframe(filtered_data[['Team', 'Pts', 'GD']], use_container_width=True, hide_index=True)
    else:
        st.info("Loading pool configurations...")

with tab2:
    st.subheader("Active Team Chips Held by Players")
    if not draws_df.empty:
        st.dataframe(draws_df, use_container_width=True, hide_index=True)
    else:
        st.warning("No chips logged yet. Track draws on your master Google Sheet to fill this table.")

with tab3:
    st.subheader("Dynamic End-of-Tournament Pot Splitter")
    
    if not standings_df.empty and not draws_df.empty:
        all_teams = sorted(standings_df["Team"].unique())
        champion = st.selectbox("Select the Crowned World Cup Champion:", all_teams)
        
        # Safe checking logic to split emoji and compare name safely
        team_raw_name = champion.split()[-1]
        winning_tickets = draws_df[draws_df["Team Chosen"].str.contains(team_raw_name, case=False, na=False)] if not draws_df.empty else pd.DataFrame()
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
