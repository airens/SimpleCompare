from fman import DirectoryPaneCommand, show_alert, load_json, OK, CANCEL, DirectoryPane
from fman.fs import exists
from fman.url import as_human_readable, join

import subprocess
from .settings import Settings

# TODO it would be good to display it in the "CompareWithSaved" command in the command palete
"""Currently selcted file to compare"""
savedToCompare = ""
settings = Settings()

class SaveToCompare(DirectoryPaneCommand):
    def __call__(self):
        global savedToCompare
        savedToCompare = self.get_chosen_files()[0]

    def is_visible(self):
        files = self.get_chosen_files()
        return len(files) == 1


class CompareWithSaved(DirectoryPaneCommand):
    def __call__(self):
        global savedToCompare
        selectedFile = self.get_chosen_files()[0]
        ComparisonToolRunner.compare_files(savedToCompare, selectedFile)
        pass

    def is_visible(self):
        global savedToCompare
        return savedToCompare != "" and len(self.get_chosen_files()) == 1

class CompareByContent(DirectoryPaneCommand):
    def __call__(self):
        ComparisonToolRunner.compare_files(self.selectedFile1, self.selectedFile2)
        pass

    def is_visible(self):
        files_len = len(self.get_chosen_files())
        self.selectedFile1 = self.pane.get_file_under_cursor()
        if files_len == 1:
            other_path = self._other_pane().get_path()
            if other_path == self.pane.get_path():
                return false
            fname = self.selectedFile1
            self.selectedFile2 = join(other_path, fname.split('/')[-1])
            return exists(self.selectedFile2)
        else:
            self.selectedFile2 = self.get_chosen_files()[1]
            return files_len == 2

    def _other_pane(self):
        panes = self.pane.window.get_panes()
        this_pane = panes.index(self.pane)
        return panes[(this_pane + 1) % len(panes)]

class ComparisonToolRunner:
    @staticmethod
    def compare_files(lhsFile: str, rhsFile: str):
        global settings
        comparisonTool = settings.get_comparison_tool()
        if comparisonTool:
            subprocess.call([comparisonTool, as_human_readable(lhsFile), as_human_readable(rhsFile)])

def _ifnull(var, val):
  if var is None:
    return val
  return var

