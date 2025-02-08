import time
import psutil
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

matplotlib.use('TkAgg')

# Global variables to store the data
times = []
cpu_usages = []
mem_usages = []

def log_performance(duration=60, interval=1):
    """Logs CPU and memory usage over a set duration and updates the plot in real-time."""
    start_time = time.time()

    def update_plot(frame):
        # Collect data every interval
        cpu_usage = psutil.cpu_percent(interval=0.5)
        mem_usage = psutil.virtual_memory().used / 1e6  # Convert to MB
        elapsed_time = time.time() - start_time

        # Store data in the global lists
        times.append(elapsed_time)
        cpu_usages.append(cpu_usage)
        mem_usages.append(mem_usage)

        # Limit the data to the duration
        if len(times) > duration:
            times.pop(0)
            cpu_usages.pop(0)
            mem_usages.pop(0)

        # Update the plot
        line_cpu.set_data(times, cpu_usages)
        line_mem.set_data(times, mem_usages)

        # Update the axes limits
        ax_cpu.relim()
        ax_cpu.autoscale_view()
        ax_mem.relim()
        ax_mem.autoscale_view()

        # Dynamically adjust y-limits of memory plot if necessary
        ax_mem.set_ylim(0, max(mem_usages) * 1.2)

        return line_cpu, line_mem

    # Set up the plot
    fig, (ax_cpu, ax_mem) = plt.subplots(2, 1, figsize=(10, 6))

    ax_cpu.set_title('CPU Usage (%)')
    ax_cpu.set_xlim(0, duration)  # Limit x-axis to the duration
    ax_cpu.set_ylim(0, 100)
    line_cpu, = ax_cpu.plot([], [], label='CPU Usage (%)', color='red')
    ax_cpu.set_ylabel('CPU Usage (%)')
    ax_cpu.legend()

    ax_mem.set_title('Memory Usage (MB)')
    ax_mem.set_xlim(0, duration)  # Limit x-axis to the duration
    ax_mem.set_ylim(0, 16)  # Set initial y-limits for memory
    line_mem, = ax_mem.plot([], [], label='Memory Usage (MB)', color='blue')
    ax_mem.set_xlabel('Time (s)')
    ax_mem.set_ylabel('Memory Usage (MB)')
    ax_mem.legend()

    # Create the animation
    ani = FuncAnimation(fig, update_plot, interval=1000, blit=True, cache_frame_data=False)

    # Display the plot
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    log_performance(duration=60, interval=1)  # Run for 60 seconds
