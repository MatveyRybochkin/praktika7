from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message: str = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        """Выводим информацию о тренировке."""
        return self.message.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action_times = action
        self.duration_hour = duration
        self.weight_kg = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action_times * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration_hour

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return (InfoMessage(self.__class__.__name__,
                self.duration_hour, self.get_distance(),
                self.get_mean_speed(), self.get_spent_calories()))


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Получаем количество затраченных калорий во время бега."""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                 * self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight_kg / self.M_IN_KM
                * self.duration_hour * self.MIN_IN_HOUR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_CALORIE_1: float = 0.035
    COEFF_CALORIE_2: float = 0.029
    KMH_IN_MSEC: float = 0.278
    CM_IN_M: int = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height_cm = height / self.CM_IN_M

    def get_spent_calories(self) -> float:
        return ((self.COEFF_CALORIE_1 * self.weight_kg
                 + ((self.KMH_IN_MSEC
                    * self.get_mean_speed()) ** 2 / self.height_cm)
                * self.COEFF_CALORIE_2 * self.weight_kg)
                * self.duration_hour * self.MIN_IN_HOUR)


class Swimming(Training):
    LEN_STEP: float = 1.38
    COEFF_SWIMMING_1: float = 1.1
    COEFF_SWIMMING_2: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool_meters = length_pool
        self.count_pool_times = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool_meters * self.count_pool_times
                / self.M_IN_KM / self.duration_hour)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.COEFF_SWIMMING_1)
                * self.COEFF_SWIMMING_2
                * self.weight_kg
                * self.duration_hour)


def read_package(workout_type: str, data: list[int]) -> Training:
    """Считываем данные полученные от датчиков."""
    training_data: dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    if workout_type not in training_data:
        raise ValueError('Передан неверный идентификатор тренировки.')
    return training_data[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    # убрал типы
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]
    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)
