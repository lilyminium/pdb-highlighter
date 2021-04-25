import flask
import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = [
    'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css']


external_scripts = ['https://code.jquery.com/jquery-3.2.1.slim.min.js',
                    'https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js',
                    'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js']

# ╔═══*.·:·.☽✧ ✦✦✦✦✦✦✦✦✦✦✦✦✦✦ ✧☾.·:·.*═══╗
#             Highlighting function            
# ╚═══*.·:·.☽✧ ✦✦✦✦✦✦✦✦✦✦✦✦✦✦ ✧☾.·:·.*═══╝

FIELDS = {
    ( 0,  6): ("#E6E6FF", "Record type"),
    ( 6, 11): ("#FF7979", "Atom serial number"),
    (11, 12): ("", ""),
    (12, 16): ("#FFAFAF", "Atom name"),
    (16, 17): ("", "Alternate location indicator"),
    (17, 20): ("#FFC179", "Residue name"),
    (20, 21): ("", ""),
    (21, 22): ("", "Chain identifier"),
    (22, 26): ("#FFD7A8", "Residue sequence number"),
    (26, 27): ("", "Insertion code"),
    (27, 30): ("", ""),
    (30, 38): ("#CC66FF", "X coordinate (angstrom)"),
    (38, 46): ("#FF99FF", "Y coordinate (angstrom)"),
    (46, 54): ("#E699FF", "Z coordinate (angstrom)"),
    (54, 60): ("#66FF99", "Occupancy"),
    (60, 66): ("#A3EDA3", "Temperature factor"),
    (66, 76): ("", ""),
    (76, 78): ("#B2C2F0", "Element"),
    (78, 80): ("#5882FA", "Atom charge")
}

def color_line(line):
    components = []
    for (i, j), (color, tooltip) in FIELDS.items():
        content = line[i:j]
        html_id = f"field_{i}_{j}"
        style = {"white-space": "pre"}
        if color:
            style["background-color"] = color
            
        span = html.Span(content, id=html_id, style=style)
        components.append(span)
        if tooltip:
            tip = dbc.Tooltip(tooltip, target=html_id)
            components.append(tip)
    return components

# Server definition

server = flask.Flask(__name__)
app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets,
                external_scripts=external_scripts,
                server=server)

app.title = 'PDB highlighting'

# HEADER
# ======

header = dbc.NavbarSimple(
    dbc.NavItem(dbc.NavLink(
        "Source", href="https://github.com/lilyminium/pdb-highlighter")),
    brand="PDB highlighter",
    brand_href="#",
    color="primary",
    dark=True
)


# COMPONENTS
# ==========

# Your components go here.

explanation = dcc.Markdown("""\
Highlight fields in a PDB document.

Inspired by Pierre Poulain's post at https://cupnet.net/pdb-format/. 
""", style={'margin': '20px'})

PDB_EXAMPLE = """
ATOM      3  N   ALA A  30      86.170  84.190  79.710  1.00  0.00           N
ATOM      4  H1  ALA A  30      86.670  83.830  80.500  1.00  0.00           H
ATOM      5  H2  ALA A  30      85.870  83.430  79.130  1.00  0.00           H
ATOM      6  H3  ALA A  30      86.770  84.790  79.180  1.00  0.00           H
ATOM      7  CA  ALA A  30      85.000  84.950  80.170  1.00  0.00           C
ATOM      8  CB  ALA A  30      83.940  85.410  79.160  1.00  0.00           C
ATOM      9  C   ALA A  30      84.270  84.000  81.120  1.00  0.00           C
ATOM     10  O   ALA A  30      84.010  82.840  80.780  1.00  0.00           O
ATOM     11  N   PRO A  31      83.880  84.460  82.310  1.00  0.00           N
"""

text = dbc.FormGroup([
    dbc.Label('Text for highlighting (copy and paste text here)'),
    dbc.Textarea(id='pdb-text',
                 rows=10,
                 placeholder='ATOM      1  N   GLY A   3      17.119   0.186  36.320  1.00 64.10           N  ',
                 value=PDB_EXAMPLE,
                 style={'fontFamily': 'monospace'})
])



submit = html.Button('Generate text', id='submit', style={'margin': '10px'})

output = dbc.FormGroup([
    dbc.Label("Highlighted text (hover your cursor over text to see what fields they are)"),
    html.Div(id='output',
             style={'fontFamily': 'monospace'})
])

footer = dbc.Label('© Copyright 2021, Lily Wang',
                   style={'marginLeft': '20px'})

# APP LAYOUT
# ==========

app.layout = html.Div([
    header,
    explanation,
    dbc.Card([
        dbc.CardBody([
            html.H3('Input'),
            text,
        ])
    ], style={'margin': '20px', 'padding': '10px'}),
    dbc.Card([
        html.H3('Highlighted'),
        dbc.CardBody([output])
    ], style={'margin': '20px', 'padding': '10px'}),
    footer
], )


# INTERACTION
# ===========

# Your interaction goes here.

@app.callback(
    Output('output', 'children'),
    [Input('pdb-text', 'value')],
)
def highlight_pdb(text):
    lines = text.split("\n")
    components = []
    for line in lines:
        line_components = color_line(line)
        p = html.P(children=line_components)
        components.append(p)
    return components


if __name__ == '__main__':
    app.run_server(debug=True)
