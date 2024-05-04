//
//  LoginView.swift
//  code-start
//
//  Created by Тимур Калимуллин on 25.02.2024.
//

import UIKit

class LoginView: UIView {
    private lazy var titleLable: UILabel = {
        let label = UILabel()
        label.translatesAutoresizingMaskIntoConstraints = false
        label.heightAnchor.constraint(equalToConstant: 100).isActive = true
        label.text = "Welcome\nBack"
        label.numberOfLines = 0
        label.font = UIFont.boldSystemFont(ofSize: 33)
        label.textColor = UIColor.white
        return label
    }()

    private lazy var usernameView: UITextField = {
        let field = UITextField()
        field.translatesAutoresizingMaskIntoConstraints = false
        field.heightAnchor.constraint(equalToConstant: 22).isActive = true
        field.placeholder = "Email"
        field.font = UIFont.systemFont(ofSize: 17)
        return field
    }()

    private lazy var passwordView: UITextField = {
        let field = UITextField()
        field.translatesAutoresizingMaskIntoConstraints = false
        field.heightAnchor.constraint(equalToConstant: 22).isActive = true
        field.placeholder = "Password"
        field.font = UIFont.systemFont(ofSize: 17)
        //field.isSecureTextEntry = true
        return field
    }()

    private lazy var forgotButton: UIButton = {
        let button = UIButton()
        button.translatesAutoresizingMaskIntoConstraints = false
        button.heightAnchor.constraint(equalToConstant: 22).isActive = true
        //button.widthAnchor.constraint(equalToConstant: 44).isActive = true
        button.setTitle("Forgot Password?", for: .normal)
        button.setTitleColor(UIColor.black, for: .normal)
        button.titleLabel?.font = UIFont.boldSystemFont(ofSize: 12)
        return button
    }()

    private lazy var signInButton: UIButton = {
        let button = UIButton()
        button.translatesAutoresizingMaskIntoConstraints = false
        button.heightAnchor.constraint(equalToConstant: 55).isActive = true
        button.setTitle("SIGN IN", for: .normal)
        button.titleLabel?.font = UIFont.boldSystemFont(ofSize: 17)
        button.setTitleColor(UIColor.white, for: .normal)
        button.backgroundColor = #colorLiteral(red: 0.02962492779, green: 0.386751771, blue: 0.3660313189, alpha: 1)
        button.titleLabel?.textAlignment = .center
        button.layer.cornerRadius = 16
        return button
    }()

    private lazy var orangeCircle: CircleBackgroundView = {
        let view = CircleBackgroundView()
        view.translatesAutoresizingMaskIntoConstraints = false
        view.heightAnchor.constraint(equalToConstant: 500).isActive = true
        view.widthAnchor.constraint(equalToConstant: 500).isActive = true
        view.backgroundColor = #colorLiteral(red: 0.9979462028, green: 0.4771344066, blue: 0.1853781641, alpha: 1)
        return view
    }()

//    private lazy var greenCircle: CircleBackgroundView = {
//        let view = CircleBackgroundView()
//        view.translatesAutoresizingMaskIntoConstraints = false
//        view.heightAnchor.constraint(equalToConstant: 300).isActive = true
//        view.widthAnchor.constraint(equalToConstant: 300).isActive = true
//        view.backgroundColor = #colorLiteral(red: 0.02962492779, green: 0.386751771, blue: 0.3660313189, alpha: 1)
//        return view
//    }()

    private lazy var greenCircle: ScrollLabel = {
        let view = ScrollLabel()
        view.translatesAutoresizingMaskIntoConstraints = false
        view.heightAnchor.constraint(equalToConstant: 300).isActive = true
        view.widthAnchor.constraint(equalToConstant: 300).isActive = true
        view.backgroundColor = #colorLiteral(red: 0.02962492779, green: 0.386751771, blue: 0.3660313189, alpha: 1)
        return view
    }()

    override init(frame: CGRect) {
        super.init(frame: frame)
        setupView()
    }

    required init?(coder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }

    private func setupView() {
        addSubview(orangeCircle)
        addSubview(greenCircle)
        addSubview(titleLable)
        addSubview(usernameView)
        addSubview(passwordView)
        addSubview(forgotButton)
        addSubview(signInButton)
        setupContraints()
        backgroundColor = .white
        clipsToBounds = true
    }

    private func setupContraints() {
        NSLayoutConstraint.activate([
            orangeCircle.centerYAnchor.constraint(equalTo: self.topAnchor, constant: 50),
            orangeCircle.centerXAnchor.constraint(equalTo: self.leadingAnchor, constant: 100),
            greenCircle.centerYAnchor.constraint(equalTo: self.topAnchor, constant: 80),
            greenCircle.centerXAnchor.constraint(equalTo: self.trailingAnchor, constant: -50),

            titleLable.topAnchor.constraint(equalTo: self.layoutMarginsGuide.topAnchor, constant: 50),
            titleLable.leadingAnchor.constraint(equalTo: self.layoutMarginsGuide.leadingAnchor, constant: 20),

            usernameView.centerYAnchor.constraint(equalTo: self.centerYAnchor),
            usernameView.leadingAnchor.constraint(equalTo: self.layoutMarginsGuide.leadingAnchor, constant: 20),
            usernameView.trailingAnchor.constraint(equalTo: self.layoutMarginsGuide.trailingAnchor, constant: -20),

            passwordView.topAnchor.constraint(equalTo: usernameView.bottomAnchor, constant: 15),
            passwordView.leadingAnchor.constraint(equalTo: self.layoutMarginsGuide.leadingAnchor, constant: 20),
            passwordView.trailingAnchor.constraint(equalTo: self.layoutMarginsGuide.trailingAnchor, constant: -20),

            forgotButton.topAnchor.constraint(equalTo: passwordView.bottomAnchor, constant: 10),
            forgotButton.leadingAnchor.constraint(equalTo: self.layoutMarginsGuide.leadingAnchor, constant: 20),

            signInButton.topAnchor.constraint(equalTo: forgotButton.bottomAnchor, constant: 15),
            signInButton.leadingAnchor.constraint(equalTo: self.layoutMarginsGuide.leadingAnchor, constant: 20),
            signInButton.trailingAnchor.constraint(equalTo: self.layoutMarginsGuide.trailingAnchor, constant: -20)
        ])
    }
}


