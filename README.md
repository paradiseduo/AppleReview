# AppleReview
A python tool to help apple review your code and ipa

## How to use
```bash

    Usage:      
        python3 scan.py -i xxx.ipa -f checklist
    
        -h show help
        -i <IPA Path>
        -f <CheckList Path>

```

## Example
You can add keyword in checklist, one keyword per line, support chinese word.

```bash
❯ python3 scan.py -i 抖音.ipa -f checklist 

以下文件包含alipay
./Payload/Aweme.app/_CodeSignature/CodeResources
./Payload/Aweme.app/AlipaySDK.bundle/bridge.js
./Payload/Aweme.app/APBToygerFacade.bundle/id.strings
./Payload/Aweme.app/APBToygerFacade.bundle/en.strings
./Payload/Aweme.app/APBToygerFacade.bundle/zh-Hant.strings
./Payload/Aweme.app/APBToygerFacade.bundle/zh-HK.strings
./Payload/Aweme.app/APBToygerFacade.bundle/zh-Hans.strings
Binary file ./Payload/Aweme.app/Frameworks/AwemeCore.framework/AwemeCore matches
Binary file ./Payload/Aweme.app/CJPay.bundle/en.lproj/CJPayLocalization.strings matches
./Payload/Aweme.app/Info.plist
==========================================
```
