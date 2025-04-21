from preswald import connect, get_df, table, text, plotly, slider, dropdown
import plotly.express as px

text("This app lets users explore how happiness scores across countries relate to factors like GDP, social support, and freedom of choice — all based on the World Happiness Report (2008–2024). You can interactively filter countries by year and happiness level, and visualize insights through scatter and bar charts.")

from preswald import connect, get_df, table, text, plotly, slider, dropdown
import plotly.express as px

# Initialize connection
connect()

# Load dataset
df = get_df("World-happiness-report-updated_2024")

# UI Components
selected_year = dropdown("Select a Year", options=sorted(df["year"].unique(), reverse=True))
score_threshold = slider("Minimum Happiness Score", min_val=2, max_val=8, default=5)

# Display title
text("Global Happiness Explorer")
text("Explore happiness trends across countries based on GDP, social support, and more.")

# Safeguard: only run the rest if both inputs have values
if selected_year is not None and score_threshold is not None:
    # Filter
    filtered_df = df[(df["year"] == selected_year) & (df["Life Ladder"] >= score_threshold)]

    # Scatter Plot
    fig = px.scatter(
        filtered_df,
        x="Log GDP per capita",
        y="Life Ladder",
        size="Social support",
        color="Country name",
        hover_name="Country name",
        title="GDP vs Happiness Score",
        labels={"Log GDP per capita": "Log GDP", "Life Ladder": "Happiness Score"}
    )
    fig.update_layout(template="plotly_white")
    plotly(fig)

    # Bar Chart
    top10 = filtered_df.sort_values(by="Life Ladder", ascending=False).head(10)
    fig2 = px.bar(
        top10,
        x="Country name",
        y="Life Ladder",
        title="Top 10 Happiest Countries",
        labels={"Country name": "Country", "Life Ladder": "Happiness Score"},
        text="Life Ladder"
    )
    fig2.update_traces(textposition='outside')
    fig2.update_layout(template="plotly_white")
    plotly(fig2)

    # Table
    table(filtered_df, title="Filtered Data Based on Year and Happiness Score")
else:
    text("Please select a year and adjust the score slider to see the results.")
