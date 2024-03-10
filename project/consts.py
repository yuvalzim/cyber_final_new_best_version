# Network constants
MASK_BYTE_ON = "255"
MAC_LENGTH = 6
PORT_DST = 8888
ARP_DLL_PATH = r"C:\Users\yuval\OneDrive\Desktop\Cyber-antivirus-project-main\ARP_send\x64\Debug\ARP_send.dll"

# Database constants
DB_NAME = "addresses.db"
INSERT_SQL_QUERY = '''INSERT INTO computers(ip, mac, is_on) VALUES(?, ?, ?)'''
UPDATE_ROW_QUERY = '''UPDATE computers SET is_on=? WHERE ROWID=?'''
GET_DATA_SQL_QUERY = '''SELECT * FROM computers'''

# GUI constants
X_DRAW_START = 100
Y_DRAW_START = 130
