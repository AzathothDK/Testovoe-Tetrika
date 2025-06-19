from typing import List, Tuple

def to_intervals(raw: List[int]) -> List[Tuple[int, int]]:
    """Преобразует плоский список в список кортежей"""
    return [(raw[i], raw[i + 1]) for i in range(0, len(raw), 2)]

def clip_intervals(intervals: List[Tuple[int, int]], lesson_start: int, lesson_end: int) -> List[Tuple[int, int]]:
    """Обрезает интервалы, чтобы они не выходили за границы урока"""
    result = []
    for start, end in intervals:
        clipped_start = max(start, lesson_start)
        clipped_end = min(end, lesson_end)
        if clipped_start < clipped_end:
            result.append((clipped_start, clipped_end))
    return result

def intersect_intervals(intervals1: List[Tuple[int, int]], intervals2: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Находит пересечения между двумя списками интервалов"""
    result = []
    i = j = 0
    while i < len(intervals1) and j < len(intervals2):
        start1, end1 = intervals1[i]
        start2, end2 = intervals2[j]
        start = max(start1, start2)
        end = min(end1, end2)
        if start < end:
            result.append((start, end))
        if end1 < end2:
            i += 1
        else:
            j += 1
    return result

def total_duration(intervals: List[Tuple[int, int]]) -> int:
    """Возвращает суммарную длительность списка интервалов"""
    return sum(end - start for start, end in intervals)

def merge_intervals(intervals: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Объединяет перекрывающиеся интервалы"""
    if not intervals:
        return []
    intervals.sort()
    merged = [intervals[0]]
    for current in intervals[1:]:
        last = merged[-1]
        if current[0] <= last[1]:  
            merged[-1] = (last[0], max(last[1], current[1]))
        else:
            merged.append(current)
    return merged

def appearance(intervals: dict[str, list[int]]) -> int:
    lesson_start, lesson_end = intervals['lesson']

    pupil_intervals = to_intervals(intervals['pupil'])
    tutor_intervals = to_intervals(intervals['tutor'])

    pupil_intervals = clip_intervals(pupil_intervals, lesson_start, lesson_end)
    tutor_intervals = clip_intervals(tutor_intervals, lesson_start, lesson_end)

    pupil_intervals = merge_intervals(pupil_intervals)
    tutor_intervals = merge_intervals(tutor_intervals)

    intersected = intersect_intervals(pupil_intervals, tutor_intervals)

    return total_duration(intersected)


#Тесты
tests = [
    {'intervals': {'lesson': [1594663200, 1594666800],
             'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
             'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117
    },
    {'intervals': {'lesson': [1594702800, 1594706400],
             'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564, 1594705150,
                       1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096, 1594705106, 1594706480,
                       1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503,
                       1594706524, 1594706524, 1594706579, 1594706641],
             'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
     'answer': 3577
    },
    {'intervals': {'lesson': [1594692000, 1594695600],
             'pupil': [1594692033, 1594696347],
             'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
     'answer': 3565
    },
]

if __name__ == '__main__':
    for i, test in enumerate(tests):
        test_answer = appearance(test['intervals'])
        expected = test['answer']
        assert test_answer == expected, f"Падает тест {i}, ответ {test_answer}, что ожидалось {expected}"
    print("Все тесты пройдены.")
