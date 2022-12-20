import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import src.config as conf

if __name__ == "__main__":
    print(conf.run_trace_alignment)