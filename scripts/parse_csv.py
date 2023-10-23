from pathlib import Path
import json
NAME_MAPPING = {'S': 'squat', 'B': 'bench', 'D': 'deadlift'}

with open(Path(__file__).parent / "prog1.csv") as prog_fin:
    program = []
    id = 0
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
                program.append({"id":id , "exercises": exercises, "programId": program_id})
                exercises = []
            
            id += 1
        if line.startswith(('S', 'B', 'D')):
            try:
                type, set, reps, rpe = line.split(',')
                if type in NAME_MAPPING:
                    exercises.append({"exerciseName": NAME_MAPPING[type], "set": int(set), "reps": int(reps), "rpe": float(rpe)})
            except ValueError:
                pass
with open(Path(__file__).parent /"program1.json", "w") as prog_fout:
    json.dump(program, prog_fout)