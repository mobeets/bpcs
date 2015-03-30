import os
from difflib import HtmlDiff
from tempfile import mkstemp

import webbrowser
GET_BROWSER = webbrowser.get("open -a '/Applications/Google Chrome.app' %s")

def show_html_diff((f1, f1_name), (f2, f2_name)):
    assert type(f1) is str
    assert type(f2) is str
    fid, htmlfile = mkstemp('.html')
    html = HtmlDiff().make_file(f1.split('\n'), f2.split('\n'), f1_name, f2_name, False, 0)
    with open(htmlfile, 'w') as f:
        f.write(html)
        os.close(fid)
        GET_BROWSER.open_new_tab(htmlfile)
        return htmlfile
    os.close(fid)
    return ''
