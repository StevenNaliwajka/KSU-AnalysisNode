from pathlib import Path
from Codebase.DataManager.data_loader import DataLoader
from Codebase.Dashboard.DashboardApp.metadata_utils import extract_all_soil_depths, extract_all_tvws_specials

data_dir = Path(__file__).resolve().parents[2] / "Data"

soil_cols = {
    "date (year-mon-day)", "time (hour-min-sec)",
    "soil moisture value", "soil temperature (°c)", "soil moisture (%)"
}
tvws_cols = {
    "date (year-mon-day)", "time (hour-min-sec)",
    "drssi", "dsnr", "urssi", "usnr"
}
ambient_cols = {
    "date", "simple date", "outdoor temperature (°f)", "feels like (°f)", "dew point (°f)",
    "wind speed (mph)", "wind gust (mph)", "max daily gust (mph)", "wind direction (°)",
    "rain rate (in/hr)", "daily rain (in)", "weekly rain (in)", "monthly rain (in)",
    "yearly rain (in)", "relative pressure (inhg)", "humidity (%)", "ultra-violet radiation index",
    "solar radiation (w/m^2)", "indoor temperature (°f)", "indoor humidity (%)",
    "avg wind direction (10 mins) (°)", "outdoor battery", "absolute pressure (inhg)",
    "indoor battery", "co2 battery", "indoor feels like (°f)", "indoor dew point (°f)"
}

loader = DataLoader()

for i in [1, 2]:
    loader.load_data("SoilData", i, soil_cols)
    loader.load_data("TVWSScenario", i, tvws_cols)

loader.load_data("AmbientWeather", 0, ambient_cols)

soil_depths = {}
tvws_specials = {}

for instance in [1, 2]:
    soil_files = list(data_dir.glob(f"**/SoilData_instance{instance}_*.csv"))
    tvws_files = list(data_dir.glob(f"**/TVWSScenario_instance{instance}_*.csv"))
    soil_depths[instance] = ', '.join(f'{d}"' for d in extract_all_soil_depths(soil_files)) or "?"
    tvws_specials[instance] = ', '.join(f'{s}"' for s in extract_all_tvws_specials(tvws_files)) or "?"

available_columns = sorted(set(soil_cols | tvws_cols | ambient_cols))