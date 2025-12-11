from implementations import *

class NetworkMonitorController:
    def __init__(self, repository: InMemoryDataRepository):
        self.repository = repository
        self.monitoring_active = False
        self.anomaly_detector = AnomalyDetectionStrategy()
    
    def start_monitoring(self):
        self.monitoring_active = True
        print("Мониторинг сети запущен")
    
    def stop_monitoring(self):
        self.monitoring_active = False
        print("Мониторинг сети остановлен")
    
    def get_network_status(self) -> Dict[str, Any]:
        objects = self.repository.get_all_network_objects()
        operational = sum(1 for obj in objects if obj.status == "operational")
        total = len(objects)
        
        return {
            "total_objects": total,
            "operational": operational,
            "maintenance": sum(1 for obj in objects if obj.status == "maintenance"),
            "failures": sum(1 for obj in objects if obj.status == "failure"),
            "health_percentage": (operational / total * 100) if total > 0 else 0
        }
    
    def get_active_anomalies(self) -> List[Anomaly]:
        return self.repository.get_active_anomalies()
    
    def detect_anomalies(self, sensor_data: SensorData, network_object: NetworkObject):
        if not self.monitoring_active:
            return
        
        context = {
            "object_id": network_object.object_id,
            "object_type": network_object.object_type.value,
            "max_load": network_object.capacity
        }
        
        historical_data = self.repository.get_sensor_data(
            sensor_data.sensor_id,
            sensor_data.timestamp - datetime.timedelta(hours=24),
            sensor_data.timestamp
        )
        
        anomaly = self.anomaly_detector.execute_analysis(
            historical_data + [sensor_data],
            context
        )
        
        if anomaly:
            self.repository.store_anomaly(anomaly)
            return anomaly
        
        return None

class RecommendationController:
    def __init__(self, repository: InMemoryDataRepository):
        self.repository = repository
    
    def generate_recommendation(self, anomaly: Anomaly) -> Recommendation:
        # Генерация рекомендаций на основе типа аномалии
        if anomaly.anomaly_type == AnomalyType.OVERLOAD:
            content = f"Переключить часть нагрузки с объекта {anomaly.affected_object_id} на резервные линии"
            priority = 5 if anomaly.severity == SeverityLevel.CRITICAL else 4
            action_type = "switching"
        elif anomaly.anomaly_type == AnomalyType.VOLTAGE_DROP:
            content = f"Проверить и отрегулировать оборудование на объекте {anomaly.affected_object_id}"
            priority = 3
            action_type = "maintenance"
        elif anomaly.anomaly_type == AnomalyType.POWER_OUTAGE:
            content = f"Восстановить питание на объекте {anomaly.affected_object_id}"
            priority = 5
            action_type = "emergency"
        else:
            content = f"Требуется анализ ситуации на объекте {anomaly.affected_object_id}"
            priority = 2
            action_type = "analysis"
        
        recommendation = Recommendation(
            recommendation_id=str(uuid.uuid4()),
            anomaly_id=anomaly.anomaly_id,
            creation_time=datetime.datetime.now(),
            content=content,
            priority=priority,
            status="pending",
            action_type=action_type
        )
        
        self.repository.store_recommendation(recommendation)
        return recommendation
    
    def approve_recommendation(self, recommendation_id: str, user_id: str):
        for rec in self.repository.recommendations:
            if rec.recommendation_id == recommendation_id:
                rec.status = "approved"
                rec.executor_id = user_id
                return True
        return False

class ForecastController:
    def __init__(self, repository: InMemoryDataRepository):
        self.repository = repository
        self.forecast_strategy = LoadForecastStrategy()
    
    def create_load_forecast(self, object_id: str, weather_data: Optional[WeatherData] = None) -> LoadForecast:
        context = {
            "object_id": object_id,
            "weather_factor": weather_data.temperature / 20.0 if weather_data else 1.0
        }
        
        # Получаем исторические данные
        historical_data = self.repository.get_historical_data(
            datetime.datetime.now() - datetime.timedelta(days=7),
            datetime.datetime.now()
        )
        
        forecast = self.forecast_strategy.execute_analysis(historical_data, context)
        self.repository.forecasts.append(forecast)
        return forecast
    
    def get_latest_forecast(self, object_id: str) -> Optional[LoadForecast]:
        forecasts = [f for f in self.repository.forecasts if f.object_id == object_id]
        if forecasts:
            return max(forecasts, key=lambda x: x.forecast_time)
        return None

class ReportController:
    def __init__(self, repository: InMemoryDataRepository):
        self.repository = repository
    
    def generate_report(self, report_type: str, start_date: datetime.datetime,
                       end_date: datetime.datetime, created_by: str) -> Report:
        anomalies = [a for a in self.repository.anomalies 
                    if start_date <= a.detection_time <= end_date]
        sensor_data = self.repository.get_historical_data(start_date, end_date)
        
        if report_type == "daily":
            title = f"Ежедневный отчет за {start_date.date()}"
            content = self._generate_daily_content(anomalies, sensor_data)
        elif report_type == "weekly":
            title = f"Еженедельный отчет за {start_date.date()} - {end_date.date()}"
            content = self._generate_weekly_content(anomalies, sensor_data)
        else:
            title = f"Отчет за период {start_date.date()} - {end_date.date()}"
            content = self._generate_general_content(anomalies, sensor_data)
        
        report = Report(
            report_id=str(uuid.uuid4()),
            title=title,
            report_type=report_type,
            creation_date=datetime.datetime.now(),
            content=content,
            created_by=created_by
        )
        
        self.repository.reports.append(report)
        return report
    
    def _generate_daily_content(self, anomalies: List[Anomaly], sensor_data: List[SensorData]) -> str:
        return f"""Ежедневный отчет
========================
Всего аномалий: {len(anomalies)}
Критические: {sum(1 for a in anomalies if a.severity == SeverityLevel.CRITICAL)}
Высокой важности: {sum(1 for a in anomalies if a.severity == SeverityLevel.HIGH)}
Средней важности: {sum(1 for a in anomalies if a.severity == SeverityLevel.MEDIUM)}

Записей данных: {len(sensor_data)}
Среднее значение: {sum(d.value for d in sensor_data)/len(sensor_data) if sensor_data else 0:.2f}
"""
    
    def _generate_weekly_content(self, anomalies: List[Anomaly], sensor_data: List[SensorData]) -> str:
        return f"""Еженедельный отчет
===========================
Статистика за неделю:
- Всего аномалий: {len(anomalies)}
- Решено аномалий: {sum(1 for a in anomalies if a.status == 'resolved')}
- Ожидают решения: {sum(1 for a in anomalies if a.status in ['detected', 'analyzing'])}
- Объем данных: {len(sensor_data)} записей

Тенденции:
- Средняя нагрузка сети: {self._calculate_average_load(sensor_data):.2f}
- Пиковая нагрузка: {max(d.value for d in sensor_data) if sensor_data else 0:.2f}
"""

    def _calculate_average_load(self, sensor_data: List[SensorData]) -> float:
        if not sensor_data:
            return 0.0
        power_data = [d for d in sensor_data if "power" in d.sensor_id.lower()]
        if power_data:
            return sum(d.value for d in power_data) / len(power_data)
        return sum(d.value for d in sensor_data) / len(sensor_data)
