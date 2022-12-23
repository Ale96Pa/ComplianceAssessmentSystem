"""
Inputs
"""
log = "inputs/IM-log.csv"
model = "inputs/IM-model.pnml"

separator = ";"
case_key = "incident_id"
activity_key = "event"
timestamp_key = "timestamp"

features = ['category','made_sla','knowledge','u_priority_confirmation','priority',
        'reassignment_count','reopen_count']
cost_key = "fitness_cost"
category_key= "category"

"""
Support dataset
"""
data_by_case = "src/dataset/utils_data/log_by_case.csv"
parameters_file = "src/dataset/results/models.csv"
report_file = "src/dataset/results/report.pdf"


"""
Configuration parameters
"""
first_run=False

"""
Benchmark parameters
"""
alpha = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
log_by_case_benchmark = "test/benchmark/log_by_case_bmk.csv"
ground_truth_file = "test/benchmark/gorund_truths.csv"
parameters_gts = "test/benchmark/parameters_gt.csv"
benchmark_file = "test/benchmark/benchmark_IM.csv"

run_GT = False
run_model = False