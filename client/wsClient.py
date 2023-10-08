# -*- coding: utf-8 -*-

import socket
import sys
import time
import random

# 서버 정보 설정
server_host = "101.101.208.213"  # 서버의 IP 주소로 변경
server_port = 8080  # 서버에서 설정한 포트 번호로 변경
delay_time = random.randint(1, 5)


# 시간을 리얼타임으로 변환
def real_time(time): 
    minute = "{}".format(time // 60)
    second = "{}".format(time % 60)
    result = "{}:{}".format(minute.zfill(2), second.zfill(2))
    # 예) 3초 => 00:03 / 100초 => 01:40
    return result

# 서버 접속 시간 리얼타임으로 변환
system_clock = real_time(delay_time)

# 서버 접속 대기 시간 출력, 대기시간 만큼 지연시킨다.
print("서버 접속 대기 시간: {}".format(delay_time))
time.sleep(delay_time)

# 소켓 생성
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 서버에 연결
client_socket.connect((server_host, server_port))
thread_num = int(client_socket.recv(1024).decode("utf-8"))

# 로그 파일 생성
client_file = open("client{}_log.txt".format(thread_num), 'w')

# 딜레이가 지난 후에 클라이언트 파일에 로그 작성
client_file.write("{} > 서버에 접속하였습니다.".format(system_clock))

client_socket.send(str(delay_time).encode("utf-8"))
print("서버에게 대기시간을 보냈습니다.")

while True:
    # 서버로부터 문제 받기 (사칙연산 문제와 클라이언트 번호 포함)
    question = client_socket.recv(1024).decode("utf-8")

    # , 를 기준으로 분해한다.
    question_split = question.split(",")

    question_q = question_split[0]

    print("서버에게 받은 문제: {}".format(question_q))

    # 문제를 받았을 때, 클라이언트 로그에 문제를 받은 시간을 적는다.
    question_recv_time = int(question_split[1])
    # 문제를 받은 시간을 로그 입력 형식에 맞게 변환시킨다.
    system_clock = real_time(question_recv_time)
    client_file.write("{} > 서버로부터 문제를 받았습니다.".format(system_clock))

    # 문제를 해결한 임의의 시간을 구한다.
    question_resolve_time = random.randint(1, 5)
    
    # 문제를 푼 시간(로그에 입력할 용도)은 문제를 받은 시간에서 문제를 해결하는데 걸린 시간을 더해주면 된다.
    question_ans_time = question_recv_time + question_resolve_time

    # 로그에 입력하는 형식에 맞게 변환시킨다.
    system_clock = real_time(question_ans_time)

    # 문제에 대한 걸린 시간과 답 보내기
    answer = sys.stdin.readline()
    # 문제를 해결하는데 걸린 시간과 답(공백제거)
    answer = '{}'.format(question_resolve_time) + answer.strip() 
    client_socket.send(answer.encode('utf-8'))
    client_file.write("{} > 서버에게 임의의 정답을 보냈습니다.".format(system_clock))

# 연결 종료 (실제로는 이 부분이 실행되지 않을 것입니다)
client_socket.close()

