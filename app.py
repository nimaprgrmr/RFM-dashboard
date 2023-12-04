import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.express as px
from data_preprocessing import read_data, make_rfm, make_rfm_scores
from io import StringIO
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate


data = read_data(path="Data/RFM_MEGAMAL_UPDATE.csv")
rfm = make_rfm(data)
rfm_scores = make_rfm_scores(rfm)
mean_scores = rfm_scores[['recency', 'monetary', 'frequency', 'Segment']].groupby('Segment', as_index=False).mean()


def generate_selected_group_data(segment):
    custom_df = rfm_scores[rfm_scores['Segment'] == segment][['phone_number', 'customer_name']]
    return custom_df


segment_product_counts = rfm_scores.groupby('Segment').size().reset_index(name='Count')

information = {
    "مشتریان ضعیف از دست رفته": f"این گروه از مشتریان مدت زیادی است از شما خرید نکرده اند و تقریبا مشتریان از دست رفته هستند اما آنها نه مجموع خرید و نه تعداد فاکتور بالایی داشته اند."
                                f"  میانگین زمانی آخرین خرید این گروه: {mean_scores[mean_scores['Segment'] == 'مشتریان ضعیف از دست رفته']['recency'].values[0]:.0f} روز، "
                                f"میانگین مبلغ خرید این گروه: {mean_scores[mean_scores['Segment'] == 'مشتریان ضعیف از دست رفته']['monetary'].values[0]:,.0f} ریال "
                                f"و میانگین تعداد فاکتور های این گروه: {mean_scores[mean_scores['Segment'] == 'مشتریان ضعیف از دست رفته']['frequency'].values[0]:.0f} عدد است.",

    "مشتریان ارزشمند از دست رفته": "این گروه از مشتریان سابقه ی خرید خوبی داشته اند، مجموع مبلغ خرید و تعداد فاکتورهای آنها زیاد بوده است اما متاسفانه مدت زیادی است از شما خرید نکرده اند و نیاز به تماس یا پیامک برای بازگشت مجدد به فروشگاها را دارند."
                                f"میانگین زمانی آخرین خرید این گروه: {mean_scores[mean_scores['Segment'] == 'مشتریان ارزشمند از دست رفته']['recency'].values[0]:.0f} روز، "
                                f"میانگین مبلغ خرید این گروه: {mean_scores[mean_scores['Segment'] == 'مشتریان ارزشمند از دست رفته']['monetary'].values[0]:,.0f} ریال"
                                f" و میانگن تعداد فاکتور های این گروه: {mean_scores[mean_scores['Segment'] == 'مشتریان ضعیف از دست رفته']['frequency'].values[0]:.0f} عدد است.",

    "مشتریانی که به توجه و تبلیغ نیاز دارند(معمولی)": "این گروه از مشتریان مدتی است که از شما خرید نکرده اند اما دارای سابقه خرید نسبتا خوبی هستند، شما میتوانید با ارائه جشنواره های مختلف مدت زمان بازگشت آنهارا کوتاه تر کنید."
                                f"میانگین زمانی آخرین خرید این گروه: {mean_scores[mean_scores['Segment'] == 'مشتریانی که به توجه و تبلیغ نیاز دارند(معمولی)']['recency'].values[0]:.0f} روز، "
                                f"میانگین مبلغ خرید این گروه: {mean_scores[mean_scores['Segment'] == 'مشتریانی که به توجه و تبلیغ نیاز دارند(معمولی)']['monetary'].values[0]:,.0f} ریال "
                                f"و میانگین تعداد فاکتورهای این گروه: {mean_scores[mean_scores['Segment'] == 'مشتریانی که به توجه و تبلیغ نیاز دارند(معمولی)']['frequency'].values[0]:.0f} عدد است.",

    "مشتریان جدید": "این گروه از مشتریان، افرادی هستند که به تازگی از شما خید کرده اند، اما هنوز تاریخچه خرید خوبی برای خود ثبت نکرده اند"
                                f" میانگین زمانی آخرین خرید این گروه: {mean_scores[mean_scores['Segment'] == 'مشتریان جدید']['recency'].values[0]:.0f} روز، "
                                f"میانگین مبلغ خرید این گروه: {mean_scores[mean_scores['Segment'] == 'مشتریان جدید']['monetary'].values[0]:,.0f} ریال "
                                f" و میانگین تعداد فاکتورهای این گروه: {mean_scores[mean_scores['Segment'] == 'مشتریان جدید']['frequency'].values[0]:.0f} عدد است.",

    "مشتریانی که پتانسیل تبدیل به بهترین مشتریان را دارند": "مشتریانی هستند که به تازگی از شما خرید کرده اند و مجموع مبلغ خرید آنها از حد میانگین بیشتراست و پتانسیل تبدیل شدن به بهترین مشتریان شمارا دارند، پیشنهاد ما این است روی این گروه از مشتریان میتوانید با جشنواره های مختلف سرمایه گذاری کنید."
                                f" میانگین زمانی آخرین خرید این گروه: {mean_scores[mean_scores['Segment'] == 'مشتریانی که پتانسیل تبدیل به بهترین مشتریان را دارند']['recency'].values[0]:.0f} روز، "
                                f" میانگین مبلغ خرید این گروه: {mean_scores[mean_scores['Segment'] == 'مشتریانی که پتانسیل تبدیل به بهترین مشتریان را دارند']['monetary'].values[0]:,.0f} ریال "
                                f" و میانگین تعداد فاکتورهای این گروه: {mean_scores[mean_scores['Segment'] == 'مشتریانی که پتانسیل تبدیل به بهترین مشتریان را دارند']['frequency'].values[0]:.0f} عدد است.",

    "بهترین مشتریان": "این گروه، مشتریانی هستند که بیشترین مجموع خرید، بیشترین تعداد فاکتور و تازه ترین تاریخ خرید به نامشان ثبت شده است "
                                f" میانگین زمانی آخرین خرید این گروه: {mean_scores[mean_scores['Segment'] == 'بهترین مشتریان']['recency'].values[0]:.0f} روز، "
                                f" میانگین مبلغ خرید این گروه: {mean_scores[mean_scores['Segment'] == 'بهترین مشتریان']['monetary'].values[0]:,.0f} ریال "
                                f" و میانگین تعداد فاکتورهای این گروه: {mean_scores[mean_scores['Segment'] == 'بهترین مشتریان']['frequency'].values[0]:.0f} عدد است.",

    "دیگران": "این گروه تاریخچه خرید خوبی ندارند و مدت نسبتا زیادی است که از شما خرید نداشته اند."
                                f" میانگین زمانی آخرین خرید این گروه: {mean_scores[mean_scores['Segment'] == 'دیگران']['recency'].values[0]:.0f} روز، "
                                f" میانگین مبلغ خرید این گروه: {mean_scores[mean_scores['Segment'] == 'دیگران']['monetary'].values[0]:,.0f} ریال "
                                f" و میانگین تعداد فاکتورهای این گروه: {mean_scores[mean_scores['Segment'] == 'دیگران']['frequency'].values[0]:.0f} عدد است."
}

