import wx
from gui.wxFrameLogin import wxFrameLogin
from gui.wxFrameToken import wxFrameToken
from gui.wxFrameChooser import wxFrameChooser
from gui.wxFrameOptions import wxFrameOptions
from gui.wxFrameDownload import wxFrameDownload

import facebook
import helpers
import downloader

import time
import logging
import os
import multiprocessing

class PhotoGrabberGUI(wx.App):
    """Control and Data Structure for GUI.

    helper - Instance of the facebook object.  Performs Graph API queries.

    target_list - People/pages to download.

    frame - Current GUI frame (wxFrame).  The PhotoGrabberGUI object is passed
            to the frame to pass data and issue control follow events.

            Each frame must implement a Setup() function and call the
            appropriate PhotoGrabberGui.to* function to advance to next frame.
    """

    logger = logging.getLogger('PhotoGrabberGUI')
    helper = None
    target_list = []

    def OnInit(self):
        wx.InitAllImageHandlers()
        self.frame = wxFrameLogin(None, -1, "")
        self.frame.Setup(self)
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return 1

    def __nextFrame(self, frame):
        """Destroy current frame then create and setup the next frame."""
        self.frame.Destroy()
        self.frame = frame
        self.frame.Setup(self)
        self.frame.Show()

    # workflow functions (called by frames)
    #   login window
    #   token window
    #   chooser window
    #   options window
    #   folder dialog
    #   download status

    def toToken(self):
        facebook.request_token()
        self.__nextFrame(wxFrameToken(None, -1, ""))

    def toChooser(self, token):
        self.helper = helpers.Helper(facebook.GraphAPI(token))
        my_info = self.helper.get_me()
        if my_info == False:
            self.logger.error('Provided Token Failed')

        self.target_list.append(my_info)
        self.target_list.extend(self.helper.get_friends('me'))
        self.target_list.extend(self.helper.get_pages('me'))
        self.target_list.extend(self.helper.get_subscriptions('me'))

        # it is possible that there could be multiple 'Tommy Murphy'
        # make sure to download all different versions that get selected

        self.__nextFrame(wxFrameChooser(None, -1, ""))

    def toOptions(self):
        self.__nextFrame(wxFrameOptions(None, -1, ""))

    def toFolder(self):
        # TODO: present folder choser
        self.toDownload()

    def toDownload(self):
        self.__nextFrame(wxFrameDownload(None, -1, ""))

    def beginDownload(self, update):
        # TODO: implement download/status updates
        pass

# end of class PhotoGrabberGUI

def start():
    PhotoGrabber = PhotoGrabberGUI(0)
    PhotoGrabber.MainLoop()
