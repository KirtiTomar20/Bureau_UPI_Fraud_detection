

def count_merchant(customer_transactions, window_days=[3, 7, 30]):
    # Ensure dateTimeTransaction is in datetime format
    customer_transactions['dateTimeTransaction'] = pd.to_datetime(customer_transactions['dateTimeTransaction'])

    # Sort transactions chronologically
    customer_transactions.sort_values(by='dateTimeTransaction', inplace=True)

    # For each window size
    for window_size in window_days:
        window_str = f'{window_size}D'

        # For each merchant category code
        for mcc in customer_transactions['merchantCategoryCode'].unique():
            mcc_mask = customer_transactions['merchantCategoryCode'] == mcc

            # Calculate rolling sum and count for each merchant category code
            # Using temp series to avoid SettingWithCopyWarning
            temp_sum = customer_transactions.loc[mcc_mask].rolling(window=window_str, on='dateTimeTransaction')[
                'transactionAmount'].sum()
            temp_count = customer_transactions.loc[mcc_mask].rolling(window=window_str, on='dateTimeTransaction')[
                'transactionAmount'].count()

            customer_transactions.loc[mcc_mask, f'Sum_{window_size}d'] = temp_sum.values
            customer_transactions.loc[mcc_mask, f'Count_{window_size}d'] = temp_count.values

    return customer_transactions