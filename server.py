from __future__ import print_function
from __future__ import unicode_literals

import os
import sys
from atexit import register

from flask import Flask, request

from recipe import Recipe

root_dir = os.path.dirname(__file__)
app = Flask(__name__,
            template_folder=os.path.join(root_dir, 'static', 'templates'),
            static_folder=os.path.join(root_dir, 'static')
            )


def main():
    try:
        port = int(sys.argv[1])
    except:
        print("Usage: %s <port>" % sys.argv[0])
        return

    resource_dir = os.path.join(root_dir, 'resources')
    Recipe.set_resource_dir(resource_dir)

    Recipe.load_recipe()
    register(Recipe.save_recipe)

    app.add_url_rule('/', view_func=Recipe.as_view('recipe'))
    app.run(host='0.0.0.0', port=port, debug=True)


if __name__ == "__main__":
    main()
