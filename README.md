# ZillowPhotosDownloader
This is a script to bulk download photos from a Zillow home listing. No API required.
<br>

The script will download the highest resolution photos (in WebP or JPG) and place them in a folder named the Zillow listing's home address. 
<br>

It will also bypass Zillow's anti-bot measures that would normally result in 403 responses.
<br>
<br>

If this was somewhat useful to you, consider buying me a mug root beer!
<center><a href="https://www.buymeacoffee.com/bacon1933" target="_blank"><img src="https://i.imgur.com/H2hMOg6.png" alt="Buy Me A Coffee" style="height: 51px !important;width: 217px !important;" ></a></center>

<br>

## Prerequisites
If you are using Windows, a python version of 3.6 or newer is required. Adding Python to your system PATH is reccomended. 

<br>

This script requires two libraries: 'requests' and 'beautifulsoup4'. You can install these with the following commands:
```
pip install requests
```
```
pip install beautifulsoup4
```


<br>


## Usage
The usage for this script is as follows:
```
python ZillowPhotosDownloader.py [Zillow URL]
```
<br>

Optionally, you can add an additional flag '-d', '-date' or '--date' to append the date and time to the directory created by the script. This would be particularly useful for Zillow listings that update frequently with new photos. Example:
```
python ZillowPhotosDownloader.py -d [Zillow URL]
```


Futhermore, if you needed the images in the JPG format, you can add '-j', '-jpg' or '--jpg' to do so. I personally would stick with WebP because it has noticeably better compression in terms of quality. The script downloads WebP by default. Example to download JPG only:
```
python ZillowPhotosDownloader.py -j [Zillow URL]
```
<br>
<br>


It is bound that Zillow's page design will change and it may interfere with the script's ability to download photos. I may or may not update this script to fix this, we'll see.




