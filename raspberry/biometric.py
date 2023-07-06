import fingerprinth

class BiometricModule:
    def __init__(self):
        self.sensor = fingerprinth.Fingerprint()
    
    def connect(self):
        """Connect to the biometric module."""
        try:
            self.sensor.open()
        except fingerprinth.FingerprintException as e:
            print(f"Failed to connect to the biometric module: {e}")

    def enroll(self, fingerprint_id):
        """Enroll a new fingerprint with the given ID."""
        try:
            self.sensor.enroll(fingerprint_id)
            print(f"Fingerprint enrolled successfully with ID: {fingerprint_id}")
        except fingerprinth.FingerprintException as e:
            print(f"Failed to enroll fingerprint: {e}")
    
    def verify(self):
        """Verify the fingerprint."""
        try:
            fingerprint_id = self.sensor.capture()
            if fingerprint_id >= 0:
                print(f"Fingerprint verified successfully with ID: {fingerprint_id}")
            else:
                print("Fingerprint verification failed")
        except fingerprinth.FingerprintException as e:
            print(f"Failed to verify fingerprint: {e}")

    def delete(self, fingerprint_id):
        """Delete the fingerprint with the given ID."""
        try:
            self.sensor.delete(fingerprint_id)
            print(f"Fingerprint with ID {fingerprint_id} deleted successfully")
        except fingerprinth.FingerprintException as e:
            print(f"Failed to delete fingerprint: {e}")

    def disconnect(self):
        """Disconnect from the biometric module."""
        self.sensor.close()

def main():
    biometric_module = BiometricModule()
    biometric_module.connect()

    try:
        # Use the biometric module
        biometric_module.enroll(1)
        biometric_module.verify()
        biometric_module.delete(1)

    except KeyboardInterrupt:
        biometric_module.disconnect()

if __name__ == '__main__':
    main()
