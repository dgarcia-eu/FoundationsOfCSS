import matplotlib.pyplot as plt
from scipy import stats

import config

# read config-----------------------------------------------------------------------------------------------------------


def diagrams(x, y, log_x, log_y):
    # draw 'True' diagrams from configuration in config.py
    if config.hist_followers:
        hist(x, 'Histogram of followers count', 'followers count')
    if config.hist_log_followers:
        hist(log_x, 'Histogram of log(followers count)', 'log(followers count)')

    if config.hist_mean_retweet:
        hist(y, 'Histogram of mean retweets', 'mean retweets')
    if config.hist_log_mean_retweet:
        hist(log_y, 'Histogram of log(mean retweets)', 'log(mean retweets)')

    if config.plot_social_impact:
        plot(log_x, log_y, 'log followers', 'log SI', 'Plot diagram social impact')

    plt.show()  # show all windows


# draw diagrams---------------------------------------------------------------------------------------------------------


def plot(x, y, x_label, y_label, title):
    # draw scatter plot
    plt.figure(num=title)
    slope, intercept, r, p, std_err = stats.linregress(x, y)  # measure linear regression of y on x lists
    res = stats.linregress(x, y)

    def get_line(x):
        return slope * x + intercept

    line = list(map(get_line, x))

    plt.scatter(x, y, color='black', s=7.5)  # scatter the dots
    plt.plot(x, line, color='orange', linewidth=1.1)  # plot line

    plt.title(f'R-squared: {res.rvalue ** 2:.6f}')  # Coefficient of determination
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    plt.draw()  # draw figure


def hist(data_list, title, x_label):
    # draw histograms
    plt.figure(num=title)

    plt.hist(data_list, ec='black', color='dimgrey')

    plt.xlabel(x_label)
    plt.ylabel('Frequency')

    plt.draw()  # draw figure

# eof-------------------------------------------------------------------------------------------------------------------
