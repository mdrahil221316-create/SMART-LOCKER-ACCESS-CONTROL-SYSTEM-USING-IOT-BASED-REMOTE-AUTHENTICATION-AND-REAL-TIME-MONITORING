"""
IoT Authentication and Security Module for Smart Locker System

This module simulates IoT-based authentication mechanisms (RFID, Biometric, Mobile)
and security features for the smart locker access control system.

Author: Internship Project Team
Date: 2024
"""

import random
import datetime
import json
import logging
import hashlib
from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AuthenticationStatus(Enum):
    """Status of authentication attempt"""
    SUCCESS = "Success"
    FAILURE = "Failure"
    TIMEOUT = "Timeout"
    NETWORK_ERROR = "Network Error"
    DEVICE_ERROR = "Device Error"


class BiometricType(Enum):
    """Types of biometric authentication"""
    FINGERPRINT = "Fingerprint"
    FACIAL_RECOGNITION = "Facial Recognition"
    IRIS_SCAN = "Iris Scan"


@dataclass
class AuthenticationAttempt:
    """Data class for authentication attempt"""
    attempt_id: str
    user_id: str
    locker_id: str
    timestamp: datetime.datetime
    method: str
    status: AuthenticationStatus
    response_time: float  # milliseconds
    confidence_score: float  # 0.0 to 1.0
    device_battery: float  # percentage
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'attempt_id': self.attempt_id,
            'user_id': self.user_id,
            'locker_id': self.locker_id,
            'timestamp': self.timestamp.isoformat(),
            'method': self.method,
            'status': self.status.value,
            'response_time': round(self.response_time, 2),
            'confidence_score': round(self.confidence_score, 3),
            'device_battery': round(self.device_battery, 2)
        }


@dataclass
class SecurityEvent:
    """Data class for security event"""
    event_id: str
    locker_id: str
    event_type: str  # 'UNAUTHORIZED_ATTEMPT', 'BRUTE_FORCE', 'NETWORK_BREACH', 'DEVICE_TAMPER'
    severity: str  # 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'
    description: str
    timestamp: datetime.datetime
    affected_users: List[str]
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'event_id': self.event_id,
            'locker_id': self.locker_id,
            'event_type': self.event_type,
            'severity': self.severity,
            'description': self.description,
            'timestamp': self.timestamp.isoformat(),
            'affected_users': self.affected_users
        }


class RFIDAuthenticator:
    """RFID-based authentication module"""
    
    def __init__(self, device_id: str):
        """Initialize RFID authenticator"""
        self.device_id = device_id
        self.battery_level = 100.0
        self.read_range = 10  # centimeters
        self.success_rate = 0.98
        self.attempts = 0
        self.authentication_log: List[AuthenticationAttempt] = []
    
    def authenticate(self, user_id: str, locker_id: str, rfid_card_id: str) -> Tuple[bool, AuthenticationAttempt]:
        """
        Authenticate using RFID card
        
        Args:
            user_id: User ID
            locker_id: Locker ID
            rfid_card_id: RFID card identifier
            
        Returns:
            Tuple of (success, AuthenticationAttempt)
        """
        timestamp = datetime.datetime.now()
        attempt_id = f"RFID_ATT_{len(self.authentication_log) + 1}"
        
        # Simulate response time (typically 100-500ms)
        response_time = random.uniform(100, 500)
        
        # Simulate authentication success/failure
        success = random.random() < self.success_rate
        
        # Calculate confidence score
        confidence = 0.95 if success else 0.15
        confidence += random.uniform(-0.05, 0.05)
        confidence = max(0.0, min(1.0, confidence))
        
        # Determine status
        if success:
            status = AuthenticationStatus.SUCCESS
        else:
            if random.random() < 0.1:
                status = AuthenticationStatus.TIMEOUT
            else:
                status = AuthenticationStatus.FAILURE
        
        # Update battery
        self.battery_level -= random.uniform(0.1, 0.3)
        
        # Create attempt record
        attempt = AuthenticationAttempt(
            attempt_id=attempt_id,
            user_id=user_id,
            locker_id=locker_id,
            timestamp=timestamp,
            method="RFID Card",
            status=status,
            response_time=response_time,
            confidence_score=confidence,
            device_battery=self.battery_level
        )
        
        self.authentication_log.append(attempt)
        self.attempts += 1
        
        return success, attempt
    
    def get_device_status(self) -> Dict:
        """Get RFID device status"""
        return {
            'device_id': self.device_id,
            'device_type': 'RFID Reader',
            'battery_level': round(self.battery_level, 2),
            'total_attempts': self.attempts,
            'success_rate': round((self.success_rate * 100), 2),
            'read_range': f"{self.read_range}cm"
        }


