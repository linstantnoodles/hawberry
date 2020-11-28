import argparse
import os
import markdown2
import re
import shutil
import pathlib
def parse(text):
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
if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="Parsing")
    subparsers = parser.add_subparsers(help='sub-command help', dest='command')
    parser_a = subparsers.add_parser('new', help='a help')
    parser_a.add_argument('type', type=str, help='project? post?')
    parser_a.add_argument('name', type=str, help='name of site')
    parser_b = subparsers.add_parser('build', help='a help')
    parser_c = subparsers.add_parser('serve', help='server')
    args = parser.parse_args()
    if args.command == "new":
        if args.type == "site":
            shutil.copytree("directory", args.name)
        if args.type == "post":
            shutil.copyfile("posts/templates/default.md", f"posts/{args.name}") 
    if args.command == "serve":
        import http.server
        import socketserver
        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                serve_path = os.path.join(pathlib.Path().absolute(), 'public')
                super().__init__(*args, directory=serve_path, **kwargs)
        PORT = 8080
        socketserver.TCPServer.allow_reuse_address = True
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print("serving at port", PORT)
            httpd.serve_forever()
    if args.command == "build":
        from jinja2 import Environment, FileSystemLoader, select_autoescape
        env = Environment(
            loader=FileSystemLoader(['layouts', 'pages']),
            autoescape=select_autoescape(['html', 'xml'])
        )
        template = env.get_template('base.html')
        ignored = {"templates"}
        files = [f for f in os.listdir(f"posts") if f not in ignored]
        for fname in files:
            fp = os.path.join("posts", fname)
            with open(fp, 'r') as fc:
                rawc = fc.read()
                text, config = parse(rawc)
                content = markdown2.markdown(text).strip()
                os.makedirs("public/posts", exist_ok=True)
                name_without_ext = os.path.splitext(fname)[0]
                with open(f"public/posts/{name_without_ext}.html", "w") as output_file:
                    output_file.write(template.render(content=content))
        for dir_path, dirs, files in os.walk("pages"):
            for name in files:
                rp = dir_path.split('/')[1:]
                parent_path = os.path.join(*rp) if rp else ""
                full_path = os.path.join(*rp, name)
                template = env.get_template(full_path)
                os.makedirs(f"public/{parent_path}", exist_ok=True)
                with open(f"public/{full_path}", "w") as f:
                    f.write(template.render())