external_stylesheets = [dbc.themes.QUARTZ]
# Create app theme
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# Creating my dashboard application
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Define layout
app.layout = dbc.Container(
    [
        dbc.Row([
            dbc.Col(html.H3("RFM مشتریان", style={'margin-top': '20px', 'margin-right': '20px'}), width=6),

            dbc.Col([
                dbc.Button('راهنما', id='help-button', n_clicks=0, color='primary', outline=True,
                           style={'background-color': 'rgb(6, 206, 255)', 'color': 'white'}),
            ], width=6, style={'text-align': 'left', 'margin-top': '10px', 'margin-bottom': '20px'}),
        ]),

        dbc.Row([
            dbc.Col(html.Label('انتخاب گروه مشتریان'), width=12, style={'margin-bottom': '5px'}),
            dbc.Col(dbc.Button('بهترین مشتریان', id='best-customers', n_clicks=0), width=1),
            dbc.Col(dbc.Button('مشتریانی که پتانسیل تبدیل به بهترین مشتریان را دارند', id='potential-to-be-best',
                               n_clicks=0), width=3),
            dbc.Col(dbc.Button('مشتریان جدید', id='new-customers', n_clicks=0), width=1),
            dbc.Col(dbc.Button('مشتریانی که به توجه و تبلیغ نیاز دارند(معمولی)', id='medium-customers', n_clicks=0),
                    width=2),
            dbc.Col(dbc.Button('مشتریان ارزشمند از دست رفته', id='valuable-lost-customers', n_clicks=0), width=2),
            dbc.Col(dbc.Button('مشتریان ضعیف از دست رفته', id='cheap-lost-customers', n_clicks=0, size='md'), width=2),
            dbc.Col(dbc.Button('دیگران', id='others', n_clicks=0), width=1),
        ], style={'margin-bottom': '10px'}),

        dbc.Row([
            dbc.Col(html.Div(id='output-container-date-range'), width=12, style={'margin-top': '15px'}),
        ]),

        dbc.Row(
            dbc.Col(
                dcc.Graph(
                    id='treemap',
                    figure=px.treemap(segment_product_counts,
                                      path=['Segment'],
                                      values='Count',
                                      color='Segment', color_discrete_sequence=px.colors.qualitative.Pastel,
                                      title='RFM Customer Segments by Value',
                                      branchvalues='total')
                ),
            ),
        ),

        dbc.Modal([
            dbc.ModalHeader("راهنمای کاربری", style={'direction': 'ltr'}),
            dbc.ModalBody(
                dcc.Markdown("""
                    راهنمای استفاده از داشبورد RFM مشتریان:

                    1. ما در این برنامه تمام مشتریان را با توجه به مجموع مبالغ خرید آنها و تاریخ آخرین خرید و تعداد فاکتور هایی که به نامشان ثبت شده به 7 گروه تقسیم بندی کردیم.
                    2. در نمودار، گروه های مختلف با رنگ های مختلف تفکیک شده اند که نام هر گروه روی آنها مشخص شده است و لازم به ذکر است که بزرگی هر گروه به تعداد مشتریانی که در آن قرار میگیرند وابسته است.
                    3. با کلیک کردن روی هر گروه اطلاعات تکمیلی راجب به ویژگی اشخاصی که داخل آن قرار گرفته اند و پیشنهادات ما برای اجرای برنامه های مختلف مناسب برای آن مشتریان، زیر نمودار نمایش داده میشود.
                    4. همچنین دکمه ای با عنوان `دانلود` نمایش داده میشود که با کلیک روی آن یک فایل اکسل حاوی شماره تماس ها و اسامی مشتریانی که در آن گروه قرار گرفته اند دانلود میشود.
                    5. لازم به ذکر است که با توجه به اطلاعات خرید مشتریان ممکن است یک گروه تعداد بسیار اندکی(7 مشتری) در خود جای دهد و میزان آن آنقدر کوچک باشد که در نمودار نمایش داده نشود.

                    موفق باشید!
                """, style={'color': 'white'})
            ),
            dbc.ModalFooter(
                dbc.Button("بستن", id="help-close-button", className="ml-auto")),
        ], id='help-modal', style={'display': 'none', 'direction': 'rtl'}),  # Make sure to set the display style
        html.Div(id='modal-background',
                 style={'position': 'fixed', 'top': 0, 'left': 0, 'width': '100%', 'height': '80%',
                        'background-color': 'rgba(6, 206, 255, 0.5)', 'display': 'none', 'color': 'rgb(6, 206, 255)'}),

        html.Div([
            html.Div(id='info-text', style={'padding': '10px'}),
            html.Div(id='download-btn-container', style={'margin-top': '20px'}),
        ], id='info-output', style={'margin-top': '50px'}),

        dbc.Button("دانلود اطلاعات تماس مشتریان", id='download-btn', n_clicks=0,
                   style={'margin-top': '40px', 'margin-bottom': '50px', 'display': 'none'}),
        # Initial display set to 'none'
        dcc.Download(id="download-data"),
        html.Div(id='button-clicked-segment', style={'display': 'none'}),

    ],
    fluid=True,  # Set to True for a fluid (100% width) container
    style={'direction': 'rtl'}
)

