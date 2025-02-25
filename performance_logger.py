import time
import psutil
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

matplotlib.use('QtAgg')

# Global variables to store the data
times = []
cpu_usages = []
mem_usages = []
cpu_core_usages = []
net_sent = []  # Network data sent (bytes)
net_recv = []  # Network data received (bytes)
disk_usage = []  # Disk usage percentage

def log_performance(duration=60, interval=1):
    """Logs CPU, memory, network, disk usage, and CPU core usage over a set duration and updates the plot in real-time."""
    start_time = time.time()

    def update_plot(frame):
        # Collect data every interval
        cpu_usage = psutil.cpu_percent(interval=0.5)
        mem_usage = psutil.virtual_memory().used / 1e6  # Convert to MB
        cpu_core_usage = psutil.cpu_percent(percpu=True)  # Get CPU usage per core
        elapsed_time = time.time() - start_time

        # Network usage (sent and received)
        net_io = psutil.net_io_counters()
        net_sent.append(net_io.bytes_sent / 1e6)  # Convert to MB
        net_recv.append(net_io.bytes_recv / 1e6)  # Convert to MB

        # Disk usage
        disk_usage_percent = psutil.disk_usage('/').percent
        disk_usage.append(disk_usage_percent)

        # Store data in the global lists
        times.append(elapsed_time)
        cpu_usages.append(cpu_usage)
        mem_usages.append(mem_usage)
        cpu_core_usages.append(cpu_core_usage)

        # Limit the data to the duration
        if len(times) > duration:
            times.pop(0)
            cpu_usages.pop(0)
            mem_usages.pop(0)
            cpu_core_usages.pop(0)
            net_sent.pop(0)
            net_recv.pop(0)
            disk_usage.pop(0)

        # Update the plot
        line_cpu.set_data(times, cpu_usages)
        line_mem.set_data(times, mem_usages)
        line_net_sent.set_data(times, net_sent)
        line_net_recv.set_data(times, net_recv)
        line_disk.set_data(times, disk_usage)

        # For CPU cores, plot each core's usage as separate lines
        for i, line in enumerate(line_cpu_cores):
            line.set_data(times, [core[i] for core in cpu_core_usages])

        # Update the axes limits
        ax_cpu.relim()
        ax_cpu.autoscale_view()
        ax_mem.relim()
        ax_mem.autoscale_view()
        ax_net_sent.relim()
        ax_net_sent.autoscale_view()
        ax_net_recv.relim()
        ax_net_recv.autoscale_view()
        ax_disk.relim()
        ax_disk.autoscale_view()

        # Dynamically adjust y-limits if necessary
        ax_mem.set_ylim(0, max(mem_usages) * 1.2)
        ax_net_sent.set_ylim(0, max(net_sent) * 1.2)
        ax_net_recv.set_ylim(0, max(net_recv) * 1.2)
        ax_disk.set_ylim(0, 100)

        # Dynamically adjust the CPU cores y-limits
        ax_cpu_cores.set_ylim(0, 100)

        return line_cpu, line_mem, line_net_sent, line_net_recv, line_disk, *line_cpu_cores

    # Set up the plot with additional subplots for network, disk usage, and CPU core usage
    fig, ((ax_cpu, ax_mem), (ax_net_sent, ax_net_recv), (ax_disk, ax_cpu_cores)) = plt.subplots(3, 2, figsize=(12, 9))

    # CPU Usage plot
    ax_cpu.set_title('CPU Usage (%)')
    ax_cpu.set_xlim(0, duration)
    ax_cpu.set_ylim(0, 100)
    line_cpu, = ax_cpu.plot([], [], label='CPU Usage (%)', color='red')
    ax_cpu.set_ylabel('CPU Usage (%)')
    ax_cpu.legend()

    # Memory Usage plot
    ax_mem.set_title('Memory Usage (MB)')
    ax_mem.set_xlim(0, duration)
    ax_mem.set_ylim(0, 16)
    line_mem, = ax_mem.plot([], [], label='Memory Usage (MB)', color='blue')
    ax_mem.set_ylabel('Memory Usage (MB)')
    ax_mem.legend()

    # Network Sent plot
    ax_net_sent.set_title('Network Sent (MB)')
    ax_net_sent.set_xlim(0, duration)
    line_net_sent, = ax_net_sent.plot([], [], label='Network Sent (MB)', color='green')
    ax_net_sent.set_ylabel('Network Sent (MB)')
    ax_net_sent.legend()

    # Network Received plot
    ax_net_recv.set_title('Network Received (MB)')
    ax_net_recv.set_xlim(0, duration)
    line_net_recv, = ax_net_recv.plot([], [], label='Network Received (MB)', color='purple')
    ax_net_recv.set_ylabel('Network Received (MB)')
    ax_net_recv.legend()

    # Disk Usage plot
    ax_disk.set_title('Disk Usage (%)')
    ax_disk.set_xlim(0, duration)
    ax_disk.set_ylim(0, 100)
    line_disk, = ax_disk.plot([], [], label='Disk Usage (%)', color='orange')
    ax_disk.set_xlabel('Time (s)')
    ax_disk.set_ylabel('Disk Usage (%)')
    ax_disk.legend()

    # CPU Core Usage plots (one for each core)
    ax_cpu_cores.set_title('CPU Core Usage (%)')
    ax_cpu_cores.set_xlim(0, duration)
    ax_cpu_cores.set_ylim(0, 100)
    line_cpu_cores = [ax_cpu_cores.plot([], [], label=f'Core {i + 1} Usage (%)')[0] for i in range(psutil.cpu_count())]
    ax_cpu_cores.set_ylabel('Core Usage (%)')
    ax_cpu_cores.legend()

    # Create the animation
    ani = FuncAnimation(fig, update_plot, interval=1000, blit=True, cache_frame_data=False)

    # Display the plot
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    log_performance(duration=60, interval=1)  # Run for 60 seconds
