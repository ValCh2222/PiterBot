import asyncio
from yaweather import Russia, YaWeatherAsync
from googletrans import Translator
yandex_dict_key = "dict.1.1.20220926T084150Z.df7531ddafd32aa9.b755620323843acb9b38592b6d76d1d31d61ca8b"


async def get_weather():
    async with YaWeatherAsync(api_key='0982f2fa-fd0d-49e5-adf4-456dafd5b765') as y:
        res = await y.forecast(Russia.SaintPetersburg)
        prognos = ""
        for f in res.forecasts:
            day = f.parts.day_short
            message = day.condition
            translator = Translator()
            text1 = message
            message = translator.translate(text1, dest='ru').text
            prognos += f'{f.date} | {day.temp} градусов, {message}\n'

        my_file = open("BabyFile.txt", "w")
        my_file.flush()
        my_file.write(prognos)

asyncio.run(get_weather())
