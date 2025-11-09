from dash import html


def render_header(title: str = "Dashboard Open Data") -> html.Header:
    """
    Render the main application header.

    Args:
        title: Text to display as the main title of the dashboard.

    Returns:
        A Dash HTML Header component.
    """
    return html.Header(
        children=html.H1(
            title,
            style={
                "margin": "0",
                "fontSize": "28px",
                "letterSpacing": "0.4px",
                "color": "#2c3e50",
            },
        ),
        style={
            "padding": "16px 20px",
            "backgroundColor": "#f6f8fa",
            "borderBottom": "1px solid #e5e7eb",
            "position": "sticky",
            "top": "0",
            "zIndex": 10,
        },
    )
