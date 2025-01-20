import api_sign

# normal balance
print(api_sign.get_response("/0/private/Balance").text)

# extended balance
print(api_sign.get_response("/0/private/BalanceEx").text)
