import psutil
import requests
import os
from pathlib import Path
from dotenv import load_dotenv
import datetime as dt

def initialize_env():
    script_path = Path(__file__).resolve()
    project_root = script_path.parents[1]
    dotenv_path = project_root / ".env"

    if not dotenv_path.exists():
        raise FileNotFoundError(f"Critical configuration file missing at {dotenv_path}")
    
    load_dotenv(dotenv_path=dotenv_path)

initialize_env()

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def format_disks_text(disks):
    string = ""

    for disk in disks:
        string += f"**{disk["device"]}**\nMount Point: {disk["mountPoint"]}\nTotal Storage Space: {bytes_to_gb(disk["totalStorageSpace"])}GB\nUsed Storage Space: {bytes_to_gb(disk["usedStorageSpace"])}GB\nFree Storage Space: {bytes_to_gb(disk["freeStorageSpace"])}GB\nPercent Storage Used: {disk["percentStorageUsed"]}%\n\n"
    
    return string

def format_net_stats(netStats):
    string =  ""
    for interface in netStats:
        string += f"**{interface["interface"]}**\nIs Up: {interface["isup"]}\nAddress: {interface["address"]}\n\n"
        
    return string

def format_discord_payload(memoryInfo, disks, netStats):
    totalMemory = memoryInfo.total
    availableMemory = memoryInfo.available
    freeMemory = memoryInfo.free
    memoryPercentage = memoryInfo.percent

    diskText = format_disks_text(disks)
    netText = format_net_stats(netStats)

    payload = {
        "embeds": [
            {
                "color": 0x0099ff,
                "title": os.uname()[1],
                "fields": [
                    {
                        "name": "Memory",
                        "value": f"Total Memory: {bytes_to_gb(totalMemory)}GB\nAvailable Memory: {bytes_to_gb(availableMemory)}GB\nFree Memory: {bytes_to_gb(freeMemory)}GB\nMemory Percentage: {memoryPercentage}%"
                    },
                    {
                        "name": "Disks",
                        "value": diskText
                    },
                    {
                        "name": "Network",
                        "value": netText
                    }
                ],
                
                "timestamp": dt.datetime.now(dt.timezone.utc).isoformat()
            }
        ]
    }
    
    return payload


def send_discord_message(payload):
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload, headers=headers)
        if response.status_code == 204:
            print('Message sent successfully!')
        else:
            print(f'Failed to send message. Status code {response.status_code}\n{response.text}\nPayload: {payload}')
    except Exception as e:
        print(f"Network error: {e}")

def bytes_to_gb(bytes):
    return f"{bytes / 1024 / 1024 / 1024:.2f}"

def main():
    ## Memory
    memoryStats = psutil.virtual_memory()

    # Disk usage
    diskPartitions = psutil.disk_partitions()
    diskUsageStats = []
    for partition in diskPartitions:
        diskStats = psutil.disk_usage(partition.mountpoint)
        diskUsageStats.append({
            "device": partition.device,
            "mountPoint": partition.mountpoint,
            "totalStorageSpace": diskStats.total,
            "usedStorageSpace": diskStats.used,
            "freeStorageSpace": diskStats.free,
            "percentStorageUsed": diskStats.percent
        })

    # Network
    ifStats = psutil.net_if_stats()
    ifAddresses = psutil.net_if_addrs()
    netStats = []
    for interface, stats in ifStats.items():
        stats = {
            "interface": interface,
            "isup": stats.isup
        }
        
        try:
            stats["address"] = ifAddresses[interface][0].address
        except Exception as e:
            stats["address"] = "No address"
        
        netStats.append(stats)


    payload = format_discord_payload(memoryStats, diskUsageStats, netStats)
    send_discord_message(payload)
    
if __name__ == "__main__":
    main()