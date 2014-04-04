#!/usr/bin/env python
import cmd
import json
import optparse
import pydoc
import sys

from pydiscourse.client import DiscourseClient


class DiscourseCmd(cmd.Cmd):
    prompt = 'discourse>'
    output = sys.stdout

    def __init__(self, client):
        cmd.Cmd.__init__(self)
        self.client = client
        self.prompt = '%s>' % self.client.host

    def __getattr__(self, attr):
        if attr.startswith('do_'):
            method = getattr(self.client, attr[3:])

            def wrapper(arg):
                args = arg.split()
                return method(*args)

            return wrapper
        elif attr.startswith('help_'):
            method = getattr(self.client, attr[5:])

            def wrapper():
                self.output.write(pydoc.render_doc(method))

            return wrapper

        raise AttributeError

    def postcmd(self, result, line):
        try:
            json.dump(result, self.output, sort_keys=True, indent=4, separators=(',', ': '))
        except TypeError:
            self.output.write(result.text)


def main():
    op = optparse.OptionParser()
    op.add_option('--host', default='localhost')
    op.add_option('--api-user', default='system')
    op.add_option('--api-key')

    options, args = op.parse_args()
    client = DiscourseClient(options.host, options.api_user, options.api_key)

    c = DiscourseCmd(client)
    if args:
        line = ' '.join(args)
        result = c.onecmd(line)
        c.postcmd(result, line)
    else:
        c.cmdloop()


if __name__ == '__main__':
    main()
