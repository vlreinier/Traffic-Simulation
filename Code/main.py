from model import Road
from agents import Vehicle, Obstacle
from mesa.batchrunner import BatchRunner


def agent_portrayal(agent):
    portrayal = {}
    if isinstance(agent, Vehicle):
        portrayal["Color"] = "#e9ffe1"
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "false"
        portrayal["Layer"] = 0
        portrayal["w"] = 0.9
        portrayal["h"] = 0.9
        portrayal["text"] = str(agent.unique_id) + agent.type
        portrayal["text_color"] = "black"
    if isinstance(agent, Obstacle):
        portrayal["Color"] = "grey"
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "false"
        portrayal["Layer"] = 0
        portrayal["w"] = 0.9
        portrayal["h"] = 0.9
        portrayal["text"] = agent.type
    return portrayal

def get_avg_speed(model):
    total_speed = 0
    for agent in model.schedule.agents:
        total_speed += agent.speed
    if total_speed == 0:
        return 0
    return total_speed / len(model.schedule.agents)

def get_agent_counts(model):
    return model.schedule.get_agent_count()



fixed_params = {
    "road_length": 50,
    "space_between_vehicles": 3,
    "lanes": 3,
}

variable_params = {
    "obstacles": [False, 0, 1, 2],
    "vehicle_frequency": [0.05, 0.2, 0.5, 0.7]
    }

batch_run = BatchRunner(
    Road,
    variable_params,
    fixed_params,
    iterations=10,
    max_steps=1000,
    model_reporters={"agent_count": get_agent_counts,
                     "speed": get_avg_speed}
)

batch_run.run_all()
run_data = batch_run.get_model_vars_dataframe()
print(run_data)