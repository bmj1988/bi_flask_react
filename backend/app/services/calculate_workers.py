import multiprocessing
import psutil
import math

def calculate_optimal_workers() -> int:
    # Memory requirements per worker (in MB)
    memory_per_worker_mb = {
        'image_processing': 10,
        'base64_overhead': 5,
        'gpt4_buffer': 15,
        'fuzzy_matching': 20,
        'results_buffer': 10
    }

    # Calculate total memory needed per worker
    total_worker_mb = sum(memory_per_worker_mb.values()) * 1.2  # 20% safety margin
    memory_per_worker_gb = total_worker_mb / 1024

    # Get system resources
    memory = psutil.virtual_memory()
    total_memory_gb = memory.total / (1024 ** 3)
    available_memory_gb = memory.available / (1024 ** 3)
    cpu_count = multiprocessing.cpu_count()

    # Calculate workers based on memory
    memory_based_workers = math.floor(available_memory_gb / memory_per_worker_gb)

    # Calculate optimal workers
    optimal_workers = min(
        cpu_count,
        memory_based_workers,
        8  # Hard upper limit
    )

    # Print detailed system information
    print("\nSystem Resources:")
    print(f"CPU Cores: {cpu_count}")
    print(f"Total Memory: {total_memory_gb:.2f} GB")
    print(f"Available Memory: {available_memory_gb:.2f} GB")
    print(f"Memory Required per Worker: {memory_per_worker_gb:.3f} GB")
    print(f"\nWorker Calculations:")
    print(f"Maximum Workers (CPU-based): {cpu_count}")
    print(f"Maximum Workers (Memory-based): {memory_based_workers}")
    print(f"\nRecommended Workers: {optimal_workers}")

    return optimal_workers

if __name__ == "__main__":
    calculate_optimal_workers()
