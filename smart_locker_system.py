"""
Smart Locker Access Control System with IoT-Based Remote Authentication
Main Module: Real-Time Locker Access Control and Monitoring

This module implements a comprehensive locker management system that simulates
real-time access control, authentication, monitoring, and security alerts.

Author: Internship Project Team
Date: 2024
"""

import json
import random
import datetime
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import logging
import hashlib

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class LockerStatus(Enum):
    """Locker operational status"""
    LOCKED = "Locked"
    UNLOCKED = "Unlocked"
    OPEN = "Open"
    TAMPERED = "Tampered"
    MAINTENANCE = "Maintenance"


class AuthenticationMethod(Enum):
    """Authentication methods supported"""
    RFID = "RFID Card"
    BIOMETRIC = "Biometric (Fingerprint)"
    MOBILE = "Mobile App"
    PIN = "PIN Code"
    MULTI_FACTOR = "Multi-Factor"


class AccessType(Enum):
    """Type of access attempt"""
    AUTHORIZED = "Authorized"
    UNAUTHORIZED = "Unauthorized"
    FORCED_ENTRY = "Forced Entry"
    TAMPER_DETECTED = "Tamper Detected"
    MAINTENANCE = "Maintenance"


class AlertSeverity(Enum):
    """Alert severity levels"""
    INFO = "Info"
    WARNING = "Warning"
    CRITICAL = "Critical"
    EMERGENCY = "Emergency"


@dataclass
class User:
    """Data class representing a locker user"""
    user_id: str
    name: str
    email: str
    phone: str
    authentication_method: AuthenticationMethod
    assigned_lockers: List[str]
    is_active: bool = True
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'authentication_method': self.authentication_method.value,
            'assigned_lockers': self.assigned_lockers,
            'is_active': self.is_active
        }


@dataclass
class AccessLog:
    """Data class representing an access event"""
    log_id: str
    locker_id: str
    user_id: str
    timestamp: datetime.datetime
    access_type: AccessType
    authentication_method: AuthenticationMethod
    authentication_success: bool
    access_duration: float  # seconds
    location: str
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'log_id': self.log_id,
            'locker_id': self.locker_id,
            'user_id': self.user_id,
            'timestamp': self.timestamp.isoformat(),
            'access_type': self.access_type.value,
            'authentication_method': self.authentication_method.value,
            'authentication_success': self.authentication_success,
            'access_duration': round(self.access_duration, 2),
            'location': self.location
        }


@dataclass
class SecurityAlert:
    """Data class representing a security alert"""
    alert_id: str
    locker_id: str
    alert_type: str  # 'UNAUTHORIZED_ACCESS', 'FORCED_ENTRY', 'TAMPER', 'NETWORK_FAILURE'
    severity: AlertSeverity
    message: str
    timestamp: datetime.datetime
    resolved: bool = False
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'alert_id': self.alert_id,
            'locker_id': self.locker_id,
            'alert_type': self.alert_type,
            'severity': self.severity.value,
            'message': self.message,
            'timestamp': self.timestamp.isoformat(),
            'resolved': self.resolved
        }


