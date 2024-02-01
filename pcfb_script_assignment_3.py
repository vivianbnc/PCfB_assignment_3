""" Created on Mo, 29.01.2024
@author: Vivian Bonacker, S5558646, University of Groningen, The Netherlands
@email: v.a.bonacker@student.rug.nl

Script for visualising critical thermal limits of the anemone Exaiptasia diaphana
"""

# import modules
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio

# functions
def import_excel(excel_file, sheet_name, usecols=None):
    """Function to import an excel file and certain sheets
    :param excel_file: contains the data to be imported
    :param sheet_name: name of the sheet to import
    :param usecols: list of columns that should be included
    :return data: now imported excel file
    :return df: dataframe with the data from the selected excel sheet
    """
    data = pd.ExcelFile(excel_file)
    df = pd.DataFrame(data.parse(sheet_name, usecols=usecols))
    return data, df
def remove_blanks(df, column):
    """Function to delete rows with blank measurements
     :param df: that contains the messy data
     :param column: that has the 'blank' statement/measurement to be removed
     :return df_clean: that contains the cleaned data without blanks
     """
    blank_rows_count = df[column].str.contains('blank').sum()
    print(f'Removing {blank_rows_count} rows with blank measurements.')
    df_clean = df[df[column].str.contains('blank') == False]

    return df_clean

def basic_statistics(df, group_column_stats, value_column_stats):
    """Calculate mean, median, and std for a specific column grouped by another column
     :param df: DataFrame containing the data
     :param group_column_stats: Column for grouping (e.g., 'Treat')
     :param value_column_stats: Column for which to calculate statistics (e.g., 'CT1')
     :return stats_df: DataFrame containing mean, median, and std for each group
     """
    stats_df = df.groupby(group_column_stats)[value_column_stats].agg(['mean', 'median', 'std']).reset_index()
    stats_df.columns = [group_column_stats, 'Mean', 'Median', 'Std']
    replicates_per_treat = df.groupby(group_column_stats).size().to_dict()
    stats_df['Replicates'] = stats_df[group_column_stats].map(replicates_per_treat)
    return stats_df

def interactive_boxplot(plot_data, group_column, value_column, treatment_order, ct_stats, title, xlabel, ylabel, legend_title):
    """Function to create an interactive plot.
    :param plot_data: dataframe that contains the data to be plotted
    :param group_column: Column name that will be used to group the data
    :param value_column: Column name that contains the actual data to plot
    :param treatment_order: contains the treatment names of the data and is used to order the data
    :param ct_stats: dataframe that contains the statistics of the data
    """
    # Create the Plotly figure
    fig = px.box(plot_data, x=group_column, y=value_column,
                 category_orders={group_column: treatment_order})
    fig.update_traces(boxpoints=False, jitter=0)
    # Add swarm plot points
    fig.add_trace(go.Scatter(x=plot_data[group_column], y=plot_data[value_column],
                             mode='markers', marker=dict(color='grey', size=6), showlegend=False))
    # Add annotations for sample size
    max_y = max(fig['data'][i]['y'].max() for i in range(len(fig['data'])))
    # Add individual sample sizes (n) for each treatment at the top of the overall boxplot
    for treat, replicate_count in zip(ct_stats[group_column], ct_stats['Replicates']):
        # Add annotation for the current treatment
        fig.add_annotation(
            x=treat,
            y=max_y,
            text=f'n={replicate_count}',
            showarrow=False,
            font=dict(size=12, color='black'),
            yshift=10,
        )

    # Update layout and style settings
    fig.update_layout(
        title=title,
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        legend_title=legend_title,
        font=dict(size=15),
        boxmode='group'
    )

    return fig

## Main script