# Your other imports and code

# Initialize info_state as an empty dictionary
info_state = {'segment': None, 'visible': False}
# Initialize default year and selected months list
select_group = "بهترین مشتریان"
selected_groups = []


# @app.callback(
#     [Output('output-container-date-range', 'children'),
#      Output('best-customers', 'style'),
#      Output('potential-to-be-best', 'style'),
#      Output('new-customers', 'style'),
#      Output('medium-customers', 'style'),
#      Output('valuable-lost-customers', 'style'),
#      Output('cheap-lost-customers', 'style'),
#      Output('others', 'style'),
#      ],
#     [Input('best-customers', 'n_clicks'),
#      Input('potential-to-be-best', 'n_clicks'),
#      Input('new-customers', 'n_clicks'),
#      Input('medium-customers', 'n_clicks'),
#      Input('valuable-lost-customers', 'n_clicks'),
#      Input('cheap-lost-customers', 'n_clicks'),
#      Input('others', 'n_clicks'),
#      ]
# )
# def update_output(*button_clicks):
#     global select_group, selected_group  # To modify global variables
#     ctx = dash.callback_context
#     if not ctx.triggered:
#         button_id = 'best-customers'  # Default to 1400 if no button clicked
#     else:
#         button_id = ctx.triggered[0]['prop_id'].split('.')[0]
#
#     # Update selected year and months based on button clicks
#     group = button_id
#     if group in selected_groups:
#         selected_groups.remove(group)
#     else:
#         selected_groups.append(group)
#     # Define default styles
#     default_style = {'background-color': 'rgb(230, 58, 144)'}
#     selected_style = {'background-color': 'lightblue'}
#     # Set styles based on selected months
#     group_styles = [selected_style if button_id == f'{group}' else default_style for button_id in
#                     ['best-customers',
#                      'potential-to-be-best',
#                      'new-customers',
#                      'medium-customers',
#                      'valuable-lost-customers',
#                      'cheap-lost-customers',
#                      'others']]
#     mapping_groups = {'best-customers': 'بهترین مشتریان',
#                       'potential-to-be-best': 'مشتریانی که پتانسیل تبدیل به بهترین مشتریان را دارند',
#                       'new-customers': 'مشتریان جدید',
#                       'medium-customers': 'مشتریانی که به توجه و تبلیغ نیاز دارند(معمولی)',
#                       'valuable-lost-customers': 'مشتریان ارزشمند از دست رفته',
#                       'cheap-lost-customers': 'مشتریان ضعیف از دست رفته',
#                       'others': 'دیگران'}
#     group = [mapping_groups[group]]
#     return group, *group_styles


