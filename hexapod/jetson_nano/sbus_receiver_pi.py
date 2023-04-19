#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
derivated from
	Sokrates80/sbus_driver_micropython git hub
	https://os.mbed.com/users/Digixx/code/SBUS-Library_16channel/file/83e415034198/FutabaSBUS/FutabaSBUS.cpp/
	https://os.mbed.com/users/Digixx/notebook/futaba-s-bus-controlled-by-mbed/
	https://www.ordinoscope.net/index.php/Electronique/Protocoles/SBUS
"""

#dsimonet

import array
import serial
import time

class SBUSReceiver():
	def __init__(self, _uart_port='/dev/ttyS0'):

		#init serial of raspberry pi
		self.ser = serial.Serial(
			port=_uart_port,
			baudrate = 100000,
			parity=serial.PARITY_EVEN,
			stopbits=serial.STOPBITS_TWO,
			bytesize=serial.EIGHTBITS,
			timeout = 0,
		)

		# constants
		self.START_BYTE = b'\x0f'
		self.END_BYTE = b'\x00'
		self.SBUS_FRAME_LEN = 25
		self.SBUS_NUM_CHAN = 18
		self.OUT_OF_SYNC_THD = 10
		self.SBUS_NUM_CHANNELS = 18
		self.SBUS_SIGNAL_OK = 0
		self.SBUS_SIGNAL_LOST = 1
		self.SBUS_SIGNAL_FAILSAFE = 2

		# Stack Variables initialization
		self.lastFrameTime = 0
		self.sbusFrame = bytearray(25)  # single SBUS Frame
		self.sbusChannels = array.array('H', [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])  # RC Channels
		self.sbusChannelsNorm = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # RC Channels
		self.failSafeStatus = self.SBUS_SIGNAL_FAILSAFE


	def get_rx_channels(self):
		"""
		Used to retrieve the last SBUS channels values reading
		:return:  an array of 18 unsigned short elements containing 16 standard channel values + 2 digitals (ch 17 and 18)
		"""

		return self.sbusChannels

	def get_rx_channel(self, num_ch):
		"""
		Used to retrieve the last SBUS channel value reading for a specific channel
		:param: num_ch: the channel which to retrieve the value for
		:return:  a short value containing
		"""

		return self.sbusChannels[num_ch]

	def get_failsafe_status(self):
		"""
		Used to retrieve the last FAILSAFE status
		:return:  a short value containing
		"""

		return self.failSafeStatus

	def scal(self,x, in_min, in_max, out_min, out_max):
		return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
	
	def decode_frame(self):

		# each values are in beetween two or tree differentes bytes . so look the mess to catch it !
		# Thanks futaba to make this.

		self.sbusChannels[0]  = (((self.sbusFrame[0])    	|(self.sbusFrame[1])<<8)									& 0x07FF);
		self.sbusChannels[1]  = (((self.sbusFrame[1])>>3 	|(self.sbusFrame[2])<<5)									& 0x07FF);
		self.sbusChannels[2]  = (((self.sbusFrame[2])>>6 	|(self.sbusFrame[3])<<2 |(self.sbusFrame[4])<<10)		& 0x07FF);
		self.sbusChannels[3]  = (((self.sbusFrame[4])>>1 	|(self.sbusFrame[5])<<7)									& 0x07FF);
		self.sbusChannels[4]  = (((self.sbusFrame[5])>>4 	|(self.sbusFrame[6])<<4)									& 0x07FF);
		self.sbusChannels[5]  = (((self.sbusFrame[6])>>7 	|(self.sbusFrame[7])<<1 |(self.sbusFrame[8])<<9)   	& 0x07FF);
		self.sbusChannels[6]  = (((self.sbusFrame[8])>>2 	|(self.sbusFrame[9])<<6)									& 0x07FF);
		self.sbusChannels[7]  = (((self.sbusFrame[9])>>5	|(self.sbusFrame[10])<<3)									& 0x07FF);
		self.sbusChannels[8]  = (((self.sbusFrame[11])   	|(self.sbusFrame[12])<<8)									& 0x07FF);
		self.sbusChannels[9]  = (((self.sbusFrame[12])>>3	|(self.sbusFrame[13])<<5)									& 0x07FF);
		self.sbusChannels[10] = (((self.sbusFrame[13])>>6	|(self.sbusFrame[14])<<2|(self.sbusFrame[15])<<10)	& 0x07FF);
		self.sbusChannels[11] = (((self.sbusFrame[15])>>1	|(self.sbusFrame[16])<<7)									& 0x07FF);
		self.sbusChannels[12] = (((self.sbusFrame[16])>>4	|(self.sbusFrame[17])<<4)									& 0x07FF);
		self.sbusChannels[13] = (((self.sbusFrame[17])>>7	|(self.sbusFrame[18])<<1|(self.sbusFrame[19])<<9)		& 0x07FF);
		self.sbusChannels[14] = (((self.sbusFrame[19])>>2	|(self.sbusFrame[20])<<6)									& 0x07FF);
		self.sbusChannels[15] = (((self.sbusFrame[20])>>5	|(self.sbusFrame[21])<<3)									& 0x07FF);

		#to be tested, No 17 & 18 channel on taranis X8R
		if (self.sbusFrame[22])  & 0x0001 :
			self.sbusChannels[16] = 2047
		else:
			self.sbusChannels[16] = 0
		#to be tested, No 17 & 18 channel on taranis X8R
		if ((self.sbusFrame[22]) >> 1) & 0x0001 :
			self.sbusChannels[17] = 2047
		else:
			self.sbusChannels[17] = 0

		#Failsafe
		self.failSafeStatus = self.SBUS_SIGNAL_OK
		if (self.sbusFrame[self.SBUS_FRAME_LEN - 3]) & (1 << 2):
			self.failSafeStatus = self.SBUS_SIGNAL_LOST
		if (self.sbusFrame[self.SBUS_FRAME_LEN - 3]) & (1 << 3):
			self.failSafeStatus = self.SBUS_SIGNAL_FAILSAFE

		for i in range(18):
			self.sbusChannelsNorm[i] = round(self.scal(self.sbusChannels[i],172.0,1811.0,-1.0,1.0),4)

	def update(self):
		"""
		we need a least 2 frame size to be sure to find one full frame
		so we take all the fuffer (and empty it) and read it by the end to
		catch the last news
		First find ENDBYTE and looking FRAMELEN backward to see if it's STARTBYTE
		"""

		#does we have enougth data in the buffer and no thread is currently trying in background?
		if self.ser.inWaiting() >= self.SBUS_FRAME_LEN:
			C_start = self.ser.read()
			if C_start == self.START_BYTE:

				tempFrame = self.ser.read(self.SBUS_FRAME_LEN-2)
				#print(tempFrame,len(tempFrame))
				C_end = self.ser.read()
				#print(C_start,C_end)
				if C_end == self.END_BYTE:
					self.sbusFrame = tempFrame
					self.decode_frame()

					self.lastFrameTime = time.time() # keep trace of the last update
					return True
				else:
					return False
			else:
				return False
		else:
			return False



# excuted if this doc is not imported
# for testing purpose only
if __name__ == '__main__':

	sbus = SBUSReceiver('COM7')

	while True:
		if(sbus.update()):
			print (sbus.get_failsafe_status(), sbus.sbusChannelsNorm, str(sbus.ser.inWaiting()).zfill(4) , (time.time()-sbus.lastFrameTime))

