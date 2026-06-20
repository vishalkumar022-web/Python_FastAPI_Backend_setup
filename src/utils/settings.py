# pydantic_settings ek library hai jo .env file ko padhne me help karti hai and ye basesetting and settingsConfigDict ka kaam ye hai ki hamare application ke settings ko manage karne me help karta hai. Ye hame environment variables ko easily access karne ka tarika provide karta hai, jisse ham apne application ke configuration ko easily manage kar sakte hai. Iska use karke ham apne application ke settings ko easily change kar sakte hai without changing the code, bas .env file me changes karke. Ye hame ek structured way me settings ko manage karne ka tarika provide karta hai, jisse hamare application ka configuration organized aur maintainable rahta hai.

from pydantic_settings import BaseSettings, SettingsConfigDict

# Hum ek 'Settings' naam ki class bana rahe hain jo BaseSettings se power leti hai
class Settings(BaseSettings):
    
    # Ye line Pydantic ko batati hai ki "Bhai, password aur configuration 
    # bahar rakhi hui '.env' naam ki file se utha lena"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # YAHAN DHYAN DO: Ye class ke ANDAR hona chahiye. 
    # Ye Pydantic ko bata raha hai ki .env me 'DB_CONNECTION' naam ka ek variable hoga 
    # aur uska type 'string' hona chahiye. (Ye tumhara Security Guard hai, data validate kar raha hai)
    DB_CONNECTION: str
    SECRET_KEY : str
    ALGORITHM : str
    EXP_TIME : int 
    BREVO_API_KEY: str

    # BAS YE EK LINE ADD KARNI HAI YAHAN:
    GOOGLE_CLIENT_ID: str


# Yahan humne us class ka ek object (instance) bana liya.
# Ab pure application me kahin bhi database url chahiye, toh hum bas 'settings.DB_CONNECTION' likhenge!
settings = Settings()