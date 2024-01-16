import socket

# AF_INETでUDPソケットを作成する
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = '0.0.0.0'
server_port = 9001
print(f'starting up on port {server_port}')

# 0.0.0.0 9001 紐付け
sock.bind((server_address, server_port))

cash_address = {}

while True:
    print('wating to receive messege')
    data, address = sock.recvfrom(4096)
   
    print(f'receive {len(data)} bytes from {address} ')
    
    if data:
        # 1バイト目はusernameの長さj
        username_length = int.from_bytes(data[:1], byteorder='big')
        
        # 2バイト目以降: usernameを取得
        username = data[1: 1+username_length].decode('utf-8')
        
        # username以降はmessage:
        message = data[1+username_length:].decode('utf-8')
        
        if not(username in cash_address):
            #user 登録
            cash_address[username] = address
            sock.sendto(f'Registered. {username}'.encode(), address)
            continue
        
        for user, address in cash_address.items():
            print(cash_address)
            if not(user == username):
                sent = sock.sendto(f'{user}: {message}'.encode(), address)
                print(f'sent {sent} bytes back to {user}')