//
//  StartAuthView.swift
//  code-start
//
//  Created by Тимур Калимуллин on 18.03.2024.
//

import Foundation
import UIKit

class StartAuthView: UIView {
    lazy var singInButton: UIButton = {
        let button = UIButton()
        button.translatesAutoresizingMaskIntoConstraints = false
        button.heightAnchor.constraint(equalToConstant: 55).isActive = true
        button.setTitle("Sign In", for: .normal)
        button.titleLabel?.font = UIFont.boldSystemFont(ofSize: 25)
        button.backgroundColor = .white.withAlphaComponent(0.90)
        button.setTitleColor(.black, for: .normal)
        button.layer.cornerRadius = 16
        button.layer.shadowColor = UIColor.black.cgColor
        button.layer.shadowOpacity = 0.5
        button.layer.shadowOffset = CGSize(width: 0, height: 0)
        button.layer.shadowRadius = 10
        return button
    }()

    lazy var singUpButton: UIButton = {
        let button = UIButton()
        button.translatesAutoresizingMaskIntoConstraints = false
        button.heightAnchor.constraint(equalToConstant: 55).isActive = true
        button.setTitle("Sign Up", for: .normal)
        button.titleLabel?.font = UIFont.boldSystemFont(ofSize: 25)
        button.backgroundColor = #colorLiteral(red: 0.5816081166, green: 1, blue: 1, alpha: 1).withAlphaComponent(0.90)
        button.setTitleColor(.black, for: .normal)
        button.layer.cornerRadius = 16
        button.layer.shadowColor = UIColor.black.cgColor
        button.layer.shadowOpacity = 0.6
        button.layer.shadowOffset = CGSize(width: 0, height: 0)
        button.layer.shadowRadius = 10
        return button
    }()

    private lazy var backgroundView: AuthBackgroundView = {
        let background = AuthBackgroundView()
        background.translatesAutoresizingMaskIntoConstraints = false
        background.backgroundColor = .clear
        return background
    }()

    override init(frame: CGRect) {
        super.init(frame: frame)
        setup()
    }

    required init?(coder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }

    private func setup() {
        backgroundColor = .white
        clipsToBounds = true
        addSubview(backgroundView)
        addSubview(singInButton)

        addSubview(singUpButton)

        NSLayoutConstraint.activate([
            backgroundView.topAnchor.constraint(equalTo: self.topAnchor),
            backgroundView.bottomAnchor.constraint(equalTo: self.bottomAnchor),
            backgroundView.leadingAnchor.constraint(equalTo: self.leadingAnchor),
            backgroundView.trailingAnchor.constraint(equalTo: self.trailingAnchor),

            singInButton.leadingAnchor.constraint(equalTo: self.leadingAnchor, constant: 100),
            singInButton.trailingAnchor.constraint(equalTo: self.trailingAnchor, constant: -100),
            singInButton.bottomAnchor.constraint(equalTo: singUpButton.topAnchor, constant: -16),

            singUpButton.bottomAnchor.constraint(equalTo: layoutMarginsGuide.bottomAnchor, constant: -100),
            singUpButton.leadingAnchor.constraint(equalTo: self.leadingAnchor, constant: 100),
            singUpButton.trailingAnchor.constraint(equalTo: self.trailingAnchor, constant: -100)
        ])
        //singUpButton.addBlurEffect(style: .light, cornerRadius: 16)
    }

    public func hideButton() {
        singInButton.isHidden = true
        singUpButton.isHidden = true
    }

    public func showButton() {
        singInButton.isHidden = false
        singUpButton.isHidden = false
    }
}


extension UIButton {
    func addBlurEffect(style: UIBlurEffect.Style = .regular, cornerRadius: CGFloat = 0, padding: CGFloat = 0) {
        backgroundColor = .clear
        let blurView = UIVisualEffectView(effect: UIBlurEffect(style: style))
        blurView.isUserInteractionEnabled = false
        blurView.backgroundColor = .clear
        //blurView.alpha = 0.7
        if cornerRadius > 0 {
            blurView.layer.cornerRadius = cornerRadius
            blurView.layer.masksToBounds = true
        }
        self.insertSubview(blurView, at: 0)

        blurView.translatesAutoresizingMaskIntoConstraints = false
        self.leadingAnchor.constraint(equalTo: blurView.leadingAnchor, constant: padding).isActive = true
        self.trailingAnchor.constraint(equalTo: blurView.trailingAnchor, constant: -padding).isActive = true
        self.topAnchor.constraint(equalTo: blurView.topAnchor, constant: padding).isActive = true
        self.bottomAnchor.constraint(equalTo: blurView.bottomAnchor, constant: -padding).isActive = true

        if let imageView = self.imageView {
            imageView.backgroundColor = .clear
            self.bringSubviewToFront(imageView)
        }
    }
}
