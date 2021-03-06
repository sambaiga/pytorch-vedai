from os import path

import matplotlib.pyplot as plt
import matplotlib.patches as patches

from .. import config


def _plot_bounding_boxes(locations, ax, is_ground_truth):
    color = 'c' if is_ground_truth else 'b'
    for _, label, score, box in locations:
        if score < config.PLOT_DETECTIONS_MIN_SCORE:
            continue

        x_min, y_min, x_max, y_max = box
        rect = patches.Rectangle((x_min, y_min), x_max-x_min, y_max-y_min,
                                linewidth=1, edgecolor=color, facecolor='none')
        ax.add_patch(rect)
        text = label if is_ground_truth else f"{label} ({int(score*100)}%)"
        ax.text(x_min, y_min, text, color=color)


def plot_detections(image, ground_truths, detections):
    fig, ax = plt.subplots(1, frameon=False)
    ax.set_axis_off()
    ax.set_position([0., 0., 1., 1.])

    image = image.permute(1, 2, 0).numpy()
    ax.imshow(image)

    _plot_bounding_boxes(ground_truths, ax, is_ground_truth=True)
    _plot_bounding_boxes(detections, ax, is_ground_truth=False)

    return fig


def plot_and_save(image, ground_truths, detections):
    fig = plot_detections(image, ground_truths, detections)

    fig_path = path.join(config.LOG_DIR, "detections.png")
    fig.savefig(fig_path)

    return fig
