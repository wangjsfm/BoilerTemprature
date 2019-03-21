
from apscheduler.schedulers.background import BackgroundScheduler
from Monitor.sched.TempratureHandle import temperatureMonitorHandle


from ..config import   SCHEDULER_INTERVAL,\
    UpperWaterWall_Area_1,HorizontalFlueSideWaterWall_Area_1,\
    ProofExport_Area_1,HorizontalFlueSideWall_Area_1,\
    RearShaftWallTube38_Area_1,RearShaftWallTube51_Area_1, \
    LowTemperatureSuperheater_Area_1,PlatenSuperheater45_Area_1, \
    PlatenSuperheater51_Area_1,HighTemperatureSuperheater45_Area_1, \
    HighTemperatureSuperheater51_Area_1,HighTemperatureReheater_Area_1,\
    LowTemperatureReheater_Area_1,LowerWaterWall_Area_1


from Monitor.utils.brokenLineFuntion import\
    economizerExportFunc,proofExportFunc\
    ,horizontalFlueSideWalltFunc \
    ,rearShaftWallTubeModle38Func,\
    rearShaftWallTubeModle51Func,lowTemperatureSuperheaterFunc,\
    platenSuperheaterModle45Func,platenSuperheaterModle51Func,\
    highTemperatureSuperheaterFunc45,highTemperatureSuperheaterFunc51,\
    highTemperatureReheaterFunc,lowTemperatureReheaterFunc,\
    upperWaterWallFunc,lowerWaterWallFunc

from .TempratureHandle import  getBoilerSteamPressure
from .Boiler_1_temp_diff_func import tempreatureDiffMonit
from .TeamRotationSch import  teamRotatinoHandle,UpdataPeriodTeam,testDemo
from Monitor.apps import  MonitorConfig

import  pyttsx3

# voiceList = ['1号机组,后竖井后包墙出口从炉左向炉右数第271根管子壁温',
#              '2号机组,后竖井后包墙出口从炉左向炉右数第251根管子壁温',
#              '1号机组,大屏过热器出口前屏沿炉宽方向从左向右数第2排，从屏外圈往内圈数第3根管子壁温',
#              '2号机组,锅炉左侧高温过热器出口管外壁温度',
#              '1号机组,侧墙上部左侧水冷壁出口从炉前向炉后数第12根管子壁温',
#              '2号机组,前墙上部水冷壁出口从炉左向炉右数第147根管子壁温'
#              ]

voiceList = ['系统已上线，开始监测锅炉壁温....',]

voiceList2 = 0



#壁温监控模块
def schGrqTask():


    #获取压力数据
    boilerSteamPressure = getBoilerSteamPressure() #锅炉蒸汽压力

