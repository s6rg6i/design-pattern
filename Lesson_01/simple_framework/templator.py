import pathlib

from jinja2 import Environment, FileSystemLoader


def render(template_name, folder='templates', **kwargs):

    env = Environment(loader=FileSystemLoader(pathlib.Path.cwd() / folder))
    template = env.get_template(template_name)
    return template.render(**kwargs)  # Рендерим шаблон с параметрами
