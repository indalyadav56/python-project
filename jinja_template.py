from jinja2 import Template

template = Template("Hello, {{ name }}!")
rendered_text = template.render(name="Bard")

print(rendered_text)
