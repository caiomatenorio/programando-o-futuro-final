from flask import make_response, render_template

from .services.session_service import add_session_cookies


def render_template_with_auth(
    template_name_or_list,
    *,
    status_code=200,
    **context,
):
    rendered = render_template(template_name_or_list, **context)
    response = make_response(rendered, status_code)
    return add_session_cookies(response)
