import urllib
import httplib

import sublime_plugin
import sublime


class DpasteCommand(sublime_plugin.TextCommand):
    """
    Pastes the selected test to dpaste.com and copies the URL to the clipboard
    """
    SYNTAXES = {
        'py': 'Python',
        'sql': 'Sql',
        'js': 'JScript',
        'css': 'Css',
        'xml': 'Xml',
        'diff': 'Diff',
        'rb': 'Ruby',
        'rhtml': 'Rhtml',
        'hs': 'Haskell',
        'sh': 'Bash'
    }

    def run(self, edit):
        params = urllib.urlencode({
            'content': self.get_selected_content(),
            'language': self.view.file_name() and DpasteCommand.SYNTAXES.get(self.view.file_name().split('.')[-1], '') or ''
        })

        connection = httplib.HTTPConnection('dpaste.com')
        connection.request('POST', '/api/v1/', params)
        response = connection.getresponse()

        if response.status == 302:
            sublime.set_clipboard(response.getheader('Location', ''))
            sublime.status_message("Dpaste URL has been copied to clipboard")
        else:
            sublime.status_message("There was an error. Please try again later.")

    def get_selected_content(self):
        """
        Return the selected region or the entire buffer contents
        if no region is selected.
        """
        content = '\n'.join([self.view.substr(region) for region in self.view.sel()])
        if not content:
            content = self.view.substr(sublime.Region(0, self.view.size()))
        return content
