from collections import Counter


def get_segment_achievements(activity):
    segments = activity.get("segment_efforts", [])

    segment_achievements = [
        get_achievement_from_segment(segment) for segment in segments
    ]

    segment_nums = sorted(filter(lambda x: x is not None, segment_achievements))

    return get_achievement_icons(segment_nums)


def get_best_effort_achievements(activity):
    best_efforts = activity.get("best_efforts", [])

    best_effort_achievements = [
        get_achievement_from_segment(segment) for segment in best_efforts
    ]

    best_effort_nums = sorted(filter(lambda x: x is not None, best_effort_achievements))

    return get_achievement_icons(best_effort_nums)


def get_achievement_from_segment(segment):
    if "is_kom" in segment and segment["is_kom"]:
        return 0

    if "pr_rank" not in segment:
        return None

    if segment["pr_rank"] == 1:
        return 1

    if segment["pr_rank"] == 2:
        return 2

    if segment["pr_rank"] == 3:
        return 3

    return None


def get_achievement_icons(num_list):
    if len(num_list) == 0:
        return ""

    medals = {
        0: ":crown:",
        1: ":first_place:",
        2: ":second_place:",
        3: ":third_place:"
    }
    icons = ""
    icon_counts = sorted(Counter(num_list).items())

    for place, count in icon_counts:
        if count >= 10:
            icons += f"{medals[place]}x{count}"
        else:
            icons += medals[place] * count

    return icons
