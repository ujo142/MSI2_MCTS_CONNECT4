from pydantic.main import BaseModel


class Config(BaseModel):
    height: int = 6
    width: int = 7
    max_rollouts: int = 1000
    time_rollouts: int = 1
    seed: int = 42
    n_games: int = 20
    stats_path: str = "stats"

    def pretty_string(self):
        return f"{self.height}_{self.width}_i{self.max_rollouts}_t{self.time_rollouts}"

