import redis
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

shared_dir = Path("data")

r = redis.Redis("localhost", port=6379, db=0)

def save_and_push_plot():
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    fig, ax = plt.subplots()
    ax.plot(x, y, label='Sine Wave')
    ax.set_title("Sample Plot")
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    ax.legend()
    ax.grid(True)

    # Save the figure
    file_name = f"plot_{str(np.random.randint(1000)).zfill(4)}.png"
    file_path = shared_dir / file_name
    fig.savefig(file_path)
    plt.close(fig)

    # Push the file path to Redis
    r.lpush('image_queue', str(file_path))

save_and_push_plot()
