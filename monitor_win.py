# import win32api
import wmi
import psutil
import time
import pynvml
import os
from colorama import init,Fore


def get_info():
    info = {}.fromkeys(('cpu','memory','gpu','net'))

    my_wmi = wmi.WMI()
    cpu = my_wmi.Win32_Processor()
    info['cpu'] = cpu[0].loadPercentage

    memory = psutil.virtual_memory()
    info['memory'] = memory.percent

    # disk = my_wmi.Win32_LogicalDisk()
    # disk = psutil.disk_io_counters()
    # print(disk)

    pynvml.nvmlInit()
    gpu_0 = pynvml.nvmlDeviceGetHandleByIndex(0)
    gpu_info = pynvml.nvmlDeviceGetMemoryInfo(gpu_0)
    # print(pynvml.nvmlDeviceGetName(gpu_0))
    # print('gpu_total_memory: ',gpu_info.total/1024/1024)
    # print('gpu_free_memory: ',gpu_info.free/1024/1024)
    # print('gpu_used_memory: ',gpu_info.used/1024/1024,'MB')
    info['gpu'] = (gpu_info.used / gpu_info.total)*100
    pynvml.nvmlShutdown()

    net = my_wmi.Win32_PerfRawData_Tcpip_TCPv4()    # Maybe ***.Win32_PerfRawData_Tcpip_TCPv4 is higher than GroundTruth a few
    down_prv = net[0].SegmentsReceivedPersec
    up_prv = net[0].SegmentsSentPersec
    time.sleep(0.01)
    net = my_wmi.Win32_PerfRawData_Tcpip_TCPv4()
    down_nxt = net[0].SegmentsReceivedPersec
    up_nxt = net[0].SegmentsSentPersec
    info['net'] = (down_nxt - down_prv) / 1024 * 8          # upload: (up_nxt - up_prv)/1024, has same problems.

    return info

def display(info):
    init(autoreset=True)
    print(Fore.GREEN + '\n== A Simple Monitor ==')
    print('+---------+-----------+')
    print('|{:^9s}|{:^11s}|'.format('name','usage'))
    print('+---------+-----------+')
    print('|{:<9s}|{:>9.3f} %|'.format('cpu',info['cpu']))
    print('|{:<9s}|{:>9.3f} %|'.format('memory',info['memory']))
    print('|{:<9s}|{:>9.3f} %|'.format('gpu',info['gpu']))
    print('|{:<9s}|{:>6.2f} MB/s|'.format('network',info['net']))      
    print('+---------+-----------+')

    time.sleep(1.5)
    info.clear()
    # os.system('cls')

if __name__ == '__main__':
    flag = 1
    while flag:
        i = get_info()
        display(info=i)

