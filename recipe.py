from __future__ import print_function
from __future__ import unicode_literals

import os
import json
import requests

from flask import request, render_template
from flask.views import View


class Recipe(View):
    recipe = None
    resource_dir = None

    @classmethod
    def set_resource_dir(cls, path):
        cls.resource_dir = path

    @classmethod
    def recipe_json_path(cls):
        return os.path.join(cls.resource_dir, "recipe.json")

    @classmethod
    def load_recipe(cls):
        try:
            with open(cls.recipe_json_path()) as f:
                cls.recipe = json.load(f)
            print('recipe loaded')
        except Exception as e:
            print("Unable to load recipe: %s" % e)

    @classmethod
    def save_recipe(cls):
        if cls.recipe is not None:
            try:
                with open(cls.recipe_json_path(), 'w') as f:
                    json.dump(cls.recipe, f, sort_keys=True,
                              separators=(',', ';'))
                print('recipe saved')
            except Exception as e:
                print("Unable to save recipe: %s" % e)

    def __init__(self):
        super(Recipe, self).__init__()
        if Recipe.recipe is None:
            self.update_recipe()

    @classmethod
    def update_recipe(cls):
        resp = requests.get('https://thegorge.kleientertainment.com/items?csrfKey=c4d3983934eb2b3ad6994d2ce2d6e42a')
        if resp.status_code != 200:
            raise Exception("Unable to get recipe: %d, %s" % (resp.status_code, resp.text))
        cls.recipe = json.loads(resp.text)
        print('recipe updated')

    def dispatch_request(self):
        if request.args.get('update') == '1':
            self.update_recipe()
        keys = sorted(map(int, self.recipe.keys()))
        recipe = []
        cravings = set()
        stations = set()
        for k in keys:
            d = self.recipe[str(k)].copy()
            d['id'] = int(k)
            c = d.get('cravings')
            if c is not None:
                cravings.update(c)
            s = d.get('station')
            if s is not None:
                stations.update(s)
            recipe.append(d)
        return render_template('recipe.html',
                               cravings=sorted(cravings),
                               stations=sorted(stations),
                               recipe=recipe,
                               )
