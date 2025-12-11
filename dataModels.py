from enums import *

@dataclass
class User:
    user_id: str
    username: str
    role: UserRole
    department: Optional[str] = None
    shift: Optional[str] = None
    email: Optional[str] = None

@dataclass
class NetworkObject:
    object_id: str
    name: str
    object_type: NetworkObjectType
    status: str  # "operational", "maintenance", "failure"
    location: str
    capacity: float = 0.0
    current_load: float = 0.0
    
    def __str__(self):
        return f"{self.name} ({self.object_type.value})"

@dataclass
class Substation(NetworkObject):
    voltage_level: str = "110kV"
    transformer_count: int = 2

@dataclass
class Feeder(NetworkObject):
    parent_substation_id: str = ""
    max_capacity: float = 1000.0
    connected_consumers: int = 0

@dataclass
class RenewableSource(NetworkObject):
    source_type: str = "solar"  # solar, wind, hydro
    current_generation: float = 0.0
    weather_dependency: bool = True

@dataclass
class Consumer(NetworkObject):
    consumer_type: str = "residential"  # residential, commercial, industrial
    address: str = ""
    contract_power: float = 0.0

@dataclass
class Sensor:
    sensor_id: str
    sensor_type: SensorType
    network_object_id: str
    status: str = "active"
    last_read: Optional[datetime.datetime] = None

@dataclass
class SensorData:
    data_id: str
    sensor_id: str
    timestamp: datetime.datetime
    value: float
    unit: str = ""

@dataclass
class WeatherData:
    station_id: str
    timestamp: datetime.datetime
    temperature: float
    wind_speed: float
    humidity: float
    conditions: str = "clear"

@dataclass
class Anomaly:
    anomaly_id: str
    detection_time: datetime.datetime
    anomaly_type: AnomalyType
    severity: SeverityLevel
    description: str
    status: str  # "detected", "analyzing", "action_required", "resolved"
    affected_object_id: str
    confidence_score: float
    recommended_action: str = ""
    
    def __str__(self):
        return f"{self.anomaly_type.value}: {self.description}"

@dataclass
class Recommendation:
    recommendation_id: str
    anomaly_id: str
    creation_time: datetime.datetime
    content: str
    priority: int  # 1-5, где 5 - наивысший
    status: str  # "pending", "approved", "rejected", "executed"
    action_type: str  # "switching", "maintenance", "alert"
    executor_id: Optional[str] = None
    execution_time: Optional[datetime.datetime] = None

@dataclass
class LoadForecast:
    forecast_id: str
    object_id: str
    forecast_time: datetime.datetime
    predicted_load: float
    confidence: float
    forecast_period: str  # "hourly", "daily", "weekly"
    weather_factor: float = 1.0

@dataclass
class SwitchScheme:
    scheme_id: str
    anomaly_id: str
    description: str
    actions: List[str]
    status: str  # "proposed", "approved", "executed"
    created_by: str = "system"

@dataclass
class Report:
    report_id: str
    title: str
    report_type: str  # "daily", "weekly", "monthly", "incident"
    creation_date: datetime.datetime
    content: str
    created_by: str

@dataclass
class MaintenanceTask:
    task_id: str
    equipment_id: str
    scheduled_time: datetime.datetime
    task_type: str
    status: str  # "scheduled", "in_progress", "completed"
    assigned_to: str
