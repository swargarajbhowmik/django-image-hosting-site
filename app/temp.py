import datetime

ExpectedDate = "9/8/2015 4:00"
ExpectedDate = datetime.datetime.strptime(ExpectedDate, "%d/%m/%Y %H:%M")
threeHourLater = ExpectedDate + datetime.timedelta(hours = 3)

CurrentDate = datetime.datetime.now()
print(CurrentDate)

print(datetime.datetime.strftime(threeHourLater , '%d/%m/%Y %H:%M'))


# if (CurrentDate-ExpectedDate)>1day