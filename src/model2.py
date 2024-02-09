# Load SyncroSim python package
import pysyncrosim as ps

# Load numpy and pandas
import numpy as np
import pandas as pd

# Get the SyncroSim Scenario that is currently running
myScenario = ps.Scenario()

# Load Run Control Datasheet to set timesteps
run_settings = myScenario.datasheets(name="RunControl")

# Set timesteps
timesteps = np.array(range(run_settings.MinimumTimestep.item(),
                           run_settings.MaximumTimestep.item() + 1))

# Load Scenario's input Datasheet from SyncroSim Library into DataFrame
my_input_dataframe = myScenario.datasheets(name="IntermediateDatasheet")

# Set up empty pandas DataFrame to accept output values
my_output_dataframe = myScenario.datasheets(name="OutputDatasheet")

# For loop through iterations
for i in range(1, run_settings.MaximumIteration.item() + 1):
    
    # Only load y for this iteration
    y = my_input_dataframe[my_input_dataframe["Iteration"] == i].y
    
    # Do calculations
    y_cum = np.cumsum(y)

    # Store relevant output in temporary data frame
    temp_data_frame = pd.DataFrame({"Timestep": timesteps,
                                    "Iteration": [i] * len(y),
                                    "yCum": y_cum})

    # Append temporary data frame to output data frame
    my_output_dataframe = my_output_dataframe.append(temp_data_frame)

# Save the output DataFrame to the Scenario output Datasheet
myScenario.save_datasheet(name="OutputDatasheet",
                          data=my_output_dataframe)
