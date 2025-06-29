import matplotlib.pyplot as plt
import seaborn as sns

def show_pie_chart(root, portfolio, stock_prices, group_by_sector=False):
    """
    Create a pie chart based on the total valuation of stocks.
    :param root: The Tkinter root window.
    :param portfolio: Dictionary of stock symbols and their shares.
    :param stock_prices: Dictionary of stock symbols and their current prices.
    :param group_by_sector: Boolean to determine if the chart should group by sector.
    :return: Matplotlib figure object.
    """
    if group_by_sector:
        # Group stocks by sector
        sectors = {}
        for symbol, shares in portfolio.items():
            sector = stock_prices[symbol].get('sector', 'Unknown')
            value = shares * stock_prices[symbol]['price']
            if sector in sectors:
                sectors[sector] += value
            else:
                sectors[sector] = value

        labels = list(sectors.keys())
        sizes = list(sectors.values())
    else:
        # Group stocks by symbol
        valuations = {symbol: shares * stock_prices[symbol]['price'] for symbol, shares in portfolio.items()}
        labels = list(valuations.keys())
        sizes = list(valuations.values())

    # Set up Seaborn theme
    sns.set_theme(style="whitegrid")

    # Create pie chart
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(
        sizes,
        labels=labels,
        autopct='%1.1f%%',
        startangle=90,
        colors=sns.color_palette("pastel"),
    )
    title = "Portfolio Valuation by Sector" if group_by_sector else "Portfolio Valuation by Symbol"
    ax.set_title(title)

    return fig