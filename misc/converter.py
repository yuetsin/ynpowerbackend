#!/usr/bin/env python3

import re

def _to_snake(camel: str) -> str:
    return re.sub(r'(?<!^)(?=[A-Z])', '_', camel).lower()


components = []

for line in sorted(open('./apis').read().splitlines(keepends=False)):
    name, _url = line.replace("bind <class '__main__.", '').split("'> to ")
    url = _url.replace('/api/', '/api/#{schema}/')
    components.append((name, url))


with open('routes.rb', 'w') as f:
    f.write('class ElectricProjectApplicationController < ActionController::Base\n')
    f.write("\tconfig.action_mailer.default_url_options = {\n\t\t:host => 'localhost:5000'\n\t}\n")
    for name, url in components:
        f.write('\t%s :to => "%s"\n' % (_to_snake(name), url))
    f.write('end\n')