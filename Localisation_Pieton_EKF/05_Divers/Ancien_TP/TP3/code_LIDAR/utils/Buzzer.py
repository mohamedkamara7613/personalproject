import RPi.GPIO as GPIO

class Buzzer:
    """
    Classe pour l'utilisation d'un buzzer.
    
    Branchement:
    
    +   : VCC 5V
    -   : GND
    SIG : PORT GPIO
    NCC : /
    
    Exemple d'utilisation:
    buzzer = Buzzer(17)  # Connexion au port GPIO 17
    buzzer.play(440)  # Joue un La (440 Hz)
    buzzer.stop()    # Stop le son
    buzzer.cleanup() # Libération des ressouces du GPIO
    
    """
    def __init__(self, pin):
        """
        Initialisation du buzzer sur un GPIO donné
        
        Arguments:
        - pin: Le pin GPIO où communique le buzzer.
        """
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 440)  # Fréquence par défaut 440 Hz
        self.pwm.start(0)  # Duty cycle à 0 pour ne pas faire de bruit au démarrage

    def play(self, frequency):
        """
        Joue un son à une fréquence donnée (Hz)
        
        Arguments:
        - frequency : la fréquence de l'audio à jouer (en Hz)
        """
        self.pwm.ChangeFrequency(frequency)
        self.pwm.start(30)

    def stop(self):
        """
        Arrête le son 
        """
        self.pwm.stop()

    def cleanup(self):
        """Libère les ressources du GPIO"""
        self.pwm.stop()
        GPIO.cleanup()
