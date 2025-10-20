"""
System Information Tools
"""
import platform
import psutil
import os
from typing import Dict, List
from datetime import datetime


def get_system_info() -> Dict:
    """Get general system information"""
    try:
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        
        return {
            "success": True,
            "system": {
                "platform": platform.system(),
                "platform_release": platform.release(),
                "platform_version": platform.version(),
                "architecture": platform.machine(),
                "hostname": platform.node(),
                "processor": platform.processor(),
                "boot_time": boot_time.strftime("%Y-%m-%d %H:%M:%S"),
                "user": os.getenv('USERNAME') or os.getenv('USER')
            }
        }
    except Exception as e:
        return {"error": str(e)}


def get_cpu_info() -> Dict:
    """Get CPU usage and information"""
    try:
        cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
        cpu_freq = psutil.cpu_freq()
        
        return {
            "success": True,
            "cpu": {
                "physical_cores": psutil.cpu_count(logical=False),
                "total_cores": psutil.cpu_count(logical=True),
                "usage_per_core": cpu_percent,
                "average_usage": sum(cpu_percent) / len(cpu_percent),
                "frequency_mhz": cpu_freq.current if cpu_freq else None,
                "max_frequency_mhz": cpu_freq.max if cpu_freq else None
            }
        }
    except Exception as e:
        return {"error": str(e)}


def get_memory_info() -> Dict:
    """Get memory usage information"""
    try:
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        return {
            "success": True,
            "memory": {
                "total_gb": round(mem.total / (1024**3), 2),
                "available_gb": round(mem.available / (1024**3), 2),
                "used_gb": round(mem.used / (1024**3), 2),
                "percent_used": mem.percent,
                "swap_total_gb": round(swap.total / (1024**3), 2),
                "swap_used_gb": round(swap.used / (1024**3), 2),
                "swap_percent": swap.percent
            }
        }
    except Exception as e:
        return {"error": str(e)}


def get_disk_info() -> Dict:
    """Get disk usage information"""
    try:
        partitions = []
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                partitions.append({
                    "device": partition.device,
                    "mountpoint": partition.mountpoint,
                    "filesystem": partition.fstype,
                    "total_gb": round(usage.total / (1024**3), 2),
                    "used_gb": round(usage.used / (1024**3), 2),
                    "free_gb": round(usage.free / (1024**3), 2),
                    "percent_used": usage.percent
                })
            except PermissionError:
                pass
        
        return {"success": True, "disks": partitions}
    except Exception as e:
        return {"error": str(e)}


def get_network_info() -> Dict:
    """Get network interface information"""
    try:
        net_io = psutil.net_io_counters()
        addresses = psutil.net_if_addrs()
        
        interfaces = []
        for interface_name, interface_addresses in addresses.items():
            for address in interface_addresses:
                if address.family == 2:  # IPv4
                    interfaces.append({
                        "interface": interface_name,
                        "ip_address": address.address,
                        "netmask": address.netmask
                    })
        
        return {
            "success": True,
            "network": {
                "interfaces": interfaces,
                "bytes_sent": net_io.bytes_sent,
                "bytes_recv": net_io.bytes_recv,
                "packets_sent": net_io.packets_sent,
                "packets_recv": net_io.packets_recv
            }
        }
    except Exception as e:
        return {"error": str(e)}


def get_battery_info() -> Dict:
    """Get battery status (if available)"""
    try:
        battery = psutil.sensors_battery()
        if battery is None:
            return {"success": True, "battery": "Not available (desktop or no battery)"}
        
        return {
            "success": True,
            "battery": {
                "percent": battery.percent,
                "plugged_in": battery.power_plugged,
                "time_remaining_minutes": battery.secsleft / 60 if battery.secsleft != psutil.POWER_TIME_UNLIMITED else "Unlimited"
            }
        }
    except Exception as e:
        return {"error": str(e)}


# Tool definitions for Claude
def get_system_tools() -> List[Dict]:
    """Get system information tool definitions"""
    return [
        {
            "name": "get_system_info",
            "description": "Get general system information like OS, hostname, architecture, boot time",
            "input_schema": {
                "type": "object",
                "properties": {}
            }
        },
        {
            "name": "get_cpu_info",
            "description": "Get CPU usage and information including core count and current usage",
            "input_schema": {
                "type": "object",
                "properties": {}
            }
        },
        {
            "name": "get_memory_info",
            "description": "Get RAM and swap memory usage information",
            "input_schema": {
                "type": "object",
                "properties": {}
            }
        },
        {
            "name": "get_disk_info",
            "description": "Get disk/drive usage information for all partitions",
            "input_schema": {
                "type": "object",
                "properties": {}
            }
        },
        {
            "name": "get_network_info",
            "description": "Get network interface information and statistics",
            "input_schema": {
                "type": "object",
                "properties": {}
            }
        },
        {
            "name": "get_battery_info",
            "description": "Get battery status and remaining time (if laptop)",
            "input_schema": {
                "type": "object",
                "properties": {}
            }
        }
    ]


# Map tool names to functions
SYSTEM_FUNCTIONS = {
    "get_system_info": get_system_info,
    "get_cpu_info": get_cpu_info,
    "get_memory_info": get_memory_info,
    "get_disk_info": get_disk_info,
    "get_network_info": get_network_info,
    "get_battery_info": get_battery_info
}
