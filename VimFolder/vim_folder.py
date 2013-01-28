import sublime
import sublime_plugin
from functools import partial

class InsertVimFoldingMarkerCommand(sublime_plugin.TextCommand):
    """Making Vim folding marker according to given comment string"""

    def run(self, edit, remarker=None, prompt=False, comment=''):
        if prompt and comment == '':
            self.view.window().show_input_panel(
                "Comment string:",
                str(comment) if comment else '',
                # pass this function as callback
                partial(self.run, edit, remarker, False),
                None, None
            )
            return  # call already handled

        # if comment == '' or (isinstance(comment, basestring) and comment.isspace()):
        #     # emtpy string or whitespaces entered in input panel
        #     return

        if type(comment) == str:
            comment = comment.decode('utf-8')

        if self.view.sel()[0].begin() != self.view.sel()[0].end():
            if comment != '':
                comment = "%s %s " % (remarker, comment)

            start_marker = "%s%s {{{" % (comment, remarker)
            end_marker = "%s }}}" % remarker

            first_line = self.view.line(self.view.sel()[0].begin())
            last_line = self.view.line(self.view.sel()[0].end())

            if first_line.end() - first_line.begin() == 0:
                start_spacing = 0
            else:
                start_spacing = 1

            if last_line.end() - last_line.begin() == 0:
                end_spacing = 0
            else:
                end_spacing = 1

            self.view.insert(edit, last_line.end(), ' '*end_spacing + end_marker)
            self.view.insert(edit, first_line.end(), ' '*start_spacing + start_marker)
