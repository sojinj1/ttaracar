# vcc : 5v, trig : 13, echo : 24, gnd : gnd
# trig = 13, echo = 24
# 카트 앞 초음파 센서로 사람에 대한 거리를 추적해서 모터를 조정
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO  # RPi.GPIO에 정의된 기능을 GPIO라는 명칭으로 사용
import time  # time 모듈

GPIO.setmode(GPIO.BCM)  # GPIO 이름은 BCM 명칭 사용
GPIO.setup(13, GPIO.OUT)  # Trig, 초음파 신호 전송핀 번호 지정 및 출력지정
GPIO.setup(24, GPIO.IN)  # Echo, 초음파 수신하는 수신 핀 번호 지정 및 입력지정

mqttc = mqtt.Client()      # MQTT Client 오브젝트 생성
mqttc.connect('localhost', 1883)    # MQTT 서버에 연결

print ('Press SW or input Ctrl+C to quit')   # 메세지 화면 출력

try:
    distance = 0
    while True:
        GPIO.output(13, False)        
        time.sleep(0.5)

        GPIO.output(13, True)  # 10us 펄스를 내보냄
        time.sleep(0.00001)  # Python에서 이 펄스는 실제 100us 근처
        GPIO.output(13, False)  # 하지만 HC-SR04 센서는 이 오차를 받아줌

        while GPIO.input(24) == 0: # echo 핀이 OFF 되는 시점을 시작 시간으로 잡음
             start = time.time()

        while GPIO.input(24) == 1: # echo 핀이 다시 ON 되는 시점을 반사파 수신시간으로 잡음
            stop = time.time()

        time_interval = stop - start  # 초음파가 수신되는 시간으로 거리를 계산
        
        if distance == 0:
            distance = time_interval * 17000
            distance = round(distance, 2)
        
        else:
            later_distance = time_interval * 17000
            later_distance = round(later_distance, 2)
            
            #print(later_distance)
            if abs(later_distance - distance) <= 3000:
                distance = later_distance
        
        
        
        if distance < 45:
            msg = "stop"
        else:
            msg = "ok"
        #print ('Object Distance => ', distance, 'cm', msg)  # 실제 거리 출력
        mqttc.publish("motor_object", msg)
        
except KeyboardInterrupt:  # Ctrl-C 입력 시
    GPIO.cleanup()  # GPIO 관련설정 Clear
    print('bye~')

