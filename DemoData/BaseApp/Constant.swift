//
//  Constant.swift
//  WeediesApp
//  Created by Admin on 6/13/22.
//

import UIKit
///---------------------------------------------------------------------------------------
/// SCREEN FRAME
///---------------------------------------------------------------------------------------
//MARK: - SCREEN FRAME
let SCREEN_WIDTH = UIScreen.main.bounds.size.width
let SCREEN_HEIGHT = UIScreen.main.bounds.size.height

let SCREEN_MAX_LENGTH = max(SCREEN_WIDTH, SCREEN_HEIGHT)
let SCREEN_MIN_LENGTH = min(SCREEN_WIDTH, SCREEN_HEIGHT)

let IS_IPAD: Bool = (UIDevice.current.userInterfaceIdiom == .pad)
let IS_IPHONE: Bool = (UIDevice.current.userInterfaceIdiom == .phone)
let IS_IPHONE_X: Bool = (IS_IPHONE&&(SCREEN_MAX_LENGTH >= 812.0))

let SHARE_APPLICATION_DELEGATE = UIApplication.shared.delegate as! AppDelegate
let heightImage = (SCREEN_WIDTH - 100 - pading * 2)/3


///---------------------------------------------------------------------------------------
/// NOTIFICATION
///---------------------------------------------------------------------------------------
//MARK: - NOTIFICATION
extension Notification.Name {
    static let didUpdateSaveLocal = Notification.Name("didUpdateSaveLocal")
    static let flagsChangedInternet = Notification.Name("flagsChangedInternet")
    static let turnOffVideo = Notification.Name("turnOffVideo")
    static let updateProgressBarVideoAWS = Notification.Name("updateProgressBarVideoAWS")
    static let kDidReceiveNotification = Notification.Name("kDidReceiveNotification")

    
}



let GOOGLEMAP_KEY = "AIzaSyBDUNgPOESk4_qei2TpnLy6Xvrhe6lndFw"
let YOUR_CLIENT_ID = "700503668143-bdc8ckjm9eob2t1nvn31d4hdn03okhk9.apps.googleusercontent.com"
let REVERSED_CLIENT_ID = "com.googleusercontent.apps.700503668143-bdc8ckjm9eob2t1nvn31d4hdn03okhk9"
let PHONE_FORMAT_NEW = "(***) ***-****"
let CHARACTER_FORMAT = "*".utf16.first!
let PHONE_NUMBER = "****-***-***"
let CARD_NUMBER = "**** **** **** ****"
let CARD_EXPIRED_TIME = "**/**"
let CARD_CVC = "****"
let valueForReplace = "{{Value}}"


let AVATAR_DEFAULT = UIImage.init(named: "avatar") ?? UIImage()
let IMAGE_DEFAULT = UIImage.init(named: "img_default") ?? UIImage()
let IMAGE_DEFAULT_LAND = UIImage.init(named: "img_default_land") ?? UIImage()
let IMAGE_DEFAULT_CHAT = UIImage.init(named: "ic_defautChat") ?? UIImage()



let QUANTITY_IMAGE = 0.1
let pading = 16.0
let ratioCL: CGFloat = 200/265
let ratioTB: CGFloat = 200/358
let ratioImage: CGFloat = 218/390
let heightProductTB: CGFloat = 100.0
let heightReviewTB: CGFloat = 200.0
let heightOpenHourTB: CGFloat = 44.0



