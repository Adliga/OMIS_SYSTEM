from interfaces import *

class InMemoryDataRepository(IDataRepository):
    def __init__(self):
        self.sensor_data: List[SensorData] = []
        self.anomalies: List[Anomaly] = []
        self.network_objects: Dict[str, NetworkObject] = {}
        self.weather_data: List[WeatherData] = []
        self.recommendations: List[Recommendation] = []
        self.forecasts: List[LoadForecast] = []
        self.reports: List[Report] = []
        
        # Инициализация тестовыми данными
        self._initialize_test_data()
    
    def _initialize_test_data(self):
        # Создание тестовых объектов сети
        substation = Substation(
            object_id="sub_001",
            name="Центральная подстанция",
            object_type=NetworkObjectType.SUBSTATION,
            status="operational",
            location="55.7558, 37.6173",
            capacity=10000.0,
            current_load=6500.0
        )
        
        feeder1 = Feeder(
            object_id="feeder_001",
            name="Фидер Северный",
            object_type=NetworkObjectType.FEEDER,
            status="operational",
            location="55.7600, 37.6200",
            capacity=500.0,
            current_load=320.0,
            parent_substation_id="sub_001",
            max_capacity=500.0,
            connected_consumers=150
        )
        
        solar_farm = RenewableSource(
            object_id="solar_001",
            name="Солнечная ферма",
            object_type=NetworkObjectType.RENEWABLE,
            status="operational",
            location="55.7500, 37.6300",
            capacity=2000.0,
            current_load=0.0,
            source_type="solar",
            current_generation=450.0,
            weather_dependency=True
        )
        
        self.network_objects = {
            substation.object_id: substation,
            feeder1.object_id: feeder1,
            solar_farm.object_id: solar_farm
        }
    
    def store_sensor_data(self, data: SensorData):
        self.sensor_data.append(data)
    
    def get_sensor_data(self, sensor_id: str, start_time: datetime.datetime, 
                       end_time: datetime.datetime) -> List[SensorData]:
        return [d for d in self.sensor_data 
                if d.sensor_id == sensor_id and start_time <= d.timestamp <= end_time]
    
    def store_anomaly(self, anomaly: Anomaly):
        self.anomalies.append(anomaly)
    
    def get_active_anomalies(self) -> List[Anomaly]:
        return [a for a in self.anomalies if a.status in ["detected", "analyzing", "action_required"]]
    
    def get_historical_data(self, start_time: datetime.datetime, 
                          end_time: datetime.datetime) -> List[SensorData]:
        return [d for d in self.sensor_data if start_time <= d.timestamp <= end_time]
    
    def get_network_object(self, object_id: str) -> Optional[NetworkObject]:
        return self.network_objects.get(object_id)
    
    def get_all_network_objects(self) -> List[NetworkObject]:
        return list(self.network_objects.values())
    
    def store_recommendation(self, recommendation: Recommendation):
        self.recommendations.append(recommendation)
    
    def get_pending_recommendations(self) -> List[Recommendation]:
        return [r for r in self.recommendations if r.status == "pending"]

class LoadForecastStrategy(IAnalysisStrategy):
    def execute_analysis(self, data: List[SensorData], context: Dict[str, Any]) -> LoadForecast:
        # Простой алгоритм прогнозирования нагрузки
        if not data:
            avg_load = 100.0
        else:
            avg_load = sum(d.value for d in data[-24:]) / min(len(data), 24)
        
        # Учет погодных условий
        weather_factor = context.get("weather_factor", 1.0)
        time_factor = self._get_time_factor(datetime.datetime.now())
        
        predicted_load = avg_load * weather_factor * time_factor
        confidence = 0.85 - abs(weather_factor - 1.0) * 0.1
        
        return LoadForecast(
            forecast_id=str(uuid.uuid4()),
            object_id=context.get("object_id", "unknown"),
            forecast_time=datetime.datetime.now(),
            predicted_load=predicted_load,
            confidence=confidence,
            forecast_period="hourly",
            weather_factor=weather_factor
        )
    
    def _get_time_factor(self, dt: datetime.datetime) -> float:
        hour = dt.hour
        if 6 <= hour < 10:  # Утро
            return 1.5
        elif 10 <= hour < 18:  # День
            return 1.2
        elif 18 <= hour < 23:  # Вечер
            return 1.8
        else:  # Ночь
            return 0.7

