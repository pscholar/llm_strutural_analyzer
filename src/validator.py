## This file contains functions of the Validator
## It cross-checks results from running the script generated by the LLM 
## against the expected results

# TODO make the Validator more robust, add syntax and semantic checks
# to generated script, and communicate to the checks to the LLM
# This module has not been well tested for production.

import json
import subprocess as subp

expected_results = [
  [27.0,28.0,28.0,36.45],
  [52.5,52.5,52.5,137.5],
  [9.3,8.7,9.3,27.90],
  [29.375,29.625,29.585,57.539],
  [-28.0,-28.0,28.0,49.0],
  [29.625,29.375,29.625,57.53904]
]

cur_task = 0
max_error = 0.1
results_path = "results.json"

# TODO add appropriate error handling

def validate_llm(script):
  perfomance = 0
  script_path = save_script(script)
  success = run_script(script_path)
  if success:
    computed_results = get_computed_results(results_path)
    perfomance = check_results(computed_results) 
  cur_task += 1
  return perfomance

def save_script(script):
  script_path = "llm_generated.py"
  script_file = open(script_path,"w")
  script_file.write(script)
  script_file.close()
  return script_path

def run_script(script_path):
  try:
    result = subp.run(['python', script_path], 
                      capture_output=True, text=True, check=True)
    print(result.stdout)
    return True
  except subp.CalledProcessError as e:
    print(f"Error: The script {script_path} failed to run.")
    print(f"Error message: {e.stderr}")
    return False
  except FileNotFoundError:
    print(f"Error: The script file {script_path} was not found.")
    return False

def get_computed_results(results_path):
  results_file = open(results_path,"r")
  computed_results = json.load(results_file)
  results_file.close(results_file)
  return computed_results

def check_results(computed_results):
  performance = 100.0
  i = 0
  for value in computed_results.values():
    error = abs(value - expected_results[cur_task][i])
    if error > max_error:
      performance -= 25.0
    i += 1
  return performance
