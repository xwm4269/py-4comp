import datetime

password_salt = 'resdthiojliufd\tt7r2r893ufgswfhjbvvfauisoiudt214-023=--=fehi'

today = datetime.datetime.now()
year = today.year
month = today.month
day = today.day
hour = today.hour
min = today.minute
today = f"{year} - {month} - {day}  {hour} : {min}"