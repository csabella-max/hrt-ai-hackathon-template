import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(
    page_title="QSR LTO Field Readiness Dashboard",
    page_icon="🚀",
    layout="wide",
)

# ── Constants ─────────────────────────────────────────────────────────────────

SCORE_COLS = [
    "training_completion",
    "product_availability",
    "signage_materials",
    "pos_menu_readiness",
    "staffing_confidence",
    "equipment_smallwares",
    "recipe_process_confidence",
    "team_communication",
]

SCORE_LABELS = {
    "training_completion": "Training Completion",
    "product_availability": "Product Availability",
    "signage_materials": "Signage / Materials",
    "pos_menu_readiness": "POS / Menu Readiness",
    "staffing_confidence": "Staffing Confidence",
    "equipment_smallwares": "Equipment & Smallwares",
    "recipe_process_confidence": "Recipe / Process Confidence",
    "team_communication": "Team Communication",
}

RECOMMENDATIONS = {
    "training_completion": "Schedule make-up training before launch and confirm all team members know where to access the launch resources.",
    "product_availability": "Confirm product delivery, par levels, and back-up supply plan before launch. Flag any shortages early so the shop is not reacting on launch day.",
    "signage_materials": "Audit signage placement and confirm all customer-facing materials match the launch plan. Escalate missing or incorrect assets before launch.",
    "pos_menu_readiness": "Run a POS/menu audit and test the LTO build path, modifiers, pricing, and order flow before launch.",
    "staffing_confidence": "Review launch-day coverage and peak-hour staffing. Identify whether the team needs additional support during the first few days of the launch.",
    "equipment_smallwares": "Check smallwares, storage, prep tools, and equipment readiness. Submit urgent orders or create a workaround plan for missing items.",
    "recipe_process_confidence": "Review recipe steps, build standards, and any common points of confusion during a pre-launch huddle. Use a quick practice round before peak volume.",
    "team_communication": "Hold a pre-launch huddle to align the team on what is launching, how to make it, what to say to customers, and where to find support resources.",
}

THRESHOLD_READY = 75
THRESHOLD_AT_RISK = 60
THRESHOLD_RECOMMENDATION = 65

# ── Helpers ───────────────────────────────────────────────────────────────────

def assign_risk_tier(row):
    overall = row[SCORE_COLS].mean()
    weak_count = (row[SCORE_COLS] < 65).sum()
    if overall < 60:
        return "At Risk"
    elif overall >= 75 and weak_count == 0:
        return "Ready"
    elif overall >= 70 and weak_count <= 1:
        return "Monitor"
    else:
        return "Needs Support"


def score_status(score):
    if score < THRESHOLD_AT_RISK:
        return "At Risk"
    elif score < THRESHOLD_READY:
        return "Needs Attention"
    else:
        return "Ready"


@st.cache_data
def load_data():
    df = pd.read_csv("data_ai/shop_readiness.csv")
    df["computed_overall"] = df[SCORE_COLS].mean(axis=1).round(1)
    df["risk_tier"] = df.apply(assign_risk_tier, axis=1)
    return df


df = load_data()

# ── Sidebar ───────────────────────────────────────────────────────────────────

st.sidebar.title("Filter")
st.sidebar.markdown("---")
shop_options = ["All Shops"] + sorted(df["shop_name"].tolist())
selected_shop = st.sidebar.selectbox("Select a Shop", options=shop_options)
st.sidebar.markdown("---")
st.sidebar.markdown("**Score Guide**")
st.sidebar.markdown("🟢 **Ready** — 75 or above")
st.sidebar.markdown("🟡 **Needs Attention** — 60 to 74")
st.sidebar.markdown("🔴 **At Risk** — below 60")
st.sidebar.markdown("---")
st.sidebar.markdown("**Launch Support Priority**")
st.sidebar.markdown("✅ **Ready** — No action needed")
st.sidebar.markdown("👀 **Monitor** — Watch one area")
st.sidebar.markdown("⚠️ **Needs Support** — Multiple gaps")
st.sidebar.markdown("🚨 **At Risk** — Immediate action required")

# ── Filter Application ────────────────────────────────────────────────────────

if selected_shop == "All Shops":
    view_df = df.copy()
    view_label = "All Shops"
    is_single_shop = False
else:
    view_df = df[df["shop_name"] == selected_shop].copy()
    view_label = selected_shop
    is_single_shop = True

# ── Header ────────────────────────────────────────────────────────────────────

st.title("🚀 QSR LTO Field Readiness Dashboard")
st.subheader(f"Limited-Time Offer Launch Readiness — {view_label}")
st.markdown(
    "This dashboard helps field operations leaders identify which shops are ready for the upcoming "
    "LTO launch, where gaps exist across key readiness areas, and what actions to take before launch day. "
    "Use the filter in the sidebar to view the full fleet or drill into a specific shop. "
    "**Scores below 65 trigger specific action recommendations.**"
)
st.divider()

