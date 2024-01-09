from paycomuz.methods_subscribe_api import Paycom
paycom = Paycom()
url = paycom.create_initialization(amount=5.00, order_id='197', return_url='https://8968-89-236-228-114.ngrok-free.app')
print(url)
