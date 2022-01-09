import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import nltk
import collections
import networkx as nx
from processor import Text_Processor
from analyzer import Text_Analyzer
import itertools


def freq_plot(year, region, number):
    df_nlp_sel, text_tot = get_dataframe(year, region)

    fig = make_subplots(rows=1, cols=1)
    if not text_tot:
        fig.add_annotation(text="No matching data found.",
                           xref="paper",
                           yref="paper",
                           showarrow=False,
                           font=dict(size=28))
        fig.update_layout(go.Layout(
            margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        ))
        return fig

    # Option 1: year 2013/2014 the years 2013 and 2014 need a special treatment because they don't have a column
    # 'increase/decrease'. So we can't make a frequency plot for both increase and decrease, so we just make a
    # frequency plot of the words in general .
    if (year == 2013) or (year == 2014):
        freq = Text_Analyzer(text_tot).get_matrix().loc['total', :].sort_values(ascending=False)[0:number]

        fig.add_trace(go.Bar(x=freq.index, y=freq, marker=dict(color='blue')))

    # Option 2: year 2015-2020
    # if the year is not 2013 or 2014, we can make a frequency plot divided into increase and decrease
    else:

        df_nlp_increase = df_nlp_sel.loc[df_nlp_sel['increase_decrease_from_last_year'] == 'Increased'].loc[:,
                          ['reason_for_increase_decrease_in_emissions']]
        df_nlp_decrease = df_nlp_sel.loc[df_nlp_sel['increase_decrease_from_last_year'] == 'Decreased'].loc[:,
                          ['reason_for_increase_decrease_in_emissions']]

        collection_words = ['emission', 'increase', 'decrease', 'reduction', 'year', 'due', 'city']

        text_increase = [
            Text_Processor(v[0].lower(), collection_words).process(lemmatize=True, clean_collection_words=True,
                                                                   clean_stopwords=True) for v in
            df_nlp_increase.values]
        text_decrease = [
            Text_Processor(v[0].lower(), collection_words).process(lemmatize=True, clean_collection_words=True,
                                                                   clean_stopwords=True) for v in
            df_nlp_decrease.values]

        string_tot = " ".join(v for v in text_tot)
        string_increase = " ".join(v for v in text_increase)
        string_decrease = " ".join(v for v in text_decrease)
        reasons = [string_tot, string_decrease, string_increase]

        freq_matrix = Text_Analyzer(reasons).get_matrix()
        freq_matrix.drop("total", axis=0, inplace=True)
        freq_matrix.index = ['Frequency total', 'Frequency decrease', 'Frequency increase']
        freq_sel = freq_matrix.sort_values(by='Frequency total', axis=1, ascending=False).iloc[:, 0:number]
        freq_sel.loc['Frequency increase'] = freq_sel.loc['Frequency increase'] / freq_sel.loc['Frequency total']
        freq_sel.loc['Frequency decrease'] = freq_sel.loc['Frequency decrease'] / freq_sel.loc['Frequency total']

        word_list_tot = string_tot.split()
        number_of_words_tot = len(word_list_tot)

        word_list_increase = string_increase.split()
        number_of_words_increase = len(word_list_increase)
        baseline_freq_increase = number_of_words_increase / number_of_words_tot

        word_list_decrease = string_decrease.split()
        number_of_words_decrease = len(word_list_decrease)
        baseline_freq_decrease = number_of_words_decrease / number_of_words_tot

        labels = freq_sel.columns

        fig.add_trace(go.Bar(x=labels, y=freq_sel.loc['Frequency decrease'],
                             name='Frequency decrease', marker_color='#3343ff'))
        fig.add_trace(go.Bar(x=labels, y=freq_sel.loc['Frequency increase'],
                             name='Frequency increase', marker_color='#ff3333'))

        fig.add_hline(y=baseline_freq_decrease, line_color='#0014ff')
        fig.add_hline(y=baseline_freq_increase, line_color='#ff0000')

    fig.update_layout(margin=dict(b=20, l=5, r=5, t=40),
                      paper_bgcolor="LightSteelBlue",
                      title='Relative frequencies of most common words by category',
                      xaxis_title='Key terms',
                      yaxis_title='Relative frequencies',
                      barmode='group')

    return fig


