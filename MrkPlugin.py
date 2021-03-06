# coding: utf-8

import json
import os
import platform
import sublime
import sublime_plugin
import pdb
from subprocess import Popen, PIPE

# monkeypatch `Region` to be iterable
sublime.Region.totuple = lambda self: (self.a, self.b)
sublime.Region.__iter__ = lambda self: self.totuple().__iter__()

SCRIPT_PATH = os.path.join(sublime.packages_path(), os.path.dirname(os.path.realpath(__file__)), 'js-plugin-code.js')

template = '''
<span>
Phantom
<a href="copy-stuff">copy</a> |
<a href="close"><close>x</close></a>
</span>
'''


class MrkPluginCommand(sublime_plugin.TextCommand):
    def __init__(self, view):
        self.view = view

    def run(self, edit):
        config = self.get_config()

        if not self.has_selection():
            region = sublime.Region(0, self.view.size())
            originalBuffer = self.view.substr(region)
            processed = self.process(originalBuffer, config)
            if processed:
                self.view.replace(edit, region, processed)
            return
        for region in self.view.sel():
            if region.empty():
                continue
            originalBuffer = self.view.substr(region)
            processed = self.process(originalBuffer, config)
            if processed:
                self.view.replace(edit, region, processed)

    def process(self, text, config):
        config = json.dumps(config)
        folder = os.path.dirname(self.view.file_name())
        try:
            p = Popen(['node', SCRIPT_PATH] + [config, folder],
                stdout=PIPE, stdin=PIPE, stderr=PIPE,
                env=self.get_env(), shell=self.is_windows())
        except OSError:
            raise Exception("Couldn't find Node.js. Make sure it's in your " +
                            '$PATH by running `node -v` in your command-line.')
        stdout, stderr = p.communicate(input=text.encode('utf-8'))
        if stdout:
            return stdout.decode('utf-8')
        else:
            sublime.error_message('JS plugin error error:\n%s' % stderr.decode('utf-8'))

    def get_env(self):
        # env = None
        # print('=======') 
        # print(os.environ.copy()) 
        # print('=======') 
        # pdb.set_trace()
        env = os.environ.copy()
        # if self.is_osx():
            # env['PATH'] += self.get_node_path()
        return env

    def get_node_path(self):
        return self.get_settings().get('node-path')

    def get_settings(self):
        settings = self.view.settings().get('MrkPlugin')
        if settings is None:
            settings = sublime.load_settings('MrkPlugin.sublime-settings')
        return settings

    def get_config(self):
        settings = self.get_settings()
        config = settings.get('config')
        return config

    def has_selection(self):
        for sel in self.view.sel():
            start, end = sel
            if start != end:
                return True
        return False

    def is_osx(self):
        return platform.system() == 'Darwin'

    def is_windows(self):
        return platform.system() == 'Windows'

