# fEVR
(f)rigate / (E)vent (V)ideo (R)ecorder. Pronounced [fee-ver]
### Main Display
![fEVR-main](https://user-images.githubusercontent.com/93575915/151338205-c1e0f12e-1d8a-4c56-be59-d4b2c5e96bd7.png)

### Menu
![fEVR-menu](https://user-images.githubusercontent.com/93575915/151338307-2df5f44d-2149-496a-850b-98e5b1c70b87.png)

### Event View
![fEVR-event](https://user-images.githubusercontent.com/93575915/151338353-ae2d7c21-8d6c-4ed8-aa8e-752b3914a9cb.png)

### Delete Event
At the moment, deleting an event will delete the associated files, but not the database entry.  This is for testing purposes.  The next update *should* include deleting the event from the database.
![fEVR-delete](https://user-images.githubusercontent.com/93575915/151338410-230f9512-4b0a-4a90-942c-0ee97d050983.png)

### Refresh Event
One *minor* bug is sometimes the clip doesn't play properly.  *Usually* refreshing the event will fix it.  However, if frigate deletes the event prior to you refreshing, the event will be lost.  This will be fixed soon, but for now it's acceptable behavior.  Remember, THIS IS NOT PRODUCTION READY!!! YOU MAY LOSE DATA!!!
![fEVR-refresh](https://user-images.githubusercontent.com/93575915/151338629-9616b08a-66f6-445f-a277-447009c2e683.png)


## Config
If you click the "config" menu item, basic configuration will be shown.  In the near future I plan on making configuration automatic throught Home Assistant's API and a couple forms.  Until then, a bit of knowledge of Home Assistant and Frigate is required.

## Pull Requests welcome!
Feel free to fork the project and submit pull requests.

Hope you find this useful.
