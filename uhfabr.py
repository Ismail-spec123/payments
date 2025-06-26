# Перепишем функцию с учетом всех условий для гарантирования заполнения ночных смен, уменьшения ошибок выборки
from turtle import pd


def stable_assign_shifts(schedule, employees):
    total_days = len(schedule[schedule['Day Shifts'] == 1])
    total_nights = len(schedule[schedule['Night Shifts'] == 2])
    max_day_shifts = total_days // len(employees) + (total_days % len(employees) > 0)
    max_night_shifts = total_nights // len(employees) + (total_nights % len(employees) > 0)

    employee_shifts = {e: {'day': 0, 'night': 0} for e in employees}

    for day in schedule.index:
        day_shift_needed = schedule.at[day, 'Day Shifts']
        night_shift_needed = schedule.at[day, 'Night Shifts']
        available_for_day = [e for e in employees if employee_shifts[e]['day'] < max_day_shifts]
        available_for_night = [e for e in employees if employee_shifts[e]['night'] < max_night_shifts]

        if day_shift_needed:
            chosen_day = np.random.choice(available_for_day)
            schedule.at[day, 'Day'] = [chosen_day]
            employee_shifts[chosen_day]['day'] += 1

        if night_shift_needed:
            # Распределяем ночные смены среди всех сотрудников, даже если это повторное назначение
            sorted_by_night_shifts = sorted(employees, key=lambda x: employee_shifts[x]['night'])
            chosen_night = sorted_by_night_shifts[:night_shift_needed]
            schedule.at[day, 'Night'] = chosen_night
            for e in chosen_night:
                employee_shifts[e]['night'] += 1

    return schedule, employee_shifts

# Применяем функцию с новой логикой распределения смен
schedule_2024, employee_shift_counts = stable_assign_shifts(schedule_2024, employees)

# Подсчет количества смен для баланса
shift_counts_2024 = pd.DataFrame(index=employees, columns=['Day Shifts', 'Night Shifts'])
shift_counts_2024['Day Shifts'] = [employee_shift_counts[emp]['day'] for emp in employees]
shift_counts_2024['Night Shifts'] = [employee_shift_counts[emp]['night'] for emp in employees]

schedule_2024, shift_counts_2024
