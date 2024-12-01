# Transitive inference training
# Foraging

from pyControl.utility import *
import hardware_definition as hw

# States and events.

states = [
    "run_start",
    "run_end",
    "init_trial",
    "B_reward",
    "C_reward",
    "inter_trial_interval",
    "all_states"
]


events = [
    "A_poke",
    "B_poke",
    "C_poke",
    "D_poke",
    "B_reset",
    "C_reset"
]



# Parameters.

# v.session_duration = 1 * hour  # Session duration.
v.trial_num = 100  # Total trial number.
v.reward_durations = [25] # Reward delivery duration (ms).
v.ITI_duration = 1 * second  # Inter trial interval duration.



# Variables.

v.n_rewards = 0  # Number of rewards obtained.
v.n_trials = 0  # Number of trials received.
v.n_delivery = 0
v.choice = "Initiation"
v.A = 0
v.B = 0
v.C = 0
v.D = 0
v.reward_count = 0
v.temp = 0
v.curr = 0
v.trial_count = 1
v.reset = 0

# Print trial information

print_variables(["n_trials", "n_rewards", "choice"])

# Run start and stop behaviour.

def run_end():
    # Turn off all hardware outputs.
    hw.off()

# State behaviour functions.
initial_state = "init_trial"


def init_trial(event):
    if event == "entry":
        v.reset = 0
    
    if event == "B_poke":
         disarm_timer('B_reset')
         disarm_timer('C_reset')
         v.curr = 1
         if v.curr == v.temp:
            v.temp = v.curr

         elif v.curr != v.temp:
            print_trial_count()
            v.trial_count += 1
            v.temp = v.curr

         if v.B == 0:
            goto_state("B_reward")
            
    elif event == "C_poke":
         disarm_timer('B_reset')
         disarm_timer('C_reset')
         v.curr = 2
         if v.curr == v.temp:
            v.temp = v.curr

         elif v.curr != v.temp:
            print_trial_count()
            v.trial_count += 1
            v.temp = v.curr

         if v.C == 0:
            goto_state("C_reward")
            
    elif event == "A_poke":
         if v.reset == 0:
            set_timer('B_reset', 10*second)
            set_timer('C_reset', 10*second)
            v.reset = 1
         v.curr = 3
         if v.curr == v.temp:
            v.temp = v.curr

         else:
            print_trial_count()
            v.trial_count += 1
            v.temp = v.curr
            
    elif event == "D_poke":
         if v.reset == 0:
            set_timer('B_reset', 10*second)
            set_timer('C_reset', 10*second)
            v.reset = 1
            
         v.curr = 4
         if v.curr == v.temp:
            v.temp = v.curr

         else:
            print_trial_count()
            v.trial_count += 1
            v.temp = v.curr

    elif event == 'B_reset':
        v.B = 0

    elif event == 'C_reset':
        v.C = 0


def B_reward(event):
    # Deliver reward to Port B.
    
    if event == "entry":
        timed_goto_state("inter_trial_interval", v.reward_durations[0])
        hw.P_B.SOL.on()
        v.n_rewards += 1
        v.n_delivery += 1
        v.B = 1
        v.C = 0
        v.reward_count += 1  # Update reward count
        print_reward_count()

    elif event == "exit":
        hw.P_B.SOL.off()


def C_reward(event):
    # Deliver reward to Port B.
    if event == "entry":
        timed_goto_state("inter_trial_interval", v.reward_durations[0])
        hw.P_C.SOL.on()
        v.n_rewards += 1
        v.n_delivery += 1
        v.C = 1
        v.B = 0
        v.reward_count += 1  # Update reward count
        print_reward_count()

    elif event == "exit":
        hw.P_C.SOL.off()

def inter_trial_interval(event):
    # Go to init trial after specified delay.
    if event == "entry":
        timed_goto_state("init_trial", v.ITI_duration)

        

# State independent behaviour.

def all_states(event):
    if v.n_trials == v.trial_num:
        stop_framework()
    # When 'session_timer' event occurs stop framework to end session.
    #  elif event == "session_timer":
    #       stop_framework()

def print_reward_count():
    print(f"Rewards delivered: {v.reward_count}")

def print_trial_count():
    print(f"Trial count: {v.trial_count}")