# Updated callback to handle toggling info visibility
@app.callback(
    [Output('info-text', 'children', allow_duplicate=True),
     Output('info-text', 'style', allow_duplicate=True),
     Output('download-btn', 'style', allow_duplicate=True)],
    [Input('treemap', 'clickData')],
    prevent_initial_call=True
)
def display_info_and_download_treemap(clickData):
    # Initialize values
    info = ""
    info_style = {'display': 'none'}  # Hide the info div
    btn_style = {'display': 'none'}  # Hide the button

    # Check if treemap is clicked
    if clickData:
        clicked_segment = clickData['points'][0].get('label', "")
        # If the same segment is clicked again, hide the info
        if info_state['segment'] == clicked_segment:
            info_state['visible'] = not info_state['visible']
        else:
            info_state['segment'] = clicked_segment
            info_state['visible'] = True

        # Segment clicked
        if info_state['visible']:
            info = f"{clicked_segment} : {information[clicked_segment]}"
            info_style = {'display': 'block', 'background-color': 'rgb(230, 58, 144)', 'padding': '10px'}  # Show the info div
            btn_style = {'display': 'block', 'padding': '10px', 'margin-bottom': '70px'}  # Show the button

    return info, info_style, btn_style


@app.callback(
    [
    Output('button-clicked-segment', 'children'),
          ],
    [Input('best-customers', 'n_clicks'),
     Input('potential-to-be-best', 'n_clicks'),
     Input('new-customers', 'n_clicks'),
     Input('medium-customers', 'n_clicks'),
     Input('valuable-lost-customers', 'n_clicks'),
     Input('cheap-lost-customers', 'n_clicks'),
     Input('others', 'n_clicks')],
    prevent_initial_call=True
)
def update_button_clicked_segment(*button_clicks):
    # Check if it's a button click
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate

    # Check which button is clicked
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    # Update selected segment based on button click
    clicked_segment = button_id.replace('-clicks', '').replace('-', ' ')

    mapping_groups = {'best customers': 'بهترین مشتریان',
                      'potential to be best': 'مشتریانی که پتانسیل تبدیل به بهترین مشتریان را دارند',
                      'new customers': 'مشتریان جدید',
                      'medium customers': 'مشتریانی که به توجه و تبلیغ نیاز دارند(معمولی)',
                      'valuable lost customers': 'مشتریان ارزشمند از دست رفته',
                      'cheap lost customers': 'مشتریان ضعیف از دست رفته',
                      'others': 'دیگران'}

    clicked_segment = [mapping_groups[clicked_segment]]
    return clicked_segment


