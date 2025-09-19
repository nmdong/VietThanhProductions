
//
//  EmptyView.swift
//  RaoVat
//
//  Created by Admin on 11/16/22.
//

import UIKit

class EmptyView: UIView {

    /*
    // Only override draw() if you perform custom drawing.
    // An empty implementation adversely affects performance during animation.
    override func draw(_ rect: CGRect) {
        // Drawing code
    }
    */
    @IBOutlet weak var lbTitle: UILabel!
    
    @IBOutlet weak var lbDesc: UILabel!
    
    func setuiWithTitle(_ title : String?, desc : String?) {
        if let title = title {
            lbTitle.text = title
        }
        if let desc = desc {
            lbDesc.text = desc
        }
    }
    
}
