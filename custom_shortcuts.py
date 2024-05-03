#!/usr/bin/env python # -*- coding: utf-8 -*- #

# NAUTILUS CUSTOM SHORTCUTS
# This file sets up custom shortcuts for Nautilus.
# By Luke Needham - LukeNeedham.com
# Based on work by Ricardo Lenz - riclc@hotmail.com
#
# SETUP
# First make sure 'Nautilus Python' is installed:
# `sudo apt install python3-nautilus`
# Learn more at:
# https://wiki.gnome.org/Projects/NautilusPython
#
# Then, place this file at: `.local/share/nautilus-python/extensions/custom_shortcuts.py`
#
# TERMINOLOGY
# GTK refers to shortcuts as 'accelerators', or 'accels' for short.
# See the relevant GTK docs here: https://docs.gtk.org/gtk3/class.Application.html
#
# CONFIGURE
# To edit shortcuts, follow these steps:
# - Set the `debug` flag to `True` - this will help with debugging
# - Restart Nautilus from the terminal with: `killall nautilus; nautilus &`
# - Check the logs in the terminal - it will list every action and its current shortcuts
# - In `configure`, add a `bind` call for every action you want a custom shortcut for
# - Restart Nautilus and check the terminal logs to see that your custom shortcuts were applied
# - Test your shortcuts in Nautilus for real
# - When you're done, set the `debug` flag back to `False` to avoid log spam
# - Enjoy!

import os, gi
gi.require_version('Nautilus', '3.0')
from gi.repository import GObject, Nautilus, Gtk, Gio, GLib

# Set to True while configuring shortcuts, to help with debugging.
# Set to False when finished, to avoid log spam.
debug = True

app = Gtk.Application.get_default()

# Helper to set shortcuts to an action.
# This will remove any other shortcuts previously assigned to `action`,
# and also remove `shortcut` from any other action previously bound to `shortcut`.
# Params:
# - action - a valid 'detailed_action_name'.
#   Use `logShortcuts` to see valid values of `action`.
# - shortcut - a list of valid keysyms - you can use xev to find these values
def bind(action, shortcuts):
    # Remove existing bindings as multiple actions for the same shortcut is usually not desired
    for shortcut in shortcuts:
        conflictingActions = app.get_actions_for_accel(shortcut)
        for conflictingAction in conflictingActions:
            allAccels = app.get_accels_for_action(conflictingAction)
            # Only remove the conflicting shortcut for the conflicting action - 
            # the other shortcuts can stay
            allAccels.remove(shortcut)
            app.set_accels_for_action(conflictingAction, allAccels)

    app.set_accels_for_action(action, shortcuts)

# Sets the custom shortcuts. Edit these values to change shortcuts.
def configure():
    # Define your custom shortcuts below!
    bind("view.new-folder", ["<Primary><Shift>o"])
    bind("view.rename", ["<Primary>k"])
    bind("win.back", ["<Primary>t"])
    bind("win.forward", ["<Primary>n"])
    bind("win.tab-previous", ["<Primary>d"])
    bind("win.tab-next", ["<Primary>h"])
    bind("win.restore-tab", ["<Primary><Shift>e"])
    bind("win.close-current-view", ["<Primary>w", "<Primary>e"])


# Debug function to print actions and their current shortcuts.
# Useful during configuration to see what actions are available, 
# and to check that their shotcuts are set correctly.
#
# Note that this will NOT log ALL valid actions!
# It will only log the actions that currently have shortcuts bound.
# Some actions don't have default shortcuts bound - 
# in those cases you have to find the action name in other ways.
def logShortcuts():
    # Lists all actions which you can set shortcuts for
    # Each string in this list is the 'detailed_action_name'
    actions = app.list_action_descriptions()
    # Sort alphabetically because it makes reading the list much easier
    actionsAlphabetical = sorted(actions)
    print("CURRENT SHORTCUTS:")
    for action in actionsAlphabetical:
        accels = app.get_accels_for_action(action)
        log = action + " : " + str(accels)
        print(log)
    

class CustomAccels(GObject.GObject, Nautilus.LocationWidgetProvider):
    def __init__(self):
        pass
    
    def get_widget(self, uri, window):
        configure()
        if(debug):
            logShortcuts()
        return None