if __name__ == '__main__':
    """
    This is the main script, change the input files and names according to your dataset.
    :param excel_file: name of the excel file you want to use
    :param sheet_name: name of the sheet you want to use
    :param use_cols: specify which columns of the excel sheet should be included, default in the function is all
    :param column: name of the column that contains the 'blank' statement
    :param group_column: name of the column that is used for grouping the data, this parameter is 
                         used in the basic_statistics function and the boxplot
    :param value_column: name of the column that is used for calculating the basic_statistics and boxplot,
                         contains the actual data
    :param stats_file_name: name of the file that will contains the mean, median, std and number of replicates for
                            every treatment, will be saved as .xlsx
    :param clean_file_name: name of the cleaned file, will be saved as .xlsx
    """
    # TODO change input files and names.
    excel_file = "CT_deadlytrio.xlsx"
    sheet_name = "dt_MO2_messy"
    use_columns = ["Specimen_ID", "Treat", "CT1"]
    column = "Specimen_ID"
    group_column = "Treat"
    value_column = "CT1"
    stats_file_name = "ct_stats.xlsx"
    clean_file_name = 'ct_cleaned.xlsx'

    # Read in file
    ct_data, ct_df = import_excel(excel_file, sheet_name, use_columns)

    # clean dataset and remove blanks
    ct_clean = remove_blanks(ct_df, column)

    # correct typo, this is specific to this dataset
    ct_clean.loc[ct_clean['Treat'] == 'HT_HC', 'Treat'] = 'HT-HC'

    # calculate mean, median, standard deviation and number of replicates
    ct_stats = basic_statistics(ct_clean, group_column, value_column)
    print("\n Calculated statistics:")
    print(ct_stats)


  # creating the boxplot
    """
    xlabel: change the name
    ylabel: change the name
    title: change the title
    plt.figure: adjust figure size to your preference
    figure_name: adjust the name to your preference, this is the name under which your boxplot will be saved
    legend_title: adjust this to your preference, this will be the title of the legend on the boxplot
    in colour_pal: you can change the palette you want to use, here "GnBu" is used, 
                look at https://r02b.github.io/seaborn_palettes/ for inspiration
    legend_labels: a manual legend can be added if you wish to
    """
    # TODO Adjust the following options according to your preferences
    plot_data = pd.DataFrame(ct_clean)
    xlabel = 'Treatment'
    ylabel = 'Critical thermal limit (°C)'
    title = "Effect of the 'deadly trio' on the critical thermal limit of anemones"
    plt.figure(figsize=(16, 14))
    figure_name = 'ct_deadly_trio.png'
    legend_title = 'Treatment'

    # define order and colouring of boxplot
    treatment_order = ct_stats[group_column].tolist()
    colour_pal = sns.color_palette("GnBu", n_colors=len(treatment_order))
    colour_dict = dict(zip(treatment_order, colour_pal))

    # TODO: Change these labels according to your dataset.
    # define labels manually
    legend_labels = {
        'C': 'Control',
        'H': 'Hypoxia',
        'HC': 'High Carbon',
        'HC-H': 'High Carbon + Hypoxia',
        'HT': 'High Temperature',
        'HT-H': 'High Temperature + Hypoxia',
        'HT-HC': 'High Temperature + High Carbon',
        'HT-HC-H': 'High Temperature + High Carbon + Hypoxia (Deadly trio)'
    }

    #the actual boxplot
    ax = sns.boxplot(x=group_column, y=value_column, data=plot_data, order=treatment_order, palette=colour_dict,
                hue=group_column, legend=False, width=0.8)
    sns.swarmplot(x=group_column, y=value_column, data=plot_data, color='grey', size=6)

    # Add number of replicates to the plot and adjust the position to above the third quantile
    for tick, replicate_count in zip(ct_stats[group_column], ct_stats['Replicates']):
        tick_pos = treatment_order.index(tick)
        # Calculate the third quantile to place sample size above that
        q3 = plot_data.loc[plot_data[group_column] == tick, value_column].quantile(0.75)
        y_pos = q3
        text_pos = tick_pos + 0.25
        ax.text(text_pos, y_pos, f'n={replicate_count}', ha='center', va='bottom',
                color='black')
        # move text to the right
        text_pos = tick_pos + 0.25
        ax.text(text_pos, y_pos, f'n={replicate_count}', ha='center', va='bottom',
                color='black')

    # Display the legend
    legend_elements = [plt.Line2D([0], [0], marker='o', color='w', label=f'{label}: {legend_labels[label]}',
                                  markerfacecolor=sns.color_palette(colour_pal)[i], markersize=10) for i, label in
                       enumerate(legend_labels)]
    ax.legend(handles=legend_elements, title=legend_title, loc="upper left", bbox_to_anchor=(0, 1),
              bbox_transform=ax.transAxes, fontsize=12, title_fontsize=12)

    # adding labels and adjusting size
    plt.xlabel(xlabel, size=25)
    plt.ylabel(ylabel, size=25)
    plt.title(title, size=25)
    plt.tick_params(axis='x', labelsize=15)
    plt.tick_params(axis='y', labelsize=15)

    # TODO here you can change the quality of the image
    # save figure as png in good quality
    plt.savefig(figure_name, dpi=300)
    plt.show()

    # optional: create an interactive plot
    int_plot = interactive_boxplot(plot_data, group_column, value_column, treatment_order, ct_stats, title, xlabel, ylabel, legend_title)
    int_plot.show()
    pio.write_html(int_plot, file='int_plot_deadlytrio.html', auto_open=True, full_html=True)

    # save statistics file and cleaned dataset
    ct_stats.to_excel(stats_file_name, index=False)
    ct_clean.to_excel(clean_file_name, index=False)