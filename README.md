Do not copy and use code

# probotron_pi
Probotron Reborn on the RasPi


### Installing on your Pi

First clone the repo

````
	sudo apt-get update
	sudo apt-get install -y git
	git clone https://github.com/nsfsmartmakerspaces/probotron_pi.git
````

Once the source code is downloaded to the Pi:

````
cd probotron_pi
sudo ./install.sh
````

Once the source code is downloaded to the Pi:

## Setting up the Screen:

Add following text at the end of the file:
max_usb_current=1
hdmi_group=2
hdmi_mode=1
hdmi_mode=87
hdmi_cvt 1024 600 60 6 0 0 0

## Important Files:
codes.csv : 
- This file holds all the codes that the program will accept, as well as the encounter numbers
- The encounter number next to the code in the file represents the encounter implementation depending on the code entered
- The file is in the fomrat column 1: code, column 2: encounter number

probes.csv :
- This file holdes all the probes/questions that are asked in the program

probotron_pi.ini :
- This file holds constant variables and the file paths that are used throughout the program

codes_reader.py :
- Holds all the code that is responsible for reading in the approved codes and encounters from codes.csv
- This file also holds important functions that return the list of approved codes and the list of encounters for the codes

probes_reader.py :
- Similarily, this file is responsible for reading in the probes.csv file

video_recorder.py :
- This file is repsonsible for creating a video recorder
- Also holds the functions for starting and stopping recordings for the program

## Screens:
confirmation_screen.py :
- This is the screen that gives the user the option to save or re-record after recording a video

evidence_screen.py :
- This is the screen that gives the user the option to select what type of evidence that they are submitting

idle_screen.py :
- Idle screen that program iterates to after timeout

instructions_screen.py :
- Screen that provides the user with instructions on how to use the program

micro_screen.py :
- Screen that displays 14 micro-credentials and gives the user the option to select up to 3

out_of_attempts_screen.py :
- Screen after 3 failed attempts to sign in with a code

prepare_for_recroding_screen.py :
- Countdown from 3 before going to the recording screen

recording_screen.py :
- Screen where the program records the user

probes2_screen.py and probes_screen.py :
- Screen that asks the user the prompt based on encounter 1 or encounter 2

screens_controller.py :
- File that sets the screenflow (sets the ordering of the screens)
- Details how the program reacts as the user moves from screen to screen
- Depending on what screen the user is on, will detail how the program reacts after pressing enter on that screen

sign_in_with_code_screen.py :
- Sign in screen with 3 attempts before redirect

start_screen.py :
- First screen that shows up, welcoming the user to the program

### Currently Done:
- The first screen that the user sees is a welcome screen that gives some sort of basic info regarding the program.
- The user is then prompted for a 3-digit code in order to access the program
- They are allowed up to two failed attempts before the program locks itself for 2 minutes, after which the user can attempt again
- After entering the code, the program will check if there is already an existing personalized folder for that person. If not, the program will create one
- Then a set of instructions are shown and then the user is given the prompt, which depends on the encounter
- The user is then recorded and they have a little progress bar at the bottom so that they know how much time they have left
- If they finish early, they can end the recording early
- At this point, if the program is in the first encounter or final encounter, the option to save or record again will be given
- Saving will save to the personalized folder that was set when the user first entered their code
- If the program is on the second encounter, the user will be prompted to select 1 out of 4 evidence options and up to 3 micro-credential options, which the program will tag at the end of the saved file name
- In the second encounter, the option to save or record again will be after these selections
- Note: If the user is on the first encounter and finishes by saving their video, then the very next time that same user accesses the program, their enconter will be switched to the second encounter because the first encounter only happens once

### TODO:
- Save the videos to an online server
- Create a website that accesses the videos from the server
- Refine the interface of the video-accessing website
- Code the automatic implementation switch from second encounter to final encounter
- Code the USB reader
- Even more stress testing and bug checking
- Animated gif for the recording screen
- Centering and refining of text boxes in the Micro-credential screen
- Refinement of the interface (Make more pleasing to the uesr)
- Add element on the code screen that tells user how many attempts they have left
- Upload to Vimeo
- Dispaly errors generally
- Display upload errors
- Check for network connections / monitor internet conenction 
- Check for file system fullness
- Add animated icons for filesystem
- Add animated icons for powermate
