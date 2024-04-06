


def customer_spending(customer_transactions, window_days=[12, 24, 168]):
    # Sort transactions chronologically
    customer_transactions = customer_transactions.sort_values('dateTimeTransaction')

    # Set transaction date and time as the index
    customer_transactions.index = customer_transactions['dateTimeTransaction']

    # For each window size
    for window_size in window_days:
        # Compute the sum of transaction amounts and number of transactions for the given window size
        sum_amount_tx_window = customer_transactions['transactionAmount'].rolling(f'{window_size}h').sum()
        nb_tx_window = customer_transactions['transactionAmount'].rolling(f'{window_size}h').count()

        # Compute the average transaction amount for the given window size
        avg_amount_tx_window = sum_amount_tx_window / nb_tx_window

        # Save feature values
        if (window_size % 24 == 0):
            customer_transactions[f'Frequency_{window_size}HR_WINDOW'] = nb_tx_window
            customer_transactions[f'Monetary_{window_size}HR_WINDOW'] = avg_amount_tx_window

        else:
            customer_transactions[f'Frequency_{window_size // 24}DAY_WINDOW'] = nb_tx_window
            customer_transactions[f'Monetary_{window_size // 24}DAY_WINDOW'] = avg_amount_tx_window

    customer_transactions = customer_transactions.sort_values('mti').reset_index(drop=True)

    # Return the dataframe with the new features
    return customer_transactions
