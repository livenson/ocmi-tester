#!/usr/bin/env python
import types

from snack import SnackScreen, ButtonChoiceWindow, Entry, EntryWindow, ListboxChoiceWindow

VERSION = '0.0.1'
TITLE='OCMI-tester v%s' % VERSION


class OCMITester(object):

    def __init__(self):
        self.cdmi_server = 'sample'
        self.occi_server = 'sample'

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
        occi_entry = Entry(30, self.occi_server)
        cdmi_entry = Entry(30, self.cdmi_server)
        command, oms_address = EntryWindow(self.screen, TITLE, 'Please, enter OCCI and CDMI endpoints',
                [('OCCI endpoint', occi_entry),
                 ('CDMI endpoint', cdmi_entry)], 
                buttons = [('Save', 'save'), ('Back', 'main_menu')])
        if command == 'save':
            self.occi_server = occi_entry.value().strip()
            self.cdmi_entry = cdmi_entry.value().strip()
        self.display_main_screen()

    def display_occi(self):
        """Displays a list of OCCI tests"""
        dummy_tests = ['OCCI test 1', 'OCCI test 2', 'OCCI test 3']
        return self._display_selection(dummy_tests, "Select an OCCI test from" % dummy_tests)

    def display_cdmi(self):
        pass

    def display_run_all(self):
        pass

    def run(self):
        self.screen = SnackScreen()
        self.display_main_screen()
        self.screen.finish()

if __name__ == "__main__":
    tui = OCMITester()
    tui.run()
