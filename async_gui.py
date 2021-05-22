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
			dpg.set_main_window_size(550, 600)
			dpg.set_main_window_resizable(False)
			
			dpg.add_checkbox('renderSkeleton', callback=self.__onOptionUpdated)
			dpg.add_slider_float3('lightPos',min_value=-5,max_value=5, default_value=self.host.lightPos, callback=self.__onOptionUpdated)
			lightColor = [255*component for component in self.host.lightColor]
			dpg.add_color_picker3('lightColor', default_value=lightColor, callback=self.__onOptionUpdated)
			
		dpg.start_dearpygui(primary_window="Main Window")

	def __onOptionUpdated(self, sender, data):
		value = dpg.get_value(sender)
		if sender=='lightColor':
			value = [component/255 for component in value[:-1]]
		self.host.setOptionAsync(sender, value)
		#self.host.renderSkeleton=True
