import argparse
import os
import markdown2
if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="Parsing")
    subparsers = parser.add_subparsers(help='sub-command help', dest='command')
    parser_a = subparsers.add_parser('new', help='a help')
    parser_a.add_argument('type', type=str, help='project? post?')
    parser_a.add_argument('--name', type=str, required=True, help='name of project')
    parser_b = subparsers.add_parser('build', help='a help')
    parser_c = subparsers.add_parser('serve', help='server')
    args = parser.parse_args()
    if args.command == "new":
        if args.type == "project":
            os.mkdir(args.name)
            os.makedirs(f"{args.name}/public")
            os.makedirs(f"{args.name}/content/posts")
    if args.command == "serve":
        import http.server
        import socketserver
        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory="/Users/alin/src/alan/hawberry/wow/public", **kwargs)
        PORT = 8080
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print("serving at port", PORT)
            httpd.serve_forever()
    if args.command == "build":
        files = os.listdir(f"wow/content/posts")
        for fname in files:
            fp = os.path.join("wow/content/posts", fname)
            with open(fp, 'r') as fc:
                rawc = fc.read()
                import re
                matches = re.findall(r'---[\s\S]+---', rawc)
                print(matches)
                content = markdown2.markdown(rawc).strip()
                with open("wow/layout/base.html", 'r') as base:
                    base_content = base.read()
                    output = base_content.replace("{{content}}", content)
                    os.makedirs("wow/public/posts", exist_ok=True)
                    name_without_ext = os.path.splitext(fname)[0]
                    with open(f"wow/public/posts/{name_without_ext}.html", "w") as output_file:
                        output_file.write(output)
