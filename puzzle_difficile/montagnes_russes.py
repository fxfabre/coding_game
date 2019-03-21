# coding=utf-8


class RollerCoaster:

    def __init__(self, nb_places_available, nb_total_turns, groups):
        super(RollerCoaster, self).__init__()
        self.nb_places_available = nb_places_available
        self.nb_total_turns = nb_total_turns
        self.groups = groups
        self.cache = {}

    def fill_day(self):
        idx = 0
        total = 0
        for turn_id in range(self.nb_total_turns):
            idx, nb_perso_in = self.fill_roller_coaster_with_cache(idx)
            total += nb_perso_in

        return total

    def fill_roller_coaster_with_cache(self, idx_first_group):
        if idx_first_group in self.cache:
            (idx, nb_people) = self.cache[idx_first_group]
        else:
            idx, nb_people = self.fill_roller_coaster(idx_first_group)
            self.cache[idx_first_group] = (idx, nb_people)
        return idx, nb_people

    def fill_roller_coaster(self, idx):
        nb_groups = len(self.groups)
        nb_perso_in = 0
        for i in range(nb_groups):
            if nb_perso_in + groups[idx] > self.nb_places_available:
                break
            nb_perso_in += groups[idx]
            idx = (idx + 1) % nb_groups

        return idx, nb_perso_in


l, c, n = [int(i) for i in input().split()]
groups = [int(input()) for i in range(n)]
print(RollerCoaster(l, c, groups).fill_day())
