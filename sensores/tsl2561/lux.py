from tsl2561 import TSL2561 


if __name__ == "__main__": 
	tsl = TSL2561(debug=1) 
	print(tsl.lux()) 
