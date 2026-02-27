from Simulation import Simulation
from Patient import Patient
from Event import *
import sys

sim = Simulation()

while True:
    print("==========ER Simulation==========")
    print("1. Enter simulation parameters")
    print("2. Run simulation")
    print("3. Exit")
    choice = input("Please make a selection: ")
    print()

    match choice:
        case "1":
            sim.resources.providers_available = input("Number of providers: ")
            sim.resources.nurses_available = input("Number of nurses: ")
            sim.resources.lab_techs_available = input("Number of lab techs: ")
            sim.resources.beds_available = input("Number of beds: ")

        case "2":
            sim.run()

        case "3":
            sys.exit()

        case _:
            print("Invalid input, try again.")




arrive_test = Arrive(sim)
arrive_test.execute()
arrive_test.execute()

triage_test = Start_Triage(sim)
triage_test.execute()

print(str(sim.queues.triage_queue))




