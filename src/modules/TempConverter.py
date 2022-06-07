from typing import Dict


class TempConverter:

    def __init__(self, convert_from: Dict, convert_to: str) -> None:
        self.from_unit:str = (convert_from['unit']).lower()
        self.from_value:float = convert_from['value']
        self.to_unit:str = convert_to.lower()

    def __fahrenheit_to_celsius(self) -> float:
        return (self.from_value - 32) * 0.5556

    def __celsius_to_fahrenheit(self) -> float:
        return (self.from_value * 1.8) + 32

    def __celsius_to_kelvin(self) -> float:
        return self.from_value + 273

    def __kelvin_to_celsius(self) -> float:
        return self.from_value - 273
    
    def __kelvin_to_fahrenheit(self) ->float:
        return (1.8 * (self.from_value - 273)) + 32
    
    def __fahrenheit_to_kelvin(self) -> float:
        return (0.5556 * (self.from_value - 32)) + 273

    def  __convert(self) -> float or None:
        if(self.from_unit == "fahrenheit" and self.to_unit == "celsius"):
            return self.__fahrenheit_to_celsius()
        if(self.from_unit == "celsius" and self.to_unit == "fahrenheit"):
            return self.__celsius_to_fahrenheit()
        if(self.from_unit == "celsius" and self.to_unit == "kelvin"):
            return self.__celsius_to_kelvin()
        if(self.from_unit == "kelvin" and self.to_unit == "celsius"):
            return self.__kelvin_to_celsius()
        if(self.from_unit == "kelvin" and self.to_unit == "fahrenheit"):
            return self.__kelvin_to_fahrenheit()
        if(self.from_unit == "fahrenheit" and self.to_unit == "kelvin"):
            return self.__fahrenheit_to_kelvin()
        return None

    def get_result(self) -> float or None:
        return self.__convert()        