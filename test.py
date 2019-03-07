from nba_api.stats.static import players
from nba_api.stats.endpoints import drafthistory,commonplayerinfo,commonallplayers

info = commonallplayers.CommonAllPlayers(is_only_current_season=1)
