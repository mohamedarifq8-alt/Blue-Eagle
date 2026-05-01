from controller import Robot

class Mavic2ProController:
    def __init__(self):
        self.robot = Robot()
        self.time_step = int(self.robot.getBasicTimeStep())
        
        # 1. تعريف الحساسات
        self.imu = self.robot.getDevice("inertial unit")
        self.imu.enable(self.time_step)
        self.gyro = self.robot.getDevice("gyro")
        self.gyro.enable(self.time_step)
        self.gps = self.robot.getDevice("gps")
        self.gps.enable(self.time_step)
        
        # 2. تعريف المحركات
        self.motors = [
            self.robot.getDevice("front left propeller"),
            self.robot.getDevice("front right propeller"),
            self.robot.getDevice("rear left propeller"),
            self.robot.getDevice("rear right propeller")
        ]
        
        for motor in self.motors:
            motor.setPosition(float('inf')) # وضع التحكم بالسرعة
            motor.setVelocity(0)

        # ثوابت PID للتوازن (القيم الناجحة التي قمت بضبطها)
        self.k_roll_p = 30.0
        self.k_roll_d = 2.0
        self.k_pitch_p = 30.0  # تم إضافة ثوابت الانحدار لتطابق الالتفاف
        self.k_pitch_d = 2.0

        self.target_altitude = 20.0 # الارتفاع المطلوب بالمتر (جربت 5 أمتار لاختبار الاستقرار)
        
        # متغير لحفظ الارتفاع السابق (مهم جداً لحساب السرعة العمودية/الفرامل)
        self.prev_altitude = 0.0

    def run(self):
        while self.robot.step(self.time_step) != -1:
            # قراءة الحساسات
            roll, pitch, yaw = self.imu.getRollPitchYaw()
            roll_rate, pitch_rate, yaw_rate = self.gyro.getValues()
            altitude = self.gps.getValues()[2]
            
            # --- حساب السرعة العمودية (الفرامل) ---
            # نقوم بحساب فرق الارتفاع بالنسبة للزمن لمعرفة سرعة صعود/هبوط الطائرة
            vertical_velocity = (altitude - self.prev_altitude) / (self.time_step / 1000.0)
            self.prev_altitude = altitude
            
            # --- متحكم الارتفاع المطور (Altitude PD Controller) ---
            altitude_error = self.target_altitude - altitude
            
            # وضع حد أقصى للخطأ لضمان صعود سلس ومستقر (كي لا تندفع الطائرة بجنون)
            MAX_ALT_ERROR = 1.5 
            if altitude_error > MAX_ALT_ERROR:
                altitude_error = MAX_ALT_ERROR
            elif altitude_error < -MAX_ALT_ERROR:
                altitude_error = -MAX_ALT_ERROR
            
            # المتحكم الجديد: الرفع الأساسي + (الزنبرك/التناسب) - (الفرامل/التفاضل)
            vertical_input = 68.5 + (altitude_error * 10.0) - (vertical_velocity * 5.0)
            
            # حماية المحركات من التشبع (Saturation) لضمان بقاء طاقة لمتحكم التوازن
            if vertical_input > 85.0:  
                vertical_input = 85.0
            elif vertical_input < 50.0: 
                vertical_input = 50.0 # لا تطفئ المحركات تماماً أثناء النزول كي لا تسقط وتتحطم
            
            # --- متحكم التوازن (Attitude Controller) ---
            roll_input = (0 - roll) * self.k_roll_p - (roll_rate * self.k_roll_d)
            pitch_input = (0 - pitch) * self.k_pitch_p - (pitch_rate * self.k_pitch_d)
            
            # مصفوفة الخلط (Mixing)
            m1 = vertical_input + roll_input - pitch_input # Front Left
            m2 = vertical_input - roll_input - pitch_input # Front Right
            m3 = vertical_input + roll_input + pitch_input # Rear Left
            m4 = vertical_input - roll_input + pitch_input # Rear Right
            
            # إرسال الأوامر للمحركات
            self.motors[0].setVelocity(m1)
            self.motors[1].setVelocity(-m2) # عكس الإشارة حسب اتجاه المروحة
            self.motors[2].setVelocity(-m3)
            self.motors[3].setVelocity(m4)

controller = Mavic2ProController()
controller.run()