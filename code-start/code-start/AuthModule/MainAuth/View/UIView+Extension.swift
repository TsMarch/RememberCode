//
//  UIView+Extension.swift
//  code-start
//
//  Created by Тимур Калимуллин on 25.02.2024.
//

import Foundation
import UIKit

class CircleBackgroundView: UIView {
    private lazy var pulse: CAGradientLayer = {
        let l = CAGradientLayer()
        l.type = .radial
        l.colors = [ #colorLiteral(red: 0.05350511521, green: 0.44603616, blue: 0.9473034739, alpha: 1).cgColor, #colorLiteral(red: 0.1370271122, green: 0.8109224439, blue: 0.9838314652, alpha: 1).cgColor, #colorLiteral(red: 0.2057334781, green: 0.7553452046, blue: 0.9536633228, alpha: 1).cgColor, #colorLiteral(red: 0.9812344909, green: 0.9084194303, blue: 0.9047674561, alpha: 1).cgColor]
        l.locations = [ 0, 0.20, 0.35, 0.90, 1]
        l.startPoint = CGPoint(x: 0.5, y: 0.5)
        l.endPoint = CGPoint(x: 1, y: 1)
        layer.addSublayer(l)
        return l
    }()

    override func layoutSubviews() {
        super.layoutSubviews()
        pulse.frame = bounds
        layer.cornerRadius = bounds.size.width / 2
        layer.masksToBounds = true
    }
}

extension NSObject {
    func copyObject<T:NSObject>() throws -> T? {
        let data = try NSKeyedArchiver.archivedData(withRootObject:self, requiringSecureCoding:false)
        return try NSKeyedUnarchiver.unarchiveTopLevelObjectWithData(data) as? T
    }
}
