def work_timer(end_time, start_time):

    execution_time = end_time - start_time
    hours = int(execution_time // 3600)
    minutes = int((execution_time % 3600) // 60)
    seconds = execution_time % 60

    if hours > 0:
        print(f"Время выполнения: {hours}ч {minutes}мин {seconds:.1f}с")
    elif minutes > 0:
        print(f"Время выполнения: {minutes}мин {seconds:.1f}с")
    else:
        print(f"Время выполнения: {seconds:.2f}с")
