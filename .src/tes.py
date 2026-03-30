import json
from pathlib import Path

files = sorted(Path(".").glob("sim-test*_summ_stats.json"))

for file_path in files:
    with open(file_path, "r") as f:
        data = json.load(f)

    results = data.get("Results", {})
    treated = results.get("# of patients fully treated")
    final_time = results.get("Final simulation time")

    if treated is None or final_time in (None, 0):
        print(f"Skipped {file_path.name}: missing values")
        continue

    corrected_throughput = round((treated / final_time) * 60, 2)

    # remove old incorrect value if present
    if "Throughput" in results:
        del results["Throughput"]

    results["Throughput (patients/hour)"] = corrected_throughput

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Updated {file_path.name}: {corrected_throughput} patients/hour")