@app.callback(
    [Output('info-text', 'children', allow_duplicate=True),
     Output('info-text', 'style', allow_duplicate=True),
     Output('download-btn', 'style', allow_duplicate=True)],
    [Input('button-clicked-segment', 'children')],
    prevent_initial_call=True
)
def display_info_and_download_button(clicked_segment):
    # Initialize values
    info = ""
    info_style = {'display': 'none'}  # Hide the info div
    btn_style = {'display': 'none'}  # Hide the button

    # Check if a segment is selected from button click
    if clicked_segment:
        # If the same segment is clicked again, hide the info
        if info_state['segment'] == clicked_segment:
            info_state['visible'] = not info_state['visible']
        else:
            info_state['segment'] = clicked_segment
            info_state['visible'] = True

        # Segment clicked
        if info_state['visible']:
            info = f"{clicked_segment} : {information[clicked_segment]}"
            info_style = {'display': 'block', 'background-color': 'rgb(230, 58, 144)', 'padding': '10px'}  # Show the info div
            btn_style = {'display': 'block', 'padding': '10px', 'margin-bottom': '70px'}  # Show the button

    return info, info_style, btn_style


# Callback to handle CSV download
@app.callback(
    Output("download-data", "data"),
    Input('download-btn', 'n_clicks'),
    prevent_initial_call=True
)
def download_csv(n_clicks):
    if n_clicks:
        # Replace this with your logic to generate the CSV data for the selected group
        df_selected_group = generate_selected_group_data(info_state['segment'])
        # Create a CSV file in memory
        csv_buffer = StringIO()
        df_selected_group.to_csv(csv_buffer, index=False)

        # Return the CSV file for download
        return dict(content=csv_buffer.getvalue(), filename=f"{info_state['segment']}_customer_data.csv")


# Define callback to update the graph
@app.callback(
    Output('treemap', 'figure'),
    [Input('treemap', 'relayoutData'),]
)
def update_graph(relayout_data):
    # Assuming you have defined rfm_scores and grouped it into segment_product_counts
    segment_product_counts = rfm_scores.groupby('Segment').size().reset_index(name='Count')
    segment_product_counts = segment_product_counts.sort_values('Count', ascending=False)

    # Set the theme for the treemap
    fig = px.treemap(segment_product_counts,
                     path=['Segment'],
                     values='Count',
                     color='Segment', color_discrete_sequence=px.colors.qualitative.Pastel,
                     title='گروه بندیه مشتریان',
                     branchvalues='total')

    fig.update_layout(template='plotly',
                      plot_bgcolor='rgba(255, 255, 255, 0.5)',
                      # Change the background color here (RGB values with alpha for transparency)
                      paper_bgcolor='rgba(255, 255, 255, 0.5)',  # Change the plot area background color here
                      title_x=0.5,  # Set the x-coordinate of the title to the center
                      title_y=0.9,  # Set the y-coordinate of the title
                      title_xanchor='center',  # Set the x-anchor to center
                      title_yanchor='top',  # Set the y-anchor to the top
                      title_font=dict(size=20),
                      margin=dict(t=100, b=50, l=50, r=50)
                      )  # Change the theme here
    return fig


@app.callback(
    Output('help-modal', 'is_open'),
    Output('modal-background', 'style'),
    Input('help-button', 'n_clicks'),
    Input('help-close-button', 'n_clicks'),
    State('help-modal', 'is_open'),
    prevent_initial_call=True
)
def toggle_modal(help_clicks, close_clicks, is_open):
    if help_clicks is None:
        help_clicks = 0

    if close_clicks is None:
        close_clicks = 0

    # Toggle the modal based on the sum of help and close clicks
    total_clicks = help_clicks + close_clicks

    if total_clicks % 2 == 1:  # Odd number of total clicks
        return not is_open, {'display': 'block'}
    else:
        return is_open, {'display': 'none'}


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
