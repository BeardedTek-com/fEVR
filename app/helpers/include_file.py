import jinja2
class include_file:
    def include_file(name):
        return jinja2.Markup(loader.get_source(env, name)[0])

    loader = jinja2.PackageLoader(__name__, 'templates')
    env = jinja2.Environment(loader=loader)
    env.globals['include_file'] = include_file

    def render():
        return env.get_template('page.html').render()

if __name__ == '__main__':
    print(include_file.render())