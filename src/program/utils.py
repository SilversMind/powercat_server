from src.program.models import Block, Subblock


def generate_blocks(db_blocks) -> list[Block]:
    blocks = []
    for db_block_name, db_block_values in db_blocks.items():
        current_block = Block(name=db_block_name, id=str(db_block_values["id"]), subblocks=[])
        for db_subblock_name, trainings_slice in db_block_values["subblocks"].items():
            start_training = trainings_slice["start"]
            end_training = trainings_slice["end"]
            current_block.subblocks.append(
                Subblock(
                    name=db_subblock_name,
                    start_training_id=start_training,
                    end_training_id=end_training,
                )
            )
        blocks.append(current_block)
    return blocks