from django.http import HttpResponse


def client_location_redirect(redirect_path):
    response = HttpResponse(status=204)
    response.headers['HX-Location'] = f'{{"path": "{redirect_path}", "target": "body"}}'
    return response


def client_redirect(redirect_path):
    response = HttpResponse(status=204)
    response.headers['HX-Redirect'] = redirect_path
    return response