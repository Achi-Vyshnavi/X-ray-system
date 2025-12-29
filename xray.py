import json
from datetime import datetime

class XRay:
    def __init__(self, log_file="xray_log.json"):
        self.steps = []
        self.log_file = log_file

    def record_step(self, step_name, input_data, output_data, reasoning="", evaluations=None):
        step = {
            "step": step_name,
            "timestamp": str(datetime.now()),
            "input": input_data,
            "output": output_data,
            "reasoning": reasoning
        }
        if evaluations:
            step["evaluations"] = evaluations
        self.steps.append(step)
        self._save_log()

    def _save_log(self):
        with open(self.log_file, "w") as f:
            json.dump(self.steps, f, indent=4)
