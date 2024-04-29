import socket
from concurrent.futures import ThreadPoolExecutor


def received_function(sock, user_info):
    while True:
        try:
            data, server = sock.recvfrom(4096)
            print(f'\n{data.decode()}')
            if data.decode() == 'close':
                return
        except Exception as e:
            print('closing socket')
            print(f'ERROR :{e}')
            sock.close()
            break

def send_message_function(sock, server_address, server_port, user_info):
    while True:
        try:
            message = input('メッセージを入力してください:').encode()
            if len(message) >= 4096:
                print(f'送信サイズが4096byteを超えています | Invalid {message} byte.')
                continue
            sent = sock.sendto(user_info + message, (server_address, server_port))
            if message.decode() == 'close':
                    return
        except Exception as e:
            print('closing socket')
            print(f'ERROR :{e}')
            sock.close()
            break
            
        
def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    server_address = input('Type in the servers address to connect to:')
    server_port = 9001

    address = ''

    # 0.0.0.0 開いてるポートに紐付け
    sock.bind((address,0))
    
    # usernameを設定
    user_info = ''
    while True:
        username = input('please input username:').encode()
        length = len(username)
        
        # 1byte(usernameの長さ)
        byte1 = length.to_bytes(1, byteorder='big')
        if length > 255:
            print('please continue username. enter no more than 255 characters') 
            continue
        
        # 1byte目と2byte目を連結
        try:
            # ユーザー登録
            user_info = byte1 + username 
            sent = sock.sendto(user_info, (server_address, server_port))
            
            data, server = sock.recvfrom(4096)
            
            print(f' {data.decode()}')
            
            if data.decode() == 'close':
                return
        
        except Exception as e:
            print('closing socket')
            print(f'ERROR :{e}')
            sock.close()
            break 
        break
        
 
    # 通信
    print('== START CHAT ==')
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(received_function, sock, user_info)
        executor.submit(send_message_function, sock, server_address, server_port, user_info)
        
    print('== END CAHT ==')
    sock.close()

if __name__ == "__main__":
    main()
