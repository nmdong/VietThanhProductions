//
//  BaseTabbarViewController.swift
//  Weedies
//
//  Created by Thien Truong on 2/20/24.
//

import UIKit
import AlamofireImage
import Alamofire

class BaseTabbarViewController: UITabBarController {
    
    override func viewDidLoad() {
        super.viewDidLoad()
        self.setupVar()
        self.setupUI()
    }
    
    func setupVar() {
        setupTabbar()
    }
    
    func setupUI() {
        self.tabBar.isTranslucent = false
        UITabBar.appearance().barTintColor = .blue
        if #available(iOS 15.0, *) {
            let appearance = UITabBarAppearance()
            appearance.configureWithOpaqueBackground()
//            appearance.stackedLayoutAppearance.selected.titleTextAttributes = [.foregroundColor: UIColor.blue, .font : UIFont.fontRegular(8)]
//            appearance.stackedLayoutAppearance.normal.titleTextAttributes = [.foregroundColor: UIColor.black, .font : UIFont.fontRegular(8)]
            appearance.stackedLayoutAppearance.normal.iconColor = UIColor.black
            appearance.backgroundColor = UIColor.white
            self.tabBar.scrollEdgeAppearance = appearance
            self.tabBar.standardAppearance = appearance
        }
        
    }
    
    func setupTabbar() {
//        let vc1 = HomeVC()
//        let item1 = UITabBarItem.init(title: "Home"), image: R.image.tab_home()!.withRenderingMode(.alwaysOriginal), selectedImage = R.image.tab_home_selected()!.withRenderingMode(.alwaysOriginal))
//        vc1.tabBarItem = item1
//        
//        let vc2 = SelectOptionLawyerVC()
//        let item2 = UITabBarItem.init(title: localized("labelFindLawyer"), image: R.image.tab_search()!.withRenderingMode(.alwaysOriginal), selectedImage: R.image.tab_search_selected()!.withRenderingMode(.alwaysOriginal))
//        vc2.tabBarItem = item2
//        
//        let vc3 = Token().tokenExists ? MyCaseViewController() : NoLoginVC()
//        let item3 = UITabBarItem.init(title: localized("labelMyCases"), image: R.image.tab_case()!.withRenderingMode(.alwaysOriginal), selectedImage: R.image.tab_case_selected()!.withRenderingMode(.alwaysOriginal))
//        vc3.tabBarItem = item3
//        
//        let vc4 = Token().tokenExists ? NotificationsVC() : NoLoginVC()
//        let item4 = UITabBarItem.init(title: localized("labelNotification"), image: R.image.tab_noti()!.withRenderingMode(.alwaysOriginal), selectedImage: R.image.tab_noti_selected()!.withRenderingMode(.alwaysOriginal))
//        vc4.tabBarItem = item4
//        
//        let vc5 = Token().tokenExists ? AccountVC() : NoLoginVC()
//        let item5 = UITabBarItem.init(title: localized("labelAccountProfile"), image: R.image.tab_account()!.withRenderingMode(.alwaysOriginal), selectedImage: R.image.tab_account_selected()!.withRenderingMode(.alwaysOriginal))
//        vc5.tabBarItem = item5
//        
//        let nav1 = BaseNavigationController.init(rootViewController: vc1)
//        let nav2 = BaseNavigationController.init(rootViewController: vc2)
//        let nav3 = BaseNavigationController.init(rootViewController: vc3)
//        let nav4 = BaseNavigationController.init(rootViewController: vc4)
//        let nav5 = BaseNavigationController.init(rootViewController: vc5)
//        self.viewControllers = [nav1,nav2, nav3, nav4, nav5]
        
    }
    
    
    
}



extension UIView {
    func asImage() -> UIImage {
        if #available(iOS 10.0, *) {
            let renderer = UIGraphicsImageRenderer(bounds: bounds)
            return renderer.image { rendererContext in
                layer.render(in: rendererContext.cgContext)
            }
        } else {
            UIGraphicsBeginImageContext(self.frame.size)
            self.layer.render(in:UIGraphicsGetCurrentContext()!)
            let image = UIGraphicsGetImageFromCurrentImageContext()
            UIGraphicsEndImageContext()
            return UIImage(cgImage: image!.cgImage!)
        }
    }
}
