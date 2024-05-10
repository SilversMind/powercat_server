from pathlib import Path
import json
import shortuuid
import re
NAME_MAPPING = {'S': 'squat', 'B': 'bench', 'D': 'deadlift'}

with open(Path(__file__).parent / "prog_force_lolo.csv") as prog_fin:
    programs = []
    trainings = []
    training_position = 0
    exercises = []
    blocks = None
    block_id = 1
    current_block = None
    current_subblock = None
    program_id = None
    for line in prog_fin.readlines():
        line = line.strip('\n')
        while line.startswith(','):
            line = line[1:]
        if line.startswith("Programme"):
            program_id = int(line.rsplit(',')[0].split(' ')[-1])
        if line.startswith("Semaine"):
            if current_subblock:
                training_list = blocks[current_block]["subblocks"][current_subblock]
                blocks[current_block]["subblocks"][current_subblock] = {"start":training_list[0], "end":training_list[-1]}
            current_subblock = re.match("(Semaine [0-9]),", line).group(1)
            blocks[current_block]["subblocks"][current_subblock] = []
        if line.startswith("Block"):
            if current_subblock:
                training_list = blocks[current_block]["subblocks"][current_subblock]
                blocks[current_block]["subblocks"][current_subblock] = {"start":training_list[0], "end":training_list[-1]}
            current_subblock = None
            current_block = re.match("Block ([a-zA-ZÀ-ÖØ-öø-Ÿÿ]+),", line).group(1)
            if not blocks:
                blocks = {current_block:{"id":block_id, "subblocks": {}}}
            else:
                blocks[current_block]= {"id":block_id, "subblocks": {}}
            block_id += 1
        if line.startswith("Entrainement"):
            if blocks:
                blocks[current_block]["subblocks"][current_subblock].append(training_position)
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

if current_subblock:
    training_list = blocks[current_block]["subblocks"][current_subblock]
    blocks[current_block]["subblocks"][current_subblock] = {"start":training_list[0], "end":training_list[-1]}
    
program = {"program_id": program_id, "blocks": blocks, "trainings":trainings}
with open(Path(__file__).parent /"program_lolo.json", "w") as prog_fout:
    json.dump(program, prog_fout, ensure_ascii=False)