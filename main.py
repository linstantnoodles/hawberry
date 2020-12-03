import os
import re
import shutil
import pathlib
import argparse
import markdown2

def new_site(name):
    shutil.copytree("directory", name)

def new_post(name):
    if os.path.isfile(f"posts/{name}.md"):
        raise FileExistsError(f"post {name}.md already exists")
    from jinja2 import Environment, FileSystemLoader, select_autoescape
    env = Environment(
        loader=FileSystemLoader(['posts/templates']),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('default.md')
    human_readable_name = " ".join([x.capitalize() for x in name.split("-")])
    content = template.render(title=f'"{human_readable_name}"')
    with open(f"posts/{name}.md", "w") as f:
        f.write(content)

def build_site():
    from jinja2 import Environment, FileSystemLoader, select_autoescape
    env = Environment(
        loader=FileSystemLoader(['layouts', 'pages']),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('base.html')
    ignored = {"templates"}
    files = [f for f in os.listdir(f"posts") if f not in ignored]
    post_metadata = []
    for fname in files:
        fp = os.path.join("posts", fname)
        with open(fp, 'r') as fc:
            rawc = fc.read()
            text, config = parse_front_matter(rawc)
            content = markdown2.markdown(text).strip()
            name_without_ext = os.path.splitext(fname)[0]
            permalink = config.get("permalink", f"posts/{name_without_ext}")
            post_dir = f"public/{permalink}"
            post_metadata.append({
                "title": config.get("title"),
                "url": f"/{permalink}"
            })
            os.makedirs(post_dir, exist_ok=True)
            with open(f"{post_dir}/index.html", "w") as output_file:
                output_file.write(template.render(content=content))
    for dir_path, dirs, files in os.walk("pages"):
        for name in [f for f in files if f.endswith(".html")]:
            rp = dir_path.split('/')[1:]
            parent_path = os.path.join(*rp) if rp else ""
            full_path = os.path.join(*rp, name)
            template = env.get_template(full_path)
            os.makedirs(f"public/{parent_path}", exist_ok=True)
            with open(f"public/{full_path}", "w") as f:
                f.write(template.render(posts=post_metadata))

def parse_front_matter(text):
    def match_and_advance(text, pattern):
        p = re.compile(pattern)
        match = p.match(text)
        size = match.end() - match.start()
        value = text[0:size]
        return (value, text[size:])
    value, text = match_and_advance(text, "---\n")
    value, text = match_and_advance(text, "[\s\S]+(?=---)")
    config = {}
    for l in [x for x in value.split("\n") if x]:
        a, b = l.split(":")
        config[a.strip()] = b.strip()
    value, text = match_and_advance(text, "---\n")
    return text, config

def start_server():
    import http.server
    import socketserver
    serve_path = os.path.join(pathlib.Path().absolute(), 'public')
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=serve_path, **kwargs)
    PORT = 8080
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving files at {serve_path} on port {PORT}")
        httpd.serve_forever()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="Hawberry - Static Site Generator")
    subparsers = parser.add_subparsers(help='sub-command help', dest='command')

    parser_a = subparsers.add_parser('new', help='a help')
    parser_a.add_argument('type', type=str, help='project? post?')
    parser_a.add_argument('name', type=str, help='name of site')

    parser_b = subparsers.add_parser('build', help='a help')

    parser_c = subparsers.add_parser('serve', help='server')

    args = parser.parse_args()
    if args.command == "new":
        if args.type == "site":
            new_site(args.name)
        if args.type == "post":
            new_post(args.name)
    if args.command == "build":
        build_site()
    if args.command == "serve":
        start_server()
