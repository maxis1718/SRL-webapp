HOW TO USE THIS PROGRAM 
======================
A: Simple Mode
--------------
	1. Copy this folder to any location
	2. Make sure you have successfully installed Python 2.7.X
	3. Make sure you have successfully installed E-HowNet Python API
	4. Put the trees to be labeled in a file, and name it 'in.txt'
	5. Put the file 'in.txt' in the directory ./test/ (Make sure the file has the same format as produced by the Sinica Parser, a sample file is already in the './test' folder)
	5. Simply run the command 'python srl.py' from this directory (i.e. './SRL>python srl.py')
	6. The output will be stored in './test/out.txt'

B: CLIENT SERVER MODE
---------------------
	1. Run the SRLServer.py and leave it running
	2. Run the SRLClient.py in one of the following two modes:
		a: simple mode: Provide the input tree like:
			>python SRLClient.py "VP(Head:VC:找出|NP(VP‧的(head:VP(D:可能|Head:VJ:包含)|Head:DE:的)|Head:Na:詞))"
		b: batch mode: provide the input and output file paths like:
			>python ./test/in.txt ./test/out.txt
		
STEPS TO INSTALL E-HOWNET API
=============================
1. Make sure you have successfully installed Python 2.7.X
2. Get E-HowNet Python API unzip it. This will creat a directory 'libehownet'
3. From the command prompt go into 'libehownet' directory
4. run the command 'python setup.py'. This will install E-HOWNET Python API. 
   To check whether you have successfully installed it or not. Type the following commands from command prompt:
   >python
   >>> from ehownet import *
   >>>
   if you don't see any error message(s). This means you have successfully installed it.
   

	