class SmartLocker:
    """Class representing a smart locker with access control"""
    
    def __init__(self, locker_id: str, location: str, capacity: float = 50.0):
        """
        Initialize a smart locker
        
        Args:
            locker_id: Unique locker identifier
            location: Physical location of the locker
            capacity: Storage capacity in liters
        """
        self.locker_id = locker_id
        self.location = location
        self.capacity = capacity
        self.current_occupancy = random.uniform(10, 40)  # Start partially filled
        self.status = LockerStatus.LOCKED
        self.owner_id: Optional[str] = None
        self.access_logs: List[AccessLog] = []
        self.security_alerts: List[SecurityAlert] = []
        self.last_access_time: Optional[datetime.datetime] = None
        self.last_accessed_by: Optional[str] = None
        self.tamper_detected = False
        self.network_connected = True
        self.battery_level = 100.0
        self.access_count = 0
        self.failed_access_count = 0
        self.maintenance_mode = False
    
    def authenticate_user(self, user_id: str, auth_method: AuthenticationMethod, 
                         authorized_users: Dict[str, User]) -> Tuple[bool, str]:
        """
        Authenticate a user attempting to access the locker
        
        Args:
            user_id: User attempting access
            auth_method: Authentication method used
            authorized_users: Dictionary of authorized users
            
        Returns:
            Tuple of (authentication_success, reason)
        """
        # Check if user exists
        if user_id not in authorized_users:
            return False, "User not found in system"
        
        user = authorized_users[user_id]
        
        # Check if user is active
        if not user.is_active:
            return False, "User account is inactive"
        
        # Check if locker is assigned to user
        if self.locker_id not in user.assigned_lockers:
            return False, "User not authorized for this locker"
        
        # Simulate authentication method verification
        if auth_method == AuthenticationMethod.RFID:
            # 98% success rate for RFID
            success = random.random() < 0.98
            reason = "RFID authentication successful" if success else "RFID card not recognized"
        elif auth_method == AuthenticationMethod.BIOMETRIC:
            # 99% success rate for biometric
            success = random.random() < 0.99
            reason = "Biometric authentication successful" if success else "Fingerprint not matched"
        elif auth_method == AuthenticationMethod.MOBILE:
            # 97% success rate for mobile
            success = random.random() < 0.97
            reason = "Mobile authentication successful" if success else "Mobile app verification failed"
        elif auth_method == AuthenticationMethod.PIN:
            # 95% success rate for PIN
            success = random.random() < 0.95
            reason = "PIN authentication successful" if success else "PIN incorrect"
        else:  # MULTI_FACTOR
            # 99.5% success rate for multi-factor
            success = random.random() < 0.995
            reason = "Multi-factor authentication successful" if success else "Multi-factor verification failed"
        
        return success, reason
    
    def process_access_request(self, user_id: str, auth_method: AuthenticationMethod,
                              authorized_users: Dict[str, User]) -> bool:
        """
        Process an access request to the locker
        
        Args:
            user_id: User requesting access
            auth_method: Authentication method
            authorized_users: Dictionary of authorized users
            
        Returns:
            True if access granted, False otherwise
        """
        timestamp = datetime.datetime.now()
        
        # Check network connectivity
        if not self.network_connected:
            alert = SecurityAlert(
                alert_id=f"ALERT_{len(self.security_alerts) + 1}",
                locker_id=self.locker_id,
                alert_type="NETWORK_FAILURE",
                severity=AlertSeverity.WARNING,
                message="Network connectivity lost - access denied",
                timestamp=timestamp
            )
            self.security_alerts.append(alert)
            logger.warning(f"Network failure for {self.locker_id}")
            return False
        
        # Check if locker is in maintenance mode
        if self.maintenance_mode:
            return False
        
        # Authenticate user
        auth_success, auth_reason = self.authenticate_user(user_id, auth_method, authorized_users)
        
        # Determine access type
        if auth_success:
            access_type = AccessType.AUTHORIZED
        else:
            access_type = AccessType.UNAUTHORIZED
            self.failed_access_count += 1
            
            # Generate alert for failed access
            if self.failed_access_count >= 3:
                alert = SecurityAlert(
                    alert_id=f"ALERT_{len(self.security_alerts) + 1}",
                    locker_id=self.locker_id,
                    alert_type="UNAUTHORIZED_ACCESS",
                    severity=AlertSeverity.CRITICAL,
                    message=f"Multiple unauthorized access attempts detected ({self.failed_access_count} attempts)",
                    timestamp=timestamp
                )
                self.security_alerts.append(alert)
                logger.critical(f"Multiple unauthorized access attempts on {self.locker_id}")
        
        # Simulate access duration
        access_duration = random.uniform(30, 300) if auth_success else random.uniform(5, 15)
        
        # Create access log
        log = AccessLog(
            log_id=f"LOG_{len(self.access_logs) + 1}",
            locker_id=self.locker_id,
            user_id=user_id,
            timestamp=timestamp,
            access_type=access_type,
            authentication_method=auth_method,
            authentication_success=auth_success,
            access_duration=access_duration,
            location=self.location
        )
        
        self.access_logs.append(log)
        
        # Update locker state if access granted
        if auth_success:
            self.status = LockerStatus.OPEN
            self.last_access_time = timestamp
            self.last_accessed_by = user_id
            self.owner_id = user_id
            self.access_count += 1
            self.failed_access_count = 0  # Reset failed attempts on successful access
            logger.info(f"Access granted to {user_id} for locker {self.locker_id}")
            
            # Simulate occupancy change
            if random.random() < 0.5:
                self.current_occupancy += random.uniform(5, 20)
            else:
                self.current_occupancy -= random.uniform(5, 20)
            
            self.current_occupancy = max(0, min(self.capacity, self.current_occupancy))
            
            # Simulate locker closing after access
            self.status = LockerStatus.LOCKED
        else:
            logger.warning(f"Access denied to {user_id} for locker {self.locker_id}: {auth_reason}")
        
        return auth_success
    
    def check_tamper(self) -> bool:
        """Check for tampering or forced entry"""
        # Simulate tamper detection with low probability
        tamper_probability = 0.02 if self.network_connected else 0.05
        
        if random.random() < tamper_probability:
            self.tamper_detected = True
            
            alert = SecurityAlert(
                alert_id=f"ALERT_{len(self.security_alerts) + 1}",
                locker_id=self.locker_id,
                alert_type="TAMPER",
                severity=AlertSeverity.EMERGENCY,
                message="Physical tampering detected on locker",
                timestamp=datetime.datetime.now()
            )
            self.security_alerts.append(alert)
            logger.critical(f"Tamper detected on locker {self.locker_id}")
            
            self.status = LockerStatus.TAMPERED
            return True
        
        return False
    
    def simulate_network_issue(self):
        """Simulate network connectivity issues"""
        if random.random() < 0.05:  # 5% chance of network issue
            self.network_connected = False
            logger.warning(f"Network issue on locker {self.locker_id}")
        else:
            self.network_connected = True
    
    def update_battery(self):
        """Update battery level"""
        self.battery_level -= random.uniform(0.1, 0.3)
        
        if self.battery_level < 10:
            alert = SecurityAlert(
                alert_id=f"ALERT_{len(self.security_alerts) + 1}",
                locker_id=self.locker_id,
                alert_type="MAINTENANCE",
                severity=AlertSeverity.WARNING,
                message=f"Battery level critical: {self.battery_level:.1f}%",
                timestamp=datetime.datetime.now()
            )
            self.security_alerts.append(alert)
    
    def get_locker_status(self) -> Dict:
        """Get current locker status"""
        return {
            'locker_id': self.locker_id,
            'location': self.location,
            'status': self.status.value,
            'occupancy_percentage': round((self.current_occupancy / self.capacity) * 100, 2),
            'owner_id': self.owner_id,
            'last_access_time': self.last_access_time.isoformat() if self.last_access_time else None,
            'access_count': self.access_count,
            'failed_access_count': self.failed_access_count,
            'battery_level': round(self.battery_level, 2),
            'network_connected': self.network_connected,
            'tamper_detected': self.tamper_detected,
            'total_alerts': len(self.security_alerts),
            'active_alerts': len([a for a in self.security_alerts if not a.resolved])
        }
    
    def get_security_metrics(self) -> Dict:
        """Calculate security metrics"""
        if len(self.access_logs) == 0:
            return {}
        
        successful_accesses = len([log for log in self.access_logs if log.authentication_success])
        failed_accesses = len([log for log in self.access_logs if not log.authentication_success])
        avg_access_duration = sum(log.access_duration for log in self.access_logs) / len(self.access_logs)
        
        return {
            'total_access_attempts': len(self.access_logs),
            'successful_accesses': successful_accesses,
            'failed_accesses': failed_accesses,
            'success_rate': round((successful_accesses / len(self.access_logs)) * 100, 2),
            'average_access_duration': round(avg_access_duration, 2),
            'security_incidents': len([a for a in self.security_alerts if a.severity in [AlertSeverity.CRITICAL, AlertSeverity.EMERGENCY]])
        }