class AnomalyDetectionStrategy(IAnalysisStrategy):
    def execute_analysis(self, data: List[SensorData], context: Dict[str, Any]) -> Optional[Anomaly]:
        if not data:
            return None
        
        latest_data = data[-1]
        object_id = context.get("object_id", "")
        obj_type = context.get("object_type", "")
        
        # Проверка на перегрузку
        max_load = context.get("max_load", 1000.0)
        if latest_data.value > max_load * 0.9:
            severity = SeverityLevel.CRITICAL if latest_data.value > max_load else SeverityLevel.HIGH
            return Anomaly(
                anomaly_id=str(uuid.uuid4()),
                detection_time=datetime.datetime.now(),
                anomaly_type=AnomalyType.OVERLOAD,
                severity=severity,
                description=f"Перегрузка на объекте {object_id}: {latest_data.value:.1f} > {max_load * 0.9:.1f}",
                status="detected",
                affected_object_id=object_id,
                confidence_score=0.9,
                recommended_action="Перераспределить нагрузку или отключить второстепенных потребителей"
            )
        
        # Проверка на падение напряжения
        if latest_data.sensor_id.endswith("_voltage") and latest_data.value < 210:
            return Anomaly(
                anomaly_id=str(uuid.uuid4()),
                detection_time=datetime.datetime.now(),
                anomaly_type=AnomalyType.VOLTAGE_DROP,
                severity=SeverityLevel.MEDIUM,
                description=f"Падение напряжения на объекте {object_id}: {latest_data.value:.1f} В",
                status="detected",
                affected_object_id=object_id,
                confidence_score=0.75,
                recommended_action="Проверить оборудование и стабилизаторы"
            )
        
        return None

class SwitchFeederCommand(ICommand):
    def __init__(self, repository: InMemoryDataRepository, feeder_id: str, 
                 new_state: str, operator: str):
        self.repository = repository
        self.feeder_id = feeder_id
        self.new_state = new_state
        self.operator = operator
        self.old_state = None
        self.feeder = None
    
    def execute(self):
        self.feeder = self.repository.get_network_object(self.feeder_id)
        if self.feeder:
            self.old_state = self.feeder.status
            self.feeder.status = self.new_state
            print(f"Команда выполнена: {self.feeder_id} -> {self.new_state}")
            return True
        return False
    
    def undo(self):
        if self.feeder and self.old_state:
            self.feeder.status = self.old_state
            print(f"Команда отменена: {self.feeder_id} -> {self.old_state}")

class GuiAlertService(IAlertService):
    def __init__(self, app_ref):
        self.app_ref = app_ref
        self.alerts = []
    
    def send_alert(self, message: str, severity: SeverityLevel, recipient: str):
        alert = {
            "id": str(uuid.uuid4()),
            "time": datetime.datetime.now(),
            "message": message,
            "severity": severity.value,
            "recipient": recipient,
            "read": False
        }
        self.alerts.append(alert)
        
        # Обновляем интерфейс, если открыта вкладка оповещений
        if hasattr(self.app_ref, 'update_alerts_display'):
            self.app_ref.update_alerts_display()
        
        # Показываем всплывающее окно для критических оповещений
        if severity in [SeverityLevel.HIGH, SeverityLevel.CRITICAL]:
            if self.app_ref:
                self.app_ref.after(0, lambda: messagebox.showwarning(
                    f"Критическое оповещение ({severity.value})",
                    message
                ))
    
    def send_notification(self, user: User, message: str):
        print(f"Уведомление для {user.username}: {message}")