####>>>>>>>>>>>  #1机组 区域   <<<<<<<<<<<#######

    #上部水冷壁
    temperatureMonitorHandle(500, upperWaterWallFunc,UpperWaterWall_Area_1)
    #下部水冷壁
    temperatureMonitorHandle(475, lowerWaterWallFunc,LowerWaterWall_Area_1)
    #顶棚出口
    temperatureMonitorHandle(boilerSteamPressure['boilerMainSteamPressure_Prcess_1'], proofExportFunc,
                             ProofExport_Area_1)


    # 水平烟道侧包墙区域温度数据监控
    temperatureMonitorHandle(boilerSteamPressure['boilerMainSteamPressure_Prcess_1'], horizontalFlueSideWalltFunc,
                             HorizontalFlueSideWall_Area_1)


    # 后竖井包墙管38区域温度数据监控
    temperatureMonitorHandle(boilerSteamPressure['boilerMainSteamPressure_Prcess_1'], rearShaftWallTubeModle38Func,
                             RearShaftWallTube38_Area_1)
    # 后竖井包墙管51区域温度数据监控
    temperatureMonitorHandle(boilerSteamPressure['boilerMainSteamPressure_Prcess_1'], rearShaftWallTubeModle51Func,
                             RearShaftWallTube51_Area_1)




    # 屏式过热器45域温度数据监控
    temperatureMonitorHandle(boilerSteamPressure['boilerMainSteamPressure_Prcess_1'], platenSuperheaterModle45Func,
                             PlatenSuperheater45_Area_1)
    # 屏式过热器51域温度数据监控
    temperatureMonitorHandle(boilerSteamPressure['boilerMainSteamPressure_Prcess_1'], platenSuperheaterModle51Func,
                             PlatenSuperheater51_Area_1)

    # 高温过热器45出口区域温度数据监控
    temperatureMonitorHandle(boilerSteamPressure['boilerMainSteamPressure_Prcess_1'], highTemperatureSuperheaterFunc45,
                             HighTemperatureSuperheater45_Area_1)
    # 高温过热器51出口区域温度数据监控
    temperatureMonitorHandle(boilerSteamPressure['boilerMainSteamPressure_Prcess_1'], highTemperatureSuperheaterFunc51,
                             HighTemperatureSuperheater51_Area_1)



    # 高温再热器区域温度数据监控
    temperatureMonitorHandle(boilerSteamPressure['highTemperatureReheater_Prcess_1'], highTemperatureReheaterFunc,
                             HighTemperatureReheater_Area_1)

    # 低温过热器区域温度数据监控
    temperatureMonitorHandle(boilerSteamPressure['boilerMainSteamPressure_Prcess_1'], lowTemperatureSuperheaterFunc,
                             LowTemperatureSuperheater_Area_1)
    # 低温再热器区域温度数据监控
    pressure = None
    if (boilerSteamPressure['lowTemperatureReheaterEntrance_L_1'] ==0) & (boilerSteamPressure['lowTemperatureReheaterEntrance_R_1'] ==0)  :
        pressure=0
    else:
        pressure = (boilerSteamPressure['lowTemperatureReheaterEntrance_L_1']+
                    boilerSteamPressure['lowTemperatureReheaterEntrance_R_1'])/2
    temperatureMonitorHandle(pressure,lowTemperatureReheaterFunc, LowTemperatureReheater_Area_1)

 ####>>>>>>>>>>>  #1机组 区域   <<<<<<<<<<<#######




####>>>>>>>>>>>>>>>> 语音报警模块
def voiceAlerm():

    # 语音报警参数设置

    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 71)  # 播放速度
    volume = engine.getProperty('volume')
    engine.setProperty('volume', volume + 0.9)  # 播放音量  0-1.0
    while len(voiceList):
        engine.say(voiceList[0]) #将报警文本存入，报警引擎
        voiceList.pop(0) #报警信息已经存入 报警引擎，清楚列表中原有信息

    engine.runAndWait()  # 开启报警引擎，并开始报警
    engine.stop()




####<<<<<<<<<<<<<<< 语音报警模块



####>>>>>>>>>>>>>>>> 温差监控模块
def temperatureDiffSch():

    alermList = tempreatureDiffMonit()  #导入温差监控模块,并返回报警 内容

    if len(alermList):  #将获取到的二维数组报警信息，存入语音报警引擎
        for item in alermList:
            voiceList.append(item)

####<<<<<<<<<<<<<<< 温差监控模块



#定时任务配置
def run_task():

    try:
        # 实例化调度器
        scheduler = BackgroundScheduler()



        scheduler.add_job(voiceAlerm, 'interval', seconds=SCHEDULER_INTERVAL)  # 语音报警
        scheduler.add_job(temperatureDiffSch, 'interval', seconds=SCHEDULER_INTERVAL)  # 温差监控
        scheduler.add_job(schGrqTask, 'interval', seconds=SCHEDULER_INTERVAL)  # 壁温监控
        scheduler.add_job(teamRotatinoHandle, 'cron',  hour='1',minute='59',second ='59')  # 每天凌晨1：59:59更新每天应该上班的班组
        scheduler.add_job(UpdataPeriodTeam, 'cron', hour='2', minute='0', second='0')  # 每天凌晨2更新正在上班的班组
        scheduler.add_job(UpdataPeriodTeam, 'cron', hour='9', minute='0', second='0')  # 每天凌晨9更新正在上班的班组
        scheduler.add_job(UpdataPeriodTeam, 'cron', hour='17', minute='0', second='0')  # 每天下午17更新正在上班的班组
        # scheduler.add_job(testDemo, 'interval', seconds=2)  #查看当前上班的值

        scheduler.start()
        #dd
    except(KeyboardInterrupt,SystemExit):
        scheduler.shutdown()

