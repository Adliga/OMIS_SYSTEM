from dataModels import *

class IDataRepository(abc.ABC):
    @abc.abstractmethod
    def store_sensor_data(self, data: SensorData):
        pass
    
    @abc.abstractmethod
    def get_sensor_data(self, sensor_id: str, start_time: datetime.datetime, 
                       end_time: datetime.datetime) -> List[SensorData]:
        pass
    
    @abc.abstractmethod
    def store_anomaly(self, anomaly: Anomaly):
        pass
    
    @abc.abstractmethod
    def get_active_anomalies(self) -> List[Anomaly]:
        pass
    
    @abc.abstractmethod
    def get_historical_data(self, start_time: datetime.datetime, 
                          end_time: datetime.datetime) -> List[SensorData]:
        pass

class IAnalysisStrategy(abc.ABC):
    @abc.abstractmethod
    def execute_analysis(self, data: List[SensorData], context: Dict[str, Any]) -> Any:
        pass

class ICommand(abc.ABC):
    @abc.abstractmethod
    def execute(self):
        pass
    
    @abc.abstractmethod
    def undo(self):
        pass

class IAlertService(abc.ABC):
    @abc.abstractmethod
    def send_alert(self, message: str, severity: SeverityLevel, recipient: str):
        pass
    
    @abc.abstractmethod
    def send_notification(self, user: User, message: str):
        pass