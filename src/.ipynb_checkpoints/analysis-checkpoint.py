import pandas as pd
import plotly.express as px

zone_df = pd.read_csv('../data/zone_scores.csv')

color_map = {
    '💀 Critical Dead Zone': '#8B0000',
    '🔴 Dead Zone':          '#e74c3c',
    '🟡 Underperforming':    '#f39c12',
    '🟢 Average':            '#27ae60',
    '⭐ Top Performer':      '#2980b9'
}

fig = px.bar(
    zone_df.sort_values('Performance_Score'),
    x='Performance_Score',
    y='Sub-Category',
    color='Zone_Tag',
    orientation='h',
    color_discrete_map=color_map,
    title='🎯 Dead Zone Performance Score — Every Product Zone Ranked',
    labels={'Performance_Score': 'Performance Score (Higher = Better)',
            'Sub-Category': 'Product Zone'}
)
fig.update_layout(height=600, showlegend=True)
fig.write_html('../visuals/dead_zone_score.html')
fig.show()


#chart 2 
pivot = df.pivot_table(
    values='Profit',
    index='Sub-Category',
    columns='Region',
    aggfunc='sum'
)

fig = px.imshow(
    pivot,
    color_continuous_scale='RdYlGn',
    title='🗺️ Profit Heatmap: Sub-Category vs Region',
    text_auto='.0f'
)
fig.update_layout(height=600)
fig.write_html('../visuals/profit_heatmap.html')
fig.show()

#chart3
fig = px.scatter(
    df,
    x='Discount',
    y='Profit',
    color='Category',
    size='Sales',
    hover_data=['Sub-Category', 'Region'],
    title='💸 Discount vs Profit — Where Discounts Destroy Value',
    trendline='ols'   # adds regression line!
)
fig.add_hline(y=0, line_dash='dash', line_color='red',
              annotation_text='Break-Even Line')
fig.write_html('../visuals/discount_vs_profit.html')
fig.show()

#chart 4
sub_profit = df.groupby('Sub-Category')['Profit'].sum().sort_values()

colors = ['red' if x < 0 else 'green' for x in sub_profit]

fig = go.Figure(go.Bar(
    x=sub_profit.values,
    y=sub_profit.index,
    orientation='h',
    marker_color=colors
))
fig.add_vline(x=0, line_color='black', line_width=2)
fig.update_layout(
    title='💰 Total Profit by Sub-Category (Red = Losses)',
    xaxis_title='Total Profit ($)',
    height=550
)
fig.write_html('../visuals/profit_waterfall.html')
fig.show()

#chart 5
sub_profit = df.groupby('Sub-Category')['Profit'].sum().sort_values()

colors = ['red' if x < 0 else 'green' for x in sub_profit]

fig = go.Figure(go.Bar(
    x=sub_profit.values,
    y=sub_profit.index,
    orientation='h',
    marker_color=colors
))
fig.add_vline(x=0, line_color='black', line_width=2)
fig.update_layout(
    title='💰 Total Profit by Sub-Category (Red = Losses)',
    xaxis_title='Total Profit ($)',
    height=550
)
fig.write_html('../visuals/profit_waterfall.html')
fig.show()

