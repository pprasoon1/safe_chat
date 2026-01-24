from inference import predict

while True:
    msg = input("Enter message: ")
    print(predict(msg))