def network_plot(year, region, number):
    _, text_tot = get_dataframe(year, region)

    fig = make_subplots(rows=1, cols=1)
    if not text_tot:
        fig.add_annotation(text="No matching data found.",
                           xref="paper",
                           yref="paper",
                           showarrow=False,
                           font=dict(size=28))
        fig.update_layout(go.Layout(
            margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        ))
        return fig

    words_in_reason = [reason.split() for reason in text_tot]
    terms_bigram = [list(nltk.bigrams(reason)) for reason in words_in_reason]
    bigrams = list(itertools.chain(*terms_bigram))
    bigram_counts = collections.Counter(bigrams)
    bigram_df = pd.DataFrame(bigram_counts.most_common(number), columns=['bigram', 'frequency'])

    d = bigram_df.set_index('bigram').T.to_dict('records')

    # Create network plot
    G = nx.Graph()

    # Create connections between nodes
    for k, v in d[0].items():
        G.add_edge(k[0], k[1], weight=(v * 10))

    G_pos = nx.spring_layout(G, k=2)

    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = G_pos[edge[0]]
        x1, y1 = G_pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=2, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = G_pos[node]
        node_x.append(x)
        node_y.append(y)

    labels = []
    for key, value in G_pos.items():
        labels.append(key)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=labels,
        textposition="bottom center",
        textfont=dict(size=15,
                      color="black"),
        hoverinfo='skip',
        marker=dict(
            color='blue',
            size=20,
            line_width=2,
            line_color='grey'))

    fig.add_trace(edge_trace)
    fig.add_trace(node_trace)
    fig.update_layout(go.Layout(
        title='Network graph for reasons to increase/decrease',
        titlefont=dict(size=16),
        showlegend=False,
        margin=dict(b=20, l=5, r=5, t=40),
        paper_bgcolor="LightSteelBlue",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

    return fig


def get_dataframe(year, region):
    # some datasets have 'region' missing
    # we can fill this in based on the country
    # therefore, we make a dictionary based on 2020 and 2017 with countries as keys and regions as values
    regions_dict_2020 = pd.read_csv('https://data.cdp.net/resource/p43t-fbkj.csv').set_index('country')[
        'cdp_region'].to_dict()
    regions_dict_2017 = dataframe = pd.read_csv('https://data.cdp.net/resource/kyi6-dk5h.csv').set_index('country')[
        'region'].to_dict()
    regions_dict = {**regions_dict_2020, **regions_dict_2017}

    regions = ['Africa', 'East Asia', 'Europe', 'Latin America', 'Middle East', 'North America',
               'South and West Asia', 'Southeast Asia and Oceania']

    # every dataset needs some adjustment in order to have uniformity (uniform names for columns etc.)
    if year == 2013:
        dataframe = pd.read_csv('https://data.cdp.net/resource/qznk-mn6r.csv')
        dataframe.rename(columns={'reason_for_change': 'reason_for_increase_decrease_in_emissions'}, inplace=True)
        dataframe.loc[:, 'region'] = dataframe.loc[:, 'country'].map(regions_dict)
    elif year == 2014:
        dataframe = pd.read_csv('https://data.cdp.net/resource/imj3-eat7.csv')
        dataframe.loc[:, 'region'] = dataframe.loc[:, 'country'].map(regions_dict)
    elif year == 2015:
        dataframe = pd.read_csv('https://data.cdp.net/resource/yasg-kzny.csv')
        dataframe.loc[:, 'region'] = dataframe.loc[:, 'country'].map(regions_dict)
    elif year == 2016:
        dataframe = pd.read_csv('https://data.cdp.net/resource/dfed-thx7.csv')
        dataframe.loc[:, 'region'] = dataframe.loc[:, 'country'].map(regions_dict)
    elif year == 2017:
        dataframe = pd.read_csv('https://data.cdp.net/resource/kyi6-dk5h.csv')
        dataframe.rename(columns={'cdp_region': 'region'}, inplace=True)
    elif year == 2018:
        dataframe = pd.read_csv('https://data.cdp.net/resource/wii4-buw5.csv')
        dataframe.rename(columns={'change_in_emissions': 'increase_decrease_from_last_year',
                                  'reason_for_change': 'reason_for_increase_decrease_in_emissions',
                                  'cdp_region': 'region'}, inplace=True)
    elif year == 2019:
        dataframe = pd.read_csv('https://data.cdp.net/resource/542d-zyj8.csv')
        dataframe.rename(columns={'change_in_emissions': 'increase_decrease_from_last_year',
                                  'reason_for_change': 'reason_for_increase_decrease_in_emissions',
                                  'cdp_region': 'region'}, inplace=True)
    elif year == 2020:
        dataframe = pd.read_csv('https://data.cdp.net/resource/p43t-fbkj.csv')
        dataframe.rename(columns={'change_in_emissions': 'increase_decrease_from_last_year',
                                  'primary_reason_for_the_change': 'reason_for_increase_decrease_in_emissions',
                                  'cdp_region': 'region'}, inplace=True)

    # if specific region is selected (rather than all regions)
    if region in regions:
        dataframe = dataframe.loc[dataframe['region'] == region]
    # Years 2013 and 2014 need a special treatment because they don't have a column 'increase/decrease'. So we can't
    # make a frequency plot for both increase and decrease, so we just make a frequency plot of the words in general .
    if year != 2013 and year != 2014:
        dataframe = dataframe.loc[:, ['reason_for_increase_decrease_in_emissions', 'increase_decrease_from_last_year']]

    df_nlp_sel = dataframe.dropna(axis=0)
    collection_words = ['emission', 'increase', 'decrease', 'reduction', 'year', 'due']

    text_tot = [Text_Processor(v[0].lower(), collection_words).process(lemmatize=True,
                                                                       clean_collection_words=True,
                                                                       clean_stopwords=True) for v in df_nlp_sel.values]

    # textfile = open("a_file.txt", "w")
    #
    # for element in text_tot:
    #     textfile.write(str(element) + "\n")
    #
    # textfile.close()

    return df_nlp_sel, text_tot
