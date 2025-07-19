# plot.py
import matplotlib.pyplot as plt
from IPython import display

plt.ion()  # interactive mode ON

def plot(scores, mean_scores):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()  # Clear figure

    plt.title('Training Progress')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    plt.plot(scores, label='Score')
    plt.plot(mean_scores, label='Mean Score')
    plt.legend()
    
    plt.ylim(ymin=0)
    plt.text(len(scores) - 1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores) - 1, mean_scores[-1], str(round(mean_scores[-1], 2)))
    plt.pause(0.1)
