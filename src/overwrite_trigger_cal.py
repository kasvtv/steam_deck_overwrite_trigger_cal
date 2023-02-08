# uncompyle6 version 3.9.0
# Python bytecode version base 3.8.0 (3413)
# Decompiled from: Python 3.8.10 (default, Nov 14 2022, 12:59:47) 
# [GCC 9.4.0]
# Embedded file name: trigger_cal.py
import sys, os, platform
from time import sleep
from controller_if import ControllerInterface

def kill_steam():
	if platform.system() == 'Linux':
		print('Stopping Steam if running...')
		os.system('killall steam > /dev/null')
		sleep(1.0)
def connect_cb(hid_dev_mgr):
	global connected
	connected = True

eps = ((10462, 4613), )
print('Steam Deck Trigger Calibration Overwrite Tool\n')
print('Connecting to controller system... ', end='')
sleep(0.2)
cntrlr_mgr = ControllerInterface(eps, connect_cb)

connection_tries = 10
connected = False

while connected == False:
	if connection_tries > 0:
		connection_tries -= 1
		sleep(0.1)

if connection_tries <= 0:
	print('Could not connect\n')
	cntrlr_mgr.shutdown()
	sys.exit(0)
else:
	print('Connected.' + os.linesep)
	sleep(0.1)
	cntrlr_mgr.load_default_mappings()
	cntrlr_mgr.load_default_settings()
	cntrlr_mgr.trigger_cancel_cal()
	
def main():
	try:
		print('Reading current calibration...\n')
		left_trigger_cal = cntrlr_mgr.trigger_get_cal(0)
		right_trigger_cal = cntrlr_mgr.trigger_get_cal(1)
		print('Current Left Trigger Cal:  ' + str(left_trigger_cal[1:-1]))
		print('Current Right Trigger Cal: ' + str(right_trigger_cal[1:-1]))
		#print('Current Left STICK Cal:  ' + str(cntrlr_mgr.thumbstick_get_cal(0)))
		#print('Current Right STICK Cal: ' + str(cntrlr_mgr.thumbstick_get_cal(1)))
		
		lmax = input("Enter LEFT  trigger MAX value (increase value to decrease start deadzone, current = " + str( left_trigger_cal[1]).rjust(5," ") +"): ")
		lmax = int(lmax) if lmax else left_trigger_cal[1]
		lmin = input("Enter LEFT  trigger MIN value (decrease value to decrease end deadzone,   current = " + str( left_trigger_cal[2]).rjust(5," ") +"): ")
		lmin = int(lmin) if lmin else left_trigger_cal[2]
		rmax = input("Enter RIGHT trigger MAX value (increase value to decrease start deadzone, current = " + str(right_trigger_cal[1]).rjust(5," ") +"): ")
		rmax = int(rmax) if rmax else right_trigger_cal[1]
		rmin = input("Enter RIGHT trigger MIN value (decrease value to decrease end deadzone,   current = " + str(right_trigger_cal[2]).rjust(5," ") +"): ")
		rmin = int(rmin) if rmin else right_trigger_cal[2]
		
		print("\nPlease review changes:\n    Left Trigger Cal:  " + str(left_trigger_cal[1:-1]) + " -> " + str((lmax,lmin)) + "\n    Right Trigger Cal: " + str(right_trigger_cal[1:-1]) + " -> " + str((rmax,rmin)))
		answer = input("\nThis may make your controls inoperable! Please double check your values! Type \"PROCEED\" to confirm: ")
		if answer != "PROCEED":
			return
		
		kill_steam()
		
		input("\nFinal warning! Press A button to apply.")
		
		cntrlr_mgr.trigger_set_cal(0, lmax, lmin, left_trigger_cal[3])
		cntrlr_mgr.trigger_set_cal(1, rmax, rmin, right_trigger_cal[3])
		
		print("Done! Please go back into Gaming Mode, go to Settings -> Controller -> Test Device Inputs, and verify")
		
	except KeyboardInterrupt:
		print('\nKeyboard Interrupt!')
		pass
	finally:
		print('\nExiting...')
		cntrlr_mgr.shutdown()
		os._exit(0)

main()