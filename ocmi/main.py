#!/usr/bin/env python
import types
from snack import SnackScreen, ButtonChoiceWindow, Entry, EntryWindow, ListboxChoiceWindow

from ocmi.config import c, cs

VERSION = '0.0.1'
TITLE='OCMI-tester v%s' % VERSION


class OCMITester(object):

    def menu_exit(self):
        pass

    def _display_selection(self, list_of_items, subtitle, default = None):
        """Display a list of items, return selected one or None, if nothing was selected"""
        if len(list_of_items) > 0:
            if not isinstance(list_of_items[0], types.TupleType):
                # if we have a list of strings, we'd prefer to get these strings as the selection result
                list_of_items = zip(list_of_items, list_of_items)
            height = 10
            scroll = 1 if len(list_of_items) > height else 0
            action, selection = ListboxChoiceWindow(self.screen, TITLE, subtitle, list_of_items, 
                                ['Ok', 'Back'], scroll = scroll, height = height, default = default)
            if action != 'back':
                return selection
        else:
            ButtonChoiceWindow(self.screen, TITLE, 'Sorry, there are no items to choose from', ['Back'])
        return None

    def display_main_screen(self):
        """Display main menu of the OCMI Tester"""
        logic = {'exit': self.menu_exit,
                 'configure': self.display_configure,
                 'occi': self.display_occi,
                 'cdmi': self.display_cdmi,
                 'runall': self.display_run_all,
                 }

        result = ButtonChoiceWindow(self.screen, TITLE, 'Welcome to the OCMI-tester', \
                [('Exit', 'exit'),
                ('Configure', 'configure'),
                ('OCCI tests', 'occi'),
                ('CDMI tests', 'cdmi'),
                ('Run all tests', 'runall'),
                ],
                42)
        logic[result]()

    def display_configure(self):
        """Display a selection menu for OCCI/CDMI configuration"""
        logic = {'exit': self.display_main_screen,
                 'occi': self.display_configure_occi,
                 'cdmi': self.display_configure_cdmi,
                 }

        result = ButtonChoiceWindow(self.screen, TITLE, 'Please, choose endpoint to configure:', \
                [('Exit', 'exit'),
                ('OCCI', 'occi'),
                ('CDMI', 'cdmi'),
                ],
                42)
        logic[result]()

    def display_configure_occi(self):
        """Display OCCI configuration menu"""
        occi_entry = Entry(30, c('occi', 'server'))
        occi_input_entry = Entry(30, c('occi', 'input_rendering'))
        occi_output_entry = Entry(30, c('occi', 'output_rendering'))
        command, _ = EntryWindow(self.screen, TITLE, 'Please, enter OCCI endpoint parameters',
                [('OCCI endpoint', occi_entry),
                 ('OCCI input rendering', occi_input_entry),
                 ('OCCI output rendering', occi_output_entry)], 
                buttons = [('Save', 'save'), ('Back', 'main_menu')])
        if command == 'save':
            cs('occi', 'server', occi_entry.value().strip())
            cs('occi', 'input_rendering', occi_input_entry.value().strip())
            cs('occi', 'output_rendering', occi_output_entry.value().strip())
        self.display_main_screen()

    def display_configure_cdmi(self):
        """Display CDMI configuration menu"""
        cdmi_entry = Entry(30, c('cdmi', 'cdmi_server'))
        cdmi_user_entry = Entry(30, c('cdmi', 'username'))
        cdmi_pass_entry = Entry(30, c('cdmi', 'password'))
        command, _ = EntryWindow(self.screen, TITLE, 'Please, enter CDMI endpoint parameters',
                [('CDMI endpoint', cdmi_entry),
                 ('Username', cdmi_user_entry),
                 ('Password', cdmi_pass_entry)], 
                buttons = [('Save', 'save'), ('Back', 'main_menu')])
        if command == 'save':
            cs('cdmi', 'server', cdmi_entry.value().strip())
            cs('cdmi', 'username', cdmi_user_entry.value().strip())
            cd('cdmi', 'password', cdmi_pass_entry.value().strip())
        self.display_main_screen()

    def display_occi(self):
        """Displays a list of OCCI tests"""
        dummy_tests = ['OCCI test 1', 'OCCI test 2', 'OCCI test 3']
        return self._display_selection(dummy_tests, "Select an OCCI test from" % dummy_tests)

    def display_cdmi(self):
        """Displays a list of CDMI tests"""
        dummy_tests = ['CDMI test 1', 'CDMI test 2', 'CDMI test 3']
        return self._display_selection(dummy_tests, "Select a CDMI test from" % dummy_tests)

    def display_run_all(self):
        pass

    def run(self):
        self.screen = SnackScreen()
        self.display_main_screen()
        self.screen.finish()

if __name__ == "__main__":
    tui = OCMITester()
    tui.run()
