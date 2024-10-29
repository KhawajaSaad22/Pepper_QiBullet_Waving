import pyttsx3
import time
import pyttsx3.voice
from qibullet import SimulationManager
from qibullet import PepperVirtual

#---------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------

# Function to simulate speech 
# (Reference: https://pyttsx3.readthedocs.io/en/latest/engine.html)
def pepper_speak(text):
    engine = pyttsx3.init()
    
    engine.setProperty('rate', 125)     # setting up new voice rate
    engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1
    engine.setProperty('voice', "English (America)")   # changing voice, uncomment three lines below to see other options
    # # unable to get female voice as in linux, all voices are male
    # voices = engine.getProperty('voices')       # getting details of all voices
    # for voice in voices:
    #     print(voice, voice.id)
    
    engine.say(text)
    engine.runAndWait() # if multiple texts, end each text with this command

    engine.stop()


#---------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------

# Function to simulate right hand waving and also speaking
# (Reference: https://github.com/softbankrobotics-research/qibullet/wiki/Tutorials:-Virtual-Robot#joint-control)
def waving_right_hand(robot):
    
    # Defined Values
    finger_val = 0.872
    speed = 0.25
    
    right_shoulder = {"RShoulderRoll": -1.5, "RShoulderPitch": 0.0} # Right shoulder joint position 
    right_elbow = {"RElbowRoll": [1.562, 1.0, 1.562]} # Right elbow roll in three different statest to make to look like wave
    right_fingers = {"RFinger11": finger_val, "RFinger12": finger_val, "RFinger13": finger_val,
                     "RFinger21": finger_val, "RFinger22": finger_val, "RFinger23": finger_val,
                     "RFinger31": finger_val, "RFinger32": finger_val, "RFinger33": finger_val,
                     "RFinger41": finger_val, "RFinger42": finger_val, "RFinger43": finger_val,
                     "RThumb1": finger_val, "RThumb2": finger_val} # Right fingers and thumb to make them straight 
    
    # for raising the right shoulder 
    for joint_name, angle in right_shoulder.items():
        print(f"joint_name = {joint_name}, angle = {angle}")
        robot.setAngles(joint_name, angle, speed)
    
    # for raising the right fingers
    for joint_name, angle in right_fingers.items():
        print(f"joint_name = {joint_name}, angle = {angle}")
        robot.setAngles(joint_name, angle, speed)

    time.sleep(1.0)
    print("Done with the movement, now speaking")
    # Simulate Pepper speaking
    pepper_speak("Hello")
    # time.sleep(1.0)

    for joint_name, angles in right_elbow.items():
        for angle in angles:
            print(f"joint_name = {joint_name}, angle = {angle}")
            robot.setAngles(joint_name, angle, speed)
            time.sleep(0.5)
    pepper_speak("How are you")
    time.sleep(1.0)
    robot.goToPosture("Stand", 0.2)
    pepper_speak("I am Pepper How can I assist you today")
    time.sleep(2.0)


#---------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------

# Function to adjust angles dynamically and verify positions without restarting the script again and again
def adjust_angle(robot, key_list):
    # Loop to allow multiple adjustments
    while True:
        key = input(f"Enter the name of the key (or type 'exit' to stop): ")
        if key.lower() == 'exit':
            break
        if key not in key_list:
            print(f"Invalid key name. Please select a valid key from: {key_list}")
            continue

        current_angle = robot.getAnglesPosition(key)
        print(f"Current angle of {key} is: {current_angle}")

        try:
            new_angle = float(input(f"Enter the new angle for {key} (between -3.14 to 3.14): "))
            if -3.14 <= new_angle <= 3.14:
                robot.setAngles(key, new_angle, 0.5)
                print(f"Set new angle {new_angle} for {key} with speed 0.5")
                time.sleep(2.0)
            else:
                print("Invalid angle value. Please enter a value between -3.14 and 3.14.")
        except ValueError:
            print("Please enter a valid numerical value.")
    

#---------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------

# Main simulation script
def main():
    # Set up the simulation environment
    simulation_manager = SimulationManager()
    client = simulation_manager.launchSimulation()

    # Spawn a virtual Pepper robot
    pepper = simulation_manager.spawnPepper(client, spawn_ground_plane=True)
    
    # Set Pepper to an initial position
    pepper.goToPosture("Stand", 1.0)
    time.sleep(1.0)

    waving_right_hand(pepper)

    # List of some of the valid keys for joints (used for testing pepper's movement on the runtime)
    # Got these values after printing "key" in line 112 from examples 
    # (https://github.com/softbankrobotics-research/qibullet/blob/master/examples/pepper_joints_error.py#L112C9-L112C12)
    key_list = ["HeadYaw", "HeadPitch", "LShoulderPitch", "LShoulderRoll", "LElbowYaw",
                "LElbowRoll", "LWristYaw", "LHand", "LFinger21", "LFinger22", "LFinger23",
                "LFinger11", "LFinger12", "LFinger13", "LFinger41", "LFinger42", "LFinger43",
                "LFinger31", "LFinger32", "LFinger33", "LThumb1", "LThumb2", "RShoulderPitch",
                "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand", "RFinger41",
                "RFinger42", "RFinger43", "RFinger31", "RFinger32", "RFinger33", "RFinger21",
                "RFinger22", "RFinger23", "RFinger11", "RFinger12", "RFinger13", "RThumb1",
                "RThumb2"]
    
    # # Allow dynamic angle adjustment (Uncomment below line to run manual value setting on runtime for joints)
    # adjust_angle(pepper, key_list)

    # Keep the simulation running
    input("Press Enter to end the simulation...")

    # Stop the simulation when done
    simulation_manager.stopSimulation(client)

if __name__ == "__main__":
    main()
