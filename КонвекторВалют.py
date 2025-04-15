__version__ = (1, 0, 0)
# meta developer: @psyhomodules

import aiohttp
import flag
from hikkatl.types import Message
from .. import loader, utils

@loader.tds
class КонвекторВалют(loader.Module):
    """Конвертер валют"""

    strings = {"name": "КонвекторВалют"}

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self.api_url = "https://api.exchangerate-api.com/v4/latest/{}"
        self.countries = {
            "USD": ("США", "🇺🇸"),
            "EUR": ("Евросоюз", "🇪🇺"),
            "RUB": ("Россия", "🇷🇺"),
            "UAH": ("Украина", "🇺🇦"),
            "GBP": ("Великобритания", "🇬🇧"),
            "JPY": ("Япония", "🇯🇵"),
            "CNY": ("Китай", "🇨🇳"),
            "AUD": ("Австралия", "🇦🇺"),
            "CAD": ("Канада", "🇨🇦"),
            "CHF": ("Швейцария", "🇨🇭"),
            "AED": ("ОАЭ", "🇦🇪"),
            "AFN": ("Афганистан", "🇦🇫"),
            "ALL": ("Албания", "🇦🇱"),
            "AMD": ("Армения", "🇦🇲"),
            "ANG": ("Нидерландские Антилы", "🇳🇱"),
            "AOA": ("Ангола", "🇦🇴"),
            "ARS": ("Аргентина", "🇦🇷"),
            "AWG": ("Аруба", "🇦🇼"),
            "AZN": ("Азербайджан", "🇦🇿"),
            "BAM": ("Босния и Герцеговина", "🇧🇦"),
            "BBD": ("Барбадос", "🇧🇧"),
            "BDT": ("Бангладеш", "🇧🇩"),
            "BGN": ("Болгария", "🇧🇬"),
            "BHD": ("Бахрейн", "🇧🇭"),
            "BIF": ("Бурунди", "🇧🇮"),
            "BMD": ("Бермуды", "🇧🇲"),
            "BND": ("Бруней", "🇧🇳"),
            "BOB": ("Боливия", "🇧🇴"),
            "BRL": ("Бразилия", "🇧🇷"),
            "BSD": ("Багамы", "🇧🇸"),
            "BTN": ("Бутан", "🇧🇹"),
            "BWP": ("Ботсвана", "🇧🇼"),
            "BYN": ("Беларусь", "🇧🇾"),
            "BZD": ("Белиз", "🇧🇿"),
            "CDF": ("Конго", "🇨🇩"),
            "CLP": ("Чили", "🇨🇱"),
            "COP": ("Колумбия", "🇨🇴"),
            "CRC": ("Коста-Рика", "🇨🇷"),
            "CUP": ("Куба", "🇨🇺"),
            "CVE": ("Кабо-Верде", "🇨🇻"),
            "CZK": ("Чехия", "🇨🇿"),
            "DJF": ("Джибути", "🇩🇯"),
            "DKK": ("Дания", "🇩🇰"),
            "DOP": ("Доминикана", "🇩🇴"),
            "DZD": ("Алжир", "🇩🇿"),
            "EGP": ("Египет", "🇪🇬"),
            "ERN": ("Эритрея", "🇪🇷"),
            "ETB": ("Эфиопия", "🇪🇹"),
            "FJD": ("Фиджи", "🇫🇯"),
            "FKP": ("Фолкленды", "🇫🇰"),
            "FOK": ("Фареры", "🇫🇴"),
            "GEL": ("Грузия", "🇬🇪"),
            "GGP": ("Гернси", "🇬🇬"),
            "GHS": ("Гана", "🇬🇭"),
            "GIP": ("Гибралтар", "🇬🇮"),
            "GMD": ("Гамбия", "🇬🇲"),
            "GNF": ("Гвинея", "🇬🇳"),
            "GTQ": ("Гватемала", "🇬🇹"),
            "GYD": ("Гайана", "🇬🇾"),
            "HKD": ("Гонконг", "🇭🇰"),
            "HNL": ("Гондурас", "🇭🇳"),
            "HRK": ("Хорватия", "🇭🇷"),
            "HTG": ("Гаити", "🇭🇹"),
            "HUF": ("Венгрия", "🇭🇺"),
            "IDR": ("Индонезия", "🇮🇩"),
            "ILS": ("Израиль", "🇮🇱"),
            "IMP": ("Остров Мэн", "🇮🇲"),
            "INR": ("Индия", "🇮🇳"),
            "IQD": ("Ирак", "🇮🇶"),
            "IRR": ("Иран", "🇮🇷"),
            "ISK": ("Исландия", "🇮🇸"),
            "JEP": ("Джерси", "🇯🇪"),
            "JMD": ("Ямайка", "🇯🇲"),
            "JOD": ("Иордания", "🇯🇴"),
            "KES": ("Кения", "🇰🇪"),
            "KGS": ("Киргизия", "🇰🇬"),
            "KHR": ("Камбоджа", "🇰🇭"),
            "KID": ("Кирибати", "🇰🇮"),
            "KMF": ("Коморы", "🇰🇲"),
            "KRW": ("Южная Корея", "🇰🇷"),
            "KWD": ("Кувейт", "🇰🇼"),
            "KYD": ("Каймановы острова", "🇰🇾"),
            "KZT": ("Казахстан", "🇰🇿"),
            "LAK": ("Лаос", "🇱🇦"),
            "LBP": ("Ливан", "🇱🇧"),
            "LKR": ("Шри-Ланка", "🇱🇰"),
            "LRD": ("Либерия", "🇱🇷"),
            "LSL": ("Лесото", "🇱🇸"),
            "LYD": ("Ливия", "🇱🇾"),
            "MAD": ("Марокко", "🇲🇦"),
            "MDL": ("Молдова", "🇲🇩"),
            "MGA": ("Мадагаскар", "🇲🇬"),
            "MKD": ("Македония", "🇲🇰"),
            "MMK": ("Мьянма", "🇲🇲"),
            "MNT": ("Монголия", "🇲🇳"),
            "MOP": ("Макао", "🇲🇴"),
            "MRU": ("Мавритания", "🇲🇷"),
            "MUR": ("Маврикий", "🇲🇺"),
            "MVR": ("Мальдивы", "🇲🇻"),
            "MWK": ("Малави", "🇲🇼"),
            "MXN": ("Мексика", "🇲🇽"),
            "MYR": ("Малайзия", "🇲🇾"),
            "MZN": ("Мозамбик", "🇲🇿"),
            "NAD": ("Намибия", "🇳🇦"),
            "NGN": ("Нигерия", "🇳🇬"),
            "NIO": ("Никарагуа", "🇳🇮"),
            "NOK": ("Норвегия", "🇳🇴"),
            "NPR": ("Непал", "🇳🇵"),
            "NZD": ("Новая Зеландия", "🇳🇿"),
            "OMR": ("Оман", "🇴🇲"),
            "PAB": ("Панама", "🇵🇦"),
            "PEN": ("Перу", "🇵🇪"),
            "PGK": ("Папуа - Новая Гвинея", "🇵🇬"),
            "PHP": ("Филиппины", "🇵🇭"),
            "PKR": ("Пакистан", "🇵🇰"),
            "PLN": ("Польша", "🇵🇱"),
            "PYG": ("Парагвай", "🇵🇾"),
            "QAR": ("Катар", "🇶🇦"),
            "RON": ("Румыния", "🇷🇴"),
            "RSD": ("Сербия", "🇷🇸"),
            "RWF": ("Руанда", "🇷🇼"),
            "SAR": ("Саудовская Аравия", "🇸🇦"),
            "SBD": ("Соломоновы острова", "🇸🇧"),
            "SCR": ("Сейшелы", "🇸🇨"),
            "SDG": ("Судан", "🇸🇩"),
            "SEK": ("Швеция", "🇸🇪"),
            "SGD": ("Сингапур", "🇸🇬"),
            "SHP": ("Остров Святой Елены", "🇸🇭"),
            "SLE": ("Сьерра-Леоне", "🇸🇱"),
            "SLL": ("Сьерра-Леоне", "🇸🇱"),
            "SOS": ("Сомали", "🇸🇴"),
            "SRD": ("Суринам", "🇸🇷"),
            "SSP": ("Южный Судан", "🇸🇸"),
            "STN": ("Сан-Томе и Принсипи", "🇸🇹"),
            "SYP": ("Сирия", "🇸🇾"),
            "SZL": ("Эсватини", "🇸🇿"),
            "THB": ("Таиланд", "🇹🇭"),
            "TJS": ("Таджикистан", "🇹🇯"),
            "TMT": ("Туркменистан", "🇹🇲"),
            "TND": ("Тунис", "🇹🇳"),
            "TOP": ("Тонга", "🇹🇴"),
            "TRY": ("Турция", "🇹🇷"),
            "TTD": ("Тринидад и Тобаго", "🇹🇹"),
            "TVD": ("Тувалу", "🇹🇻"),
            "TWD": ("Тайвань", "🇹🇼"),
            "TZS": ("Танзания", "🇹🇿"),
            "UGX": ("Уганда", "🇺🇬"),
            "UYU": ("Уругвай", "🇺🇾"),
            "UZS": ("Узбекистан", "🇺🇿"),
            "VES": ("Венесуэла", "🇻🇪"),
            "VND": ("Вьетнам", "🇻🇳"),
            "VUV": ("Вануату", "🇻🇺"),
            "WST": ("Самоа", "🇼🇸"),
            "XAF": ("Центральная Африка", "🇨🇫"),
            "XCD": ("Восточные Карибы", "🇦🇬"),
            "XCG": ("Криптовалюта", "🌐"),
            "XDR": ("МВФ", "🏦"),
            "XOF": ("Западная Африка", "🇨🇮"),
            "XPF": ("Французская Полинезия", "🇵🇫"),
            "YER": ("Йемен", "🇾🇪"),
            "ZAR": ("ЮАР", "🇿🇦"),
        }

    async def cvcmd(self, message: Message):
        """Конвертация валют: .cv [сумма] [из валюты] [в валюту] (например, .cv 100 USD RUB)"""
        args = utils.get_args_raw(message).upper().split()
        if len(args) < 3:
            await utils.answer(message, "<b>❌ Укажите сумму, исходную и целевую валюту!\nПример: .cv 100 USD RUB</b>")
            return

        try:
            amount = float(args[0])
            from_currency = args[1]
            to_currency = args[2]
        except (ValueError, IndexError):
            await utils.answer(message, "<b>❌ Неверный формат! Используйте: .cv [сумма] [из валюты] [в валюту]</b>")
            return

        if from_currency not in self.countries or to_currency not in self.countries:
            await utils.answer(message, "<b>❌ Одна из валют не поддерживается! Используйте .currencies для списка.</b>")
            return

        async with aiohttp.ClientSession() as session:
            async with session.get(self.api_url.format(from_currency)) as response:
                if response.status != 200:
                    await utils.answer(message, "<b>❌ Ошибка API! Попробуйте позже.</b>")
                    return
                data = await response.json()

        rate = data["rates"].get(to_currency)
        if not rate:
            await utils.answer(message, "<b>❌ Валюта не найдена в API!</b>")
            return

        result = amount * rate
        from_flag = self.countries[from_currency][1]
        to_flag = self.countries[to_currency][1]
        from_country = self.countries[from_currency][0]
        to_country = self.countries[to_currency][0]

        response = (
            f"<b>💸 Конвертация валют</b>\n\n"
            f"{from_flag} <b>{amount:.2f} {from_currency}</b> ({from_country})\n"
            f"➡️ <b>{result:.2f} {to_currency}</b> {to_flag} ({to_country})\n\n"
            f"📊 <i>Курс: 1 {from_currency} = {rate:.4f} {to_currency}</i>\n"
            f"🕒 <i>Обновлено: {data['date']}</i>"
        )
        await utils.answer(message, response)

    async def _page_cb(self, call, index):
        if index < 0:
            index = 3
        elif index > 3:
            index = 0 

        sorted_currencies = sorted(self.countries.items())
        groups = [sorted_currencies[i:i+44] for i in range(0, 132, 44)]
        groups.append(sorted_currencies[132:175])
        groups.append(sorted_currencies[175:218]) 

        response = f"<b>🌍 Список валют мира (страница {index + 1}/4)</b>\n\n"
        for code, (country, flag) in groups[index]:
            response += f"{flag} <code>{code}</code> — <b>{country}</b>\n"

        buttons = [
            [
                {"text": "⬅️", "callback": self._page_cb, "args": (index - 1,)},
                {"text": "➡️", "callback": self._page_cb, "args": (index + 1,)}
            ]
        ]

        await call.edit(response, reply_markup=buttons)

    async def currenciescmd(self, message: Message):
        """Список валют и их номера"""
        sorted_currencies = sorted(self.countries.items())
        groups = [sorted_currencies[i:i+44] for i in range(0, 132, 44)]
        groups.append(sorted_currencies[132:175])
        groups.append(sorted_currencies[175:218])

        response = "<b>🌍 Список валют мира (страница 1/4)</b>\n\n"
        for code, (country, flag) in groups[0]:
            response += f"{flag} <code>{code}</code> — <b>{country}</b>\n"

        buttons = [
            [
                {"text": "⬅️", "callback": self._page_cb, "args": (3,)}, 
                {"text": "➡️", "callback": self._page_cb, "args": (1,)} 
            ]
        ]

        await utils.answer(message, response, reply_markup=buttons)