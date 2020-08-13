while 1:
    UseObject(ObjAtLayer(RhandLayer()))
    WaitForTarget(2000)
    if TargetPresent():
        print("Target Present")
        CancelTarget()
        Wait(1000)