class LockerManagementSystem:
    """System managing multiple smart lockers"""
    
    def __init__(self, num_lockers: int = 20):
        """Initialize locker management system"""
        self.lockers: Dict[str, SmartLocker] = {}
        self.users: Dict[str, User] = {}
        self.all_access_logs: List[AccessLog] = []
        self.all_alerts: List[SecurityAlert] = []
        self.operation_log: List[Dict] = []
        
        self._initialize_system(num_lockers)
        logger.info(f"Locker Management System initialized with {num_lockers} lockers")
    
    def _initialize_system(self, num_lockers: int):
        """Initialize lockers and users"""
        locations = ["Floor 1", "Floor 2", "Floor 3", "Basement"]
        
        # Create lockers
        for i in range(num_lockers):
            locker_id = f"LOCKER_{i+1:03d}"
            location = locations[i % len(locations)]
            locker = SmartLocker(locker_id, location)
            self.lockers[locker_id] = locker
        
        # Create users
        auth_methods = [AuthenticationMethod.RFID, AuthenticationMethod.BIOMETRIC, 
                       AuthenticationMethod.MOBILE, AuthenticationMethod.PIN]
        
        for i in range(10):
            user_id = f"USER_{i+1:03d}"
            name = f"User {i+1}"
            email = f"user{i+1}@example.com"
            phone = f"555-{1000+i}"
            auth_method = auth_methods[i % len(auth_methods)]
            
            # Assign 2-3 random lockers to each user
            num_assigned = random.randint(2, 3)
            assigned_lockers = random.sample(list(self.lockers.keys()), num_assigned)
            
            user = User(user_id, name, email, phone, auth_method, assigned_lockers)
            self.users[user_id] = user
    
    def simulate_access_requests(self, num_requests: int = 50):
        """Simulate random access requests"""
        for _ in range(num_requests):
            # Select random user and locker
            user_id = random.choice(list(self.users.keys()))
            locker_id = random.choice(list(self.lockers.keys()))
            user = self.users[user_id]
            locker = self.lockers[locker_id]
            
            # Process access request
            locker.process_access_request(user_id, user.authentication_method, self.users)
            
            # Check for tampering
            locker.check_tamper()
            
            # Simulate network issues
            locker.simulate_network_issue()
            
            # Update battery
            locker.update_battery()
            
            # Collect logs and alerts
            for log in locker.access_logs:
                if log not in self.all_access_logs:
                    self.all_access_logs.append(log)
            
            for alert in locker.security_alerts:
                if alert not in self.all_alerts:
                    self.all_alerts.append(alert)
    
    def get_system_statistics(self) -> Dict:
        """Get system-wide statistics"""
        total_lockers = len(self.lockers)
        locked_lockers = len([l for l in self.lockers.values() if l.status == LockerStatus.LOCKED])
        unlocked_lockers = len([l for l in self.lockers.values() if l.status == LockerStatus.UNLOCKED])
        tampered_lockers = len([l for l in self.lockers.values() if l.tamper_detected])
        
        # Count alert types
        alert_distribution = {}
        for alert in self.all_alerts:
            alert_distribution[alert.alert_type] = alert_distribution.get(alert.alert_type, 0) + 1
        
        return {
            'total_lockers': total_lockers,
            'locked_lockers': locked_lockers,
            'unlocked_lockers': unlocked_lockers,
            'tampered_lockers': tampered_lockers,
            'total_access_logs': len(self.all_access_logs),
            'total_alerts': len(self.all_alerts),
            'active_alerts': len([a for a in self.all_alerts if not a.resolved]),
            'alert_distribution': alert_distribution
        }
    
    def get_hourly_report(self) -> Dict:
        """Generate hourly monitoring report"""
        stats = self.get_system_statistics()
        
        report = {
            'timestamp': datetime.datetime.now().isoformat(),
            'statistics': stats,
            'locker_details': {locker_id: locker.get_locker_status() for locker_id, locker in self.lockers.items()}
        }
        
        self.operation_log.append({
            'timestamp': datetime.datetime.now().isoformat(),
            'total_lockers': stats['total_lockers'],
            'locked_lockers': stats['locked_lockers'],
            'active_alerts': stats['active_alerts']
        })
        
        return report
    
    def export_to_json(self, filename: str):
        """Export system data to JSON"""
        data = {
            'system_name': 'Smart Locker Access Control System',
            'total_lockers': len(self.lockers),
            'total_users': len(self.users),
            'lockers': {locker_id: locker.get_locker_status() for locker_id, locker in self.lockers.items()},
            'access_logs': [log.to_dict() for log in self.all_access_logs[-100:]],  # Last 100 logs
            'alerts': [alert.to_dict() for alert in self.all_alerts],
            'operation_log': self.operation_log
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Data exported to {filename}")


if __name__ == "__main__":
    # Create locker management system
    system = LockerManagementSystem(num_lockers=20)
    
    # Simulate access requests
    system.simulate_access_requests(num_requests=100)
    
    # Generate report
    report = system.get_hourly_report()
    
    # Print report
    print("\n" + "="*60)
    print("SMART LOCKER ACCESS CONTROL SYSTEM - SIMULATION REPORT")
    print("="*60)
    print(json.dumps(report, indent=2))
    
    # Export data
    system.export_to_json('/home/ubuntu/smart_locker_system_data.json')
