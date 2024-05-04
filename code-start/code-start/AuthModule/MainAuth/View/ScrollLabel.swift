//
//  ScrollLabel.swift
//  code-start
//
//  Created by Тимур Калимуллин on 30.03.2024.
//

import Foundation
import UIKit

class ScrollLabel: UIView {
    let textLabel: String = String(repeating: "RemeberCode  ", count: 10)
    let labelScrollingSpeed: Double = 10

    private lazy var label: UILabel = {
        let label = UILabel()
        label.translatesAutoresizingMaskIntoConstraints = false
        label.text = textLabel
        label.font = UIFont.systemFont(ofSize: 14)
        label.textColor = #colorLiteral(red: 0.1370271122, green: 0.8109224439, blue: 0.9838314652, alpha: 1)
        return label
    }()

    override init(frame: CGRect) {
       super.init(frame: frame)
    }

    required init?(coder: NSCoder) {
        super.init(coder: coder)
        setupView()
    }

    private func setupView() {
        addSubview(label)
        NSLayoutConstraint.activate([
            label.topAnchor.constraint(equalTo: self.topAnchor),
            //label.leadingAnchor.constraint(equalTo: self.leadingAnchor),
            label.centerXAnchor.constraint(equalTo: self.centerXAnchor),
            label.bottomAnchor.constraint(equalTo: self.bottomAnchor),
        ])
    }

    public func startAnimate(toRight: Bool) {
        if toRight {
            moveRight()
        } else {
            moveLeft()
        }
    }

    func pauseAnimate() {
        let layer = label.layer
        let pausedTime = layer.convertTime(CACurrentMediaTime(), from: nil)
        layer.speed = 0.0
        layer.timeOffset = pausedTime
    }

    func resumeAnimate(){
        let layer = label.layer
        let pauseTime = layer.timeOffset
        if pauseTime > 0{
            layer.speed = 1.0
            layer.timeOffset = 0.0
            layer.beginTime = 0.0
            let timeSincePause = layer.convertTime(CACurrentMediaTime(), from: nil) - pauseTime
            layer.beginTime = timeSincePause
        }
    }

    private func moveRight(){
        self.layoutIfNeeded()
        UIView.animate(withDuration: labelScrollingSpeed, delay: 0, options: ([.curveLinear, .repeat]), animations: {() -> Void in
          self.label.frame.origin.x = self.label.frame.origin.x + 200
        }, completion:  {_ in})
    }

    private func moveLeft() {
        self.layoutIfNeeded()

        UIView.animate(withDuration: labelScrollingSpeed, delay: 0, options: ([.curveLinear, .repeat]), animations: {() -> Void in
            self.label.frame.origin.x = self.label.frame.origin.x + 100
        }, completion:  { _ in })
    }
}
