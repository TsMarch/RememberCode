//
//  AuthBackgroundView.swift
//  code-start
//
//  Created by Тимур Калимуллин on 02.04.2024.
//

import Foundation
import UIKit

class AuthBackgroundView: UIView {
    let fontSize: CGFloat = 14
    let height: CGFloat = 18
    let padding: CGFloat = 15

    private lazy var label: ScrollLabel = {
        let label = ScrollLabel()
        label.translatesAutoresizingMaskIntoConstraints = false
        label.heightAnchor.constraint(equalToConstant: height).isActive = true
        label.transform =  CGAffineTransform(rotationAngle: -.pi/6 )
        label.backgroundColor = .clear
        return label
    }()

    override init(frame: CGRect) {
        super.init(frame: frame)
        setupView()
    }

    required init?(coder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }

    private func setupView() {
        backgroundColor = .clear
        let quantatyOfLabels = Int((UIScreen.main.bounds.height + 150) / (height + padding)) + 4
        for i in 0...quantatyOfLabels {
            guard let labelToAdd = try? label.copyObject() as? ScrollLabel else { return }
            addSubview(labelToAdd)
            (i % 2 == 0) ? labelToAdd.startAnimate(toRight: true) : labelToAdd.startAnimate(toRight: false)
            if i == 0 {
                labelToAdd.topAnchor.constraint(equalTo: layoutMarginsGuide.topAnchor, constant: -125).isActive = true
                labelToAdd.leadingAnchor.constraint(equalTo: self.leadingAnchor, constant: -75).isActive = true
                labelToAdd.trailingAnchor.constraint(equalTo: self.trailingAnchor).isActive = true
            } else {
                guard let beforeView = self.subviews.suffix(2).first else { return }
                labelToAdd.topAnchor.constraint(equalTo: beforeView.bottomAnchor , constant: padding).isActive = true
                labelToAdd.leadingAnchor.constraint(equalTo: self.leadingAnchor, constant: -75).isActive = true
                labelToAdd.trailingAnchor.constraint(equalTo: self.trailingAnchor).isActive = true
            }
        }
    }
}
