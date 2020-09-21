CREATE TABLE matches (
	activision_id TEXT,
	start_time INT,
	end_time INT PRIMARY KEY,
	map_name TEXT,
	result INT,
	kills INT,
	deaths INT
	);

-- Description of column names:
-- MatchID
-- MatchStart
-- MatchEnd
-- Map
-- Win/Loss
-- Kills
-- Deaths