# CODE_SCAFFOLD_OPS-002: Observabilidade Básica (Logs + Uptime) - Backend Scaffolding

## 1. Estrutura do Projeto

```
ops-002/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   └── logging.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── log.py
│   │   ├── metric.py
│   │   ├── health.py
│   │   └── alert.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── logger_service.py
│   │   ├── metrics_service.py
│   │   ├── health_service.py
│   │   └── alert_service.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── health.py
│   │   ├── metrics.py
│   │   └── logs.py
│   ├── middleware/
│   │   ├── __init__.py
│   │   ├── logging_middleware.py
│   │   ├── metrics_middleware.py
│   │   └── correlation_middleware.py
│   └── utils/
│       ├── __init__.py
│       ├── decorators.py
│       ├── helpers.py
│       └── validators.py
├── tests/
│   ├── __init__.py
│   ├── test_logger.py
│   ├── test_metrics.py
│   ├── test_health.py
│   ├── test_alerts.py
│   └── test_integration.py
├── requirements.txt
├── pyproject.toml
├── Makefile
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

## 2. DTOs (Data Transfer Objects)

### **2.1 Log DTOs**

#### **LogEntry**
```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum

class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class LogEntry(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    level: LogLevel
    message: str
    service: str
    version: str
    environment: str
    request_id: Optional[str] = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    correlation_id: Optional[str] = None
    trace_id: Optional[str] = None
    span_id: Optional[str] = None
    duration: Optional[float] = None
    status_code: Optional[int] = None
    method: Optional[str] = None
    path: Optional[str] = None
    user_agent: Optional[str] = None
    ip_address: Optional[str] = None
    error_code: Optional[str] = None
    error_message: Optional[str] = None
    stack_trace: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
```

#### **LogQuery**
```python
class LogQuery(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    level: Optional[LogLevel] = None
    service: Optional[str] = None
    environment: Optional[str] = None
    request_id: Optional[str] = None
    user_id: Optional[str] = None
    correlation_id: Optional[str] = None
    message_contains: Optional[str] = None
    limit: int = Field(default=100, ge=1, le=1000)
    offset: int = Field(default=0, ge=0)
```

#### **LogResponse**
```python
class LogResponse(BaseModel):
    logs: List[LogEntry]
    total: int
    limit: int
    offset: int
    has_more: bool
```

### **2.2 Metric DTOs**

#### **MetricEntry**
```python
from enum import Enum

class MetricType(str, Enum):
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"

class MetricEntry(BaseModel):
    name: str
    type: MetricType
    value: float
    labels: Dict[str, str]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    service: str
    version: str
    environment: str
    instance: str
    method: Optional[str] = None
    endpoint: Optional[str] = None
    status_code: Optional[int] = None
    user_type: Optional[str] = None
    region: Optional[str] = None
    datacenter: Optional[str] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
```

#### **MetricQuery**
```python
class MetricQuery(BaseModel):
    name: Optional[str] = None
    type: Optional[MetricType] = None
    service: Optional[str] = None
    environment: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    labels: Optional[Dict[str, str]] = None
    aggregation: Optional[str] = None
    interval: Optional[str] = None
    limit: int = Field(default=100, ge=1, le=1000)
```

#### **MetricResponse**
```python
class MetricResponse(BaseModel):
    metrics: List[MetricEntry]
    total: int
    aggregation: Optional[str] = None
    interval: Optional[str] = None
    has_more: bool
```

### **2.3 Health Check DTOs**

#### **HealthCheck**
```python
class HealthStatus(str, Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    DEGRADED = "degraded"

class HealthCheck(BaseModel):
    name: str
    status: HealthStatus
    message: Optional[str] = None
    response_time: Optional[float] = None
    last_check: datetime = Field(default_factory=datetime.utcnow)
    error: Optional[str] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
```

#### **HealthResponse**
```python
class HealthResponse(BaseModel):
    status: HealthStatus
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: str
    uptime: float
    response_time: float
    checks: List[HealthCheck]
    service: str
    environment: str

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
```

### **2.4 Alert DTOs**

#### **Alert**
```python
class AlertSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AlertStatus(str, Enum):
    ACTIVE = "active"
    RESOLVED = "resolved"
    SUPPRESSED = "suppressed"

class Alert(BaseModel):
    id: str
    name: str
    description: str
    severity: AlertSeverity
    status: AlertStatus
    condition: str
    value: float
    threshold: float
    service: str
    environment: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    resolved_at: Optional[datetime] = None
    labels: Optional[Dict[str, str]] = None
    annotations: Optional[Dict[str, str]] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
```

#### **AlertQuery**
```python
class AlertQuery(BaseModel):
    status: Optional[AlertStatus] = None
    severity: Optional[AlertSeverity] = None
    service: Optional[str] = None
    environment: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    limit: int = Field(default=100, ge=1, le=1000)
    offset: int = Field(default=0, ge=0)
```

#### **AlertResponse**
```python
class AlertResponse(BaseModel):
    alerts: List[Alert]
    total: int
    limit: int
    offset: int
    has_more: bool
```

## 3. Requirements/PyProject

### **3.1 requirements.txt**
```txt
# Core dependencies
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0

# Database
sqlalchemy==2.0.23
alembic==1.13.1
psycopg2-binary==2.9.9

# Monitoring
prometheus-client==0.19.0
structlog==23.2.0
python-json-logger==2.0.7

# HTTP client
httpx==0.25.2
aiohttp==3.9.1

# Utilities
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
httpx==0.25.2

# Development
black==23.11.0
isort==5.12.0
flake8==6.1.0
mypy==1.7.1

# Production
gunicorn==21.2.0
```

### **3.2 pyproject.toml**
```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "concurso-ai-monitoring"
version = "0.1.0"
description = "Observabilidade básica para Concurso AI"
authors = [
    {name = "Concurso AI Team", email = "team@concurso-ai.com"}
]
readme = "README.md"
requires-python = ">=3.9"
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
]
dependencies = [
    "fastapi>=0.104.1",
    "uvicorn[standard]>=0.24.0",
    "pydantic>=2.5.0",
    "pydantic-settings>=2.1.0",
    "sqlalchemy>=2.0.23",
    "alembic>=1.13.1",
    "psycopg2-binary>=2.9.9",
    "prometheus-client>=0.19.0",
    "structlog>=23.2.0",
    "python-json-logger>=2.0.7",
    "httpx>=0.25.2",
    "aiohttp>=3.9.1",
    "python-multipart>=0.0.6",
    "python-jose[cryptography]>=3.3.0",
    "passlib[bcrypt]>=1.7.4",
    "python-dotenv>=1.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.3",
    "pytest-asyncio>=0.21.1",
    "pytest-cov>=4.1.0",
    "black>=23.11.0",
    "isort>=5.12.0",
    "flake8>=6.1.0",
    "mypy>=1.7.1",
]
prod = [
    "gunicorn>=21.2.0",
]

[project.urls]
Homepage = "https://github.com/g4trader/concurso-ai-orchestrated"
Repository = "https://github.com/g4trader/concurso-ai-orchestrated"
Documentation = "https://docs.concurso-ai.com"

[tool.setuptools.packages.find]
where = ["src"]

[tool.black]
line-length = 88
target-version = ['py39']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | build
  | dist
)/
'''

[tool.isort]
profile = "black"
multi_line_output = 3
line_length = 88
known_first_party = ["src"]

[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true
strict_equality = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--strict-markers",
    "--strict-config",
    "--cov=src",
    "--cov-report=term-missing",
    "--cov-report=html",
    "--cov-report=xml",
]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
    "unit: marks tests as unit tests",
]
```

## 4. Makefile

```makefile
.PHONY: help install install-dev test test-cov lint format clean run run-dev build deploy

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install production dependencies
	pip install -r requirements.txt

install-dev: ## Install development dependencies
	pip install -r requirements.txt
	pip install -e ".[dev]"

test: ## Run tests
	pytest

test-cov: ## Run tests with coverage
	pytest --cov=src --cov-report=html --cov-report=term-missing

lint: ## Run linting
	flake8 src tests
	mypy src

format: ## Format code
	black src tests
	isort src tests

clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/

run: ## Run the application
	uvicorn src.main:app --host 0.0.0.0 --port 8000

run-dev: ## Run the application in development mode
	uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

build: ## Build Docker image
	docker build -t concurso-ai-monitoring:latest .

deploy: ## Deploy to production
	docker-compose up -d

health-check: ## Check application health
	curl -f http://localhost:8000/health || exit 1

logs: ## View application logs
	docker-compose logs -f

setup-db: ## Setup database
	alembic upgrade head

migrate: ## Run database migrations
	alembic revision --autogenerate -m "$(message)"
	alembic upgrade head

monitor: ## Start monitoring services
	docker-compose -f docker-compose.monitoring.yml up -d

stop-monitor: ## Stop monitoring services
	docker-compose -f docker-compose.monitoring.yml down

test-alerts: ## Test alert system
	python scripts/test_alerts.py

test-health: ## Test health checks
	python scripts/test_health.py

test-metrics: ## Test metrics collection
	python scripts/test_metrics.py

test-logs: ## Test logging system
	python scripts/test_logs.py
```

## 5. Logs e Observabilidade

### **5.1 Structured Logging**
```python
# src/config/logging.py
import structlog
import logging
import sys
from typing import Any, Dict

def configure_logging(level: str = "INFO") -> None:
    """Configure structured logging"""
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, level.upper()),
    )

def get_logger(name: str) -> structlog.BoundLogger:
    """Get a structured logger"""
    return structlog.get_logger(name)
```

### **5.2 Metrics Collection**
```python
# src/services/metrics_service.py
from prometheus_client import Counter, Histogram, Gauge, Summary
from typing import Dict, Any
import time

class MetricsService:
    def __init__(self):
        self._counters: Dict[str, Counter] = {}
        self._histograms: Dict[str, Histogram] = {}
        self._gauges: Dict[str, Gauge] = {}
        self._summaries: Dict[str, Summary] = {}
    
    def get_counter(self, name: str, description: str, labels: list = None) -> Counter:
        """Get or create a counter metric"""
        if name not in self._counters:
            self._counters[name] = Counter(
                name, description, labels or []
            )
        return self._counters[name]
    
    def get_histogram(self, name: str, description: str, labels: list = None) -> Histogram:
        """Get or create a histogram metric"""
        if name not in self._histograms:
            self._histograms[name] = Histogram(
                name, description, labels or []
            )
        return self._histograms[name]
    
    def get_gauge(self, name: str, description: str, labels: list = None) -> Gauge:
        """Get or create a gauge metric"""
        if name not in self._gauges:
            self._gauges[name] = Gauge(
                name, description, labels or []
            )
        return self._gauges[name]
    
    def get_summary(self, name: str, description: str, labels: list = None) -> Summary:
        """Get or create a summary metric"""
        if name not in self._summaries:
            self._summaries[name] = Summary(
                name, description, labels or []
            )
        return self._summaries[name]
    
    def record_request_duration(self, method: str, endpoint: str, status_code: int, duration: float):
        """Record request duration"""
        histogram = self.get_histogram(
            "http_request_duration_seconds",
            "HTTP request duration in seconds",
            ["method", "endpoint", "status_code"]
        )
        histogram.labels(
            method=method,
            endpoint=endpoint,
            status_code=str(status_code)
        ).observe(duration)
    
    def record_request_count(self, method: str, endpoint: str, status_code: int):
        """Record request count"""
        counter = self.get_counter(
            "http_requests_total",
            "Total HTTP requests",
            ["method", "endpoint", "status_code"]
        )
        counter.labels(
            method=method,
            endpoint=endpoint,
            status_code=str(status_code)
        ).inc()
    
    def record_error_count(self, error_type: str, service: str):
        """Record error count"""
        counter = self.get_counter(
            "errors_total",
            "Total errors",
            ["error_type", "service"]
        )
        counter.labels(
            error_type=error_type,
            service=service
        ).inc()
    
    def set_active_connections(self, count: int):
        """Set active connections gauge"""
        gauge = self.get_gauge(
            "active_connections",
            "Number of active connections"
        )
        gauge.set(count)
    
    def record_response_time(self, service: str, endpoint: str, duration: float):
        """Record response time summary"""
        summary = self.get_summary(
            "response_time_seconds",
            "Response time in seconds",
            ["service", "endpoint"]
        )
        summary.labels(
            service=service,
            endpoint=endpoint
        ).observe(duration)
```

### **5.3 Health Checks**
```python
# src/services/health_service.py
import asyncio
import time
from typing import Dict, List, Optional
from datetime import datetime
import httpx
import psycopg2
from .models.health import HealthCheck, HealthResponse, HealthStatus

class HealthService:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.start_time = time.time()
        self.checks: List[HealthCheck] = []
    
    async def check_database(self) -> HealthCheck:
        """Check database connectivity"""
        start_time = time.time()
        try:
            conn = psycopg2.connect(
                host=self.config.get("database_host"),
                port=self.config.get("database_port"),
                database=self.config.get("database_name"),
                user=self.config.get("database_user"),
                password=self.config.get("database_password"),
                connect_timeout=5
            )
            conn.close()
            response_time = time.time() - start_time
            return HealthCheck(
                name="database",
                status=HealthStatus.HEALTHY,
                message="Database connection successful",
                response_time=response_time
            )
        except Exception as e:
            response_time = time.time() - start_time
            return HealthCheck(
                name="database",
                status=HealthStatus.UNHEALTHY,
                message=f"Database connection failed: {str(e)}",
                response_time=response_time,
                error=str(e)
            )
    
    async def check_cache(self) -> HealthCheck:
        """Check cache connectivity"""
        start_time = time.time()
        try:
            # Implement cache check logic
            response_time = time.time() - start_time
            return HealthCheck(
                name="cache",
                status=HealthStatus.HEALTHY,
                message="Cache connection successful",
                response_time=response_time
            )
        except Exception as e:
            response_time = time.time() - start_time
            return HealthCheck(
                name="cache",
                status=HealthStatus.UNHEALTHY,
                message=f"Cache connection failed: {str(e)}",
                response_time=response_time,
                error=str(e)
            )
    
    async def check_external_apis(self) -> HealthCheck:
        """Check external APIs"""
        start_time = time.time()
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # Check external APIs
                response = await client.get("https://httpbin.org/status/200")
                response.raise_for_status()
            
            response_time = time.time() - start_time
            return HealthCheck(
                name="external_apis",
                status=HealthStatus.HEALTHY,
                message="External APIs accessible",
                response_time=response_time
            )
        except Exception as e:
            response_time = time.time() - start_time
            return HealthCheck(
                name="external_apis",
                status=HealthStatus.UNHEALTHY,
                message=f"External APIs check failed: {str(e)}",
                response_time=response_time,
                error=str(e)
            )
    
    async def check_disk_space(self) -> HealthCheck:
        """Check disk space"""
        start_time = time.time()
        try:
            import shutil
            total, used, free = shutil.disk_usage("/")
            usage_percent = (used / total) * 100
            
            if usage_percent > 85:
                status = HealthStatus.UNHEALTHY
                message = f"Disk usage high: {usage_percent:.1f}%"
            else:
                status = HealthStatus.HEALTHY
                message = f"Disk usage normal: {usage_percent:.1f}%"
            
            response_time = time.time() - start_time
            return HealthCheck(
                name="disk_space",
                status=status,
                message=message,
                response_time=response_time
            )
        except Exception as e:
            response_time = time.time() - start_time
            return HealthCheck(
                name="disk_space",
                status=HealthStatus.UNHEALTHY,
                message=f"Disk space check failed: {str(e)}",
                response_time=response_time,
                error=str(e)
            )
    
    async def check_memory(self) -> HealthCheck:
        """Check memory usage"""
        start_time = time.time()
        try:
            import psutil
            memory = psutil.virtual_memory()
            usage_percent = memory.percent
            
            if usage_percent > 90:
                status = HealthStatus.UNHEALTHY
                message = f"Memory usage high: {usage_percent:.1f}%"
            else:
                status = HealthStatus.HEALTHY
                message = f"Memory usage normal: {usage_percent:.1f}%"
            
            response_time = time.time() - start_time
            return HealthCheck(
                name="memory",
                status=status,
                message=message,
                response_time=response_time
            )
        except Exception as e:
            response_time = time.time() - start_time
            return HealthCheck(
                name="memory",
                status=HealthStatus.UNHEALTHY,
                message=f"Memory check failed: {str(e)}",
                response_time=response_time,
                error=str(e)
            )
    
    async def run_all_checks(self) -> HealthResponse:
        """Run all health checks"""
        start_time = time.time()
        
        # Run all checks concurrently
        checks = await asyncio.gather(
            self.check_database(),
            self.check_cache(),
            self.check_external_apis(),
            self.check_disk_space(),
            self.check_memory(),
            return_exceptions=True
        )
        
        # Process results
        health_checks = []
        overall_status = HealthStatus.HEALTHY
        
        for check in checks:
            if isinstance(check, Exception):
                health_checks.append(HealthCheck(
                    name="unknown",
                    status=HealthStatus.UNHEALTHY,
                    message=f"Check failed: {str(check)}",
                    error=str(check)
                ))
                overall_status = HealthStatus.UNHEALTHY
            else:
                health_checks.append(check)
                if check.status == HealthStatus.UNHEALTHY:
                    overall_status = HealthStatus.UNHEALTHY
                elif check.status == HealthStatus.DEGRADED and overall_status == HealthStatus.HEALTHY:
                    overall_status = HealthStatus.DEGRADED
        
        response_time = time.time() - start_time
        uptime = time.time() - self.start_time
        
        return HealthResponse(
            status=overall_status,
            version=self.config.get("version", "unknown"),
            uptime=uptime,
            response_time=response_time,
            checks=health_checks,
            service=self.config.get("service_name", "monitoring"),
            environment=self.config.get("environment", "development")
        )
```

### **5.4 Alert System**
```python
# src/services/alert_service.py
import asyncio
import httpx
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from .models.alert import Alert, AlertSeverity, AlertStatus, AlertQuery

class AlertService:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.alerts: List[Alert] = []
        self.alert_rules = self._load_alert_rules()
    
    def _load_alert_rules(self) -> List[Dict[str, Any]]:
        """Load alert rules from configuration"""
        return [
            {
                "name": "high_error_rate",
                "condition": "error_rate > 5%",
                "duration": "5m",
                "severity": AlertSeverity.CRITICAL,
                "channels": ["webhook", "email", "slack"]
            },
            {
                "name": "high_response_time",
                "condition": "response_time_p95 > 2s",
                "duration": "10m",
                "severity": AlertSeverity.WARNING,
                "channels": ["webhook", "slack"]
            },
            {
                "name": "service_down",
                "condition": "health_check_failed",
                "duration": "1m",
                "severity": AlertSeverity.CRITICAL,
                "channels": ["webhook", "email", "slack", "sms"]
            },
            {
                "name": "disk_space_low",
                "condition": "disk_usage > 85%",
                "duration": "5m",
                "severity": AlertSeverity.WARNING,
                "channels": ["webhook", "slack"]
            },
            {
                "name": "memory_high",
                "condition": "memory_usage > 90%",
                "duration": "5m",
                "severity": AlertSeverity.WARNING,
                "channels": ["webhook", "slack"]
            }
        ]
    
    async def evaluate_alerts(self, metrics: Dict[str, Any]) -> List[Alert]:
        """Evaluate alert rules against current metrics"""
        new_alerts = []
        
        for rule in self.alert_rules:
            if self._evaluate_condition(rule["condition"], metrics):
                alert = Alert(
                    id=f"{rule['name']}_{int(datetime.utcnow().timestamp())}",
                    name=rule["name"],
                    description=f"Alert: {rule['condition']}",
                    severity=rule["severity"],
                    status=AlertStatus.ACTIVE,
                    condition=rule["condition"],
                    value=metrics.get("value", 0),
                    threshold=rule.get("threshold", 0),
                    service=metrics.get("service", "unknown"),
                    environment=metrics.get("environment", "unknown"),
                    labels=metrics.get("labels", {}),
                    annotations=rule.get("annotations", {})
                )
                
                new_alerts.append(alert)
                await self._send_alert(alert, rule["channels"])
        
        return new_alerts
    
    def _evaluate_condition(self, condition: str, metrics: Dict[str, Any]) -> bool:
        """Evaluate alert condition"""
        # Simple condition evaluation
        # In production, use a proper expression evaluator
        try:
            if "error_rate > 5%" in condition:
                return metrics.get("error_rate", 0) > 5
            elif "response_time_p95 > 2s" in condition:
                return metrics.get("response_time_p95", 0) > 2
            elif "health_check_failed" in condition:
                return metrics.get("health_check_failed", False)
            elif "disk_usage > 85%" in condition:
                return metrics.get("disk_usage", 0) > 85
            elif "memory_usage > 90%" in condition:
                return metrics.get("memory_usage", 0) > 90
            return False
        except Exception:
            return False
    
    async def _send_alert(self, alert: Alert, channels: List[str]) -> None:
        """Send alert to configured channels"""
        for channel in channels:
            try:
                if channel == "webhook":
                    await self._send_webhook_alert(alert)
                elif channel == "email":
                    await self._send_email_alert(alert)
                elif channel == "slack":
                    await self._send_slack_alert(alert)
                elif channel == "sms":
                    await self._send_sms_alert(alert)
            except Exception as e:
                # Log error but don't fail the alert
                print(f"Failed to send alert via {channel}: {e}")
    
    async def _send_webhook_alert(self, alert: Alert) -> None:
        """Send alert via webhook"""
        webhook_url = self.config.get("webhook_url")
        if not webhook_url:
            return
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            await client.post(
                webhook_url,
                json={
                    "alert": alert.dict(),
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
    
    async def _send_email_alert(self, alert: Alert) -> None:
        """Send alert via email"""
        # Implement email sending logic
        pass
    
    async def _send_slack_alert(self, alert: Alert) -> None:
        """Send alert via Slack"""
        slack_webhook = self.config.get("slack_webhook_url")
        if not slack_webhook:
            return
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            await client.post(
                slack_webhook,
                json={
                    "text": f"🚨 Alert: {alert.name}",
                    "attachments": [
                        {
                            "color": "danger" if alert.severity == AlertSeverity.CRITICAL else "warning",
                            "fields": [
                                {"title": "Service", "value": alert.service, "short": True},
                                {"title": "Severity", "value": alert.severity, "short": True},
                                {"title": "Description", "value": alert.description, "short": False},
                                {"title": "Condition", "value": alert.condition, "short": False}
                            ]
                        }
                    ]
                }
            )
    
    async def _send_sms_alert(self, alert: Alert) -> None:
        """Send alert via SMS"""
        # Implement SMS sending logic
        pass
    
    def get_alerts(self, query: AlertQuery) -> List[Alert]:
        """Get alerts based on query"""
        filtered_alerts = self.alerts
        
        if query.status:
            filtered_alerts = [a for a in filtered_alerts if a.status == query.status]
        
        if query.severity:
            filtered_alerts = [a for a in filtered_alerts if a.severity == query.severity]
        
        if query.service:
            filtered_alerts = [a for a in filtered_alerts if a.service == query.service]
        
        if query.environment:
            filtered_alerts = [a for a in filtered_alerts if a.environment == query.environment]
        
        if query.start_time:
            filtered_alerts = [a for a in filtered_alerts if a.created_at >= query.start_time]
        
        if query.end_time:
            filtered_alerts = [a for a in filtered_alerts if a.created_at <= query.end_time]
        
        # Apply pagination
        start = query.offset
        end = start + query.limit
        
        return filtered_alerts[start:end]
    
    def resolve_alert(self, alert_id: str) -> Optional[Alert]:
        """Resolve an alert"""
        for alert in self.alerts:
            if alert.id == alert_id:
                alert.status = AlertStatus.RESOLVED
                alert.resolved_at = datetime.utcnow()
                alert.updated_at = datetime.utcnow()
                return alert
        return None
```

---

**Este documento fornece o scaffolding completo para o sistema de observabilidade básica, incluindo estrutura de projeto, DTOs, requirements, Makefile e implementações de logging, métricas, health checks e alertas.**
