import argparse
import os
import markdown2
import re
import shutil

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
                # FIXME: this should serve when run in the root project 
                super().__init__(*args, directory="public/", **kwargs)
        PORT = 8080
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print("serving at port", PORT)
            httpd.serve_forever()
    if args.command == "build":
        ignored = {"templates"}
        files = [f for f in os.listdir(f"posts") if f not in ignored]
        for fname in files:
            fp = os.path.join("posts", fname)
            with open(fp, 'r') as fc:
                rawc = fc.read()
                text, config = parse(rawc)
                content = markdown2.markdown(text).strip()
                with open("layouts/base.html", 'r') as base:
                    base_content = base.read()
                    output = base_content.replace("{{content}}", content)
                    os.makedirs("public/posts", exist_ok=True)
                    name_without_ext = os.path.splitext(fname)[0]
                    with open(f"public/posts/{name_without_ext}.html", "w") as output_file:
                        output_file.write(output)
