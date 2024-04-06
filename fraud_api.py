import json
from datetime import datetime, timedelta
from rules import check_rule_1, check_rule_2
from flask import Flask, request

from services.DbManager import MongoManager
from services.RedisManager import RedisCacheManager

db_client = MongoManager()
cache = RedisCacheManager()
app = Flask(__name__)


@app.route("/bureau/stream/verify_transaction", methods=['POST'])
def send_event():
    transaction_log = []
    try:
        event = request.get_json()
    except json.decoder.JSONDecodeError as err:
        print("Invalid json request", err)
        return json.dumps({"message": "Invalid json request, please send proper json data"}), 400

    current_time = datetime.utcfromtimestamp(event["dateTimeTransaction"])
    # current_time = datetime.strptime(event["dateTimeTransaction"], "%d%m%y%H%M")
    start_window = current_time - timedelta(hours=12)
    cache.set_value(event["encryptedHexCardNo"], event)
    transaction_log = db_client.get_past_transactions(str(start_window), current_time)
    if len(transaction_log) == 0:
        rule1 = check_rule_1.verify(event, transaction_log)
        rule2 = check_rule_2.verify([event])
    else:
        rule1 = check_rule_1.verify(event, transaction_log)
        rule2 = check_rule_2.verify(transaction_log.append(event))

    if rule1 == 1 and rule2 == 1:
        return json.dumps(
            {"status": "ALERT",
             "ruleViolated": ["RULE-001", "RULE-002"],
             "timestamp": str(int(datetime.now().timestamp()))}
        ), 200
    if rule1 == 1:
        return json.dumps(
            {"status": "ALERT",
             "ruleViolated": ["RULE-001"],
             "timestamp": str(int(datetime.now().timestamp()))}
        ), 200
    if rule2 == 1:
        return json.dumps(
            {"status": "ALERT",
             "ruleViolated": ["RULE-002"],
             "timestamp": str(int(datetime.now().timestamp()))}
        ), 200

    return json.dumps({"status": "OK", "ruleViolated": [], "timestamp": str(int(datetime.now().timestamp()))})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
