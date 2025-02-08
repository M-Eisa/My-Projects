import time
import psutil
import csv
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')
def log_performance(duration=60, interval=1, log_file="cpu_memory_log.csv"):
    """Logs CPU and memory usage over a set duration."""
    with open(log_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Time", "CPU Usage (%)", "Memory Usage (MB)"])
        start_time = time.time()

        try:
            print("Logging performance data... Press Ctrl+C to stop.")
            while time.time() - start_time < duration:
                cpu_usage = psutil.cpu_percent(interval=0.5)
                mem_usage = psutil.virtual_memory().used / 1e6  # Convert to MB
                elapsed_time = time.time() - start_time

                writer.writerow([elapsed_time, cpu_usage, mem_usage])
                print(f"Time: {elapsed_time:.2f}s | CPU: {cpu_usage}% | Memory: {mem_usage:.2f} MB", end="\r")
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\nLogging stopped.")

def plot_performance(log_file="cpu_memory_log.csv"):
    """Plots CPU and memory usage over time from log file."""
    times, cpu_usages, mem_usages = [], [], []

    with open(log_file, "r") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip headers
        for row in reader:
            times.append(float(row[0]))
            cpu_usages.append(float(row[1]))
            mem_usages.append(float(row[2]))

    plt.figure(figsize=(10, 5))
    plt.subplot(2, 1, 1)
    plt.plot(times, cpu_usages, label='CPU Usage (%)', color='red')
    plt.ylabel('CPU Usage (%)')
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(times, mem_usages, label='Memory Usage (MB)', color='blue')
    plt.xlabel('Time (s)')
    plt.ylabel('Memory Usage (MB)')
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    log_performance(duration=30)  # Run for 30 seconds
    plot_performance()