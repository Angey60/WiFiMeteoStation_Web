from django.db import models

# Create your models here.
class Sensors(models.Model):
    id = models.CharField(primary_key=True, max_length=256)
    title = models.CharField(max_length=256)
    
    def __str__(self):
        return (
            f"{self.id} "
            f"{self.title}"
        )
        
    class Meta:
        managed = False
        db_table = "sensors"
        

class Devices(models.Model):
    device_id = models.CharField(primary_key=True, max_length=256)
    name = models.CharField(max_length=256)
    note = models.CharField(max_length=256)
    
    def __str__(self):
        return (
            f"{self.device_id} "
            f"{self.name} "
            f"{self.note}"
        )
    
    class Meta:
        managed = False
        db_table = "devices"
        
class DevicesView(models.Model):
    device_name = models.CharField(max_length=256)
    device_properties_name = models.CharField(max_length=256)
    device_properties_note = models.CharField(max_length=256)
    device_properties_value = models.CharField(max_length=256)
    
    class Meta:
        managed = False
        db_table = "view_devices"
        
'''   

CREATE VIEW view_devices WITH ( security_invoker = TRUE ) AS SELECT devices.name AS device_name, device_properties.name AS device_properties_name, device_properties.note AS device_properties_note, device_property_values_new.device_property_value AS device_properties_value 
FROM  device_property_values_new 
LEFT JOIN devices 
ON device_property_values_new.device_id = devices.device_id
LEFT JOIN device_properties
ON device_property_values_new.device_property = device_properties.device_property
WHERE device_property_values_new.device_property != 'timestamp'

#	device_name	device_properties_name	device_properties_note	device_properties_value
1	"Wi-Fi Slot"	"Барометр"	"Барометр v2, МЭМС-датчик LPS25HB"	"749.66"
2	"Wi-Fi Slot"	"Влажность"	"Цифровой метеодатчик, микросхема SHT31"	"57.36"
3	"Wi-Fi Slot"	"Температура"	"Цифровой метеодатчик, микросхема SHT31"	"30.87"

'''  