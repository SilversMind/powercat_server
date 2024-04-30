from src.profile.models import Profile
from src.trainings.models import Training
MINIMUM_WEIGHT_STEP = 2.5

def generate_weight(user: Profile, training: Training):
    for exercise in training.exercises:
        for set in exercise.sets:
            set.weight = compute_pr_by_repetition_number(
                user.PR[exercise.name], set.reps, set.rpe
            )
    return training

def compute_pr_by_repetition_number(PR: int, repetitions: int, rpe: int) -> int:
    raw_nbr = PR * pow(0.96, repetitions)*pow(0.96, 10-rpe)
    # Check to round to the lower or upper weight
    remainder = raw_nbr % MINIMUM_WEIGHT_STEP
    lower_weight = raw_nbr - remainder
    to_add = 0
    if MINIMUM_WEIGHT_STEP - remainder < remainder:
        to_add += MINIMUM_WEIGHT_STEP
    full_weigth = lower_weight + to_add
    return full_weigth