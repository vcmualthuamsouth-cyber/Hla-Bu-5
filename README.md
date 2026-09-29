# MFEB HLA BU - Android app

## A awlsam ber: GitHub hmangin APK siam (PC/Android Studio a ngai lo)
1. github.com-ah repository thar siam la (private pawh ok).
2. He folder zawng zawng (hidden `.github` folder tel) upload rawh.
3. Repository > **Actions** > **Build APK** > **Run workflow**.
4. Minute 5-10 hnuah run a zo chuan, a chhunga **MFEB-HLA-BU-apk** download la, zip hawng la `app-debug.apk` phone-ah install rawh.
   (Phone setting-ah "Install unknown apps" allow a ngai.)

## PC-ah build (Node 18+, JDK 17, Android Studio a ngai)
```
npm install
npx cap add android
npm run icons
npx cap sync android
npx cap open android      # Android Studio-ah Build > Build APK(s)
```

## Hla thlak / dah belh
`www/index.html` chhunga `RAW` list hi edit rawh. Chumi hnuah `npx cap sync android` tih leh rawh.

## Play Store tan
Release build-ah signing key a ngai (Android Studio > Build > Generate Signed Bundle). `appId` (`com.mfeb.hlabu`) hi `capacitor.config.json`-ah i duh anga thlak theih; Play Store-ah upload hnuah thlak thei tawh lo.

## iOS
Mac leh Xcode a ngai: `npm i @capacitor/ios && npx cap add ios && npx cap open ios`

## Status bar leh Navigation bar
GitHub build hunah `scripts/patch_android.py` a run a, status bar leh navigation button bar zawng zawng transparent (lang tlang) a siam a, phone in bar height dik tak app hnenah a pe thung. Android Studio-ah build chuan `npx cap sync android` hnuah `python3 scripts/patch_android.py` run leh rawh.
