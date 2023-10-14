from pathlib import Path
import json
NAME_MAPPING = {'S': 'squat', 'B': 'bench', 'D': 'deadlift'}

with open(Path(__file__).parent / "prog1.csv") as prog_fin:
    program = []
    id = 0
    exercises = []
    for line in prog_fin.readlines():
        line = line.strip('\n')
        while line.startswith(','):
            line = line[1:]
        if line.startswith("Entrainement"):
            if exercises:
                program.append({"id":id , "exercises": exercises})
                exercises = []
            
            id += 1
        if line.startswith(('S', 'B', 'D')):
            type, set, reps, rpe = line.split(',')
            if type in NAME_MAPPING:
                exercises.append({"type": NAME_MAPPING[type], "set": int(set), "reps": int(reps), "rpe": float(rpe)})

with open(Path(__file__).parent /"program1.json", "w") as prog_fout:
    json.dump(program, prog_fout)