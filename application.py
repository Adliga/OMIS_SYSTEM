from controllers import *

class SmartGridManagementApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Система интеллектуального управления энергосетями умного города")
        self.geometry("1400x800")
        
        # Инициализация компонентов
        self.repository = InMemoryDataRepository()
        self.alert_service = GuiAlertService(self)
        self.monitor_controller = NetworkMonitorController(self.repository)
        self.recommendation_controller = RecommendationController(self.repository)
        self.forecast_controller = ForecastController(self.repository)
        self.report_controller = ReportController(self.repository)
        
        # Текущий пользователь
        self.current_user = None
        self.data_generation_active = False
        
        self.show_login_screen()
    
    def show_login_screen(self):
        """Экран входа в систему"""
        self.clear_window()
        
        login_frame = tk.Frame(self, padx=50, pady=50)
        login_frame.pack(expand=True)
        
        tk.Label(login_frame, text="Система управления энергосетями", 
                font=("Arial", 20, "bold")).pack(pady=20)
        
        tk.Label(login_frame, text="Выберите роль для входа:", 
                font=("Arial", 12)).pack(pady=10)
        
        # Кнопки выбора роли
        roles_frame = tk.Frame(login_frame)
        roles_frame.pack(pady=20)
        
        dispatcher_btn = tk.Button(roles_frame, text="Диспетчер", 
                                  command=lambda: self.login_as(UserRole.DISPATCHER),
                                  width=20, height=3, bg="#4CAF50", fg="white",
                                  font=("Arial", 11))
        dispatcher_btn.pack(side=tk.LEFT, padx=10)
        
        analyst_btn = tk.Button(roles_frame, text="Инженер-аналитик",
                               command=lambda: self.login_as(UserRole.ANALYST),
                               width=20, height=3, bg="#2196F3", fg="white",
                               font=("Arial", 11))
        analyst_btn.pack(side=tk.LEFT, padx=10)
        
        admin_btn = tk.Button(roles_frame, text="Администратор",
                             command=lambda: self.login_as(UserRole.ADMIN),
                             width=20, height=3, bg="#FF9800", fg="white",
                             font=("Arial", 11))
        admin_btn.pack(side=tk.LEFT, padx=10)
    
    def login_as(self, role: UserRole):
        """Вход под выбранной ролью"""
        users = {
            UserRole.DISPATCHER: User("disp_001", "Иванов А.И.", UserRole.DISPATCHER, 
                                     "Оперативный отдел", "Дневная смена"),
            UserRole.ANALYST: User("anal_001", "Петрова С.В.", UserRole.ANALYST,
                                  "Аналитический отдел"),
            UserRole.ADMIN: User("admin_001", "Сидоров П.К.", UserRole.ADMIN,
                                "Администрация", email="admin@smartgrid.city")
        }
        
        self.current_user = users[role]
        self.alert_service.send_notification(
            self.current_user, 
            f"Добро пожаловать в систему, {self.current_user.username}!"
        )
        
        self.setup_main_interface()
        self.start_data_generation()
    
    def setup_main_interface(self):
        """Настройка основного интерфейса"""
        self.clear_window()
        
        # Верхняя панель
        top_bar = tk.Frame(self, bg="#2E3B4E", height=60)
        top_bar.pack(fill=tk.X)
        top_bar.pack_propagate(False)
        
        tk.Label(top_bar, text=f"Управление энергосетями | {self.current_user.role.value}: {self.current_user.username}",
                font=("Arial", 14, "bold"), bg="#2E3B4E", fg="white").pack(side=tk.LEFT, padx=20, pady=10)
        
        logout_btn = tk.Button(top_bar, text="Выход", command=self.show_login_screen,
                              bg="#E74C3C", fg="white", font=("Arial", 10))
        logout_btn.pack(side=tk.RIGHT, padx=20, pady=10)
        
        # Основной контейнер
        main_container = tk.Frame(self)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Боковая панель навигации
        self.sidebar = tk.Frame(main_container, bg="#34495E", width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)
        
        # Область контента
        self.content_area = tk.Frame(main_container, bg="white")
        self.content_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Заполнение боковой панели
        self.setup_sidebar()
        
        # Показываем панель мониторинга по умолчанию
        self.show_monitoring_dashboard()
    
    def setup_sidebar(self):
        """Настройка боковой панели навигации"""
        tk.Label(self.sidebar, text="Меню", font=("Arial", 16, "bold"),
                bg="#34495E", fg="white").pack(pady=20)
        
        # Кнопки навигации в зависимости от роли
        buttons = []
        
        if self.current_user.role == UserRole.DISPATCHER:
            buttons = [
                ("📊 Мониторинг", self.show_monitoring_dashboard),
                ("⚠️ Аномалии", self.show_anomalies_view),
                ("💡 Рекомендации", self.show_recommendations_view),
                ("🔧 Управление", self.show_control_panel),
                ("📈 Графики", self.show_charts),
                ("🔔 Оповещения", self.show_alerts_view)
            ]
        elif self.current_user.role == UserRole.ANALYST:
            buttons = [
                ("📊 Мониторинг", self.show_monitoring_dashboard),
                ("📈 Аналитика", self.show_analytics_view),
                ("🔮 Прогнозы", self.show_forecasts_view),
                ("📋 Отчеты", self.show_reports_view),
                ("🔧 Моделирование", self.show_modeling_view)
            ]
        elif self.current_user.role == UserRole.ADMIN:
            buttons = [
                ("📊 Мониторинг", self.show_monitoring_dashboard),
                ("📋 Отчеты", self.show_reports_view),
                ("👥 Пользователи", self.show_users_view),
                ("⚙️ Настройки", self.show_settings_view),
                ("📊 Эффективность", self.show_efficiency_view)
            ]
        
        for text, command in buttons:
            btn = tk.Button(self.sidebar, text=text, command=command,
                           bg="#2C3E50", fg="white", font=("Arial", 11),
                           relief=tk.FLAT, width=20, anchor="w")
            btn.pack(pady=5, padx=10)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#1ABC9C"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#2C3E50"))
    
    def clear_window(self):
        """Очистка окна"""
        for widget in self.winfo_children():
            widget.destroy()
    
    def clear_content_area(self):
        """Очистка области контента"""
        for widget in self.content_area.winfo_children():
            widget.destroy()
    
    # ============================================
    # VIEWS (Представления)
    # ============================================
    
    def show_monitoring_dashboard(self):
        """Панель мониторинга"""
        self.clear_content_area()
        
        # Заголовок
        header = tk.Frame(self.content_area, bg="#ECF0F1", height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="Панель мониторинга сети", 
                font=("Arial", 18, "bold"), bg="#ECF0F1").pack(pady=20)
        
        # Основной контент
        main_content = tk.Frame(self.content_area)
        main_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Левая колонка - статус сети
        left_column = tk.Frame(main_content)
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        status_frame = tk.LabelFrame(left_column, text="Статус сети", 
                                    font=("Arial", 12, "bold"), padx=10, pady=10)
        status_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        status = self.monitor_controller.get_network_status()
        
        tk.Label(status_frame, text=f"Всего объектов: {status['total_objects']}", 
                font=("Arial", 11)).pack(anchor="w", pady=5)
        tk.Label(status_frame, text=f"Работоспособно: {status['operational']}", 
                font=("Arial", 11), fg="green").pack(anchor="w", pady=5)
        tk.Label(status_frame, text=f"На обслуживании: {status['maintenance']}", 
                font=("Arial", 11), fg="orange").pack(anchor="w", pady=5)
        tk.Label(status_frame, text=f"Аварии: {status['failures']}", 
                font=("Arial", 11), fg="red").pack(anchor="w", pady=5)
        
        health_color = "green" if status['health_percentage'] > 80 else \
                      "orange" if status['health_percentage'] > 60 else "red"
        tk.Label(status_frame, text=f"Здоровье сети: {status['health_percentage']:.1f}%", 
                font=("Arial", 11, "bold"), fg=health_color).pack(anchor="w", pady=5)
        
        # Кнопки управления мониторингом
        control_frame = tk.Frame(status_frame)
        control_frame.pack(pady=10)
        
        start_btn = tk.Button(control_frame, text="▶️ Запустить мониторинг",
                             command=self.start_monitoring,
                             bg="#27AE60", fg="white", font=("Arial", 10))
        start_btn.pack(side=tk.LEFT, padx=5)
        
        stop_btn = tk.Button(control_frame, text="⏹️ Остановить мониторинг",
                            command=self.stop_monitoring,
                            bg="#E74C3C", fg="white", font=("Arial", 10))
        stop_btn.pack(side=tk.LEFT, padx=5)
        
        # Список объектов сети
        objects_frame = tk.LabelFrame(left_column, text="Объекты сети", 
                                     font=("Arial", 12, "bold"), padx=10, pady=10)
        objects_frame.pack(fill=tk.BOTH, expand=True)
        
        objects_list = tk.Listbox(objects_frame, font=("Arial", 10), height=10)
        objects_list.pack(fill=tk.BOTH, expand=True)
        
        for obj in self.repository.get_all_network_objects():
            status_color = "green" if obj.status == "operational" else \
                          "orange" if obj.status == "maintenance" else "red"
            objects_list.insert(tk.END, f"{obj.name} - {obj.status}")
            objects_list.itemconfig(tk.END, fg=status_color)
        
        # Правая колонка - активные аномалии
        right_column = tk.Frame(main_content)
        right_column.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(20, 0))
        
        anomalies_frame = tk.LabelFrame(right_column, text="Активные аномалии", 
                                       font=("Arial", 12, "bold"), padx=10, pady=10)
        anomalies_frame.pack(fill=tk.BOTH, expand=True)
        
        anomalies = self.repository.get_active_anomalies()
        
        if not anomalies:
            tk.Label(anomalies_frame, text="Активных аномалий не обнаружено", 
                    font=("Arial", 11), fg="green").pack(pady=20)
        else:
            for anomaly in anomalies[:5]:  # Показываем максимум 5
                frame = tk.Frame(anomalies_frame, relief=tk.RAISED, borderwidth=1)
                frame.pack(fill=tk.X, pady=5, padx=5)
                
                severity_colors = {
                    SeverityLevel.CRITICAL: "red",
                    SeverityLevel.HIGH: "orange",
                    SeverityLevel.MEDIUM: "yellow",
                    SeverityLevel.LOW: "lightgreen"
                }
                
                tk.Label(frame, text=anomaly.anomaly_type.value, 
                        font=("Arial", 10, "bold"),
                        fg=severity_colors.get(anomaly.severity, "black")).pack(anchor="w")
                tk.Label(frame, text=anomaly.description, 
                        font=("Arial", 9), wraplength=300).pack(anchor="w")
                tk.Label(frame, text=f"Обнаружено: {anomaly.detection_time.strftime('%H:%M')}", 
                        font=("Arial", 8), fg="gray").pack(anchor="w")
        
        # Кнопка просмотра всех аномалий
        if anomalies:
            tk.Button(anomalies_frame, text="Показать все аномалии →",
                     command=self.show_anomalies_view,
                     font=("Arial", 10)).pack(pady=10)
    
    def show_anomalies_view(self):
        """Просмотр аномалий"""
        self.clear_content_area()
        
        header = tk.Frame(self.content_area, bg="#ECF0F1", height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="Управление аномалиями", 
                font=("Arial", 18, "bold"), bg="#ECF0F1").pack(pady=20)
        
        # Панель управления
        control_panel = tk.Frame(self.content_area, padx=20, pady=10)
        control_panel.pack(fill=tk.X)
        
        tk.Button(control_panel, text="Обновить список", 
                 command=lambda: self.show_anomalies_view(),
                 font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        
        tk.Button(control_panel, text="Сгенерировать тестовую аномалию", 
                 command=self.generate_test_anomaly,
                 font=("Arial", 10), bg="#3498DB", fg="white").pack(side=tk.LEFT, padx=5)
        
        # Таблица аномалий
        main_frame = tk.Frame(self.content_area)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Создаем Treeview для отображения таблицы
        columns = ("ID", "Время", "Тип", "Критичность", "Статус", "Объект", "Описание")
        tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120 if col != "Описание" else 300)
        
        # Заполняем данными
        anomalies = self.repository.anomalies
        for anomaly in sorted(anomalies, key=lambda x: x.detection_time, reverse=True):
            tree.insert("", tk.END, values=(
                anomaly.anomaly_id[:8],
                anomaly.detection_time.strftime("%Y-%m-%d %H:%M"),
                anomaly.anomaly_type.value,
                anomaly.severity.value,
                anomaly.status,
                anomaly.affected_object_id,
                anomaly.description[:50] + "..." if len(anomaly.description) > 50 else anomaly.description
            ))
        
        # Полоса прокрутки
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Панель действий
        action_frame = tk.Frame(self.content_area, pady=10)
        action_frame.pack(fill=tk.X)
        
        tree.bind("<<TreeviewSelect>>", lambda e: self.on_anomaly_select(tree))
        
        tk.Button(action_frame, text="Создать рекомендацию", 
                 command=lambda: self.create_recommendation_for_selected(tree),
                 font=("Arial", 10), bg="#2ECC71", fg="white").pack(side=tk.LEFT, padx=5)
        
        tk.Button(action_frame, text="Отметить как решенную", 
                 command=lambda: self.resolve_anomaly(tree),
                 font=("Arial", 10), bg="#9B59B6", fg="white").pack(side=tk.LEFT, padx=5)
    
    def on_anomaly_select(self, tree):
        """Обработка выбора аномалии"""
        selection = tree.selection()
        if selection:
            item = tree.item(selection[0])
            print(f"Выбрана аномалия: {item['values']}")
    
    def create_recommendation_for_selected(self, tree):
        """Создание рекомендации для выбранной аномалии"""
        selection = tree.selection()
        if selection:
            item = tree.item(selection[0])
            anomaly_id = item['values'][0]
            
            # Находим полный ID аномалии
            for anomaly in self.repository.anomalies:
                if anomaly.anomaly_id.startswith(anomaly_id):
                    recommendation = self.recommendation_controller.generate_recommendation(anomaly)
                    messagebox.showinfo("Рекомендация создана", 
                                      f"Создана рекомендация: {recommendation.content}")
                    self.show_recommendations_view()
                    break
    
    def resolve_anomaly(self, tree):
        """Пометить аномалию как решенную"""
        selection = tree.selection()
        if selection:
            item = tree.item(selection[0])
            anomaly_id = item['values'][0]
            
            for anomaly in self.repository.anomalies:
                if anomaly.anomaly_id.startswith(anomaly_id):
                    anomaly.status = "resolved"
                    messagebox.showinfo("Аномалия решена", 
                                      f"Аномалия отмечена как решенная")
                    self.show_anomalies_view()
                    break
    
    def show_recommendations_view(self):
        """Просмотр рекомендаций"""
        self.clear_content_area()
        
        header = tk.Frame(self.content_area, bg="#ECF0F1", height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="Рекомендации системы", 
                font=("Arial", 18, "bold"), bg="#ECF0F1").pack(pady=20)
        
        recommendations = self.repository.get_pending_recommendations()
        
        if not recommendations:
            tk.Label(self.content_area, text="Нет ожидающих рекомендаций", 
                    font=("Arial", 14), pady=50).pack()
            return
        
        # Создаем фреймы для каждой рекомендации
        main_frame = tk.Frame(self.content_area)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        canvas = tk.Canvas(main_frame)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for i, rec in enumerate(recommendations):
            frame = tk.Frame(scrollable_frame, relief=tk.RAISED, borderwidth=2, 
                           padx=10, pady=10, bg="#F8F9F9")
            frame.pack(fill=tk.X, pady=5, padx=5)
            
            priority_colors = {5: "#E74C3C", 4: "#E67E22", 3: "#F1C40F", 
                              2: "#2ECC71", 1: "#3498DB"}
            
            # Заголовок
            title_frame = tk.Frame(frame, bg="#F8F9F9")
            title_frame.pack(fill=tk.X)
            
            tk.Label(title_frame, text=f"Рекомендация #{i+1}", 
                    font=("Arial", 12, "bold"), bg="#F8F9F9").pack(side=tk.LEFT)
            
            tk.Label(title_frame, text=f"Приоритет: {rec.priority}", 
                    font=("Arial", 11, "bold"), 
                    fg=priority_colors.get(rec.priority, "black"),
                    bg="#F8F9F9").pack(side=tk.RIGHT, padx=10)
            
            # Содержимое
            tk.Label(frame, text=rec.content, font=("Arial", 11), 
                    bg="#F8F9F9", wraplength=800, justify="left").pack(anchor="w", pady=5)
            
            # Метаданные
            meta_frame = tk.Frame(frame, bg="#F8F9F9")
            meta_frame.pack(fill=tk.X, pady=5)
            
            tk.Label(meta_frame, text=f"Создана: {rec.creation_time.strftime('%Y-%m-%d %H:%M')}", 
                    font=("Arial", 9), fg="gray", bg="#F8F9F9").pack(side=tk.LEFT)
            
            tk.Label(meta_frame, text=f"Тип действия: {rec.action_type}", 
                    font=("Arial", 9), fg="gray", bg="#F8F9F9").pack(side=tk.LEFT, padx=20)
            
            # Кнопки действий
            action_frame = tk.Frame(frame, bg="#F8F9F9")
            action_frame.pack(fill=tk.X, pady=(10, 0))
            
            if rec.status == "pending":
                approve_btn = tk.Button(action_frame, text="✅ Одобрить",
                                       command=lambda r=rec: self.approve_recommendation(r),
                                       font=("Arial", 10), bg="#2ECC71", fg="white")
                approve_btn.pack(side=tk.LEFT, padx=5)
                
                reject_btn = tk.Button(action_frame, text="❌ Отклонить",
                                      command=lambda r=rec: self.reject_recommendation(r),
                                      font=("Arial", 10), bg="#E74C3C", fg="white")
                reject_btn.pack(side=tk.LEFT, padx=5)
            
            elif rec.status == "approved":
                tk.Label(action_frame, text="✅ Одобрена", 
                        font=("Arial", 10, "bold"), fg="green", bg="#F8F9F9").pack(side=tk.LEFT)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def approve_recommendation(self, recommendation: Recommendation):
        """Одобрить рекомендацию"""
        if self.recommendation_controller.approve_recommendation(
            recommendation.recommendation_id, self.current_user.user_id):
            messagebox.showinfo("Рекомендация одобрена", 
                              "Рекомендация была успешно одобрена.")
            self.show_recommendations_view()
    
    def reject_recommendation(self, recommendation: Recommendation):
        """Отклонить рекомендацию"""
        recommendation.status = "rejected"
        messagebox.showinfo("Рекомендация отклонена", 
                          "Рекомендация была отклонена.")
        self.show_recommendations_view()
    
    def show_control_panel(self):
        """Панель управления для диспетчера"""
        self.clear_content_area()
        
        header = tk.Frame(self.content_area, bg="#ECF0F1", height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="Панель управления оборудованием", 
                font=("Arial", 18, "bold"), bg="#ECF0F1").pack(pady=20)
        
        main_frame = tk.Frame(self.content_area)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Левая колонка - переключение фидеров
        left_col = tk.Frame(main_frame)
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tk.Label(left_col, text="Управление фидерами", 
                font=("Arial", 14, "bold")).pack(pady=(0, 10))
        
        for obj in self.repository.get_all_network_objects():
            if obj.object_type == NetworkObjectType.FEEDER:
                frame = tk.Frame(left_col, relief=tk.RAISED, borderwidth=1, padx=10, pady=10)
                frame.pack(fill=tk.X, pady=5)
                
                tk.Label(frame, text=obj.name, font=("Arial", 11, "bold")).pack(anchor="w")
                
                status_frame = tk.Frame(frame)
                status_frame.pack(anchor="w", pady=5)
                
                tk.Label(status_frame, text=f"Статус: {obj.status}", 
                        font=("Arial", 10)).pack(side=tk.LEFT)
                
                load_label = tk.Label(status_frame, 
                                     text=f"Нагрузка: {obj.current_load:.1f}/{obj.capacity:.1f} кВт",
                                     font=("Arial", 10))
                load_label.pack(side=tk.LEFT, padx=20)
                
                # Индикатор нагрузки
                load_percent = (obj.current_load / obj.capacity * 100) if obj.capacity > 0 else 0
                load_color = "green" if load_percent < 70 else \
                            "orange" if load_percent < 90 else "red"
                tk.Label(status_frame, text=f"({load_percent:.0f}%)", 
                        font=("Arial", 10, "bold"), fg=load_color).pack(side=tk.LEFT)
                
                # Кнопки управления
                btn_frame = tk.Frame(frame)
                btn_frame.pack(anchor="w", pady=5)
                
                if obj.status == "operational":
                    tk.Button(btn_frame, text="Отключить", 
                             command=lambda o=obj: self.toggle_feeder(o, "maintenance"),
                             bg="#E74C3C", fg="white").pack(side=tk.LEFT, padx=2)
                else:
                    tk.Button(btn_frame, text="Включить", 
                             command=lambda o=obj: self.toggle_feeder(o, "operational"),
                             bg="#2ECC71", fg="white").pack(side=tk.LEFT, padx=2)
                
                tk.Button(btn_frame, text="Аварийное откл.", 
                         command=lambda o=obj: self.toggle_feeder(o, "failure"),
                         bg="#8E44AD", fg="white").pack(side=tk.LEFT, padx=2)
        
        # Правая колонка - быстрые команды
        right_col = tk.Frame(main_frame)
        right_col.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(20, 0))
        
        tk.Label(right_col, text="Быстрые команды", 
                font=("Arial", 14, "bold")).pack(pady=(0, 10))
        
        commands = [
            ("⚡ Аварийное снижение нагрузки", self.emergency_load_reduction),
            ("🔁 Переключить на резерв", self.switch_to_backup),
            ("📊 Обновить данные всех датчиков", self.update_all_sensors),
            ("🚨 Отправить оповещение бригаде", self.send_crew_alert),
            ("📈 Сгенерировать отчет по нагрузкам", self.generate_load_report)
        ]
        
        for text, command in commands:
            btn = tk.Button(right_col, text=text, command=command,
                           font=("Arial", 11), height=2, width=30,
                           bg="#3498DB", fg="white")
            btn.pack(pady=5)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#2980B9"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#3498DB"))
    
    def toggle_feeder(self, feeder: Feeder, new_status: str):
        """Переключение статуса фидера"""
        command = SwitchFeederCommand(self.repository, feeder.object_id, 
                                     new_status, self.current_user.user_id)
        if command.execute():
            messagebox.showinfo("Команда выполнена", 
                              f"Статус {feeder.name} изменен на '{new_status}'")
            self.show_control_panel()
    
    def emergency_load_reduction(self):
        """Аварийное снижение нагрузки"""
        for obj in self.repository.get_all_network_objects():
            if hasattr(obj, 'current_load') and obj.current_load > obj.capacity * 0.8:
                obj.current_load *= 0.7  # Снижаем нагрузку на 30%
        
        self.alert_service.send_alert(
            "Выполнено аварийное снижение нагрузки",
            SeverityLevel.HIGH,
            "all_dispatchers"
        )
        messagebox.showinfo("Выполнено", "Аварийное снижение нагрузки выполнено")
        self.show_control_panel()
    
    def switch_to_backup(self):
        """Переключение на резервное питание"""
        messagebox.showinfo("Выполнено", "Переключение на резервные линии выполнено")
        self.alert_service.send_alert(
            "Активировано резервное питание",
            SeverityLevel.MEDIUM,
            "maintenance_team"
        )
    
    def update_all_sensors(self):
        """Обновление данных всех датчиков"""
        # Генерируем тестовые данные
        self.generate_sensor_data()
        messagebox.showinfo("Обновлено", "Данные датчиков обновлены")
    
    def send_crew_alert(self):
        """Отправка оповещения ремонтной бригаде"""
        self.alert_service.send_alert(
            "Требуется выезд ремонтной бригады",
            SeverityLevel.HIGH,
            "repair_crew"
        )
        messagebox.showinfo("Оповещение отправлено", 
                          "Ремонтная бригада оповещена")
    
    def generate_load_report(self):
        """Генерация отчета по нагрузкам"""
        report = self.report_controller.generate_report(
            "daily",
            datetime.datetime.now() - datetime.timedelta(days=1),
            datetime.datetime.now(),
            self.current_user.username
        )
        messagebox.showinfo("Отчет создан", 
                          f"Создан отчет: {report.title}")
    
    def show_charts(self):
        """Графики и визуализация"""
        self.clear_content_area()
        
        header = tk.Frame(self.content_area, bg="#ECF0F1", height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="Визуализация данных", 
                font=("Arial", 18, "bold"), bg="#ECF0F1").pack(pady=20)
        
        main_frame = tk.Frame(self.content_area)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Создаем график нагрузки
        fig = Figure(figsize=(10, 6), dpi=100)
        ax = fig.add_subplot(111)
        
        # Генерируем тестовые данные
        hours = list(range(24))
        loads = [random.uniform(500, 900) for _ in hours]
        
        ax.plot(hours, loads, 'b-', linewidth=2, marker='o')
        ax.fill_between(hours, loads, alpha=0.3)
        ax.set_xlabel('Часы суток', fontsize=12)
        ax.set_ylabel('Нагрузка (кВт)', fontsize=12)
        ax.set_title('Суточный профиль нагрузки сети', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # Добавляем пороговые значения
        ax.axhline(y=800, color='r', linestyle='--', alpha=0.7, label='Критический уровень')
        ax.axhline(y=700, color='y', linestyle='--', alpha=0.7, label='Предупреждение')
        
        ax.legend()
        ax.set_xticks(range(0, 24, 2))
        
        # Встраиваем график в Tkinter
        canvas = FigureCanvasTkAgg(fig, master=main_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Добавляем панель инструментов
        toolbar = NavigationToolbar2Tk(canvas, main_frame)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Нижняя панель с дополнительной информацией
        info_frame = tk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(info_frame, text=f"Максимальная нагрузка: {max(loads):.1f} кВт",
                font=("Arial", 11)).pack(side=tk.LEFT, padx=20)
        tk.Label(info_frame, text=f"Средняя нагрузка: {sum(loads)/len(loads):.1f} кВт",
                font=("Arial", 11)).pack(side=tk.LEFT, padx=20)
        tk.Label(info_frame, text=f"Время пика: {loads.index(max(loads)):02d}:00",
                font=("Arial", 11)).pack(side=tk.LEFT, padx=20)
    
    def show_alerts_view(self):
        """Просмотр оповещений"""
        self.clear_content_area()
        
        header = tk.Frame(self.content_area, bg="#ECF0F1", height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="Оповещения системы", 
                font=("Arial", 18, "bold"), bg="#ECF0F1").pack(pady=20)
        
        alerts = self.alert_service.alerts
        
        if not alerts:
            tk.Label(self.content_area, text="Нет непрочитанных оповещений", 
                    font=("Arial", 14), pady=50).pack()
            return
        
        main_frame = tk.Frame(self.content_area)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        for alert in sorted(alerts, key=lambda x: x['time'], reverse=True):
            frame = tk.Frame(main_frame, relief=tk.RAISED, borderwidth=1, 
                           padx=10, pady=10)
            frame.pack(fill=tk.X, pady=5)
            
            severity_colors = {
                "Критический": "#E74C3C",
                "Высокий": "#E67E22",
                "Средний": "#F1C40F",
                "Низкий": "#2ECC71"
            }
            
            tk.Label(frame, text=alert['message'], 
                    font=("Arial", 11), wraplength=800, justify="left").pack(anchor="w")
            
            meta_frame = tk.Frame(frame)
            meta_frame.pack(fill=tk.X, pady=5)
            
            tk.Label(meta_frame, 
                    text=alert['time'].strftime("%Y-%m-%d %H:%M:%S"),
                    font=("Arial", 9), fg="gray").pack(side=tk.LEFT)
            
            tk.Label(meta_frame, text=f"Важность: {alert['severity']}", 
                    font=("Arial", 9), 
                    fg=severity_colors.get(alert['severity'], "black")).pack(side=tk.LEFT, padx=20)
            
            tk.Label(meta_frame, text=f"Получатель: {alert['recipient']}", 
                    font=("Arial", 9), fg="gray").pack(side=tk.LEFT, padx=20)
            
            if not alert['read']:
                tk.Button(frame, text="Отметить как прочитанное",
                         command=lambda a=alert: self.mark_alert_read(a),
                         font=("Arial", 9)).pack(anchor="e")
    
    def mark_alert_read(self, alert):
        """Пометить оповещение как прочитанное"""
        alert['read'] = True
        self.show_alerts_view()
    
    def show_analytics_view(self):
        """Представление аналитики для инженера-аналитика"""
        self.clear_content_area()
        
        header = tk.Frame(self.content_area, bg="#ECF0F1", height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="Аналитика сети", 
                font=("Arial", 18, "bold"), bg="#ECF0F1").pack(pady=20)
        
        main_frame = tk.Frame(self.content_area)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Создаем несколько графиков
        fig = Figure(figsize=(12, 8), dpi=100)
        
        # График 1: Распределение типов аномалий
        ax1 = fig.add_subplot(221)
        anomaly_types = [a.anomaly_type.value for a in self.repository.anomalies]
        if anomaly_types:
            from collections import Counter
            counts = Counter(anomaly_types)
            ax1.pie(counts.values(), labels=counts.keys(), autopct='%1.1f%%')
            ax1.set_title('Распределение типов аномалий')
        
        # График 2: Тенденция нагрузок
        ax2 = fig.add_subplot(222)
        days = list(range(7))
        avg_loads = [random.uniform(600, 800) for _ in days]
        ax2.plot(days, avg_loads, 'g-', linewidth=2)
        ax2.set_xlabel('Дни')
        ax2.set_ylabel('Средняя нагрузка (кВт)')
        ax2.set_title('Тенденция нагрузок за неделю')
        ax2.grid(True, alpha=0.3)
        
        # График 3: Эффективность решения аномалий
        ax3 = fig.add_subplot(223)
        anomalies = self.repository.anomalies
        resolved = sum(1 for a in anomalies if a.status == "resolved")
        pending = sum(1 for a in anomalies if a.status in ["detected", "analyzing"])
        ax3.bar(['Решено', 'Ожидают'], [resolved, pending], color=['green', 'orange'])
        ax3.set_title('Эффективность решения аномалий')
        
        # График 4: Нагрузка по времени суток
        ax4 = fig.add_subplot(224)
        hours = list(range(24))
        typical_load = [300 + 400 * (0.5 + 0.5 * abs(12 - h) / 12) for h in hours]
        ax4.plot(hours, typical_load, 'purple', linewidth=2)
        ax4.fill_between(hours, typical_load, alpha=0.3, color='purple')
        ax4.set_xlabel('Час дня')
        ax4.set_ylabel('Типичная нагрузка (кВт)')
        ax4.set_title('Типичный суточный профиль')
        ax4.grid(True, alpha=0.3)
        
        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=main_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Панель инструментов
        toolbar = NavigationToolbar2Tk(canvas, main_frame)
        toolbar.update()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def show_forecasts_view(self):
        """Просмотр прогнозов"""
        self.clear_content_area()
        
        header = tk.Frame(self.content_area, bg="#ECF0F1", height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="Прогнозирование нагрузок", 
                font=("Arial", 18, "bold"), bg="#ECF0F1").pack(pady=20)
        
        main_frame = tk.Frame(self.content_area)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Создаем прогнозы для всех объектов
        forecasts = []
        for obj in self.repository.get_all_network_objects():
            forecast = self.forecast_controller.create_load_forecast(obj.object_id)
            forecasts.append((obj, forecast))
        
        for obj, forecast in forecasts:
            frame = tk.Frame(main_frame, relief=tk.GROOVE, borderwidth=2, 
                           padx=15, pady=15)
            frame.pack(fill=tk.X, pady=10)
            
            tk.Label(frame, text=obj.name, 
                    font=("Arial", 12, "bold")).pack(anchor="w")
            
            info_frame = tk.Frame(frame)
            info_frame.pack(fill=tk.X, pady=5)
            
            tk.Label(info_frame, text=f"Текущая нагрузка: {obj.current_load:.1f} кВт",
                    font=("Arial", 10)).pack(side=tk.LEFT, padx=10)
            
            tk.Label(info_frame, text=f"Прогноз: {forecast.predicted_load:.1f} кВт",
                    font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=10)
            
            confidence_color = "green" if forecast.confidence > 0.8 else \
                              "orange" if forecast.confidence > 0.6 else "red"
            tk.Label(info_frame, text=f"Доверие: {forecast.confidence:.0%}",
                    font=("Arial", 10), fg=confidence_color).pack(side=tk.LEFT, padx=10)
            
            # Индикатор сравнения
            diff = forecast.predicted_load - obj.current_load
            diff_percent = (diff / obj.current_load * 100) if obj.current_load > 0 else 0
            
            diff_frame = tk.Frame(frame)
            diff_frame.pack(fill=tk.X, pady=5)
            
            if diff > 0:
                tk.Label(diff_frame, text=f"↑ Рост на {diff_percent:.1f}%",
                        font=("Arial", 10), fg="red").pack(side=tk.LEFT)
            elif diff < 0:
                tk.Label(diff_frame, text=f"↓ Снижение на {abs(diff_percent):.1f}%",
                        font=("Arial", 10), fg="green").pack(side=tk.LEFT)
            else:
                tk.Label(diff_frame, text="→ Без изменений",
                        font=("Arial", 10), fg="gray").pack(side=tk.LEFT)
    
    def show_reports_view(self):
        """Просмотр отчетов"""
        self.clear_content_area()
        
        header = tk.Frame(self.content_area, bg="#ECF0F1", height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="Отчеты системы", 
                font=("Arial", 18, "bold"), bg="#ECF0F1").pack(pady=20)
        
        # Панель создания отчетов
        create_frame = tk.LabelFrame(self.content_area, text="Создать новый отчет",
                                    padx=20, pady=20, font=("Arial", 12, "bold"))
        create_frame.pack(fill=tk.X, padx=20, pady=(10, 20))
        
        tk.Label(create_frame, text="Тип отчета:", 
                font=("Arial", 11)).pack(side=tk.LEFT, padx=5)
        
        report_type_var = tk.StringVar(value="daily")
        report_types = [("Ежедневный", "daily"), ("Еженедельный", "weekly"), 
                       ("Ежемесячный", "monthly"), ("По инциденту", "incident")]
        
        for text, value in report_types:
            tk.Radiobutton(create_frame, text=text, variable=report_type_var,
                          value=value, font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        
        tk.Button(create_frame, text="Создать отчет", 
                 command=lambda: self.create_report(report_type_var.get()),
                 font=("Arial", 11), bg="#3498DB", fg="white").pack(side=tk.RIGHT, padx=10)
        
        # Существующие отчеты
        main_frame = tk.Frame(self.content_area)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        if not self.repository.reports:
            tk.Label(main_frame, text="Отчеты еще не созданы", 
                    font=("Arial", 14), pady=50).pack()
            return
        
        # Создаем Treeview для отчетов
        columns = ("ID", "Название", "Тип", "Дата создания", "Автор")
        tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120 if col != "Название" else 200)
        
        for report in sorted(self.repository.reports, 
                           key=lambda x: x.creation_date, reverse=True):
            tree.insert("", tk.END, values=(
                report.report_id[:8],
                report.title,
                report.report_type,
                report.creation_date.strftime("%Y-%m-%d %H:%M"),
                report.created_by
            ))
        
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Кнопка просмотра отчета
        tk.Button(main_frame, text="Просмотреть выбранный отчет", 
                 command=lambda: self.view_selected_report(tree),
                 font=("Arial", 11), bg="#2ECC71", fg="white").pack(pady=10)
    
    def create_report(self, report_type: str):
        """Создание нового отчета"""
        if report_type == "daily":
            start_date = datetime.datetime.now() - datetime.timedelta(days=1)
        elif report_type == "weekly":
            start_date = datetime.datetime.now() - datetime.timedelta(days=7)
        elif report_type == "monthly":
            start_date = datetime.datetime.now() - datetime.timedelta(days=30)
        else:  # incident
            start_date = datetime.datetime.now() - datetime.timedelta(days=1)
        
        report = self.report_controller.generate_report(
            report_type,
            start_date,
            datetime.datetime.now(),
            self.current_user.username
        )
        
        messagebox.showinfo("Отчет создан", 
                          f"Создан отчет: {report.title}\n\n{report.content}")
        self.show_reports_view()
    
    def view_selected_report(self, tree):
        """Просмотр выбранного отчета"""
        selection = tree.selection()
        if selection:
            item = tree.item(selection[0])
            report_id = item['values'][0]
            
            for report in self.repository.reports:
                if report.report_id.startswith(report_id):
                    # Создаем отдельное окно для просмотра отчета
                    report_window = tk.Toplevel(self)
                    report_window.title(f"Отчет: {report.title}")
                    report_window.geometry("800x600")
                    
                    text_widget = tk.Text(report_window, wrap="word", font=("Arial", 11))
                    text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
                    
                    text_widget.insert("1.0", f"{report.title}\n")
                    text_widget.insert("2.0", "=" * 50 + "\n\n")
                    text_widget.insert("3.0", report.content)
                    text_widget.insert("end", f"\n\nСоздан: {report.creation_date.strftime('%Y-%m-%d %H:%M:%S')}")
                    text_widget.insert("end", f"\nАвтор: {report.created_by}")
                    
                    text_widget.config(state="disabled")
                    
                    tk.Button(report_window, text="Закрыть", 
                             command=report_window.destroy,
                             font=("Arial", 11)).pack(pady=10)
                    break
    
    def show_modeling_view(self):
        """Моделирование для инженера-аналитика"""
        self.clear_content_area()
        
        header = tk.Frame(self.content_area, bg="#ECF0F1", height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="Моделирование развития сети", 
                font=("Arial", 18, "bold"), bg="#ECF0F1").pack(pady=20)
        
        main_frame = tk.Frame(self.content_area)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Левая панель - параметры моделирования
        left_panel = tk.Frame(main_frame)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tk.Label(left_panel, text="Параметры нового объекта", 
                font=("Arial", 14, "bold")).pack(pady=(0, 10))
        
        # Форма ввода параметров
        form_frame = tk.Frame(left_panel)
        form_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(form_frame, text="Тип объекта:", width=15, 
                font=("Arial", 11)).grid(row=0, column=0, sticky="w", pady=5)
        
        obj_type_var = tk.StringVar(value="consumer")
        obj_types = [("Потребитель", "consumer"), ("Генератор", "generator"),
                    ("Подстанция", "substation"), ("Фидер", "feeder")]
        
        for i, (text, value) in enumerate(obj_types):
            tk.Radiobutton(form_frame, text=text, variable=obj_type_var,
                          value=value, font=("Arial", 10)).grid(row=0, column=i+1, padx=5)
        
        tk.Label(form_frame, text="Мощность (кВт):", width=15, 
                font=("Arial", 11)).grid(row=1, column=0, sticky="w", pady=5)
        power_entry = tk.Entry(form_frame, font=("Arial", 11))
        power_entry.grid(row=1, column=1, columnspan=3, sticky="ew", pady=5)
        power_entry.insert(0, "1000")
        
        tk.Label(form_frame, text="Местоположение:", width=15, 
                font=("Arial", 11)).grid(row=2, column=0, sticky="w", pady=5)
        location_entry = tk.Entry(form_frame, font=("Arial", 11))
        location_entry.grid(row=2, column=1, columnspan=3, sticky="ew", pady=5)
        location_entry.insert(0, "55.75, 37.62")
        
        tk.Label(form_frame, text="Ожидаемая нагрузка:", width=15, 
                font=("Arial", 11)).grid(row=3, column=0, sticky="w", pady=5)
        load_entry = tk.Entry(form_frame, font=("Arial", 11))
        load_entry.grid(row=3, column=1, columnspan=3, sticky="ew", pady=5)
        load_entry.insert(0, "500")
        
        # Кнопки моделирования
        button_frame = tk.Frame(left_panel)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Смоделировать объект", 
                 command=lambda: self.simulate_object(obj_type_var.get(), 
                                                     power_entry.get(),
                                                     location_entry.get(),
                                                     load_entry.get()),
                 font=("Arial", 11), bg="#3498DB", fg="white",
                 width=20).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Рассчитать узкие места", 
                 command=self.calculate_bottlenecks,
                 font=("Arial", 11), bg="#9B59B6", fg="white",
                 width=20).pack(side=tk.LEFT, padx=5)
        
        # Правая панель - результаты моделирования
        right_panel = tk.Frame(main_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(20, 0))
        
        tk.Label(right_panel, text="Результаты моделирования", 
                font=("Arial", 14, "bold")).pack(pady=(0, 10))
        
        self.modeling_results = tk.Text(right_panel, height=15, width=50,
                                       font=("Arial", 10))
        self.modeling_results.pack(fill=tk.BOTH, expand=True)
        self.modeling_results.insert("1.0", "Результаты моделирования будут отображаться здесь.\n\n")
        self.modeling_results.config(state="disabled")
    
    def simulate_object(self, obj_type: str, power: str, location: str, load: str):
        """Моделирование нового объекта"""
        try:
            power_val = float(power)
            load_val = float(load)
            
            results = f"""Результаты моделирования нового объекта:
            
Тип объекта: {obj_type}
Мощность: {power_val} кВт
Местоположение: {location}
Ожидаемая нагрузка: {load_val} кВт

Анализ влияния:
1. Требуемая дополнительная мощность: {load_val * 1.2:.1f} кВт
2. Влияние на существующие объекты: умеренное
3. Рекомендуемые меры:
   - Усиление ближайшей подстанции на {load_val * 0.3:.1f} кВт
   - Прокладка резервной линии питания
   - Установка стабилизаторов напряжения

Вероятные проблемы:
- Временное падение напряжения при подключении
- Необходимость обновления защитной автоматики
"""
            
            self.modeling_results.config(state="normal")
            self.modeling_results.delete("1.0", tk.END)
            self.modeling_results.insert("1.0", results)
            self.modeling_results.config(state="disabled")
            
        except ValueError:
            messagebox.showerror("Ошибка", "Введите числовые значения для мощности и нагрузки")
    
    def calculate_bottlenecks(self):
        """Расчет узких мест в сети"""
        bottlenecks = []
        
        for obj in self.repository.get_all_network_objects():
            if hasattr(obj, 'current_load') and hasattr(obj, 'capacity'):
                if obj.capacity > 0:
                    utilization = obj.current_load / obj.capacity * 100
                    if utilization > 80:
                        bottlenecks.append(f"{obj.name}: {utilization:.1f}% загрузки")
        
        results = "Выявленные узкие места в сети:\n\n"
        if bottlenecks:
            for i, bottleneck in enumerate(bottlenecks, 1):
                results += f"{i}. {bottleneck}\n"
            
            results += f"\nВсего выявлено узких мест: {len(bottlenecks)}\n"
            results += "Рекомендуемые действия:\n"
            results += "1. Перераспределить нагрузки\n"
            results += "2. Рассмотреть возможность усиления оборудования\n"
            results += "3. Запланировать техническое обслуживание\n"
        else:
            results += "Узких мест не обнаружено. Сеть работает в нормальном режиме.\n"
        
        self.modeling_results.config(state="normal")
        self.modeling_results.delete("1.0", tk.END)
        self.modeling_results.insert("1.0", results)
        self.modeling_results.config(state="disabled")
    
    def show_users_view(self):
        """Управление пользователями (для администратора)"""
        self.clear_content_area()
        
        header = tk.Frame(self.content_area, bg="#ECF0F1", height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="Управление пользователями", 
                font=("Arial", 18, "bold"), bg="#ECF0F1").pack(pady=20)
        
        # Тестовые данные пользователей
        test_users = [
            User("disp_001", "Иванов А.И.", UserRole.DISPATCHER, "Оперативный отдел", "Дневная"),
            User("disp_002", "Петров С.М.", UserRole.DISPATCHER, "Оперативный отдел", "Ночная"),
            User("anal_001", "Сидорова Е.В.", UserRole.ANALYST, "Аналитический отдел"),
            User("anal_002", "Козлов Д.Н.", UserRole.ANALYST, "Аналитический отдел"),
            User("admin_001", "Васильев П.К.", UserRole.ADMIN, "Администрация"),
        ]
        
        main_frame = tk.Frame(self.content_area)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Создаем Treeview для пользователей
        columns = ("ID", "Имя", "Роль", "Отдел", "Смена", "Статус")
        tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        for user in test_users:
            tree.insert("", tk.END, values=(
                user.user_id,
                user.username,
                user.role.value,
                user.department or "",
                user.shift or "",
                "Активен"
            ))
        
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Панель управления пользователями
        control_frame = tk.Frame(self.content_area)
        control_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        tk.Button(control_frame, text="Добавить пользователя", 
                 command=self.add_user_dialog,
                 font=("Arial", 11), bg="#2ECC71", fg="white").pack(side=tk.LEFT, padx=5)
        
        tk.Button(control_frame, text="Изменить роль", 
                 font=("Arial", 11), bg="#3498DB", fg="white").pack(side=tk.LEFT, padx=5)
        
        tk.Button(control_frame, text="Деактивировать", 
                 font=("Arial", 11), bg="#E74C3C", fg="white").pack(side=tk.LEFT, padx=5)
    
    def add_user_dialog(self):
        """Диалог добавления пользователя"""
        dialog = tk.Toplevel(self)
        dialog.title("Добавить нового пользователя")
        dialog.geometry("400x300")
        
        tk.Label(dialog, text="Добавление пользователя", 
                font=("Arial", 14, "bold")).pack(pady=10)
        
        form_frame = tk.Frame(dialog, padx=20, pady=10)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        fields = [
            ("Имя пользователя:", "entry"),
            ("Роль:", "combobox"),
            ("Отдел:", "entry"),
            ("Смена:", "entry"),
            ("Email:", "entry")
        ]
        
        entries = {}
        for i, (label, field_type) in enumerate(fields):
            tk.Label(form_frame, text=label, font=("Arial", 11)).grid(row=i, column=0, sticky="w", pady=5)
            
            if field_type == "entry":
                entry = tk.Entry(form_frame, font=("Arial", 11))
                entry.grid(row=i, column=1, sticky="ew", pady=5, padx=10)
                entries[label] = entry
            elif field_type == "combobox":
                combo = ttk.Combobox(form_frame, values=[r.value for r in UserRole], 
                                    font=("Arial", 11), state="readonly")
                combo.grid(row=i, column=1, sticky="ew", pady=5, padx=10)
                combo.current(0)
                entries[label] = combo
        
        button_frame = tk.Frame(dialog)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Добавить", 
                 command=lambda: self.save_new_user(entries, dialog),
                 font=("Arial", 11), bg="#2ECC71", fg="white").pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Отмена", 
                 command=dialog.destroy,
                 font=("Arial", 11)).pack(side=tk.LEFT, padx=5)
    
    def save_new_user(self, entries, dialog):
        """Сохранение нового пользователя"""
        messagebox.showinfo("Пользователь добавлен", 
                          "Новый пользователь успешно добавлен (в демо-версии)")
        dialog.destroy()
    
    def show_settings_view(self):
        """Настройки системы"""
        self.clear_content_area()
        
        header = tk.Frame(self.content_area, bg="#ECF0F1", height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="Настройки системы", 
                font=("Arial", 18, "bold"), bg="#ECF0F1").pack(pady=20)
        
        main_frame = tk.Frame(self.content_area)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Настройки мониторинга
        monitor_frame = tk.LabelFrame(main_frame, text="Настройки мониторинга",
                                     font=("Arial", 12, "bold"), padx=20, pady=20)
        monitor_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(monitor_frame, text="Интервал обновления (сек):", 
                font=("Arial", 11)).pack(side=tk.LEFT, padx=5)
        
        interval_var = tk.StringVar(value="5")
        interval_spin = tk.Spinbox(monitor_frame, from_=1, to=60, textvariable=interval_var,
                                  font=("Arial", 11), width=10)
        interval_spin.pack(side=tk.LEFT, padx=5)
        
        tk.Checkbutton(monitor_frame, text="Автоматический мониторинг", 
                      font=("Arial", 11)).pack(side=tk.LEFT, padx=20)
        
        # Настройки оповещений
        alert_frame = tk.LabelFrame(main_frame, text="Настройки оповещений",
                                   font=("Arial", 12, "bold"), padx=20, pady=20)
        alert_frame.pack(fill=tk.X, pady=(0, 10))
        
        alert_settings = [
            ("Критические аномалии", True),
            ("Высокий приоритет", True),
            ("Средний приоритет", True),
            ("Низкий приоритет", False),
            ("Техническое обслуживание", True)
        ]
        
        for text, default in alert_settings:
            var = tk.BooleanVar(value=default)
            tk.Checkbutton(alert_frame, text=text, variable=var, 
                          font=("Arial", 11)).pack(anchor="w", pady=2)
        
        # Настройки интерфейса
        ui_frame = tk.LabelFrame(main_frame, text="Настройки интерфейса",
                                font=("Arial", 12, "bold"), padx=20, pady=20)
        ui_frame.pack(fill=tk.X)
        
        tk.Label(ui_frame, text="Тема интерфейса:", 
                font=("Arial", 11)).pack(side=tk.LEFT, padx=5)
        
        theme_var = tk.StringVar(value="Светлая")
        theme_combo = ttk.Combobox(ui_frame, textvariable=theme_var,
                                  values=["Светлая", "Темная", "Авто"],
                                  font=("Arial", 11), state="readonly", width=15)
        theme_combo.pack(side=tk.LEFT, padx=5)
        
        tk.Checkbutton(ui_frame, text="Показывать уведомления", 
                      font=("Arial", 11)).pack(side=tk.LEFT, padx=20)
        
        # Кнопки сохранения
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Сохранить настройки", 
                 command=lambda: messagebox.showinfo("Сохранено", "Настройки сохранены"),
                 font=("Arial", 11), bg="#3498DB", fg="white").pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Сбросить к умолчаниям", 
                 font=("Arial", 11)).pack(side=tk.LEFT, padx=5)
    
    def show_efficiency_view(self):
        """Анализ эффективности"""
        self.clear_content_area()
        
        header = tk.Frame(self.content_area, bg="#ECF0F1", height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="Анализ эффективности системы", 
                font=("Arial", 18, "bold"), bg="#ECF0F1").pack(pady=20)
        
        main_frame = tk.Frame(self.content_area)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Показатели эффективности
        metrics = [
            ("Надежность сети", "98.5%", "Выше целевого показателя (95%)"),
            ("Среднее время восстановления", "45 мин", "В пределах нормы"),
            ("Эффективность обнаружения аномалий", "92%", "Отличный показатель"),
            ("Время реакции на инциденты", "8 мин", "Быстрое реагирование"),
            ("Удовлетворенность пользователей", "4.7/5", "Высокий уровень"),
            ("Энергоэффективность", "15% экономии", "Превосходит цели")
        ]
        
        for i, (metric, value, status) in enumerate(metrics):
            frame = tk.Frame(main_frame, relief=tk.GROOVE, borderwidth=1, 
                           padx=20, pady=15)
            frame.pack(fill=tk.X, pady=5)
            
            tk.Label(frame, text=metric, font=("Arial", 12, "bold"), 
                    width=25, anchor="w").pack(side=tk.LEFT)
            
            tk.Label(frame, text=value, font=("Arial", 14, "bold"), 
                    fg="#2C3E50", width=15).pack(side=tk.LEFT, padx=20)
            
            status_color = "green" if "Выше" in status or "Отличный" in status or "Высокий" in status else \
                          "orange" if "В пределах" in status or "Быстрое" in status else "black"
            tk.Label(frame, text=status, font=("Arial", 11), 
                    fg=status_color).pack(side=tk.LEFT)
    
    # ============================================
    # DATA GENERATION (Генерация данных)
    # ============================================
    
    def start_monitoring(self):
        """Запуск мониторинга"""
        self.monitor_controller.start_monitoring()
        messagebox.showinfo("Мониторинг", "Мониторинг сети запущен")
    
    def stop_monitoring(self):
        """Остановка мониторинга"""
        self.monitor_controller.stop_monitoring()
        messagebox.showinfo("Мониторинг", "Мониторинг сети остановлен")
    
    def start_data_generation(self):
        """Запуск генерации тестовых данных"""
        self.data_generation_active = True
        self.generate_data_thread()
    
    def generate_data_thread(self):
        """Поток для генерации данных"""
        def generate():
            while self.data_generation_active:
                self.generate_sensor_data()
                time.sleep(5)  # Генерация данных каждые 5 секунд
                
                # Периодически генерируем аномалии
                if random.random() < 0.1:  # 10% шанс
                    self.generate_test_anomaly()
        
        thread = threading.Thread(target=generate, daemon=True)
        thread.start()
    
    def generate_sensor_data(self):
        """Генерация тестовых данных с датчиков"""
        for obj in self.repository.get_all_network_objects():
            # Генерируем различные типы данных в зависимости от объекта
            sensor_types = [
                ("power", SensorType.POWER, 100, 1000),
                ("voltage", SensorType.VOLTAGE, 210, 240),
                ("current", SensorType.CURRENT, 10, 100)
            ]
            
            for sensor_suffix, sensor_type, min_val, max_val in sensor_types:
                sensor_id = f"{obj.object_id}_{sensor_suffix}"
                
                # Добавляем случайные колебания
                base_value = obj.current_load if sensor_suffix == "power" else (min_val + max_val) / 2
                fluctuation = random.uniform(-0.1, 0.1) * base_value
                value = max(min_val, min(max_val, base_value + fluctuation))
                
                data = SensorData(
                    data_id=str(uuid.uuid4()),
                    sensor_id=sensor_id,
                    timestamp=datetime.datetime.now(),
                    value=value,
                    unit="кВт" if sensor_suffix == "power" else "В" if sensor_suffix == "voltage" else "А"
                )
                
                self.repository.store_sensor_data(data)
                
                # Обновляем текущую нагрузку объекта
                if sensor_suffix == "power" and hasattr(obj, 'current_load'):
                    obj.current_load = value
                
                # Проверяем на аномалии
                anomaly = self.monitor_controller.detect_anomalies(data, obj)
                if anomaly:
                    self.alert_service.send_alert(
                        f"Обнаружена аномалия: {anomaly.description}",
                        anomaly.severity,
                        self.current_user.user_id
                    )
    
    def generate_test_anomaly(self):
        """Генерация тестовой аномалии"""
        objects = self.repository.get_all_network_objects()
        if not objects:
            return
        
        obj = random.choice(objects)
        anomaly_types = list(AnomalyType)
        severity_levels = list(SeverityLevel)
        
        anomaly = Anomaly(
            anomaly_id=str(uuid.uuid4()),
            detection_time=datetime.datetime.now(),
            anomaly_type=random.choice(anomaly_types),
            severity=random.choice(severity_levels[1:]),  # Исключаем LOW
            description=f"Тестовая аномалия на объекте {obj.name}",
            status="detected",
            affected_object_id=obj.object_id,
            confidence_score=random.uniform(0.7, 0.95),
            recommended_action="Требуется анализ и принятие мер"
        )
        
        self.repository.store_anomaly(anomaly)
        
        # Отправляем оповещение
        self.alert_service.send_alert(
            f"Обнаружена {anomaly.severity.value.lower()} аномалия: {anomaly.description}",
            anomaly.severity,
            self.current_user.user_id
        )
        
        # Если открыт вид аномалий, обновляем его
        if hasattr(self, 'current_view_name') and self.current_view_name == "anomalies":
            self.show_anomalies_view()
        
        return anomaly