# ── KPI Cards ─────────────────────────────────────────────────────────────────

avg_score = view_df["computed_overall"].mean()
shops_ready = int((view_df["risk_tier"] == "Ready").sum())
shops_at_risk = int((view_df["risk_tier"] == "At Risk").sum())
total_shops = len(view_df)
pct_ready = (shops_ready / total_shops * 100) if total_shops > 0 else 0

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.metric(
        label="Avg Overall Score",
        value=f"{avg_score:.1f}",
        help="Mean of all 8 readiness category scores across selected shops",
    )
with kpi2:
    st.metric(
        label="Shops Ready",
        value=f"{shops_ready} / {total_shops}",
        help="Shops with Risk Tier = Ready (overall ≥ 75, no category below 65)",
    )
with kpi3:
    st.metric(
        label="Shops At Risk",
        value=str(shops_at_risk),
        help="Shops with overall score below 60 — require immediate attention before launch",
    )
with kpi4:
    st.metric(
        label="% Launch Ready",
        value=f"{pct_ready:.0f}%",
        help="Percentage of shops that are fully ready to launch",
    )

st.divider()

# ── Launch Support Priority Summary (All Shops view) ─────────────────────────

if not is_single_shop:
    st.subheader("Launch Support Priority")
    st.caption(
        "Each shop is assigned a priority tier based on its overall score and the number of "
        "readiness categories scoring below 65."
    )

    tier_order = ["Ready", "Monitor", "Needs Support", "At Risk"]
    tier_icons = {"Ready": "✅", "Monitor": "👀", "Needs Support": "⚠️", "At Risk": "🚨"}
    tier_desc = {
        "Ready": "Overall ≥ 75, no weak areas",
        "Monitor": "Overall ≥ 70, one area to watch",
        "Needs Support": "Multiple gaps before launch",
        "At Risk": "Overall < 60, significant risk",
    }
    tier_counts = view_df["risk_tier"].value_counts()

    t1, t2, t3, t4 = st.columns(4)
    for col_widget, tier in zip([t1, t2, t3, t4], tier_order):
        count = int(tier_counts.get(tier, 0))
        shop_word = "shop" if count == 1 else "shops"
        body = f"**{tier_icons[tier]} {tier}**\n\n**{count}** {shop_word}\n\n{tier_desc[tier]}"
        with col_widget:
            if tier == "Ready":
                st.success(body)
            elif tier == "At Risk":
                st.error(body)
            else:
                st.warning(body)

    st.divider()

# ── Category Score Bar Chart ──────────────────────────────────────────────────

st.subheader("Readiness by Category")
st.caption(
    "Average score per readiness area across the selected shops. "
    "🟢 Ready (≥75)  🟡 Needs Attention (60–74)  🔴 At Risk (<60)"
)

cat_means = view_df[SCORE_COLS].mean().reset_index()
cat_means.columns = ["col_key", "Score"]
cat_means["Category"] = cat_means["col_key"].map(SCORE_LABELS)
cat_means["Score"] = cat_means["Score"].round(1)
cat_means["Status"] = cat_means["Score"].apply(score_status)

status_order = ["At Risk", "Needs Attention", "Ready"]
color_range = ["#e74c3c", "#f39c12", "#2ecc71"]

bars = (
    alt.Chart(cat_means)
    .mark_bar(cornerRadius=4)
    .encode(
        x=alt.X("Score:Q", scale=alt.Scale(domain=[0, 100]), title="Average Score"),
        y=alt.Y("Category:N", sort="-x", title=None),
        color=alt.Color(
            "Status:N",
            scale=alt.Scale(domain=status_order, range=color_range),
            legend=alt.Legend(title="Status", orient="bottom"),
        ),
        tooltip=[
            alt.Tooltip("Category:N", title="Category"),
            alt.Tooltip("Score:Q", title="Avg Score", format=".1f"),
            alt.Tooltip("Status:N", title="Status"),
        ],
    )
)

text_labels = (
    alt.Chart(cat_means)
    .mark_text(align="left", dx=6, fontSize=13, fontWeight="bold")
    .encode(
        x=alt.X("Score:Q"),
        y=alt.Y("Category:N", sort="-x"),
        text=alt.Text("Score:Q", format=".1f"),
        color=alt.value("#333333"),
    )
)

st.altair_chart((bars + text_labels).properties(height=320), width="stretch")

st.divider()

# ── Shop Table / Single-Shop Scorecard ────────────────────────────────────────

