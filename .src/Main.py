from Simulation import Simulation
from Event import *
from Resource import *
from Patient import *

sims = []
def val_input(prompt):
    while True:
        try:
            val = int(input(prompt))
            if val < 1:
                print('Please enter a value >= 1.')
            else:
                return val
        except ValueError:
            print('Invalid input.')    


while True:
    print("==========ER Simulation==========")
    print("1. Create a new simulation")
    print("2. Run a simulation")
    print('3. Delete a simulation')
    print("4. Exit")
    choice = input("Please make a selection: ")
    print()

    match choice:
        case "1":
            sim_name = input('Please enter a name for the simulation: ')
            print()

            num_triage_nurse = val_input("Number of triage nurses: ")
            num_providers = val_input("Number of providers: ")
            num_nurses = val_input("Number of nurses: ")
            num_techs = val_input("Number of lab techs: ")
            num_beds = val_input("Number of beds: ")
            print()

            max_time = val_input("Simulation time: ")
            mean_num_patients = float(val_input("Average # of patients: "))
            rand_seed = int(input('Please enter a random seed (-1 for random selection): '))
            sim_state_interv = int(input('Please enter an interval to record simulation state statistics: '))

            Patient.id_count = 0
            Resource.staff_id_count = 0
            Resource.bed_id_count = 0
            sim = Simulation(sim_name,num_triage_nurse,num_nurses,num_providers,num_techs,num_beds,
                             max_time,mean_num_patients,rand_seed,sim_state_interv)
            sims.append(sim)
            
            
            sim.resources.triage_nurses_available = num_triage_nurse
            sim.resources.providers_available = num_providers
            sim.resources.nurses_available = num_nurses
            sim.resources.lab_techs_available = num_techs
            sim.resources.beds_available = num_beds

            

            for i in range(num_triage_nurse):
                triage_nurse = TriageNurse()
                sim.resources.triage_nurse_stack.push(triage_nurse)
            for i in range(num_providers):
                provider = Provider()
                sim.resources.provider_stack.push(provider)
            for i in range(num_nurses):
                nurse = Nurse()
                sim.resources.nurse_stack.push(nurse)
            for i in range(num_techs):
                tech = LabTech()
                sim.resources.tech_stack.push(tech)
            for i in range(num_beds):
                bed = Bed()
                sim.resources.bed_stack.push(bed)
            print()

            
        case "2":
            while True:
                print('==========Simulations==========')
                for i, sim in enumerate(sims):
                    print(str(i)+') '+sim.sim_id)

                print(str(len(sims))+') Go back')

                selec = int(input('Enter the menu number for the simulation you would like to run: '))

                if(selec == len(sims)):
                    print()
                    break

                run_sim = sims[selec]
                print()
                
                Patient.id_count = 0
                Resource.staff_id_count = 0
                Resource.bed_id_count = 0

                run_sim.run()
                break
        case '3':
            while True:
                print('==========Simulations==========')
                for i, sim in enumerate(sims):
                    print(str(i)+') '+sim.sim_id)

                print(str(len(sims))+') Go back')

                selec = int(input('Enter the menu number for the simulation you would like to delete: '))

                if(selec == len(sims)):
                    print()
                    break
                
                del_sim_name = sims[selec].sim_id
                sims.remove(sims[selec])
                print('\n'+del_sim_name+' has been deleted.')
                print()
                break
        case "4":
            break
        case _:
            print("Invalid input, try again.")





