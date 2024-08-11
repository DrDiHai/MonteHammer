class CombatResult:
    def __init__(
        self,
        hit_rate,
        raw_wound_rate,
        wound_rate,
        raw_unsaved_rate,
        unsaved_rate,
        raw_unwarded_rate,
        unwarded_rate,
        raw_unregenerated_rate,
        unregenerated_rate,
        kill_rate,
    ):
        self.hit_rate = hit_rate
        self.raw_wound_rate = raw_wound_rate
        self.wound_rate = wound_rate
        self.raw_unsaved_rate = raw_unsaved_rate
        self.unsaved_rate = unsaved_rate
        self.raw_unwarded_rate = raw_unwarded_rate
        self.unwarded_rate = unwarded_rate
        self.raw_unregenerated_rate = raw_unregenerated_rate
        self.unregenerated_rate = unregenerated_rate
        self.kill_rate = kill_rate
