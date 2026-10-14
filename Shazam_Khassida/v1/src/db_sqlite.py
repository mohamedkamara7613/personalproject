import sqlite3

class HashDB:
    def __init__(self, db_path='data/processed/hashes.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Table des empreintes (hashes)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fingerprints (
                hash TEXT NOT NULL,
                khassida_id TEXT NOT NULL,
                version_id TEXT NOT NULL,
                offset REAL NOT NULL
            )
        ''')
        
        # Création d'un index pour accélérer massivement la recherche sur 'hash'
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_hash ON fingerprints (hash)
        ''')
        
        self.conn.commit()

    def insert_hashes(self, hashes_data):
        """
        Insère un lot de hashs dans la base de données.
        hashes_data est une liste de tuples : (hash, khassida_id, version_id, offset)
        """
        cursor = self.conn.cursor()
        
        # executemany est vital pour la rapidité lors de l'insertion massive
        cursor.execute('BEGIN TRANSACTION')
        cursor.executemany('''
            INSERT INTO fingerprints (hash, khassida_id, version_id, offset)
            VALUES (?, ?, ?, ?)
        ''', hashes_data)
        self.conn.commit()

    def find_matches(self, hashes):
        """
        Recherche des correspondances dans la base de données pour une liste de (hash, offset).
        hashes est une liste de (hash_str, offset_float)
        Retourne : { (khassida_id, version_id) : [ (db_offset - sample_offset), ... ] }
        """
        cursor = self.conn.cursor()
        
        # Pour optimiser, on construit une grosse requête SQL avec IN
        hash_list = [h[0] for h in hashes]
        hash_dict = {h[0]: h[1] for h in hashes} # Map {hash_str: sample_offset}
        
        results = []
        # Chunking the list to avoid sqlite3 "too many SQL variables" limit (999 limit usually)
        BATCH_SIZE = 900
        for i in range(0, len(hash_list), BATCH_SIZE):
            batch = hash_list[i : i + BATCH_SIZE]
            placeholders = ','.join(['?'] * len(batch))
            
            query = f'''
                SELECT hash, khassida_id, version_id, offset 
                FROM fingerprints 
                WHERE hash IN ({placeholders})
            '''
            
            cursor.execute(query, batch)
            results.extend(cursor.fetchall())
        
        # Construction du dictionnaire des offsets (Alignement Temporel)
        matches = {}
        for row in results:
            db_hash, k_id, v_id, db_offset = row
            sample_offset = hash_dict[db_hash]
            
            # db_offset est retourné par la db, potentiellement comme un byte string (ex: b'7\x00\x00\x00\x00\x00\x00\x00')
            # C'est parce qu'on insère des types np.int64 dans SQLite. 
            # On s'assure de les traiter soit depuis un int natif, soit depuis le buffer brut
            if isinstance(db_offset, bytes):
                import struct
                # np.int64 correspond à 'q' en struct (long long, 8 bytes)
                db_offset_val = struct.unpack('<q', db_offset)[0]
            else:
                db_offset_val = db_offset
                
            delta_offset = float(db_offset_val) - float(sample_offset)
            
            key = (k_id, v_id)
            if key not in matches:
                matches[key] = []
                
            matches[key].append(delta_offset)
            
        return matches

    def close(self):
        self.conn.close()
