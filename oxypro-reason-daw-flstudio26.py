# name=OXYGENPRO-XPORT-OBL # that is for FL Studio to list this profile when it parses the available profiles on startup
#
# @oshablue on github
# Please see README.md in this repo
#
# Use as a controller profile for M-Audio Oxygen Pro 49 
# set to REASON DAW mode with FL Studio 2026 to enable transport controls 
# like record, loop, forward, backward
#
# Tested on Mac OS Tahoe with OxyPro49 FW v2.1.2 Nov 2022
#
# 10-26-26 v1.0
# 
# Key Resource is:
# https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/midi_scripting.htm
# Image-Line's Python implementation API
#
# Inspiration & Acknowledgments:
# See also this repo's (@oshablue) README for inspiration, acknowledgments, and references
#
# Gratuitous' forum announcement:
# https://forum.image-line.com/viewtopic.php?f=1994&t=253539
# and their contact at https://itsGratuiTous.com/contact
# 
# And see the 2020 implementation from PotcFdk:
# https://github.com/PotcFdk/FLStudioOxygenPro49 
#
#
# See this (@oshablue) repo's README for Installation and Configuration details
#
# There are several M-Audio Oxygen (Pro) Models. The concept is basically the same. In fact, you could probably 
# modify this script for any kind of device as long as you map out the controls and messages.
#
# Way to go Image-Line for implementing this Python scripting API.
#
#
# TODO FUTURE
# - Implement other non-natively or default-ly implemented control messages from the controller
#

# Message data1 values for what we want to implement
# Use FL Studio's Debugging log to see messages from control button presses under various DAW modes on the OxyPro49 for example
# BC = control change message
# the next number in the triplet is the data1, like the particular button for example
# the 3rd value is similar to a note's pressure/velocity for example
# Here, for transport, in the REASON DAW OP49 profile
# 0xBC => 0xB0 | 0x0C where 0xB0 is the control change message upper nibble and 0x0C is the channel
# In this script, we just look for the control change message and forget about the channel, to capture any channel, 
# for now. You can see MIDI implementation guides elsewhere to dig in. At the moment, here, the more general, the 
# better, until specifics are needed.
# The value 0x7F means all the way "ON", so like when the Play Button is pressed, that is, first clicked down
# And then the value 0x00 means all the way "OFF", so like when the Play Button is released.
#


# MIDI Event Data (event.data1) values that need to be caught and acted upon (handled)
# Below are decimal values or you can just use hex, as this is python
# FL Studio's debugging log shows the messages as hex
# The OxyPro49 in REASON DAW mode also outputs the FA and FC messages for the Play and Stop buttons
# and those are natively handled by the generic controller profile, so we are omitting them here
# as it is unnecessary and breaks or doubles the response, needing a 3rd response to get back to response 1
# if you know what is meant there
#

import transport    # Transport controls
import ui           # To be able to print stuff to the little hint area top left in FL Studio
import midi         # MIDI message processing and fields

xport_rec =   0x74   # 116 		# BC 74 7F/00
xport_loop =  0x75   # 117 		# BC 75 7F/00
xport_back =  0x70   # 112		# BC 70 7F/00
xport_fwd =   0x71   # 113	    # BC 71 7F/00
#xport_play = 0x73   # 115 		# BC 73 7F/00 # natively handled
#xport_stop = 0x72   # 114 		# BC 72 7F/00 # natively handled

# See Image-Line's API:
# https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/midi_scripting.htm

def OnMidiMsg(event):

    # When it hits this code, set to False unless it is truly handled herein
    event.handled = False

    if ( 
        (event.status & 0xF0) == midi.MIDI_CONTROLCHANGE
        and event.data2 > 0 # Handle only the click button down event not the release message
    ):

        if event.data1 == xport_loop:
            transport.setLoopMode()
            ui.setHintMsg('Pattern Mode' if transport.getLoopMode() else 'Song Mode') # Gotta love it
            event.handled = True

        elif event.data1 == xport_rec:
            transport.record()          # Brings up the generic record mode/type selection modal window
            ui.setHintMsg('Not Recording' if transport.isRecording() else 'Recording')
            event.handled = True 

        elif event.data1 == xport_back:
            transport.globalTransport(midi.FPT_Jog, -1, 2, 8) # See API docs: (command is FPT_Jog, value as bars, pmeflags = PME_System, flags = GT_Global)
            ui.setHintMsg('<<')
            event.handled = True 

        elif event.data1 == xport_fwd:
            transport.globalTransport(midi.FPT_Jog, 1, 2, 8) # See API docs: (command is FPT_Jog, value as bars, pmeflags = PME_System, flags = GT_Global)
            ui.setHintMsg('>>')
            event.handled = True

    # TODO FUTURE could add any other unhandled messages here if they are transmitted in REASON DAW mode - TBD
    # End if data2 (value) > 0 handling keypress event (not keyup) for MIDI_CONTROLCHANGE

