import dearpygui.core as dpg
import dearpygui.simple as sdpg
import threading

from OpenGL.GL import *

class AsyncGUI(threading.Thread):
	def __init__(self, host):
		threading.Thread.__init__(self)
		self.host = host
	def run(self):
		with sdpg.window('Main Window'):
			dpg.set_main_window_size(550, 550)
			dpg.set_main_window_resizable(False)
			
			dpg.add_checkbox('renderSkeleton', callback=self.__onOptionUpdated)
		dpg.start_dearpygui(primary_window="Main Window")

	def __onOptionUpdated(self, sender, data):
		#print(dpg.get_value(sender))
		self.host.setOptionAsync(sender, dpg.get_value(sender))
		#self.host.renderSkeleton=True
