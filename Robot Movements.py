import random
import time
import pandas as pd
from datetime import datetime

robot_names = ["RobotA", "RobotB", "RobotC"]
moves = ["grab", "set", "implement"]

def generate_robot_data(robot_name):
    robot_moves = [random.choice(moves) for _ in range(3)]
    times = [random.uniform(0.1, 2.0) for _ in range(3)]
    total_time = sum(times)
    return {"Robot Name": robot_name, "Moves": robot_moves, "Times": times, "Total Time": total_time}

def main():
    data_list = []

    iteration_count = 0

    while True:
        for robot_name in robot_names:
            robot_data = generate_robot_data(robot_name)
            for move, time_taken in zip(robot_data["Moves"], robot_data["Times"]):
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                data_list.append([robot_name, move, timestamp, time_taken])

                # Display each line of output
                print(f"{timestamp} - {robot_name} - Move: {move}, Time: {time_taken:.2f} seconds")
                time.sleep(1)

                # Check with the user after every 10 lines
                if len(data_list) % 100 == 0:
                    stop = input("Do you want to stop? (yes/no): ")
                    if stop.lower() == "yes":
                        # Creating a DataFrame from the collected data
                        columns = ["Robot Name", "Move", "Timestamp", "Time"]
                        df = pd.DataFrame(data_list, columns=columns)

                        # Export DataFrame to JSON file
                        json_filename = f"robot_movement_data_{iteration_count}.json"
                        df.to_json(json_filename, orient="records", lines=True)
                        
                        # Displaying the DataFrame
                        print("\nGenerated Robot Movement Data:")
                        print(df)

                        return

    # If the loop completes without stopping, create a DataFrame at the end
    columns = ["Robot Name", "Move", "Timestamp", "Time"]
    df = pd.DataFrame(data_list, columns=columns)

    # Export DataFrame to JSON file
    json_filename = f"robot_movement_data_{iteration_count}.json"
    df.to_json(json_filename, orient="records", lines=True)

    # Displaying the DataFrame
    print("\nGenerated Robot Movement Data:")
    print(df)

if __name__ == "__main__":
    main()
