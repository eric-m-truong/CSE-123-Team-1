INIT_PLUG = """
            CREATE TABLE Plugs (
                mac_addr TEXT PRIMARY KEY,
                alias TEXT,
                is_on BOOLEAN NOT NULL
            )
            """
INIT_DATA = """
            CREATE TABLE Data (
                timestamp DATETIME,
                plug_id TEXT,
                power FLOAT,
                FOREIGN KEY(plug_id) REFERENCES Plugs(mac_addr)
            )
            """
INS_PLUG = "INSERT INTO Plugs VALUES (:mac_addr, :alias, :is_on)"
INS_DATA = "INSERT INTO Data VALUES (:timestamp, :plug_id, :power)"
SEL_PLUG_BY_MAC = "SELECT * FROM Plugs WHERE mac_addr=(?)"
SEL_PLUG_SUM = "SELECT plug_id, SUM(power) FROM Data GROUP BY plug_id"
