from fastapi import APIRouter

from services.history_service import (
    get_all_experiments,
    delete_experiment
)

router = APIRouter()


@router.get("/history")
def experiment_history():

    experiments = get_all_experiments()

    return {
        "total_experiments": len(experiments),
        "experiments": experiments
    }

@router.delete("/history/{experiment_id}")
def remove_experiment(experiment_id: int):

    delete_experiment(experiment_id)

    return {
        "message": "Experiment deleted"
    }