DEFAULT_THEME = 'modern'


def get_theme(_request=None):
    return DEFAULT_THEME


def template_path(name: str) -> str:
    return f'modern/{name}'
