import datetime
import uuid
import random
import tkinter as tk
from tkinter import messagebox, ttk
from dataclasses import dataclass
from typing import Dict, List, Optional, Callable, Any
import abc
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import threading
import time
from enum import Enum

class UserRole(Enum):
    DISPATCHER = "Диспетчер"
    ANALYST = "Инженер-аналитик"
    ADMIN = "Администратор"

class NetworkObjectType(Enum):
    SUBSTATION = "Подстанция"
    FEEDER = "Фидер"
    GENERATOR = "Генератор"
    CONSUMER = "Потребитель"
    RENEWABLE = "Возобновляемый источник"
    LINE = "Линия электропередачи"

class SensorType(Enum):
    VOLTAGE = "Напряжение"
    CURRENT = "Ток"
    POWER = "Мощность"
    TEMPERATURE = "Температура"
    CONSUMPTION = "Потребление"

class AnomalyType(Enum):
    OVERLOAD = "Перегрузка"
    VOLTAGE_DROP = "Падение напряжения"
    POWER_OUTAGE = "Отключение питания"
    EQUIPMENT_FAILURE = "Отказ оборудования"
    UNUSUAL_CONSUMPTION = "Необычное потребление"

class SeverityLevel(Enum):
    LOW = "Низкий"
    MEDIUM = "Средний"
    HIGH = "Высокий"
    CRITICAL = "Критический"