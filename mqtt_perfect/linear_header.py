# dir1 : 23, dir2 : 22, pwm1 : 18, pwm2 : 17, gnd : gnd
# 1 -> rightMotor, 2-> leftMotor
# 모터 핀 설정 및 모터 구동을 위한 함수들 정의
# 핀 번호 설정해야 함
import RPi.GPIO as io
io.setmode(io.BCM)

PWM_MAX = 100

io.setwarnings(False)
 
leftMotor_DIR_pin = 22
io.setup(leftMotor_DIR_pin, io.OUT)
rightMotor_DIR_pin = 23
io.setup(rightMotor_DIR_pin, io.OUT)  
io.output(leftMotor_DIR_pin, False)
io.output(rightMotor_DIR_pin, False)  
  
leftMotor_PWM_pin = 17
rightMotor_PWM_pin = 18
io.setup(leftMotor_PWM_pin, io.OUT)  
io.setup(rightMotor_PWM_pin, io.OUT)  

leftMotorPWM = io.PWM(leftMotor_PWM_pin,20)  
rightMotorPWM = io.PWM(rightMotor_PWM_pin,20)  
  
leftMotorPWM.start(0)  
leftMotorPWM.ChangeDutyCycle(0)  
rightMotorPWM.start(0)  
rightMotorPWM.ChangeDutyCycle(0)  

leftMotorPower = 0  
rightMotorPower = 0  

def getMotorPowers():  # 모터 속도 반환
	return (leftMotorPower,rightMotorPower)

def setMotorLeft(power):  # 왼쪽 모터 set
	if power < 0:
		io.output(leftMotor_DIR_pin, False)
		pwm = -int(PWM_MAX * power)  

		if pwm > PWM_MAX:  
			pwm = PWM_MAX
	elif power > 0:  
		io.output(leftMotor_DIR_pin, True)  
		pwm = int(PWM_MAX * power)  

		if pwm > PWM_MAX:  
			pwm = PWM_MAX
	else: 
		io.output(leftMotor_DIR_pin, False)  
		pwm = 0

	leftMotorPower = pwm  
	leftMotorPWM.ChangeDutyCycle(pwm)
		
def setMotorRight(power):  # 오른쪽 모터 set
	if power < 0:  
		io.output(rightMotor_DIR_pin, True)  
		pwm = -int(PWM_MAX * power)  

		if pwm > PWM_MAX:  
			pwm = PWM_MAX  
	elif power > 0: 
		io.output(rightMotor_DIR_pin, False)  
		pwm = int(PWM_MAX * power)

		if pwm > PWM_MAX:  
			pwm = PWM_MAX  
	else:
		io.output(rightMotor_DIR_pin, False)  
		pwm = 0

	rightMotorPower = pwm  
	rightMotorPWM.ChangeDutyCycle(pwm)

def exit():  # 종료
	io.output(leftMotor_DIR_pin, False)
	io.output(rightMotor_DIR_pin, False)
	io.cleanup()