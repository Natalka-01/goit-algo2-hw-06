import hashlib

class BloomFilter:
    def __init__(self, size=1000, num_hashes=3):
        
        self.size = size
        
        self.num_hashes = num_hashes
        
        self.bit_array = [False] * size

    def _get_hashes(self, item):
        
        hashes = []
        for i in range(self.num_hashes):
            
            data = (str(i) + item).encode('utf-8')
            hash_int = int(hashlib.md5(data).hexdigest(), 16)
            hashes.append(hash_int % self.size)
        return hashes

    def add(self, item):
        # Handle invalid or empty items
        if not isinstance(item, str) or not item:
            return
        
        # Calculate hashes and set bits to True (1)
        for h in self._get_hashes(item):
            self.bit_array[h] = True

    def contains(self, item):
        # Handle invalid or empty items
        if not isinstance(item, str) or not item:
            return False
        
        
        for h in self._get_hashes(item):
            if not self.bit_array[h]:
                return False
        return True

def check_password_uniqueness(bloom, passwords):
    results = {}
    for password in passwords:
        # Handle empty or incorrect data types gracefully
        if not isinstance(password, str) or not password:
            results[str(password)] = "некоректне значення"
            continue
            
        # Check the filter to see if the password exists
        if bloom.contains(password):
            results[password] = "вже використаний"
        else:
            results[password] = "унікальний"
            
    return results

if __name__ == "__main__":
    
    bloom = BloomFilter(size=1000, num_hashes=3)

    
    existing_passwords = ["password123", "admin123", "qwerty123"]
    for password in existing_passwords:
        bloom.add(password)
        
    
    new_passwords_to_check = ["password123", "newpassword", "admin123", "guest"]
    results = check_password_uniqueness(bloom, new_passwords_to_check)

    
    for password, status in results.items():
        print(f"Пароль '{password}' — {status}.")