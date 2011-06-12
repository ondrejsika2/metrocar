'''
Created on 17.3.2010

@author: xaralis
'''

from django import template

register = template.Library() 

class ActivePages(template.Node):

    def __init__(self, string, out, strict):
        self.string = string.decode('utf-8')
        self.strict = strict
        self.out = out

    def render(self, context):
        req = context['request']
        self.string = template.Variable(self.string).resolve(context)

        try:
            path = req.get_full_path()

            for str in self.string.split(','):
                if path.find(str) == 0:
                    if self.strict:
                        if len(path) != len(str): continue
                    return self.out
        except:
            pass

        return ""

@register.tag
def in_active_pages(parser, token):
    """
    Prints out class="active" if given string is in active pages.

    Syntax:
        {% in_active_pages 'varname,varname2' 'str-to-add' [strict] %}

    Example usage:
        {% in_active_pages '/o-nas/,/skolni-jidelna/' 'id="tray-active"' strict %}
    """

    input = token.split_contents()

    if len(input) < 3:
        raise template.TemplateSyntaxError, "%r tag requires at least 1 argument" % input[0]

    if "strict" in input:
        return ActivePages(input[1], input[2], True)
    else:
        return ActivePages(input[1], input[2], False)