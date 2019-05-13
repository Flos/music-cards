
﻿

# music-cards(nfcpy)

Fork of [https://github.com/frebeg/music-cards](https://github.com/frebeg/music-cards)

 - play Local Music with nfc tag
 - play Spotify with nfc tag
 - change volume with nfc tag
 - (optional: change volume with push buttons)

## Summary

```
NFC tag set.      -> play music.
NFC tag released. -> pause music.
Same NFC tag set. -> play music. From the time of pause.
Another tag set.  -> clear queue. and play music.
```
https://youtu.be/s8S5DVblT0k

## What you need to buy

- Raspberry Pi
- NFC read/write device (has to work with nfcpy) ([Supported devices](https://nfcpy.readthedocs.io/en/latest/overview.html#supported-devices))
- NFC tags
- optional: Push-Buttons + jump wires

#### What I bought
- PN532 ([Amazon Link](https://www.amazon.de/Module-Reader-Writer-Android-MIFARE/dp/B01E452FV8))
- NFC NTAG213 ([Amazon Link]( https://www.amazon.de/Tags-Sticker-NTAG213-Circus-144Byte/dp/B00BTKAI7U))
- Push Buttons ([Amazon Link](https://www.amazon.de/momentanen-Taster-Schalter-Druckknopf-AC250V/dp/B01FDJLRRW/ref=sr_1_7?keywords=pushbutton&qid=1557738106&s=diy&sr=1-7))

## Support your reader
If you're not using the same reader, u probably have to edit the **Reader.py** script to support it.
In most cases you just have to modify the lines containing  ```nfc.ContactlessFrontend('tty:S0')```

## How to install
- install nfcpy  
```
sudo pip install nfcpy
```

- install python-mpd2  
```
sudo pip install python-mpd2
```

- install a music server (must can be controlled with mpd)    
**highly recommended:** [Mopidy](https://docs.mopidy.com/en/latest/installation/debian/) with the [spotify-extension](https://github.com/mopidy/mopidy-spotify#installation)

- music-cards install
```
git clone https://github.com/frebeg/music-cards
```

## How to use

### How to write NFC tags
I personally use an Android app called NFC Tools ([Play Store](https://play.google.com/store/apps/details?id=com.wakdev.wdnfc))

 1. Open the NFC Tools app and go to the **Write** Tab.
 2. Tap on **Add a record** and choose **Text**
 3. Find a Spotify URI by clicking "Share" on any song, album, playlist, or profile on Spotify Desktop App, and then clicking "URI"
 4. Paste the URI in the Text Field

It should look like this:

![Imgur](https://i.imgur.com/4cfcuJD.jpg)


If you don't have an android -> use senyoltw's (the person i forked this repo from) method.
He uses the **add_card.py**. Visit [his repo](https://github.com/senyoltw/music-cards) for instructions. The python script **box.py** just reads the string on the nfc tag and will call ``` mpc add [string] ```

#### Additionally
If you want to use a mopidy local Playlist, write this on your tag:
``` mopidy:[playlistname] ```

If you want to modify the mopidy-volume:
``` volume:[number] ``` *0-100*

### How to Push Buttons to change volume
If you want to use push buttons to change the raspberry volume you have to connect the buttons to the raspberry GPIO and change the code of the **volume_control.py** script. ([Tutorial](https://raspberrypihq.com/use-a-push-button-with-raspberry-pi-gpio/))

## Daemonization

main function:
```
cd music-cards/
sudo cp musiccards.service /etc/systemd/system/musiccards.service
sudo systemctl daemon-reload
sudo systemctl start musiccards.service
sudo systemctl enable musiccards.service
```
volume-control function:
```
cd music-cards/
sudo cp volume_control.service /etc/systemd/system/volume_control.service
sudo systemctl daemon-reload
sudo systemctl start volume_control.service
sudo systemctl enable volume_control.service
```
