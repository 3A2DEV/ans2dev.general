#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2024, Marco Noce <nce.marco@gmail.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: charts
short_description: Generate charts images.
description:
  - This module generates various types of charts like C(line), C(bar), C(pie) and C(donut) and saves them as images.
  - It provides customization options for titles, axis labels, colors, sizes, fonts, and legends.
  - Uses `Plotly` and `Kaleido` for image generation.
version_added: "0.1.0"
requirements:
  - requests
  - plotly
  - kaleido
options:
  titlechart:
    description:
      - Title of the chart.
    required: false
    type: str
  type:
    description:
      - Type of chart to generate.
    required: true
    type: str
    choices: [line, bar, pie, donut]
  xaxis:
    description:
      - X-axis data values for V(line) and V(bar) charts.
    required: false
    type: list
    elements: str
    default: []
  xaxisname:
    description:
      - Label for the X-axis for V(line) and V(bar) charts.
    required: false
    type: str
  yaxis:
    description:
      - List of Y-axis data series for V(line) and V(bar) charts.
    required: false
    type: list
    elements: list
    default: []
  yaxisname:
    description:
      - Labels for the Y-axis data series for V(line) and V(bar) charts.
    required: false
    type: list
    elements: str
    default: []
  yaxiscolor:
    description:
      - Colors for the Y-axis data series for V(line) and V(bar) charts.
    required: false
    type: list
    elements: str
    default: []
  imgwidth:
    description:
      - Width of the generated chart image (in pixels).
    required: false
    type: int
    default: 1920
  imgheight:
    description:
      - Height of the generated chart image (in pixels).
    required: false
    type: int
    default: 1080
  shape_line:
    description:
      - Line shape for V(line) charts.
    required: false
    type: str
    choices: [spline, linear]
  format:
    description:
      - Image format for saving the chart.
    required: false
    type: str
    choices: [png, jpeg, webp, svg, pdf, eps]
    default: png
  path:
    description:
      - Path where the chart image will be saved.
    required: true
    type: str
  filename:
    description:
      - Filename for the saved chart image.
    required: true
    type: str
  fontsize:
    description:
      - Font size for labels and text.
    required: false
    type: int
    default: 20
  fontcolor:
    description:
      - Font color for chart text.
    required: false
    type: str
    default: '#333333'
  titlelegend:
    description:
      - Title for the legend.
    required: false
    type: str
  slicedata:
    description:
      - Data values for V(pie) or V(donut) chart slices.
    required: false
    type: list
    elements: float
    default: []
  slicelabel:
    description:
      - Labels for V(pie) or V(donut) chart slices.
    required: false
    type: list
    elements: str
    default: []
  slicecolor:
    description:
      - Colors for V(pie) or V(donut) chart slices.
    required: false
    type: list
    elements: str
    default: []
  sizehole:
    description:
      - Size of the hole in a V(donut) chart (0 for a full pie chart).
    required: false
    type: float
    default: 0.5
author:
  - Marco Noce (@NomakCooper)
'''

EXAMPLES = r'''
- name: Generate a line chart for CPU Usage Over Time
  ans2dev.general.charts:
    type: "line"
    titlechart: "CPU Usage Over Time"
    xaxis: ['00:00', '02:00', '04:00', '06:00', '08:00']
    xaxisname: "Time"
    yaxis: [[20, 30, 40, 50, 60]]
    yaxisname: ["CPU Usage %"]
    yaxiscolor: ["red"]
    shape_line: "spline"
    imgwidth: 1920
    imgheight: 1080
    path: "/charts"
    filename: "cpu_usage"
    format: "png"
    titlelegend: "Usage"
  delegate_to: localhost

- name: Generate a pie chart for Resource Distribution
  ans2dev.general.charts:
    type: "pie"
    titlechart: "Resource Distribution"
    slicedata: [10, 20, 30, 40]
    slicelabel: ["A", "B", "C", "D"]
    slicecolor: ["#ff0000", "#00ff00", "#0000ff", "#ffff00"]
    imgwidth: 800
    imgheight: 600
    path: "/charts"
    filename: "resource_distribution"
    format: "png"
  delegate_to: localhost
'''

RETURN = r'''
changed:
    description: Indicates whether the chart image was successfully generated.
    type: bool
    returned: always
    sample: true
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import missing_required_lib
import os
import traceback

PLOTLY_IMPORT_ERROR = ""
try:
    import plotly.graph_objects as go
except ImportError:
    HAS_PLOTLY = False
    PLOTLY_IMPORT_ERROR = traceback.format_exc()
else:
    HAS_PLOTLY = True


def save_figure(fig, module):
    """ Save figure to the specified path with given format """
    filepath = module.params['path']
    imgname = module.params['filename']
    fileformat = module.params['format']

    os.makedirs(filepath, exist_ok=True)

    fig.write_image(f"{filepath}/{imgname}.{fileformat}")


