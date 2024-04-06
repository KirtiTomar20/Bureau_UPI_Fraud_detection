import json

from faker import Faker
import random
from location_generator import generate_lat_long
from datetime import datetime, timedelta
import numpy as np

fake = Faker()
# Initialize Faker instance

hex_cards_list = ['3fadf92fe341fab73289bac0096af6ff7d3a4471d68291a3a153a8661a8c3b78', '5501f85b06357a0cf27a139f503debee3e8c58e2ee89e99462abe7696092084f', 'fd16539471e56db1ff1389fd63a0286146020c3ed3efaad8e1327fb521317d03', 'c0aeeccecd3f7c058fcde375de0f634592f1c293e25cded6fa65109c7eb54e72', 'd3caeb7bc69714c1d8a0376a5fe88ca21a36efeeb0c8c812ae61d14073f875a0', 'f8d5807785822a7d9c6f04bcbd3c7dbd8efaf35f2f17b952bc7286fcac75741b', '840ebf1bfe7923e2dc5f5c696ac23e5f39e57d4a564af7526725970eb751449b', '018419909276d201ce07cf40b993e2abe40077626dc03688b6e3e123babd2f83', 'da1e19eae5aac4a64cd3881e39c7966d3808096d0c284e205b7bbcbb7248d1ba', 'd10375c2fbbdcc151588830367af4ecdf3680998862492adfd9d3093200e240b']
merchant_code = ['1000', '1093', '1044', '1056', '1019', '1046', '1024', '1094', '1066', '1059', '1013', '1035', '1004', '1041', '1012', '1072', '1055', '1038', '1098', '1025', '1003', '1053', '1063', '1060', '1033', '1100', '1088', '1081', '1079', '1015', '1014', '1006', '1058', '1021', '1091', '1001', '1051', '1075', '1026', '1064', '1080', '1045', '1040', '1048', '1083', '1070', '1076', '1029', '1005', '1016', '1089', '1020', '1099', '1074', '1009', '1017', '1007', '1087', '1011', '1068', '1028', '1065', '1097', '1078', '1069', '1043', '1096', '1071', '1086', '1018', '1090', '1082', '1036', '1022', '1062', '1008', '1002', '1023', '1050', '1054', '1042', '1052', '1027', '1037', '1077', '1031', '1010', '1039', '1032', '1085', '1092', '1047', '1049', '1073', '1057', '1034', '1095', '1061', '1084', '1067', '1030']
def generate_random_transaction():

    transaction_time = datetime.now() - timedelta(hours=random.randint(1, 24))
    nyc_center_lat = np.radians(40.7128)
    nyc_center_long = np.radians(-74.0060)

    # Generate 10 random latitude and longitude points within about 10km of NYC center
    generated_points = generate_lat_long(nyc_center_lat, nyc_center_long, num_points=1, max_distance_km=10, min_distance=4)
    for point in generated_points:
        transaction = {
            "mti": "0100",
            "processingCode": "000000",
            "transactionAmount": f"{random.randint(100, 10000)}.00",
            "dateTimeTransaction": int(transaction_time.timestamp()),
            "cardholderBillingConversionRate": "61000000",
            "stan": str(random.randint(10000, 99999)),
            "timeLocalTransaction": fake.time(pattern='%H%M%S'),
            "dateLocalTransaction": fake.date(pattern='%d%m'),
            "expiryDate": fake.date(pattern='%m%y'),
            "conversionDate": fake.date(pattern='%m%d'),
            "merchantCategoryCode": str(random.choice(merchant_code)),
            "posEntryMode": "810",
            "acquiringInstitutionCode": str(random.randint(100000, 999999)),
            "forwardingInstitutionCode": str(random.randint(100000, 999999)),
            "rrn": str(random.randint(1000000000, 9999999999)),
            "cardAcceptorTerminalId": str(random.randint(1000000, 9999999)),
            "cardAcceptorId": str(random.randint(10000000, 99999999)),
            "cardAcceptorNameLocation": fake.company(),
            "cardBalance": f"{random.randint(100, 10000)}.00",
            "additionalData48": "T",
            "transactionCurrencyCode": "840",
            "cardholderBillingCurrencyCode": "840",
            "posDataCode": fake.random_int(min=100000000000000000, max=999999999999999999),
            "originalDataElement": str(random.randint(100000000000000000, 999999999999999999)),
            "channel": "ECOM",
            "encryptedPan": fake.sha256(),
            "network": fake.random_element(elements=('MASTER', 'VISA', 'AMEX')),
            "dcc": fake.boolean(),
            "kitNo": str(random.randint(1000000000, 9999999999)),
            "factorOfAuthorization": random.random(),
            "authenticationScore": random.randint(0, 100),
            "contactless": fake.boolean(),
            "international": fake.boolean(),
            "preValidated": fake.boolean(),
            "enhancedLimitWhiteListing": fake.boolean(),
            "transactionOrigin": "ECOM",
            "transactionType": "ECOM",
            "isExternalAuth": fake.boolean(),
            "encryptedHexCardNo": str(random.choice(hex_cards_list)),
            "isTokenized": fake.boolean(),
            "entityId": fake.uuid4(),
            "moneySendTxn": fake.boolean(),
            "mcRefundTxn": fake.boolean(),
            "mpqrtxn": fake.boolean(),
            "authorisationStatus": fake.boolean(),
            "latitude": str(point[0]),
            "longitude": str(point[1])
        }
        return transaction

# Generate random data
merchant_list = []
encryptedHexCardNo_list = []
for i in range(40000):
    random_data = generate_random_transaction()
    # print(random_data)
    merchant_list.append(random_data['merchantCategoryCode'])
    encryptedHexCardNo_list.append(random_data['encryptedHexCardNo'])

    with open("data.json", "a") as f:
        json_string = json.dumps(random_data)
        f.write(json_string + "\n")

final_merchant_list = set(merchant_list)
final_encryptedHexCardNo_list = set(encryptedHexCardNo_list)
print(final_merchant_list)
print(final_encryptedHexCardNo_list)
print(len(final_encryptedHexCardNo_list))