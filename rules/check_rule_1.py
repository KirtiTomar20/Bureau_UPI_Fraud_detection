import json
from datetime import datetime, timedelta

# Example transaction log for a card (In a real application, this would be fetched from a database)
transaction_log = [
    # Example transactions within the last 12 hours
    {"transactionAmount": 50000, "dateTimeTransaction": "070420240900"},  # Rs 50,000 transaction
    {"transactionAmount": 100000, "dateTimeTransaction": "070420241100"},  # Rs 1,00,000 transaction
    # Add more transactions as needed
]


# Function to check Rule 1
def verify(transaction, transaction_log):
    # Parse the transaction_data JSON
    # transaction = json.loads(transactiontion_data)

    # Extract relevant fields
    transaction_amount = int(transaction["transactionAmount"])
    card_balance = int(transaction["cardBalance"])
    current_time = datetime.utcfromtimestamp(transaction["dateTimeTransaction"])
    # start_window = current_time - timedelta(hours=12)
    # Check if balance >= Rs 3,00,000
    # if card_balance < 300000:
    #     return 0

    # transaction_log = get_past_transactions(start_window,current_time)
    # Calculate the total amount in the last 12 hours including the current transaction
    total_amount = transaction_amount
    for past_transaction in transaction_log:
        past_transaction_time = datetime.strptime(past_transaction["dateTimeTransaction"], "%d%m%y%H%M")
        if current_time - timedelta(hours=12) <= past_transaction_time <= current_time:
            total_amount += past_transaction["transactionAmount"]

    # Check if the total amount >= 70% of the card balance
    if total_amount >= 0.7 * card_balance:
        return 1
    else:
        return 0

