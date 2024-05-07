from pathlib import Path
import json
import shortuuid

NAME_MAPPING = {'S': 'squat', 'B': 'bench', 'D': 'deadlift'}

with open(Path(__file__).parent / "prog_force_lolo.csv") as prog_fin:
    programs = []
    trainings = []
    training_position = 0
    exercises = []
    program_id = None
    for line in prog_fin.readlines():
        line = line.strip('\n')
        while line.startswith(','):
            line = line[1:]
        if line.startswith("Programme"):
            program_id = int(line.rsplit(',')[0].split(' ')[-1])
        if line.startswith("Entrainement"):
            if exercises:
                trainings.append({"training_position":training_position , "exercises": exercises, "id": shortuuid.uuid()})
                exercises = []
            
            training_position += 1
        if line.startswith(('S', 'B', 'D')):
            try:
                type, set, reps, rpe = line.split(',')
                if type in NAME_MAPPING:
                    sets = []
                    for i in range(int(set)):
                        sets.append({"id": shortuuid.uuid(), "reps": int(reps), "rpe":float(rpe)})
                    exercises.append({"name": NAME_MAPPING[type], "sets": sets})
            except ValueError:
                pass
with open(Path(__file__).parent /"program_lolo.json", "w") as prog_fout:
    json.dump(trainings, prog_fout)