class BiometricAuthenticator:
    """Biometric-based authentication module"""
    
    def __init__(self, device_id: str, biometric_type: BiometricType = BiometricType.FINGERPRINT):
        """Initialize biometric authenticator"""
        self.device_id = device_id
        self.biometric_type = biometric_type
        self.battery_level = 100.0
        self.success_rate = 0.99 if biometric_type == BiometricType.FINGERPRINT else 0.98
        self.attempts = 0
        self.authentication_log: List[AuthenticationAttempt] = []
        self.enrolled_users: Dict[str, str] = {}  # user_id -> biometric_template
    
    def enroll_user(self, user_id: str, biometric_data: str) -> bool:
        """Enroll a user with biometric data"""
        # Simulate biometric template storage
        template_hash = hashlib.sha256(biometric_data.encode()).hexdigest()
        self.enrolled_users[user_id] = template_hash
        logger.info(f"User {user_id} enrolled for {self.biometric_type.value}")
        return True
    
    def authenticate(self, user_id: str, locker_id: str, biometric_sample: str) -> Tuple[bool, AuthenticationAttempt]:
        """
        Authenticate using biometric data
        
        Args:
            user_id: User ID
            locker_id: Locker ID
            biometric_sample: Biometric sample (fingerprint, face image, etc.)
            
        Returns:
            Tuple of (success, AuthenticationAttempt)
        """
        timestamp = datetime.datetime.now()
        attempt_id = f"BIO_ATT_{len(self.authentication_log) + 1}"
        
        # Check if user is enrolled
        if user_id not in self.enrolled_users:
            success = False
            confidence = 0.0
            status = AuthenticationStatus.FAILURE
        else:
            # Simulate biometric matching
            sample_hash = hashlib.sha256(biometric_sample.encode()).hexdigest()
            
            # Simulate match with some error rate
            success = random.random() < self.success_rate
            
            # Calculate confidence score
            if success:
                confidence = random.uniform(0.95, 0.99)
                status = AuthenticationStatus.SUCCESS
            else:
                confidence = random.uniform(0.1, 0.4)
                if random.random() < 0.05:
                    status = AuthenticationStatus.DEVICE_ERROR
                else:
                    status = AuthenticationStatus.FAILURE
        
        # Simulate response time (typically 500-1500ms)
        response_time = random.uniform(500, 1500)
        
        # Update battery
        self.battery_level -= random.uniform(0.2, 0.5)
        
        # Create attempt record
        attempt = AuthenticationAttempt(
            attempt_id=attempt_id,
            user_id=user_id,
            locker_id=locker_id,
            timestamp=timestamp,
            method=f"Biometric ({self.biometric_type.value})",
            status=status,
            response_time=response_time,
            confidence_score=confidence,
            device_battery=self.battery_level
        )
        
        self.authentication_log.append(attempt)
        self.attempts += 1
        
        return success, attempt
    
    def get_device_status(self) -> Dict:
        """Get biometric device status"""
        return {
            'device_id': self.device_id,
            'device_type': f'Biometric Reader ({self.biometric_type.value})',
            'battery_level': round(self.battery_level, 2),
            'total_attempts': self.attempts,
            'enrolled_users': len(self.enrolled_users),
            'success_rate': round((self.success_rate * 100), 2)
        }


class MobileAuthenticator:
    """Mobile app-based authentication module"""
    
    def __init__(self, system_id: str):
        """Initialize mobile authenticator"""
        self.system_id = system_id
        self.server_uptime = 99.9  # percentage
        self.success_rate = 0.97
        self.attempts = 0
        self.authentication_log: List[AuthenticationAttempt] = []
        self.registered_devices: Dict[str, str] = {}  # user_id -> device_token
    
    def register_device(self, user_id: str, device_token: str) -> bool:
        """Register a mobile device for a user"""
        self.registered_devices[user_id] = device_token
        logger.info(f"Mobile device registered for user {user_id}")
        return True
    
    def authenticate(self, user_id: str, locker_id: str, device_token: str) -> Tuple[bool, AuthenticationAttempt]:
        """
        Authenticate using mobile app
        
        Args:
            user_id: User ID
            locker_id: Locker ID
            device_token: Mobile device token
            
        Returns:
            Tuple of (success, AuthenticationAttempt)
        """
        timestamp = datetime.datetime.now()
        attempt_id = f"MOBILE_ATT_{len(self.authentication_log) + 1}"
        
        # Check if device is registered
        if user_id not in self.registered_devices:
            success = False
            confidence = 0.0
            status = AuthenticationStatus.FAILURE
        else:
            # Check server uptime
            if random.random() > (self.server_uptime / 100):
                success = False
                confidence = 0.0
                status = AuthenticationStatus.NETWORK_ERROR
            else:
                # Simulate authentication
                success = random.random() < self.success_rate
                
                if success:
                    confidence = random.uniform(0.96, 0.99)
                    status = AuthenticationStatus.SUCCESS
                else:
                    confidence = random.uniform(0.1, 0.3)
                    status = AuthenticationStatus.FAILURE
        
        # Simulate response time (typically 200-1000ms)
        response_time = random.uniform(200, 1000)
        
        # Create attempt record
        attempt = AuthenticationAttempt(
            attempt_id=attempt_id,
            user_id=user_id,
            locker_id=locker_id,
            timestamp=timestamp,
            method="Mobile App",
            status=status,
            response_time=response_time,
            confidence_score=confidence,
            device_battery=random.uniform(20, 100)  # Simulated mobile device battery
        )
        
        self.authentication_log.append(attempt)
        self.attempts += 1
        
        return success, attempt
    
    def get_system_status(self) -> Dict:
        """Get mobile authentication system status"""
        return {
            'system_id': self.system_id,
            'system_type': 'Mobile Authentication Server',
            'server_uptime': round(self.server_uptime, 2),
            'total_attempts': self.attempts,
            'registered_devices': len(self.registered_devices),
            'success_rate': round((self.success_rate * 100), 2)
        }


