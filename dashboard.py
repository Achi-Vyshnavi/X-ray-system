import streamlit as st
import pandas as pd
import json
import plotly.express as px
st.markdown("""
    <style>
    .stApp {
        background-color: #F6F0F0;  /* pastel purple */
    }
    </style>
""", unsafe_allow_html=True)
# Load X-Ray log
with open("xray_log.json") as f:
    logs = json.load(f)

st.set_page_config(page_title="X-Ray Dashboard", layout="wide")
st.title("🚀 X-Ray Decision Dashboard")
st.markdown("Visualize multi-step decision-making and candidate evaluations")

# Collect all candidates for summary
all_candidates = []
for step in logs:
    if "evaluations" in step:
        for e in step["evaluations"]:
            e_copy = e.copy()
            e_copy["step"] = step["step"]
            all_candidates.append(e_copy)

# Summary metrics
if all_candidates:
    total_candidates = len(all_candidates)
    passed_filters = sum(1 for c in all_candidates if c.get("qualified"))
    top_candidates = [c["title"] for c in all_candidates if c.get("asin")==logs[-1]["output"]["selection"]["asin"]] if logs[-1]["output"].get("selection") else ["N/A"]
    
    st.markdown("### 📊 Summary Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Candidates", total_candidates)
    col2.metric("Passed Filters", passed_filters)
    col3.metric("Top Candidate", ", ".join(top_candidates))
    
    # Summary bar chart (EasyBI style)
    summary_df = pd.DataFrame({"Status": ["Passed", "Failed"], 
                               "Count": [passed_filters, total_candidates - passed_filters]})
    fig_summary = px.bar(summary_df, x="Status", y="Count", color="Status", text="Count",
                         color_discrete_map={"Passed": "lightgreen", "Failed": "lightcoral"})
    st.plotly_chart(fig_summary, use_container_width=True)

# Display each step
for step in logs:
    with st.expander(f"{step['step']} ({step.get('timestamp','')})", expanded=False):
        
        # Input & Output side by side
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Input")
            st.json(step.get("input", {}), expanded=False)
        with col2:
            st.subheader("Output")
            st.json(step.get("output", {}), expanded=False)
        
        # Reasoning
        st.subheader("Reasoning")
        st.write(step.get("reasoning", ""))

        # Candidate Evaluations
        if "evaluations" in step:
            st.subheader("Candidate Evaluations")
            evals = step["evaluations"]
            df = pd.DataFrame([
                {
                    "Title": e["title"],
                    "Price": e["metrics"]["price"],
                    "Rating": e["metrics"]["rating"],
                    "Reviews": e["metrics"]["reviews"],
                    "Qualified": "✅" if e["qualified"] else "❌",
                    "Top Candidate": "⭐" if step.get("output", {}).get("selection") and e["asin"]==step["output"]["selection"]["asin"] else ""
                }
                for e in evals
            ])

            # Color-coding rows
            def highlight(row):
                return ['background-color: gold' if v=="⭐" else
                        'background-color: lightgreen' if v=="✅" else
                        'background-color: lightcoral' if v=="❌" else '' for v in row]
            
            st.table(df.style.apply(highlight, axis=1))

            # Interactive filtering
            st.subheader("Filter Candidates")
            qualified_filter = st.selectbox("Show candidates:", ["All", "Passed", "Failed"])
            if qualified_filter != "All":
                filtered_df = df[df["Qualified"]=="✅"] if qualified_filter=="Passed" else df[df["Qualified"]=="❌"]
            else:
                filtered_df = df
            st.dataframe(filtered_df, use_container_width=True)

st.markdown("---")
st.markdown("Dashboard powered by **X-Ray SDK** | Demo by Candidate")
