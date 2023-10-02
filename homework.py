from typing import Dict, Type
from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        return self.MESSAGE.format(
            training_type=self.training_type,
            duration=self.duration,
            distance=self.distance,
            speed=self.speed,
            calories=self.calories
        )


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError()

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info = InfoMessage(
            training_type=self.__class__.__name__,
            duration=self.duration,
            distance=self.get_distance(),
            speed=self.get_mean_speed(),
            calories=self.get_spent_calories()
        )
        return info


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        time_minutes = self.duration * self.MIN_IN_H
        calories = (
            (self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
             + self.CALORIES_MEAN_SPEED_SHIFT)
            * self.weight / self.M_IN_KM * time_minutes
        )
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_1 = 0.035
    COEFF_2 = 0.029
    MIN_IN_H = 60
    TO_M_PER_SEC = 0.278
    CM_TO_METERS = 100

    def __init__(self, action: int, duration: float,
                 weight: float, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height / self.CM_TO_METERS

    def get_spent_calories(self) -> float:
        m_per_s_speed = self.get_mean_speed() * self.TO_M_PER_SEC
        calories = (
            (self.COEFF_1 * self.weight
             + (m_per_s_speed ** 2 / self.height)
             * self.COEFF_2 * self.weight) * (self.duration * self.MIN_IN_H)
        )
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38  # Расстояние, преодолеваемое за один гребок, в м
    COEFF_SWIM = 1.1
    COEFF_SWIM2 = 2

    def __init__(self, action: int, duration: float,
                 weight: float, length_pool: float, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        mean_speed = (
            self.length_pool * self.count_pool / self.M_IN_KM
            / self.duration
        )
        return mean_speed

    def get_spent_calories(self) -> float:
        calories = ((self.get_mean_speed() + self.COEFF_SWIM)
                    * self.weight * self.COEFF_SWIM2 * self.duration)
        return calories


workout_mapping: Dict[str, Type[Training]] = {
    'RUN': Running,
    'WLK': SportsWalking,
    'SWM': Swimming,
}


def read_package(workout_type: str, data: list) -> Training:
    if workout_type in workout_mapping:
        action, duration, weight, *extra_data = data
        workout_class = workout_mapping[workout_type]
        return workout_class(action, duration, weight, *extra_data)
    raise NotImplementedError('неподдерживаемый тип тренировки')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        try:
            training = read_package(workout_type, data)
            main(training)
        except ValueError:
            print('упс. ошибка')