class SecurityMonitor:
    """Security monitoring and threat detection"""
    
    def __init__(self, system_id: str):
        """Initialize security monitor"""
        self.system_id = system_id
        self.security_events: List[SecurityEvent] = []
        self.failed_attempts_threshold = 5
        self.brute_force_window = 300  # seconds
        self.user_failed_attempts: Dict[str, List[datetime.datetime]] = {}
    
    def check_brute_force(self, user_id: str, locker_id: str, 
                         failed_attempts: List[datetime.datetime]) -> Tuple[bool, Optional[SecurityEvent]]:
        """
        Check for brute force attack patterns
        
        Args:
            user_id: User ID
            locker_id: Locker ID
            failed_attempts: List of failed attempt timestamps
            
        Returns:
            Tuple of (is_brute_force, SecurityEvent or None)
        """
        # Count failed attempts within the window
        now = datetime.datetime.now()
        recent_failures = [attempt for attempt in failed_attempts 
                          if (now - attempt).total_seconds() < self.brute_force_window]
        
        if len(recent_failures) >= self.failed_attempts_threshold:
            event = SecurityEvent(
                event_id=f"EVENT_{len(self.security_events) + 1}",
                locker_id=locker_id,
                event_type="BRUTE_FORCE",
                severity="CRITICAL",
                description=f"Brute force attack detected: {len(recent_failures)} failed attempts in {self.brute_force_window}s",
                timestamp=now,
                affected_users=[user_id]
            )
            self.security_events.append(event)
            logger.critical(f"Brute force attack detected for user {user_id} on locker {locker_id}")
            return True, event
        
        return False, None
    
    def detect_unauthorized_access(self, user_id: str, locker_id: str) -> Optional[SecurityEvent]:
        """Detect unauthorized access attempts"""
        event = SecurityEvent(
            event_id=f"EVENT_{len(self.security_events) + 1}",
            locker_id=locker_id,
            event_type="UNAUTHORIZED_ATTEMPT",
            severity="HIGH",
            description=f"Unauthorized access attempt by user {user_id}",
            timestamp=datetime.datetime.now(),
            affected_users=[user_id]
        )
        self.security_events.append(event)
        logger.warning(f"Unauthorized access attempt detected")
        return event
    
    def get_security_status(self) -> Dict:
        """Get security monitoring status"""
        critical_events = len([e for e in self.security_events if e.severity == "CRITICAL"])
        high_events = len([e for e in self.security_events if e.severity == "HIGH"])
        
        return {
            'monitor_id': self.system_id,
            'total_events': len(self.security_events),
            'critical_events': critical_events,
            'high_events': high_events,
            'brute_force_threshold': self.failed_attempts_threshold,
            'system_health': "Secure" if critical_events == 0 else "At Risk"
        }


if __name__ == "__main__":
    # Test RFID authenticator
    rfid = RFIDAuthenticator("RFID_001")
    success, attempt = rfid.authenticate("USER_001", "LOCKER_001", "CARD_12345")
    print(f"RFID Authentication: {attempt.to_dict()}")
    
    # Test Biometric authenticator
    bio = BiometricAuthenticator("BIO_001", BiometricType.FINGERPRINT)
    bio.enroll_user("USER_001", "fingerprint_data_001")
    success, attempt = bio.authenticate("USER_001", "LOCKER_001", "fingerprint_data_001")
    print(f"Biometric Authentication: {attempt.to_dict()}")
    
    # Test Mobile authenticator
    mobile = MobileAuthenticator("MOBILE_001")
    mobile.register_device("USER_001", "device_token_001")
    success, attempt = mobile.authenticate("USER_001", "LOCKER_001", "device_token_001")
    print(f"Mobile Authentication: {attempt.to_dict()}")
    
    # Test Security Monitor
    monitor = SecurityMonitor("MONITOR_001")
    status = monitor.get_security_status()
    print(f"Security Status: {status}")
