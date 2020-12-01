# KatApp

## Befor you run the app

In your python environment execute the following:
```
pip install -r requirements.txt
```
You need a chrome browser to be installed.  
In case of linux OS you need to extract the _chromedriver_ and replace the mac version with it.

## Start the app:
```
python main.py
```

## Text message:
You can define 2 different text messeg for the invitation.  
The following placeholders are available:  
_{f_name}_  
_{l_name}_  
_{company}_  

### Example:  
```
Hello {f_name},  
  
I see you are also working at {company}.  
  
Br,  
Rick Root 
``` 
```
Hi {f_name},  
  
Thanks for accepting my request.  
  
Br,  
Rick Root 
```  

