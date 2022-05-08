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
SEL_DATA_RANGE = """
                 SELECT plug_id, power FROM Data
                     WHERE timestamp >= strftime('%s', 'now', ?)
                     ORDER BY timestamp DESC
                 """
SEL_UNIQ_TS = """
              SELECT DISTINCT CAST(timestamp as INTEGER) FROM Data
                  WHERE timestamp >= strftime('%s', 'now', ?)
                  ORDER BY timestamp ASC
              """
SEL_DATA_BY_APPROX_TS = """ SELECT plug_id, power FROM Data
                                WHERE CAST(timestamp AS INTEGER) = ?
                        """
UPD_ALIAS = """ UPDATE Plugs SET alias = (?) WHERE mac_addr = (?) """
UPD_STATUS = """ UPDATE Plugs SET is_on = (?) WHERE mac_addr = (?) """
SEL_PLUG_DAY_AVG_BY_HR = """
                         SELECT
                             CAST(strftime('%H', timestamp, 'unixepoch') AS INT)
                                 AS hour,
                             plug_id,
                             AVG(power)
                         FROM Data
                           WHERE timestamp >= strftime('%s', 'now', '-1 day')
                           GROUP BY plug_id, hour;
                         """