def create_line_or_bar_chart(module, chart_type):
    """ Create a Line or Bar chart with a professional light theme """
    fig = go.Figure()
    xdata = module.params['xaxis']
    ydata = module.params['yaxis']
    ynames = module.params['yaxisname']
    ycolors = module.params['yaxiscolor']

    shape = module.params.get('shape_line', 'spline') if chart_type == "line" else None

    for y, name, color in zip(ydata, ynames, ycolors):
        if chart_type == "line":
            fig.add_trace(go.Scatter(
                x=xdata, y=y, name=name,
                line=dict(color=color, shape=shape, width=3),
                mode='lines+markers',
                marker=dict(size=8, symbol='circle', line=dict(width=1, color="black"))
            ))
        elif chart_type == "bar":
            fig.add_trace(go.Bar(
                x=xdata, y=y, name=name,
                marker=dict(
                    color=color,
                    line=dict(width=1, color="black"),
                    opacity=0.9
                )
            ))

    update_layout(fig, module, is_bar=(chart_type == "bar"))
    return fig


def create_pie_or_donut_chart(module, chart_type):
    """ Create a Pie or Donut chart with a professional light theme """
    fig = go.Figure()

    fig.add_trace(go.Pie(
        labels=module.params['slicelabel'],
        values=module.params['slicedata'],
        marker=dict(colors=module.params['slicecolor'],
                    line=dict(color="black", width=2)),
        hole=module.params['sizehole'] if chart_type == "donut" else 0,
        pull=[0.05 if i % 2 == 0 else 0 for i in range(len(module.params['slicelabel']))],
        textinfo='label+percent',
        insidetextorientation='radial'
    ))

    update_layout(fig, module, is_pie=True)
    return fig


def update_layout(fig, module, is_bar=False, is_pie=False):
    """ Update layout with a modern, professional aesthetic """
    fig.update_layout(
        autosize=False,
        width=module.params['imgwidth'],
        height=module.params['imgheight'],
        title=dict(
            text=module.params['titlechart'],
            font=dict(size=28, color='#333333', family="Roboto, Montserrat, Arial Black"),
            x=0.5
        ),
        xaxis=dict(
            title=module.params.get('xaxisname'),
            title_font=dict(size=18, family="Roboto, Montserrat"),
            showgrid=True,
            gridcolor="rgba(200,200,200,0.4)",
            zeroline=False,
            showline=True,
            linecolor="rgba(100,100,100,0.5)"
        ),
        yaxis=dict(
            title=", ".join(module.params.get('yaxisname', [])),
            title_font=dict(size=18, family="Roboto, Montserrat"),
            showgrid=True,
            gridcolor="rgba(200,200,200,0.4)",
            zeroline=False,
            showline=True,
            linecolor="rgba(100,100,100,0.5)"
        ) if not is_bar else None,
        legend=dict(
            title_text=module.params.get('titlelegend'),
            font=dict(size=16, family="Roboto, Montserrat"),
            bordercolor="rgba(50,50,50,0.3)",
            borderwidth=1,
            x=1.02,
            y=0.5
        ),
        font=dict(
            family="Roboto, Montserrat",
            size=16,
            color="black"
        ),
        plot_bgcolor="rgba(245, 245, 245, 1)",
        paper_bgcolor="white"
    )


def run_module():
    module_args = dict(
        titlechart=dict(type='str'),
        type=dict(type='str', required=True, choices=['line', 'bar', 'pie', 'donut']),
        xaxis=dict(type='list', elements='str', default=[]),
        xaxisname=dict(type='str'),
        yaxis=dict(type='list', elements='list', default=[]),
        yaxisname=dict(type='list', elements='str', default=[]),
        yaxiscolor=dict(type='list', elements='str', default=[]),
        imgwidth=dict(type='int', default=1920),
        imgheight=dict(type='int', default=1080),
        shape_line=dict(type='str', choices=['spline', 'linear']),
        format=dict(type='str', default='png', choices=['png', 'jpeg', 'webp', 'svg', 'pdf', 'eps']),
        path=dict(type='str', required=True),
        filename=dict(type='str', required=True),
        fontsize=dict(type='int', default=20),
        fontcolor=dict(type='str', default='#333333'),
        titlelegend=dict(type='str'),
        slicedata=dict(type='list', elements='float', default=[]),
        slicelabel=dict(type='list', elements='str', default=[]),
        slicecolor=dict(type='list', elements='str', default=[]),
        sizehole=dict(type='float', default=0.5),
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    if not HAS_PLOTLY:
        module.fail_json(
            msg=missing_required_lib('plotly'),
            exception=PLOTLY_IMPORT_ERROR
        )

    result = dict(changed=False)

    chart_type = module.params['type']
    fig = None

    if chart_type in ["line", "bar"]:
        fig = create_line_or_bar_chart(module, chart_type)
    elif chart_type in ["pie", "donut"]:
        fig = create_pie_or_donut_chart(module, chart_type)

    if fig:
        save_figure(fig, module)
        result['changed'] = True

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
