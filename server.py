import socket
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

CASH_ADDRESS = {}

def delete_inactive_users(sock):
    while True:  
        time.sleep(3)
        current_time = datetime.now()
        
        if len(CASH_ADDRESS) > 0:
            for user in CASH_ADDRESS:
                past_time = CASH_ADDRESS[user]['last_access_time']
                time_difference = current_time - past_time
                seconds_difference = time_difference.total_seconds()
                if seconds_difference > 60:
                    print(f'delete inactive user: {user}')
                    sock.sendto(f'Connected lost. {user}'.encode(), CASH_ADDRESS[user]['address'])
                    del CASH_ADDRESS[user]
                       
def received_function(sock):
    while True:
        print('wating to receive messege')
        data, address = sock.recvfrom(4096)
   
        print(f'receive {len(data)} bytes from {address} ')
    
        if data:
            # 1バイト目はusernameの長さ
            username_length = int.from_bytes(data[:1], byteorder='big')
            # 2バイト目以降: usernameを取得
            username = data[1: 1+username_length].decode('utf-8')
        
            # username以降はmessage:
            message = data[1+username_length:].decode('utf-8')
        
            #user 登録
            if not(username in CASH_ADDRESS):
                CASH_ADDRESS[username] = {'address': address, 'last_access_time': datetime.now()}
                sock.sendto(f'Registered. {username}'.encode(), CASH_ADDRESS[username]['address'])
                continue
            
            # 全クライアントに送信
            for cash_user in CASH_ADDRESS:
                if not(cash_user == username):
                    sock.sendto(f'{cash_user}: {message}'.encode(), CASH_ADDRESS[cash_user]['address'])
                    print(f'sent ??? bytes back to {cash_user}')
            
            # 送信時間の更新
            CASH_ADDRESS[username]['last_access_time'] = datetime.now()
            

def main():
    # AF_INETでUDPソケットを作成する
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_port = 9001
    server_address = '0.0.0.0'
    print(f'starting up on port {server_port}')

    # 0.0.0.0 9001 紐付け
    sock.bind((server_address, server_port))

    # 通信
    print('== START CHAT ==')
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(received_function, sock)
        executor.submit(delete_inactive_users, sock)
        
    print('== END CAHT ==')
    sock.close()

if __name__ == "__main__":
    main()