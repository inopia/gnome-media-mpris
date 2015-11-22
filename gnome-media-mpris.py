#!/usr/bin/env python
"""
Send gnome multimedia keys to mpris.MediaPlayer2.Player programs via dbus.

This makes multimedia keys work with programs like VLC and gnome-mplayer.
"""
import gobject
import dbus
import dbus.service
import dbus.mainloop.glib

dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
bus = dbus.Bus(dbus.Bus.TYPE_SESSION)

def on_mediakey(comes_from, what):
    """ gets called when multimedia keys are pressed down.
    """
    print ('comes from:%s  what:%s') % (comes_from, what)
    if what in ['Stop','Play','Next','Previous']:
        print ('Got a multimedia key!')
    else:
        print ('Got a multimedia key...')

    for name in bus.list_names():
        if name.startswith("org.mpris.MediaPlayer2"):
            iface = dbus.Interface(
                bus.get_object(name, '/org/mpris/MediaPlayer2'),
                'org.mpris.MediaPlayer2.Player')

            if what == "Stop":
                iface.Stop()
            elif what == "Play":
                iface.PlayPause()
            elif what == "Next":
                iface.Next()
            elif what == "Previous":
                iface.Previous()


# set up the glib main loop.
bus_object = bus.get_object('org.gnome.SettingsDaemon',
                            '/org/gnome/SettingsDaemon/MediaKeys')

# this is what gives us the multi media keys.
dbus_interface='org.gnome.SettingsDaemon.MediaKeys'
bus_object.GrabMediaPlayerKeys("MyMultimediaThingy", 0,
                               dbus_interface=dbus_interface)

# connect_to_signal registers our callback function.
bus_object.connect_to_signal('MediaPlayerKeyPressed',
                             on_mediakey)

# and we start the main loop.
mainloop = gobject.MainLoop()
mainloop.run()
