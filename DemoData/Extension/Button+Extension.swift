//
//  Button.swift
//  FreshaForCustomer  Created by Admin on 30/03/2023.
//

import Foundation
import UIKit

extension UIButton {
    func leftImage(image: UIImage?, padding: CGFloat = 16, renderMode: UIImage.RenderingMode = .alwaysOriginal) {
        guard let image = image else {return}
        self.setImage(image.withRenderingMode(renderMode), for: .normal)
        contentHorizontalAlignment = .left
        let availableSpace = bounds.inset(by: contentEdgeInsets)
        let availableWidth = availableSpace.width - imageEdgeInsets.right - (imageView?.frame.width ?? 0) - (titleLabel?.frame.width ?? 0)
        titleEdgeInsets = UIEdgeInsets(top: 0, left: availableWidth / 2, bottom: 0, right: 0)
        imageEdgeInsets = UIEdgeInsets(top: 0, left: padding, bottom: 0, right: 0)
    }
    
    func rightImage(image: UIImage?, padding: CGFloat = 16, renderMode: UIImage.RenderingMode = .alwaysOriginal){
        guard let image = image else {return}
        self.setImage(image.withRenderingMode(renderMode), for: .normal)
        semanticContentAttribute = .forceRightToLeft
        contentHorizontalAlignment = .right
        let availableSpace = bounds.inset(by: contentEdgeInsets)
        let availableWidth = availableSpace.width - imageEdgeInsets.left - (imageView?.frame.width ?? 0) - (titleLabel?.frame.width ?? 0)
        titleEdgeInsets = UIEdgeInsets(top: 0, left: 0, bottom: 0, right: availableWidth / 2)
        imageEdgeInsets = UIEdgeInsets(top: 0, left: 0, bottom: 0, right: padding)
    }
    
    private var states: [UIControl.State] {
        return [.normal, .selected, .highlighted, .disabled]
    }

    func setImageForAllStates(_ image: UIImage?) {
        states.forEach { setImage(image, for: $0) }
    }
}