if is_single_shop:
    shop_row = view_df.iloc[0]
    overall = shop_row["computed_overall"]
    tier = shop_row["risk_tier"]

    st.subheader(f"Shop Scorecard — {shop_row['shop_name']}")

    info_col, tier_col = st.columns([3, 1])
    with info_col:
        st.markdown(
            f"**Region:** {shop_row['region']}  |  "
            f"**Manager:** {shop_row['manager_name']}  |  "
            f"**Overall Score:** {overall:.1f} / 100"
        )
    with tier_col:
        if tier == "Ready":
            st.success(f"✅ **{tier}**\n\nOn track for launch.")
        elif tier == "At Risk":
            st.error(f"🚨 **{tier}**\n\nNeeds immediate attention.")
        elif tier == "Monitor":
            st.info(f"👀 **{tier}**\n\nOne area to watch.")
        else:
            st.warning(f"⚠️ **{tier}**\n\nMultiple gaps to address.")

    st.markdown("**Category Scores**")
    sc1, sc2 = st.columns(2)
    for i, col_key in enumerate(SCORE_COLS):
        score = int(shop_row[col_key])
        target_col = sc1 if i % 2 == 0 else sc2
        target_col.metric(label=SCORE_LABELS[col_key], value=f"{score} / 100")

else:
    st.subheader("Shop Readiness Table")
    st.caption("Sorted by Overall Score. All scores are out of 100. Click a column header to re-sort.")

    display_cols = ["shop_name", "region", "manager_name", "risk_tier"] + SCORE_COLS + ["computed_overall"]
    display_df = view_df[display_cols].copy()
    display_df = display_df.rename(columns={
        "shop_name": "Shop",
        "region": "Region",
        "manager_name": "Manager",
        "risk_tier": "Priority Tier",
        "computed_overall": "Overall Score",
        **SCORE_LABELS,
    })
    display_df = display_df.sort_values("Overall Score", ascending=False)

    column_config = {"Priority Tier": st.column_config.TextColumn("Priority Tier")}
    for label in list(SCORE_LABELS.values()) + ["Overall Score"]:
        column_config[label] = st.column_config.ProgressColumn(
            label=label,
            min_value=0,
            max_value=100,
            format="%.0f",
        )

    st.dataframe(
        display_df,
        width="stretch",
        hide_index=True,
        column_config=column_config,
        height=460,
    )

st.divider()

# ── Top Risk Areas ────────────────────────────────────────────────────────────

st.subheader("Top Risk Areas")
st.caption("The three lowest-scoring readiness categories for the selected view.")

cat_means_series = view_df[SCORE_COLS].mean()
bottom3 = cat_means_series.nsmallest(3)

rc1, rc2, rc3 = st.columns(3)
for col_widget, (col_key, score) in zip([rc1, rc2, rc3], bottom3.items()):
    label = SCORE_LABELS[col_key]
    rounded = round(float(score), 1)
    with col_widget:
        if score < THRESHOLD_AT_RISK:
            st.error(f"**{label}**\n\nAvg Score: **{rounded}**\n\n🔴 At Risk")
        elif score < THRESHOLD_READY:
            st.warning(f"**{label}**\n\nAvg Score: **{rounded}**\n\n🟡 Needs Attention")
        else:
            st.success(f"**{label}**\n\nAvg Score: **{rounded}**\n\n🟢 Ready")

st.divider()

# ── Recommended Next Actions ──────────────────────────────────────────────────

st.subheader("Recommended Next Actions")

triggered = [
    (col_key, SCORE_LABELS[col_key], view_df[col_key].mean())
    for col_key in SCORE_COLS
    if view_df[col_key].mean() < THRESHOLD_RECOMMENDATION
]
triggered.sort(key=lambda x: x[2])

if not triggered:
    st.success(
        "✅ All readiness categories are scoring at or above 65. "
        "This shop is on track for launch — continue monitoring in the days ahead."
    )
else:
    count = len(triggered)
    areas = "area" if count == 1 else "areas"
    requires = "requires" if count == 1 else "require"
    st.markdown(f"**{count} {areas} {requires} attention** (scoring below {THRESHOLD_RECOMMENDATION}):")
    for col_key, label, avg in triggered:
        with st.expander(f"{label}  —  Avg Score: {avg:.1f}", expanded=True):
            if avg < THRESHOLD_AT_RISK:
                st.error(f"🚨 **Action Required:** {RECOMMENDATIONS[col_key]}")
            else:
                st.warning(f"⚠️ **Action Recommended:** {RECOMMENDATIONS[col_key]}")

# ── Footer ────────────────────────────────────────────────────────────────────

st.divider()
st.caption(
    "QSR LTO Field Readiness Dashboard  ·  Launch Readiness Assessment — Cycle 1  ·  "
    "For questions, contact your District Operations Manager."
)
